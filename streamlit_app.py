import re
import io
import time as _time_module
from datetime import datetime

import pandas as pd
import streamlit as st
import streamlit.components.v1 as _components
import json as _json

# ── Local modules ─────────────────────────────────────────────────────────────
from styles    import CSS, HERO_HTML, LEGEND_HTML, TOP_STRIP_HTML
from constants import USA_TSA_DESTS, QUEUE_DESTS, TWO_TEAM_LEADS_DESTS, ROLE_COLUMNS
from helpers   import (
    clean_text, safe_html, normalize_role_label, gender_role_label,
    is_time_text, to_datetime_time, time_to_minutes,
    short_flight_number, flight_key, name_key,
    classify_shift, shift_length, break_label_for_employee,
    employee_shift_text, break_deadline_before_flight,
)
from data_loader import (
    build_shift_map_from_excel, apply_shift_map_to_employees,
    load_daily_schedule, normalize_employees,
)
from scheduler import (
    get_requirements, requirements_text, build_schedule, upgrade_teamleads,
    is_within_shift, get_qualified_candidates_for_swap, do_swap,
)
from display import (
    build_next_task_labels, build_output_table, build_workload,
    build_counter_continuity_rows, build_available_in_hall, build_unassigned_agents,
    render_flight_card, render_flight_card_with_swap,
    to_excel_bytes,
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="iSchedule",
    page_icon="👩🏼‍🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)

# =========================
# LANDING PAGE (shown before files are uploaded)
# =========================

LANDING_PAGE = """
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
/* Hide Streamlit chrome on landing */
header[data-testid="stHeader"]  { display: none !important; }
#MainMenu                        { display: none !important; }
footer                           { display: none !important; }
.block-container                 { padding: 0 !important; max-width: 100% !important; }

#ischedule-landing {
    min-height: 100vh;
    background: linear-gradient(145deg, #050d1a 0%, #0a1a35 55%, #071430 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 24px 60px;
    font-family: 'Heebo', Arial, sans-serif;
    position: relative;
    overflow: hidden;
}

/* Animated background orbs */
.lp-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.22;
    animation: lpFloat 10s ease-in-out infinite;
    pointer-events: none;
}
.lp-o1 { width: 520px; height: 520px; background: radial-gradient(circle, #1a6bff, transparent); top: -140px; left: -100px; animation-duration: 11s; }
.lp-o2 { width: 400px; height: 400px; background: radial-gradient(circle, #00d4ff, transparent); bottom: -90px; right: -70px; animation-duration: 9s; animation-delay: -4s; }
.lp-o3 { width: 280px; height: 280px; background: radial-gradient(circle, #f59e0b, transparent); top: 42%; left: 63%; animation-duration: 13s; animation-delay: -7s; }

@keyframes lpFloat {
    0%, 100% { transform: translate(0, 0); }
    50%       { transform: translate(28px, -36px); }
}

/* Logo */
.lp-logo {
    font-size: 72px;
    font-weight: 900;
    letter-spacing: -3px;
    background: linear-gradient(125deg, #00d4ff 0%, #1a6bff 42%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    animation: lpFadeDown .7s ease both;
}

.lp-plane {
    display: inline-block;
    -webkit-text-fill-color: #00d4ff;
    margin-left: 6px;
    animation: lpFly 2.8s ease-in-out infinite;
}

@keyframes lpFly {
    0%, 100% { transform: translateX(0) rotate(-4deg); }
    50%       { transform: translateX(8px) rotate(5deg); }
}

.lp-subtitle {
    font-size: 18px;
    color: rgba(255, 255, 255, .6);
    margin: 12px 0 48px;
    direction: rtl;
    text-align: center;
    animation: lpFadeDown .7s .15s ease both;
    letter-spacing: .3px;
}

/* Feature grid */
.lp-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    max-width: 760px;
    width: 100%;
    margin-bottom: 48px;
    animation: lpFadeUp .7s .3s ease both;
}

.lp-card {
    background: rgba(255, 255, 255, .055);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, .11);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    direction: rtl;
    transition: transform .25s ease, background .25s ease, border-color .25s ease;
    cursor: default;
}
.lp-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, .1);
    border-color: rgba(0, 212, 255, .25);
}

.lp-card-icon { font-size: 28px; display: block; margin-bottom: 8px; }
.lp-card-title { font-size: 13px; font-weight: 700; color: rgba(255,255,255,.92); margin: 0; }
.lp-card-desc  { font-size: 11px; color: rgba(255,255,255,.42); margin: 4px 0 0; }

/* CTA pill */
.lp-cta {
    background: linear-gradient(120deg, #1a6bff 0%, #00d4ff 100%);
    border-radius: 50px;
    padding: 14px 34px;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    direction: rtl;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 32px rgba(26, 107, 255, .45);
    animation: lpFadeUp .7s .5s ease both;
    cursor: default;
    border: none;
}

.lp-arrow { animation: lpBounce 1.4s ease-in-out infinite; display: inline-block; }
@keyframes lpBounce { 0%,100%{transform:translateX(0)} 50%{transform:translateX(-7px)} }

/* Keyframes */
@keyframes lpFadeDown { from { opacity:0; transform:translateY(-16px); } to { opacity:1; transform:translateY(0); } }
@keyframes lpFadeUp   { from { opacity:0; transform:translateY(16px);  } to { opacity:1; transform:translateY(0); } }
</style>

<div id="ischedule-landing">
  <div class="lp-orb lp-o1"></div>
  <div class="lp-orb lp-o2"></div>
  <div class="lp-orb lp-o3"></div>

  <div class="lp-logo"><span class="lp-plane">✈</span>iSchedule</div>
  <p class="lp-subtitle">מערכת שיבוץ חכמה לפעילות שדה תעופה</p>

  <div class="lp-grid">
    <div class="lp-card">
      <span class="lp-card-icon">🚀</span>
      <p class="lp-card-title">שיבוץ אוטומטי</p>
      <p class="lp-card-desc">הקצאת עובדים לטיסות לפי הכשרות ומשמרות</p>
    </div>
    <div class="lp-card">
      <span class="lp-card-icon">📅</span>
      <p class="lp-card-title">גאנט עובדים</p>
      <p class="lp-card-desc">ויזואליזציה של כל המשימות ביום</p>
    </div>
    <div class="lp-card">
      <span class="lp-card-icon">🛡️</span>
      <p class="lp-card-title">ניהול TSA</p>
      <p class="lp-card-desc">מפקחים ושומרים לטיסות ארה"ב</p>
    </div>
    <div class="lp-card">
      <span class="lp-card-icon">⏰</span>
      <p class="lp-card-title">הפסקות חובה</p>
      <p class="lp-card-desc">מעקב הפסקות לפי אורך משמרת</p>
    </div>
    <div class="lp-card">
      <span class="lp-card-icon">🔄</span>
      <p class="lp-card-title">החלפת עובדים</p>
      <p class="lp-card-desc">גמישות בזמן אמת לשינוי שיבוצים</p>
    </div>
    <div class="lp-card">
      <span class="lp-card-icon">📊</span>
      <p class="lp-card-title">עומס עובדים</p>
      <p class="lp-card-desc">ניתוח דקות עבודה ועומס כולל</p>
    </div>
  </div>

  <div class="lp-cta">
    <span class="lp-arrow">←</span>
    העלי קובץ סידור + עובדים בסרגל הצד להתחלה
  </div>
</div>
"""

# =========================
# UI
# =========================

with st.sidebar:
    st.header("📂 העלאת קבצים")
    daily_file     = st.file_uploader("קובץ סידור יומי", type=["xlsx"], key="sidebar_daily") or st.session_state.get("daily_file_obj")
    employees_file = st.file_uploader("קובץ עובדים / הסמכות", type=["xlsx"], key="sidebar_emp") or st.session_state.get("employees_file_obj")

if not daily_file or not employees_file:
    _components.html(
        f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body style='margin:0;padding:0'>{LANDING_PAGE}</body></html>",
        height=750,
        scrolling=False,
    )
    st.stop()

# Restore app chrome for the main app
st.markdown(HERO_HTML, unsafe_allow_html=True)
st.markdown(LEGEND_HTML, unsafe_allow_html=True)
st.markdown(TOP_STRIP_HTML, unsafe_allow_html=True)

try:
    flights_df = load_daily_schedule(daily_file)
    employees_file.seek(0)
    employees_df = pd.read_excel(employees_file)
    employees_df = normalize_employees(employees_df)

    shift_map = build_shift_map_from_excel(daily_file)
    daily_file.seek(0)
    employees_df = apply_shift_map_to_employees(employees_df, shift_map)
except Exception as exc:
    st.error("לא הצלחתי לקרוא את הקבצים.")
    st.exception(exc)
    st.stop()

with st.expander("🕒 בדיקת שעות משמרת שנקראו מקובץ העובדים"):
    preview_cols = [col for col in ["שם", "תחילת משמרת", "סוף משמרת"] if col in employees_df.columns]
    st.dataframe(employees_df[preview_cols], use_container_width=True)

st.markdown(
    '<div class="ops-rtl"><h3>🛫 טיסות מהסידור היומי</h3>'
    '<div class="small-note">השלימי כאן גייט, רישוי, נוסעים וסוג הכשרה.</div></div>',
    unsafe_allow_html=True,
)

flights_editor_df = flights_df.drop(columns=["טרייני רצ"], errors="ignore").copy()

# Merge saved edits from previous session
if "saved_flight_edits" in st.session_state:
    saved = st.session_state["saved_flight_edits"]
    for col in ["גייט", "רישוי", "נוסעים", "סוג הכשרה"]:
        if col in saved.columns and col in flights_editor_df.columns:
            merge = saved[["טיסה", col]].dropna(subset=[col])
            merge = merge[merge[col].astype(str).str.strip() != ""]
            for _, mrow in merge.iterrows():
                mask = flights_editor_df["טיסה"] == mrow["טיסה"]
                if mask.any():
                    flights_editor_df.loc[mask, col] = mrow[col]

# ── FIDS loader ──────────────────────────────────────────────────────────────
with st.expander("📡 טעינת נתוני FIDS (גייט / רישוי / נוסעים)", expanded=False):
    st.caption("טען נתוני FIDS מקובץ Excel/CSV")
    fids_file = st.file_uploader("קובץ Excel / CSV", type=["xlsx", "csv"], key="fids_uploader")
    if fids_file:
        try:
            fids_df = pd.read_csv(fids_file, dtype=str) if fids_file.name.endswith(".csv") else pd.read_excel(fids_file, dtype=str)
            fids_df.columns = fids_df.columns.astype(str).str.strip()
            fc = next((c for c in fids_df.columns if "טיסה" in c or c.lower() in {"flight", "flightno"}), None)
            if not fc:
                st.error("לא נמצאה עמודת טיסה.")
            else:
                fids_df["_fk"] = fids_df[fc].astype(str).str.upper().str.replace(r"\s+", "", regex=True)
                base = st.session_state.get("saved_flight_edits", flights_editor_df.copy())
                base["_fk"] = base["טיסה"].astype(str).str.upper().str.replace(r"\s+", "", regex=True)
                COL_MAP = {
                    "גייט":   ["גייט", "gate", "Gate", "GATE"],
                    "רישוי":  ["רישוי", "reg", "Reg", "registration", "REG"],
                    "נוסעים": ["נוסעים", "pax", "Pax", "PAX", "passengers"],
                }
                filled = 0
                for target_col, aliases in COL_MAP.items():
                    src = next((a for a in aliases if a in fids_df.columns), None)
                    if not src or target_col not in base.columns:
                        continue
                    for _, fr in fids_df.iterrows():
                        val = clean_text(fr.get(src, ""))
                        if not val:
                            continue
                        mask = base["_fk"] == str(fr["_fk"])
                        if mask.any():
                            base.loc[mask, target_col] = val
                            filled += 1
                base = base.drop(columns=["_fk"])
                st.session_state["saved_flight_edits"] = base
                st.success(f"✅ נטענו נתונים עבור {filled} שדות.")
        except Exception as exc:
            st.error("שגיאה בקריאת קובץ FIDS.")
            st.exception(exc)

with st.form("flights_form"):
    edited_flights = st.data_editor(
        flights_editor_df,
        use_container_width=True,
        num_rows="dynamic",
        key="flights_editor",
    )
    col_save, col_clear = st.columns([3, 1])
    with col_save:
        save_clicked = st.form_submit_button("💾 שמור נתונים", use_container_width=True)
    with col_clear:
        clear_clicked = st.form_submit_button("🗑️ נקה", use_container_width=True)

if save_clicked:
    st.session_state["saved_flight_edits"] = edited_flights.copy()
    st.success("הנתונים נשמרו ✅")

if clear_clicked:
    st.session_state.pop("saved_flight_edits", None)
    st.rerun()

m1, m2, m3, m4 = st.columns(4)
m1.metric("טיסות", len(edited_flights))
m2.metric("עובדים", len(employees_df))
m3.metric("יעדי TSA", edited_flights["יעד"].isin(list(USA_TSA_DESTS)).sum())
m4.metric(
    "עובדי טרייני רצ",
    (employees_df["טרייני רצ"].astype(str).str.strip() == "כן").sum()
    if "טרייני רצ" in employees_df.columns else 0,
)


def recompute_from_schedule(schedule_df, flights_df, employees_df):
    labeled_df    = build_next_task_labels(schedule_df, employees_df)
    workload_df   = build_workload(schedule_df, employees_df)
    continuity_df = build_counter_continuity_rows(labeled_df, employees_df)
    output_df     = build_output_table(flights_df, labeled_df, employees_df)
    return labeled_df, workload_df, continuity_df, output_df


# ── Build button ──────────────────────────────────────────────────────────────
if st.button("🚀 בנה שיבוץ", use_container_width=True):
    try:
        schedule_df = build_schedule(edited_flights, employees_df)
        schedule_df = upgrade_teamleads(schedule_df, employees_df)
        st.session_state["schedule_df"]    = schedule_df.copy()
        st.session_state["flights_snap"]   = edited_flights.copy()
        st.session_state["employees_snap"] = employees_df.copy()
        st.success("השיבוץ נבנה בהצלחה.")
    except Exception as exc:
        st.error("הייתה שגיאה בבניית השיבוץ.")
        st.exception(exc)


# ── Display ───────────────────────────────────────────────────────────────────
if "schedule_df" in st.session_state:
    try:
        live_schedule  = st.session_state["schedule_df"]
        live_flights   = st.session_state["flights_snap"]
        live_employees = st.session_state["employees_snap"]

        labeled_df, workload_df, continuity_df, output_df = recompute_from_schedule(
            live_schedule, live_flights, live_employees
        )
        missing = live_schedule[live_schedule["עובד"].astype(str).str.contains("❌", na=False)]

        (tab_schedule, tab_gantt, tab_missing, tab_available,
         tab_unassigned, tab_breaks, tab_workload, tab_continuity, tab_raw) = st.tabs([
            "✈️ לוח מבצעים", "📅 גאנט", "❌ חוסרים", "🟡 פנויים באולם",
            "🏠 לא משובצים", "⏰ הפסקות חובה", "📊 עומס עובדים",
            "🧭 רצף אזורי", "🧾 פירוט גולמי",
        ])

        # ── Tab: לוח מבצעים ──────────────────────────────────────────────────
        with tab_schedule:
            st.markdown('<div class="ops-rtl"><h3>✈️ Assignment Board</h3></div>', unsafe_allow_html=True)
            search       = st.text_input("🔎 חיפוש לפי טיסה / יעד / עובד")
            only_missing = st.checkbox("הצג רק טיסות עם חוסר")
            display_df   = output_df.copy()
            if only_missing:
                display_df = display_df[
                    display_df.astype(str).apply(
                        lambda row: row.str.contains("❌", na=False).any(), axis=1
                    )
                ]
            if search:
                mask = display_df.astype(str).apply(
                    lambda row: row.str.contains(search, case=False, na=False).any(), axis=1
                )
                display_df = display_df[mask]
            for _, row in display_df.iterrows():
                render_flight_card_with_swap(
                    row,
                    st.session_state["schedule_df"],
                    st.session_state["employees_snap"],
                )

        # ── Tab: גאנט ────────────────────────────────────────────────────────
        with tab_gantt:
            timed_g = live_schedule[live_schedule["התחלה"].astype(str).str.strip() != ""].copy()

            if timed_g.empty:
                st.info("אין נתוני שיבוץ להצגה.")
            else:
                ROLE_COLORS_G = {
                    "ראש צוות":   "#8e24aa",
                    "דיילת":      "#5b9bd5",
                    "דייל":       "#5b9bd5",
                    "מתאם תורים": "#f0a000",
                    "מפקח TSA":   "#d32f2f",
                    "שומר TSA":   "#2e7d32",
                    "טרייני ר״צ": "#f9a825",
                    "טרייני רצ":  "#f9a825",
                }
                all_s = pd.to_datetime(timed_g["התחלה"], format="%H:%M", errors="coerce")
                all_e = pd.to_datetime(timed_g["סיום"],   format="%H:%M", errors="coerce")
                g_min = max(int(all_s.dt.hour.min()) - 1, 0)
                g_max = min(int(all_e.dt.hour.max()) + 2, 24)

                all_workers = sorted(
                    [w for w in timed_g["עובד"].unique() if "❌" not in str(w)]
                )
                workers_data = []
                for worker in all_workers:
                    tasks = timed_g[timed_g["עובד"] == worker]
                    tlist = []
                    for idx, task in tasks.iterrows():
                        role = normalize_role_label(str(task.get("תפקיד בסיס", "")))
                        tlist.append({
                            "flight": str(task.get("טיסה", "")).replace("LY", "").strip(),
                            "role":   role,
                            "start":  str(task.get("התחלה", "")),
                            "end":    str(task.get("סיום", "")),
                            "color":  ROLE_COLORS_G.get(role, "#9fb7d7"),
                        })
                    workers_data.append({"name": worker, "tasks": tlist})

                gdata   = _json.dumps(workers_data,  ensure_ascii=False)
                rcolors = _json.dumps(ROLE_COLORS_G, ensure_ascii=False)

                gantt_page = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>גאנט</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:Arial,sans-serif;background:#f4f7fb;padding:10px;}}
#gantt{{overflow-x:auto;border:1px solid #d9e2ef;border-radius:14px;background:#fff;}}
#inner{{position:relative;}}
.hour-line{{position:absolute;top:0;bottom:0;border-left:1px solid #e8eef7;pointer-events:none;}}
.hour-label{{position:absolute;top:5px;font-size:11px;color:#8a9ab5;}}
.wrow{{display:flex;align-items:stretch;border-bottom:1px solid #eef2f8;min-height:44px;}}
.wrow:nth-child(even){{background:#f8fbff;}}
.wlabel{{width:120px;min-width:120px;display:flex;align-items:center;justify-content:flex-end;
         padding:4px 8px;border-right:2px solid #e0e8f4;position:sticky;left:0;
         font-size:12px;font-weight:900;color:#071b3a;text-align:right;direction:rtl;
         background:inherit;}}
.timeline{{position:relative;flex:1;height:44px;}}
.task{{position:absolute;height:28px;border-radius:7px;display:flex;align-items:center;
       justify-content:center;font-size:10px;font-weight:800;color:white;
       white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 5px;
       box-shadow:0 2px 5px rgba(0,0,0,0.15);}}
</style></head><body>
<div id="gantt"><div id="inner"></div></div>
<script>
const WORKERS={gdata},COLORS={rcolors};
const DAY_MIN={g_min},DAY_MAX={g_max},HOURS=DAY_MAX-DAY_MIN,HPX=90,LW=120,HDR=26;
function h2px(s){{const[h,m]=(s||"0:0").split(":").map(Number);return(h+m/60-DAY_MIN)*HPX;}}
const inner=document.getElementById("inner");
inner.style.cssText=`position:relative;width:${{LW+HOURS*HPX+20}}px;padding-top:${{HDR}}px;`;
for(let h=0;h<=HOURS;h++){{
  const x=LW+h*HPX;
  const ln=document.createElement("div");ln.className="hour-line";ln.style.left=x+"px";inner.appendChild(ln);
  const lb=document.createElement("div");lb.className="hour-label";lb.style.left=(x+3)+"px";
  lb.textContent=String(DAY_MIN+h).padStart(2,"0")+":00";inner.appendChild(lb);
}}
WORKERS.forEach(w=>{{
  const row=document.createElement("div");row.className="wrow";
  const lbl=document.createElement("div");lbl.className="wlabel";lbl.textContent=w.name;row.appendChild(lbl);
  const tl=document.createElement("div");tl.className="timeline";
  w.tasks.forEach(t=>{{
    const x1=h2px(t.start),x2=h2px(t.end),bw=Math.max(x2-x1,6);
    const d=document.createElement("div");d.className="task";
    d.style.cssText=`left:${{x1.toFixed(1)}}px;width:${{bw.toFixed(1)}}px;top:7px;background:${{t.color}};`;
    d.textContent=t.flight;d.title=`${{w.name}} | ${{t.role}} | ${{t.start}}–${{t.end}}`;
    tl.appendChild(d);
  }});
  row.appendChild(tl);inner.appendChild(row);
}});
</script></body></html>"""

                st.download_button("⬇️ הורד גאנט כקובץ HTML", data=gantt_page.encode("utf-8"),
                                   file_name="gantt_workers.html", mime="text/html", use_container_width=True)
                st.caption(f"מציג {len(all_workers)} עובדים")
                _components.html(gantt_page, height=max(500, len(all_workers) * 48 + 120), scrolling=False)

            st.subheader("❌ חוסרים")
            if missing.empty:
                st.success("אין חוסרים 🎉")
            else:
                st.warning(f"נמצאו {len(missing)} חוסרים")
                st.dataframe(missing, use_container_width=True)

        # ── Tab: פנויים באולם ─────────────────────────────────────────────────
        with tab_available:
            st.subheader("🟡 עובדים פנויים באולם היציאה")
            available_df = build_available_in_hall(live_schedule, live_employees, live_flights)
            if available_df.empty:
                st.success("אין עובדים פנויים כרגע באולם היציאה 🎉")
            else:
                total_free = available_df["עובד"].nunique()
                long_gaps  = available_df[available_df["פנות (דק׳)"] >= 60]["עובד"].nunique()
                sc1, sc2 = st.columns(2)
                sc1.metric("עובדים פנויים באולם", total_free)
                sc2.metric("מתוכם פנויים שעה+", long_gaps)
                st.markdown("---")
                roles = ["הכל"] + sorted(available_df["תפקיד עיקרי"].dropna().unique().tolist())
                selected_role = st.selectbox("סנן לפי תפקיד:", roles, key="avail_role_filter")
                filtered = available_df if selected_role == "הכל" else available_df[available_df["תפקיד עיקרי"] == selected_role]
                for _, r in filtered.iterrows():
                    gap_color  = "#fff3cd" if r["פנות (דק׳)"] < 60 else "#d4edda"
                    gap_border = "#ffc107" if r["פנות (דק׳)"] < 60 else "#28a745"
                    st.markdown(
                        f'<div style="direction:rtl;background:{gap_color};border-right:5px solid {gap_border};'
                        f'border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px;">'
                        f'<strong>{safe_html(r["עובד"])}</strong> · {safe_html(r["תפקיד עיקרי"])} · משמרת: {safe_html(r["משמרת"])}<br>'
                        f'🕒 פנוי: <strong>{safe_html(r["פנוי מ"])} – {safe_html(r["פנוי עד"])}</strong>'
                        f' ({r["פנות (דק׳)"]} דק׳) · הבא: {safe_html(r["משימה הבאה"])}<br>'
                        f'<span style="color:#555;font-size:12px">{safe_html(r["הערה"])}</span></div>',
                        unsafe_allow_html=True,
                    )

        # ── Tab: לא משובצים ───────────────────────────────────────────────────
        with tab_unassigned:
            st.subheader("🏠 דיילים וראשי צוות שלא שובצו לטיסות היום")
            if "break_log" not in st.session_state:
                st.session_state["break_log"] = {}

            shift_map_ref = build_shift_map_from_excel(daily_file)
            unassigned_df = build_unassigned_agents(live_schedule, live_employees, shift_map_ref)

            if unassigned_df.empty:
                st.success("כל העובדים שובצו לטיסות 🎉")
            else:
                st.metric("סה״כ לא משובצים", len(unassigned_df))
                st.markdown("---")
                for shift_label, group in unassigned_df.groupby("משמרת"):
                    start_h = shift_label.split("-")[0] if "-" in shift_label else "00:00"
                    try:
                        sh = int(start_h.split(":")[0])
                        if   5 <= sh < 12:  emoji, label = "🌅", f"משמרת בוקר — {shift_label}"
                        elif 12 <= sh < 18:  emoji, label = "☀️", f"משמרת צהריים — {shift_label}"
                        elif 18 <= sh < 22:  emoji, label = "🌆", f"משמרת ערב — {shift_label}"
                        else:                emoji, label = "🌙", f"משמרת לילה — {shift_label}"
                    except Exception:
                        emoji, label = "🕐", f"משמרת — {shift_label}"

                    st.markdown(
                        f'<div style="direction:rtl;background:#eef5ff;border-right:4px solid #3b82f6;'
                        f'border-radius:10px;padding:8px 14px;margin:10px 0 6px 0;'
                        f'font-size:14px;font-weight:900;color:#071b3a;">'
                        f'{emoji} {safe_html(label)} ({len(group)} עובדים)</div>',
                        unsafe_allow_html=True,
                    )
                    for _, r in group.iterrows():
                        name = r["שם"]
                        role = r["תפקיד"]
                        btn_key    = re.sub(r"[^a-zA-Zא-ת0-9]", "_", name)
                        role_color = "#8e24aa" if role == "ראש צוות" else "#5b9bd5"
                        break_info = st.session_state["break_log"].get(name, {})
                        on_break   = bool(break_info.get("ts")) and not break_info.get("end_ts")
                        break_done = bool(break_info.get("ts")) and bool(break_info.get("end_ts"))
                        emp_row_m  = live_employees[live_employees["שם"] == name]
                        bl = break_label_for_employee(emp_row_m.iloc[0]) if not emp_row_m.empty else ""
                        break_duration = 65 if bl == "הפסקה ורענון" else 45 if bl == "הפסקה" else 20

                        if on_break:
                            card_bg, card_border, card_label = "#fef3c7", role_color, "☕ בהפסקה"
                        elif break_done:
                            card_bg, card_border, card_label = "#d1fae5", role_color, "✅ הפסקה הסתיימה"
                        else:
                            card_bg, card_border, card_label = "#fff", role_color, ""

                        st.markdown(
                            f'<div style="direction:rtl;background:{card_bg};border:1px solid #e0e8f4;'
                            f'border-right:4px solid {card_border};border-radius:8px;'
                            f'padding:6px 12px;margin-bottom:2px;font-size:13px;">'
                            f'<strong style="color:#071b3a;">{safe_html(name)}</strong>'
                            f'&nbsp;<span style="color:{role_color};font-weight:800;">({safe_html(role)})</span>'
                            + (f'&nbsp;&nbsp;<span style="color:#92400e;">{card_label}</span>' if card_label else "") +
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        col_start, col_end, col_reset = st.columns([2, 2, 1])
                        with col_start:
                            if not on_break and not break_done:
                                if st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}", use_container_width=True):
                                    st.session_state["break_log"][name] = {"ts": int(_time_module.time()), "end_ts": None}
                                    st.rerun()
                            else:
                                st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}", disabled=True, use_container_width=True)
                        with col_end:
                            if on_break:
                                if st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}", use_container_width=True):
                                    st.session_state["break_log"][name]["end_ts"] = int(_time_module.time())
                                    st.rerun()
                            else:
                                st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}", disabled=True, use_container_width=True)
                        with col_reset:
                            if break_info:
                                if st.button("↺", key=f"brk_reset_{btn_key}", help="אפס הפסקה"):
                                    st.session_state["break_log"].pop(name, None)
                                    st.rerun()

        # ── Tab: הפסקות חובה ──────────────────────────────────────────────────
        with tab_breaks:
            st.subheader("⏰ עובדים שחייבים לצאת להפסקה עד שעה מסוימת")
            timed_br = live_schedule[
                (live_schedule["התחלה"].astype(str).str.strip() != "") &
                (~live_schedule["עובד"].astype(str).str.contains("❌", na=False))
            ].copy()
            break_rows = []
            for emp_name in timed_br["עובד"].unique():
                emp_row_df = live_employees[live_employees["שם"] == emp_name]
                if emp_row_df.empty:
                    continue
                emp_row = emp_row_df.iloc[0]
                if classify_shift(emp_row) != "early_morning":
                    continue
                emp_tasks = timed_br[timed_br["עובד"] == emp_name].sort_values("התחלה")
                if emp_tasks.empty:
                    continue
                first_task    = emp_tasks.iloc[0]
                task_start_dt = to_datetime_time(first_task["התחלה"])
                task_start_min = task_start_dt.hour * 60 + task_start_dt.minute
                deadline = break_deadline_before_flight(emp_row, task_start_min)
                if deadline:
                    flight = str(first_task.get("טיסה", "")).replace("LY", "").strip()
                    role   = normalize_role_label(str(first_task.get("תפקיד בסיס", "")))
                    shift  = employee_shift_text(live_employees, emp_name)
                    break_rows.append({
                        "עובד":           emp_name,
                        "משמרת":          shift,
                        "הפסקה עד":       deadline,
                        "טיסה ראשונה":    flight,
                        "שעת כניסה לשער": first_task["התחלה"],
                        "תפקיד":          role,
                    })

            if not break_rows:
                st.success("אין עובדים עם חובת הפסקה מיוחדת היום 🎉")
            else:
                break_df = pd.DataFrame(break_rows).sort_values("הפסקה עד")
                st.metric("עובדים עם הפסקת חובה", len(break_df))
                for _, r in break_df.iterrows():
                    st.markdown(
                        f'<div style="direction:rtl;background:#fff8e1;border-right:5px solid #f59e0b;'
                        f'border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px;color:#1a1a1a;">'
                        f'⏰ <strong>{safe_html(r["עובד"])}</strong>'
                        f' ({safe_html(r["תפקיד"])}) | משמרת: {safe_html(r["משמרת"])}<br>'
                        f'חייב/ת לצאת להפסקה עד: '
                        f'<strong style="color:#b45309;font-size:16px;">{safe_html(r["הפסקה עד"])}</strong>'
                        f' → טיסה {safe_html(r["טיסה ראשונה"])} | כניסה לשער: {safe_html(r["שעת כניסה לשער"])}</div>',
                        unsafe_allow_html=True,
                    )

        # ── Tabs: workload / continuity / raw ─────────────────────────────────
        with tab_workload:
            st.subheader("📊 עומס עובדים")
            st.dataframe(workload_df, use_container_width=True)

        with tab_continuity:
            st.subheader("🧭 רצף אזורי")
            st.dataframe(continuity_df, use_container_width=True)

        with tab_raw:
            st.subheader("🧾 פירוט גולמי")
            st.dataframe(labeled_df, use_container_width=True)

        excel_data = to_excel_bytes(output_df, workload_df, labeled_df, continuity_df)
        st.download_button(
            "⬇️ הורדת אקסל מלא",
            data=excel_data,
            file_name="ISCHEDULE_OPS_BOARD.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("הייתה שגיאה בהצגת השיבוץ.")
        st.exception(exc)
