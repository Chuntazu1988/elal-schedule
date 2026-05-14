import io
import os
import re
import json
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# iSchedule - גאנט עובדים מקובץ סידור עבודה מוכן + 2 FIDS
# =========================================================

st.set_page_config(
    page_title="iSchedule - גאנט עובדים",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = "_ischedule_uploaded_files"
os.makedirs(DATA_DIR, exist_ok=True)

SCHEDULE_PATH = os.path.join(DATA_DIR, "last_schedule.xlsx")
TODAY_FIDS_PATH = os.path.join(DATA_DIR, "last_today_fids")
TOMORROW_FIDS_PATH = os.path.join(DATA_DIR, "last_tomorrow_fids")
TODAY_FIDS_NAME_PATH = os.path.join(DATA_DIR, "last_today_fids_name.txt")
TOMORROW_FIDS_NAME_PATH = os.path.join(DATA_DIR, "last_tomorrow_fids_name.txt")


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #f4f7fb;
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
.ops-hero {
    direction: rtl;
    text-align: center;
    background: linear-gradient(90deg, #06172f 0%, #0b3972 50%, #06172f 100%);
    color: white;
    border-radius: 22px;
    padding: 26px 22px;
    margin-bottom: 18px;
    box-shadow: 0 12px 32px rgba(6,23,47,.22);
}
.ops-hero h1 {
    font-size: 34px;
    margin: 0;
    font-weight: 900;
}
.ops-hero p {
    margin: 8px 0 0 0;
    opacity: .86;
    font-size: 15px;
}
.ops-card {
    direction: rtl;
    text-align: right;
    background: white;
    border: 1px solid #dbe5f2;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 8px 22px rgba(20, 40, 80, .07);
    margin-bottom: 14px;
}
.small-note {
    direction: rtl;
    color: #5e6d82;
    font-size: 13px;
}
.stButton > button {
    direction: rtl;
    font-weight: 900;
    border-radius: 14px;
    min-height: 48px;
}
a.gantt-link {
    display: inline-block;
    background: #003B71;
    color: white !important;
    padding: 14px 24px;
    border-radius: 14px;
    text-decoration: none !important;
    font-weight: 900;
    margin-top: 8px;
    box-shadow: 0 8px 18px rgba(0, 59, 113, .24);
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# Helpers
# =========================================================

def save_uploaded_file(uploaded_file, path: str, name_path: str | None = None) -> None:
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    if name_path:
        with open(name_path, "w", encoding="utf-8") as f:
            f.write(uploaded_file.name or "uploaded_file")


def read_uploaded_table(file_obj_or_path, original_name: str | None = None) -> pd.DataFrame:
    """Reads xlsx/csv/html files robustly."""
    name = original_name or getattr(file_obj_or_path, "name", "") or str(file_obj_or_path)
    lower_name = name.lower()

    if hasattr(file_obj_or_path, "seek"):
        file_obj_or_path.seek(0)

    if lower_name.endswith(".csv"):
        try:
            return pd.read_csv(file_obj_or_path, dtype=str, encoding="utf-8-sig")
        except Exception:
            if hasattr(file_obj_or_path, "seek"):
                file_obj_or_path.seek(0)
            return pd.read_csv(file_obj_or_path, dtype=str, encoding="cp1255")

    if lower_name.endswith(".html") or lower_name.endswith(".htm"):
        tables = pd.read_html(file_obj_or_path)
        if not tables:
            return pd.DataFrame()
        return tables[0].astype(str)

    return pd.read_excel(file_obj_or_path, dtype=str)


def read_saved_fids(path: str, name_path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    name = "uploaded.xlsx"
    if os.path.exists(name_path):
        name = open(name_path, "r", encoding="utf-8").read().strip() or name
    return read_uploaded_table(path, name)


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace("\n", " ") for c in df.columns]
    return df


def norm_text(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()


def find_col(df: pd.DataFrame, groups: list[list[str]]) -> str | None:
    cols = list(df.columns)
    low = {c: re.sub(r"\s+", "", str(c).lower()) for c in cols}

    for aliases in groups:
        aliases_low = [re.sub(r"\s+", "", a.lower()) for a in aliases]
        for c in cols:
            if low[c] in aliases_low:
                return c
        for c in cols:
            if any(a in low[c] for a in aliases_low):
                return c
    return None


def parse_time_to_minutes(value) -> int | None:
    txt = norm_text(value)
    if not txt:
        return None

    # Excel timestamp / datetime string
    dt = pd.to_datetime(txt, errors="coerce", dayfirst=True)
    if not pd.isna(dt):
        return int(dt.hour) * 60 + int(dt.minute)

    # HH:MM / H:MM / HH.MM
    m = re.search(r"(\d{1,2})[:.](\d{2})", txt)
    if m:
        h = int(m.group(1))
        mi = int(m.group(2))
        if 0 <= h <= 29 and 0 <= mi <= 59:
            return h * 60 + mi

    # Excel fraction of day, for example 0.25 = 06:00
    try:
        num = float(txt)
        if 0 <= num < 1:
            return int(round(num * 24 * 60))
    except Exception:
        pass

    return None


def minutes_to_hhmm(minutes: int | None) -> str:
    if minutes is None:
        return ""
    minutes = int(minutes)
    h = (minutes // 60) % 24
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def sort_key_from_0200(minutes: int | None) -> int:
    if minutes is None:
        return 999999
    base = 2 * 60
    return (minutes - base) % (24 * 60)


def add_day_rollover(start_m: int | None, end_m: int | None) -> tuple[int | None, int | None]:
    if start_m is None or end_m is None:
        return start_m, end_m
    if end_m <= start_m:
        end_m += 24 * 60
    return start_m, end_m


def build_fids_lookup(today_df: pd.DataFrame, tomorrow_df: pd.DataFrame) -> dict:
    lookup = {}
    for source_name, df in [("היום", today_df), ("מחר", tomorrow_df)]:
        if df.empty:
            continue
        df = clean_columns(df)
        flight_col = find_col(df, [["טיסה", "flight", "flightno", "flight no", "מספר טיסה"]])
        if not flight_col:
            continue
        gate_col = find_col(df, [["גייט", "gate", "שער"]])
        dest_col = find_col(df, [["יעד", "destination", "dest"]])
        reg_col = find_col(df, [["רישוי", "registration", "reg", "מטוס"]])
        pax_col = find_col(df, [["נוסעים", "pax", "passengers"]])

        for _, row in df.iterrows():
            key = re.sub(r"\s+", "", norm_text(row.get(flight_col, "")).upper())
            if not key:
                continue
            lookup[key] = {
                "יום": source_name,
                "גייט": norm_text(row.get(gate_col, "")) if gate_col else "",
                "יעד": norm_text(row.get(dest_col, "")) if dest_col else "",
                "רישוי": norm_text(row.get(reg_col, "")) if reg_col else "",
                "נוסעים": norm_text(row.get(pax_col, "")) if pax_col else "",
            }
    return lookup


def prepare_gantt_data(schedule_df: pd.DataFrame, fids_lookup: dict) -> tuple[list[dict], dict, list[str]]:
    df = clean_columns(schedule_df)

    employee_col = find_col(df, [["עובד", "שם עובד", "שם", "employee", "name"]])
    start_col = find_col(df, [["התחלה", "שעת התחלה", "start", "from", "משעה"]])
    end_col = find_col(df, [["סיום", "שעת סיום", "end", "to", "עד שעה"]])
    shift_start_col = find_col(df, [["תחילת משמרת", "משמרת התחלה", "כניסה", "shift start"]])
    shift_end_col = find_col(df, [["סוף משמרת", "סיום משמרת", "יציאה", "shift end"]])
    flight_col = find_col(df, [["טיסה", "flight", "flight no", "flightno"]])
    role_col = find_col(df, [["תפקיד בסיס", "תפקיד", "משימה", "role", "task"]])
    dest_col = find_col(df, [["יעד", "destination", "dest"]])

    missing = []
    if not employee_col:
        missing.append("עמודת עובד / שם")
    if not start_col:
        missing.append("עמודת התחלה")
    if not end_col:
        missing.append("עמודת סיום")

    if missing:
        return [], {}, missing

    role_colors = {
        "ראש צוות": "#8e24aa",
        "דיילת": "#5b9bd5",
        "דייל": "#5b9bd5",
        "מתאם תורים": "#f0a000",
        "מפקח TSA": "#d32f2f",
        "שומר TSA": "#2e7d32",
        "טרייני רצ": "#f9a825",
        "טרייני ר\"צ": "#f9a825",
        "הפסקה": "#607d8b",
        "אחר": "#9fb7d7",
    }

    workers = {}

    for _, row in df.iterrows():
        worker = norm_text(row.get(employee_col, ""))
        if not worker or "❌" in worker:
            continue

        s = parse_time_to_minutes(row.get(start_col, ""))
        e = parse_time_to_minutes(row.get(end_col, ""))
        s, e = add_day_rollover(s, e)
        if s is None or e is None:
            continue

        shift_s = parse_time_to_minutes(row.get(shift_start_col, "")) if shift_start_col else None
        shift_e = parse_time_to_minutes(row.get(shift_end_col, "")) if shift_end_col else None

        flight = norm_text(row.get(flight_col, "")) if flight_col else ""
        flight_key = re.sub(r"\s+", "", flight.upper())
        fids = fids_lookup.get(flight_key, {})

        role = norm_text(row.get(role_col, "")) if role_col else "משימה"
        if not role:
            role = "משימה"

        dest = norm_text(row.get(dest_col, "")) if dest_col else ""
        if not dest:
            dest = fids.get("יעד", "")

        gate = fids.get("גייט", "")
        pax = fids.get("נוסעים", "")
        reg = fids.get("רישוי", "")

        label_parts = []
        if flight:
            label_parts.append(flight.replace("LY", ""))
        if role:
            label_parts.append(role)
        label = " · ".join(label_parts) if label_parts else "משימה"

        tooltip_parts = [worker, role, f"{minutes_to_hhmm(s)}–{minutes_to_hhmm(e)}"]
        if flight:
            tooltip_parts.append(f"טיסה: {flight}")
        if dest:
            tooltip_parts.append(f"יעד: {dest}")
        if gate:
            tooltip_parts.append(f"גייט: {gate}")
        if pax:
            tooltip_parts.append(f"נוסעים: {pax}")
        if reg:
            tooltip_parts.append(f"רישוי: {reg}")

        if worker not in workers:
            workers[worker] = {
                "name": worker,
                "shift_start": shift_s,
                "shift_end": shift_e,
                "first_task": s,
                "last_task": e,
                "tasks": [],
            }
        else:
            workers[worker]["first_task"] = min(workers[worker]["first_task"], s)
            workers[worker]["last_task"] = max(workers[worker]["last_task"], e)
            if workers[worker]["shift_start"] is None and shift_s is not None:
                workers[worker]["shift_start"] = shift_s
            if workers[worker]["shift_end"] is None and shift_e is not None:
                workers[worker]["shift_end"] = shift_e

        color = "#9fb7d7"
        for key, val in role_colors.items():
            if key != "אחר" and key in role:
                color = val
                break

        workers[worker]["tasks"].append({
            "label": label,
            "role": role,
            "start": s,
            "end": e,
            "start_txt": minutes_to_hhmm(s),
            "end_txt": minutes_to_hhmm(e),
            "color": color,
            "title": " | ".join([p for p in tooltip_parts if p]),
        })

    workers_list = list(workers.values())
    for w in workers_list:
        w["tasks"] = sorted(w["tasks"], key=lambda t: t["start"])
        if w["shift_start"] is None:
            w["shift_start"] = w["first_task"]
        if w["shift_end"] is None:
            w["shift_end"] = w["last_task"]

    workers_list.sort(key=lambda w: (sort_key_from_0200(w.get("shift_start")), w.get("shift_end") or 99999, w["name"]))
    return workers_list, role_colors, []


def build_gantt_html(workers: list[dict], role_colors: dict, fullscreen: bool = False) -> str:
    all_starts = [t["start"] for w in workers for t in w["tasks"]]
    all_ends = [t["end"] for w in workers for t in w["tasks"]]

    if not all_starts or not all_ends:
        return "<div style='direction:rtl;font-family:Arial;padding:30px'>אין משימות להצגה.</div>"

    day_min = max((min(all_starts) // 60) * 60 - 60, 0)
    day_max = ((max(all_ends) + 59) // 60) * 60 + 60
    if day_max <= day_min:
        day_max = day_min + 12 * 60

    hour_width = 96
    label_width = 190
    row_height = 48
    header_height = 42
    total_width = label_width + ((day_max - day_min) / 60) * hour_width + 40

    data_json = json.dumps(workers, ensure_ascii=False)
    colors_json = json.dumps(role_colors, ensure_ascii=False)
    body_padding = "0" if fullscreen else "10px"

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>גאנט עובדים</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:Arial,'Noto Sans Hebrew',sans-serif;background:#f4f7fb;padding:{body_padding};}}
.wrap{{direction:ltr;width:100%;height:{'100vh' if fullscreen else 'auto'};overflow:auto;background:white;border:1px solid #d9e2ef;border-radius:{'0' if fullscreen else '18px'};box-shadow:0 8px 26px rgba(20,40,80,.08);}}
.inner{{position:relative;width:{total_width:.0f}px;min-height:{header_height + len(workers)*row_height}px;padding-top:{header_height}px;}}
.top-title{{position:sticky;top:0;z-index:9;left:0;width:{label_width}px;height:{header_height}px;background:#06172f;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;direction:rtl;border-bottom:1px solid #d9e2ef;}}
.hour-line{{position:absolute;top:0;bottom:0;border-left:1px solid #e5edf7;pointer-events:none;}}
.hour-label{{position:absolute;top:0;height:{header_height}px;display:flex;align-items:center;font-size:12px;color:#51627a;font-weight:800;}}
.row{{display:flex;align-items:stretch;border-bottom:1px solid #eef2f8;min-height:{row_height}px;direction:ltr;}}
.row:nth-child(even){{background:#f8fbff;}}
.name{{width:{label_width}px;min-width:{label_width}px;position:sticky;left:0;z-index:5;background:inherit;border-right:2px solid #dde8f5;display:flex;flex-direction:column;align-items:flex-end;justify-content:center;padding:4px 10px;text-align:right;direction:rtl;}}
.name strong{{font-size:13px;color:#06172f;}}
.name span{{font-size:10.5px;color:#718096;margin-top:2px;}}
.timeline{{position:relative;flex:1;height:{row_height}px;}}
.task{{position:absolute;top:9px;height:30px;border-radius:9px;color:white;font-size:11px;font-weight:900;display:flex;align-items:center;justify-content:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 7px;box-shadow:0 2px 7px rgba(0,0,0,.18);direction:rtl;}}
.legend{{direction:rtl;display:flex;gap:10px;flex-wrap:wrap;padding:10px 12px;background:#fff;border-bottom:1px solid #e5edf7;position:sticky;top:0;z-index:20;}}
.leg{{font-size:12px;color:#26364a;font-weight:800;display:flex;align-items:center;gap:6px;}}
.dot{{width:12px;height:12px;border-radius:50%;display:inline-block;}}
</style>
</head>
<body>
<div class="legend" id="legend"></div>
<div class="wrap">
  <div class="inner" id="inner">
    <div class="top-title">עובדים</div>
  </div>
</div>
<script>
const WORKERS = {data_json};
const COLORS = {colors_json};
const DAY_MIN = {day_min};
const DAY_MAX = {day_max};
const HOUR_WIDTH = {hour_width};
const LABEL_WIDTH = {label_width};
const ROW_HEIGHT = {row_height};
const HEADER_HEIGHT = {header_height};
const inner = document.getElementById('inner');
const legend = document.getElementById('legend');

Object.entries(COLORS).forEach(([name, color]) => {{
  if (name === 'אחר') return;
  const el = document.createElement('div');
  el.className = 'leg';
  el.innerHTML = `<span class="dot" style="background:${{color}}"></span>${{name}}`;
  legend.appendChild(el);
}});

function xFromMin(m) {{ return LABEL_WIDTH + ((m - DAY_MIN) / 60) * HOUR_WIDTH; }}
function hhmm(total) {{
  let h = Math.floor(total / 60) % 24;
  let m = total % 60;
  return String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0');
}}

for (let m = DAY_MIN; m <= DAY_MAX; m += 60) {{
  const x = xFromMin(m);
  const line = document.createElement('div');
  line.className = 'hour-line';
  line.style.left = x + 'px';
  inner.appendChild(line);

  const label = document.createElement('div');
  label.className = 'hour-label';
  label.style.left = (x + 5) + 'px';
  label.textContent = hhmm(m);
  inner.appendChild(label);
}}

WORKERS.forEach((worker) => {{
  const row = document.createElement('div');
  row.className = 'row';

  const name = document.createElement('div');
  name.className = 'name';
  name.innerHTML = `<strong>${{worker.name}}</strong><span>${{hhmm(worker.shift_start)}}–${{hhmm(worker.shift_end)}}</span>`;
  row.appendChild(name);

  const timeline = document.createElement('div');
  timeline.className = 'timeline';

  worker.tasks.forEach((task) => {{
    const x1 = ((task.start - DAY_MIN) / 60) * HOUR_WIDTH;
    const x2 = ((task.end - DAY_MIN) / 60) * HOUR_WIDTH;
    const width = Math.max(x2 - x1, 8);
    const d = document.createElement('div');
    d.className = 'task';
    d.style.left = x1 + 'px';
    d.style.width = width + 'px';
    d.style.background = task.color;
    d.textContent = task.label;
    d.title = task.title;
    timeline.appendChild(d);
  }});

  row.appendChild(timeline);
  inner.appendChild(row);
}});
</script>
</body>
</html>"""


# =========================================================
# Fullscreen Gantt page
# =========================================================

query_gantt = st.query_params.get("workers_gantt") == "true"

if query_gantt:
    st.markdown(
        """
<style>
header[data-testid="stHeader"], #MainMenu, footer, section[data-testid="stSidebar"] {display:none !important;}
.block-container {padding:0 !important; max-width:100% !important;}
</style>
""",
        unsafe_allow_html=True,
    )

    if not os.path.exists(SCHEDULE_PATH):
        st.error("אין עדיין קובץ סידור שמור. חזרי לעמוד הראשי והעלי את שלושת הקבצים.")
        st.stop()

    try:
        schedule_df = pd.read_excel(SCHEDULE_PATH, dtype=str)
        today_fids_df = read_saved_fids(TODAY_FIDS_PATH, TODAY_FIDS_NAME_PATH)
        tomorrow_fids_df = read_saved_fids(TOMORROW_FIDS_PATH, TOMORROW_FIDS_NAME_PATH)
        fids_lookup = build_fids_lookup(today_fids_df, tomorrow_fids_df)
        workers, colors, missing_cols = prepare_gantt_data(schedule_df, fids_lookup)
        if missing_cols:
            st.error("חסרות עמודות בקובץ הסידור: " + ", ".join(missing_cols))
            st.stop()
        html = build_gantt_html(workers, colors, fullscreen=True)
        components.html(html, height=980, scrolling=False)
    except Exception as exc:
        st.error("הייתה שגיאה בפתיחת הגאנט.")
        st.exception(exc)
    st.stop()


# =========================================================
# Main page
# =========================================================

st.markdown(
    """
<div class="ops-hero">
    <h1>✈️ iSchedule · גאנט עובדים</h1>
    <p>העלי סידור עבודה מוכן + FIDS של היום + FIDS של מחר. רק אחרי שלושת הקבצים יופיע הסידור והכפתור לגאנט.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="ops-card">', unsafe_allow_html=True)
    st.subheader("📂 העלאת קבצים")

    c1, c2, c3 = st.columns(3)
    with c1:
        schedule_file = st.file_uploader(
            "📋 העלה קובץ סידור עבודה מוכן",
            type=["xlsx"],
            key="schedule_file",
        )
    with c2:
        today_fids = st.file_uploader(
            "✈️ העלה FIDS של היום",
            type=["xlsx", "csv", "html"],
            key="today_fids",
        )
    with c3:
        tomorrow_fids = st.file_uploader(
            "🌙 העלה FIDS של מחר",
            type=["xlsx", "csv", "html"],
            key="tomorrow_fids",
        )

    st.markdown('</div>', unsafe_allow_html=True)

if schedule_file is None or today_fids is None or tomorrow_fids is None:
    st.info("יש להעלות סידור עבודה מוכן + FIDS של היום + FIDS של מחר")
    st.stop()

try:
    save_uploaded_file(schedule_file, SCHEDULE_PATH)
    save_uploaded_file(today_fids, TODAY_FIDS_PATH, TODAY_FIDS_NAME_PATH)
    save_uploaded_file(tomorrow_fids, TOMORROW_FIDS_PATH, TOMORROW_FIDS_NAME_PATH)

    schedule_df = pd.read_excel(schedule_file, dtype=str)
    today_fids_df = read_uploaded_table(today_fids, today_fids.name)
    tomorrow_fids_df = read_uploaded_table(tomorrow_fids, tomorrow_fids.name)
    fids_lookup = build_fids_lookup(today_fids_df, tomorrow_fids_df)
except Exception as exc:
    st.error("לא הצלחתי לקרוא את אחד הקבצים.")
    st.exception(exc)
    st.stop()

st.markdown('<div class="ops-card">', unsafe_allow_html=True)
st.subheader("📋 סידור עבודה")
st.caption("זה הקובץ שממנו הגאנט ישאב את העובדים, שעות המשמרת והמשימות.")
st.dataframe(schedule_df, use_container_width=True, height=420)
st.markdown('</div>', unsafe_allow_html=True)

workers, colors, missing_cols = prepare_gantt_data(schedule_df, fids_lookup)

if missing_cols:
    st.error("חסרות עמודות בקובץ הסידור כדי לבנות גאנט: " + ", ".join(missing_cols))
    st.info("צריך עמודת עובד/שם, התחלה וסיום. רצוי גם תחילת משמרת, סוף משמרת, טיסה ותפקיד.")
    st.stop()

st.markdown('<div class="ops-card">', unsafe_allow_html=True)
st.subheader("📊 גאנט עובדים")
st.write(f"נמצאו **{len(workers)} עובדים** עם משימות מתוזמנות.")

col_a, col_b = st.columns([1, 2])
with col_a:
    open_inline = st.button("📊 פתח גאנט עובדים", use_container_width=True)
with col_b:
    st.markdown(
        '<a class="gantt-link" href="?workers_gantt=true" target="_blank">🖥️ פתח גאנט במסך מלא בטאב חדש</a>',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

if open_inline:
    st.session_state["show_workers_gantt"] = True

if not st.session_state.get("show_workers_gantt", False):
    st.stop()

html = build_gantt_html(workers, colors, fullscreen=False)
components.html(html, height=max(620, len(workers) * 52 + 120), scrolling=True)

st.download_button(
    "⬇️ הורד גאנט כקובץ HTML",
    data=html.encode("utf-8"),
    file_name="workers_gantt.html",
    mime="text/html",
    use_container_width=True,
)
