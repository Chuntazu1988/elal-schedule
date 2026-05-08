import io
import re
import html
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="סידורומט",
    page_icon="👩🏼‍🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# STYLE
# =========================

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

.ops-rtl {
    direction: rtl;
    text-align: right;
    font-family: Arial, "Noto Sans Hebrew", sans-serif;
}

.ops-hero {
    direction: rtl;
    text-align: center;
    background: linear-gradient(90deg, #06172f 0%, #0b3972 50%, #06172f 100%);
    color: white;
    border-radius: 18px;
    padding: 26px 20px;
    margin-bottom: 16px;
    box-shadow: 0 10px 28px rgba(7, 27, 58, 0.24);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.ops-title {
    font-size: 34px;
    font-weight: 900;
    margin: 0;
}

.ops-subtitle {
    color: #d8e8ff;
    font-size: 18px;
    font-weight: 800;
    margin-top: 8px;
}

.flight-card {
    direction: rtl;
    text-align: right;
    border: 1px solid #d9e2ef;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 3px 12px rgba(0,0,0,.07);
    overflow: hidden;
    margin-bottom: 14px;
}

.flight-head {
    background: #071b3a;
    color: white;
    padding: 13px 16px;
}

.flight-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
}

.flight-name {
    font-size: 21px;
    font-weight: 900;
}

.flight-meta {
    color: #cfe2ff;
    font-size: 13px;
    font-weight: 800;
}

.req-line {
    margin-top: 10px;
    background: #123b70;
    border: 1px solid #315c91;
    border-radius: 12px;
    padding: 8px 10px;
    color: white;
    font-size: 13px;
    font-weight: 800;
}

.panel-title {
    direction: rtl;
    text-align: right;
    color: #0b3d78;
    font-size: 16px;
    font-weight: 900;
    margin: 8px 0 8px 0;
}

.assignment-line {
    direction: rtl;
    text-align: right;
    padding: 8px 10px;
    margin-bottom: 7px;
    border-radius: 10px;
    border: 1px solid #edf1f7;
    line-height: 1.45;
    font-size: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,.03);
}

.role-teamlead {
    background: #faf5ff;
    color: #5e168a;
    border-right: 5px solid #8e24aa;
    font-weight: 900;
}

.role-inspector {
    background: #fff5f5;
    color: #a30d19;
    border-right: 5px solid #d32f2f;
    font-weight: 900;
}

.role-guard {
    background: #f0fff4;
    color: #106b2f;
    border-right: 5px solid #2e7d32;
    font-weight: 900;
}

.role-agent {
    background: #ffffff;
    color: #1f2933;
    border-right: 5px solid #9fb7d7;
}

.role-queue {
    background: #fffaf0;
    color: #8a4b00;
    border-right: 5px solid #f0a000;
    font-weight: 900;
}

.role-trainee {
    background: #fffde7;
    color: #7a5a00;
    border-right: 5px solid #ffd54f;
    font-weight: 900;
}

.role-missing {
    background: #ffe8e8;
    color: #9b0000;
    border-right: 5px solid #d32f2f;
    font-weight: 900;
}

.small-note {
    direction: rtl;
    text-align: right;
    color: #667085;
    font-size: 13px;
}

@media (max-width: 850px) {
    .ops-title { font-size: 25px; }
    .ops-subtitle { font-size: 15px; }
    .flight-name { font-size: 18px; }
}

.color-legend {
    direction: rtl;
    text-align: right;
    background:#f8fbff;
    border:1px solid #d9e2ef;
    border-radius:14px;
    padding:12px 14px;
    margin-bottom:14px;
    font-size:14px;
    line-height:1.9;
}

.legend-item {
    display:inline-flex;
    align-items:center;
    gap:6px;
    margin-left:18px;
    white-space:nowrap;
    font-weight:800;
}

.legend-dot {
    width:13px;
    height:13px;
    border-radius:50%;
    display:inline-block;
    border:1px solid rgba(0,0,0,.18);
}

.dot-teamlead { background:#8e24aa; }
.dot-agent { background:#9fb7d7; }
.dot-queue { background:#f0a000; }
.dot-inspector { background:#d32f2f; }
.dot-guard { background:#2e7d32; }
.dot-trainee { background:#ffd54f; }
.dot-missing { background:#9b0000; }


/* Professional ops look */
body {
    background: #f4f7fb;
}

.ops-hero {
    position: relative;
    overflow: hidden;
    min-height: 115px;
}

.ops-hero::before {
    content: "✈︎";
    position: absolute;
    left: 24px;
    top: -18px;
    font-size: 92px;
    opacity: .12;
    transform: rotate(-12deg);
}

.ops-hero::after {
    content: "LY OPS  •  CHECK-IN  •  GATES  •  TSA  •  BOARDING";
    position: absolute;
    bottom: 10px;
    left: 20px;
    right: 20px;
    text-align: center;
    color: rgba(255,255,255,.16);
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 900;
}

.ops-title, .ops-subtitle {
    position: relative;
    z-index: 2;
}

.ops-top-strip {
    direction: rtl;
    text-align: center;
    display: grid;
    grid-template-columns: repeat(4, minmax(120px, 1fr));
    gap: 10px;
    margin: 12px 0 16px 0;
}

.ops-mini-card {
    background: white;
    border: 1px solid #d9e2ef;
    border-radius: 14px;
    padding: 10px 12px;
    box-shadow: 0 2px 8px rgba(7,27,58,.06);
    font-weight: 900;
    color: #071b3a;
}

.ops-mini-card span {
    display: block;
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    margin-top: 2px;
}

.color-legend {
    direction: rtl;
    text-align: right;
    background: #ffffff;
    border: 1px solid #d9e2ef;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 16px;
    box-shadow: 0 2px 10px rgba(7,27,58,.06);
}

.color-legend-title {
    font-weight: 900;
    color: #071b3a;
    margin-bottom: 10px;
    font-size: 15px;
}

.legend-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 8px 12px;
}

.legend-item {
    display: grid;
    grid-template-columns: 16px 82px 1fr;
    align-items: center;
    gap: 8px;
    background: #f8fbff;
    border: 1px solid #e8eef7;
    border-radius: 999px;
    padding: 7px 10px;
    font-size: 13px;
}

.legend-dot {
    width:13px;
    height:13px;
    border-radius:50%;
    display:inline-block;
    border:1px solid rgba(0,0,0,.18);
}

.legend-color-name {
    color: #475467;
    font-weight: 900;
}

.legend-role-name {
    color: #071b3a;
    font-weight: 900;
}

.dot-teamlead { background:#8e24aa; }
.dot-agent { background:#9fb7d7; }
.dot-queue { background:#f0a000; }
.dot-inspector { background:#d32f2f; }
.dot-guard { background:#2e7d32; }
.dot-trainee { background:#ffd54f; }
.dot-missing { background:#9b0000; }

.flight-card {
    border: 1px solid #cfd9e8;
}

.flight-head {
    background:
      radial-gradient(circle at 12% 10%, rgba(255,255,255,.14), transparent 24%),
      linear-gradient(90deg, #06172f 0%, #092b58 48%, #071b3a 100%);
}

.flight-name::before {
    content: "LY ";
    color: #ffd166;
    font-size: 12px;
    margin-left: 5px;
    letter-spacing: 1px;
}

.req-line {
    display: inline-block;
    max-width: 100%;
}

.panel-title {
    background: #eef5ff;
    border: 1px solid #d9e8fb;
    border-radius: 10px;
    padding: 8px 10px;
}

.assignment-line {
    font-weight: 750;
}

/* ── Swap row wrapper ── */
.swap-row-wrap {
    position: relative;
    margin-bottom: 7px;
}

/* The assignment line inside a swap row — no bottom margin (wrap handles it) */
.swap-row-wrap .assignment-line {
    margin-bottom: 0;
    cursor: default;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
}

/* Arrow trigger button */
.swap-arrow-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 15px;
    color: #6b7fa3;
    padding: 2px 4px;
    border-radius: 6px;
    transition: background 0.15s, color 0.15s;
    flex-shrink: 0;
    line-height: 1;
}
.swap-arrow-btn:hover {
    background: #e0eaff;
    color: #1a3d7a;
}

/* Popup card */
.swap-popup {
    direction: rtl;
    background: #ffffff;
    border: 1.5px solid #b8cef0;
    border-radius: 14px;
    box-shadow: 0 8px 32px rgba(7,27,58,0.18), 0 2px 8px rgba(7,27,58,0.08);
    padding: 16px 18px 14px 18px;
    margin-top: 6px;
    animation: popIn 0.18s cubic-bezier(.4,1.4,.6,1) both;
    z-index: 100;
}

@keyframes popIn {
    from { opacity: 0; transform: translateY(-8px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)   scale(1);    }
}

.swap-popup-title {
    font-size: 13px;
    font-weight: 900;
    color: #071b3a;
    margin-bottom: 10px;
    border-bottom: 1px solid #e8eef7;
    padding-bottom: 8px;
}

.swap-popup-label {
    font-size: 12px;
    font-weight: 800;
    color: #475467;
    margin-bottom: 4px;
    margin-top: 10px;
}

.swap-confirm-hint {
    font-size: 11px;
    color: #6b7fa3;
    margin-top: 10px;
    text-align: center;
}

@media (max-width: 850px) {
    .ops-top-strip { grid-template-columns: repeat(2, 1fr); }
    .legend-grid { grid-template-columns: 1fr; }
    .legend-item { grid-template-columns: 16px 70px 1fr; }
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ops-hero">
  <div class="ops-title">סידורומט 👩🏼‍🔧</div>
  <div class="ops-subtitle">סידור עבודה? קטן עלי!</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="color-legend">
  <div class="color-legend-title">מקרא צבעים</div>
  <div class="legend-grid">
    <div class="legend-item"><span class="legend-dot dot-teamlead"></span><span class="legend-color-name">סגול</span><span class="legend-role-name">ראש צוות</span></div>
    <div class="legend-item"><span class="legend-dot dot-agent"></span><span class="legend-color-name">כחול בהיר</span><span class="legend-role-name">דיילת</span></div>
    <div class="legend-item"><span class="legend-dot dot-queue"></span><span class="legend-color-name">כתום</span><span class="legend-role-name">מתאם תורים</span></div>
    <div class="legend-item"><span class="legend-dot dot-inspector"></span><span class="legend-color-name">אדום</span><span class="legend-role-name">מפקח TSA</span></div>
    <div class="legend-item"><span class="legend-dot dot-guard"></span><span class="legend-color-name">ירוק</span><span class="legend-role-name">שומר TSA</span></div>
    <div class="legend-item"><span class="legend-dot dot-trainee"></span><span class="legend-color-name">צהוב</span><span class="legend-role-name">טרייני רצ</span></div>
    <div class="legend-item"><span class="legend-dot dot-missing"></span><span class="legend-color-name">אדום כהה</span><span class="legend-role-name">חוסר שיבוץ</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ops-top-strip">
  <div class="ops-mini-card">🛫 המראות<span>סידור לפי טיסה</span></div>
  <div class="ops-mini-card">🧳 דלפקים<span>Check-in continuity</span></div>
  <div class="ops-mini-card">🚪 שערים<span>Boarding gates</span></div>
  <div class="ops-mini-card">🛡️ TSA<span>יעדים מיוחדים</span></div>
</div>
""", unsafe_allow_html=True)



# =========================
# RULE SETTINGS
# =========================

USA_TSA_DESTS = {"JFK", "LAX", "EWR", "FLL", "MIA", "BOS"}
QUEUE_DESTS = {"CDG", "LHR", "JFK", "EWR", "BCN"}
TWO_TEAM_LEADS_DESTS = {"BKK", "HKT"}

NARROW_REG_PREFIXES = ("EH", "EK")
WIDE_REG_PREFIXES = ("EC", "ED", "ER")
REMOTE_GATES = {"D1", "D1A", "C1", "C1A", "B1", "B1A", "E1", "E1A"}

ROLE_COLUMNS = [
    "ראש צוות",
    "דייל",
    "מתאם תורים",
    "מפקח TSA",
    "שומר TSA",
    "חונך רצים",
    "מסמיך רצים",
    "טרייני רצ",
]

ROLE_ORDER = ["ראש צוות", "טרייני רצ", "דייל", "מתאם תורים", "מפקח TSA", "שומר TSA"]


# =========================
# BASIC HELPERS
# =========================

def clean_text(value) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "nat"} else text


def safe_html(value) -> str:
    return html.escape(str(value))


def normalize_yes_no(value) -> str:
    text = clean_text(value).upper()
    return "כן" if text in {"Y", "YES", "כן", "TRUE", "1", "V", "✓", "✔"} else "לא"


def normalize_time_text(value: str) -> str:
    value = clean_text(value)
    match = re.search(r"(\d{1,2}):(\d{2})(?::\d{2})?", value)
    if not match:
        return ""
    return f"{int(match.group(1)):02d}:{int(match.group(2)):02d}"


def extract_shift_range_from_text(value):
    text = clean_text(value)
    text = (
        text.replace("–", "-")
            .replace("—", "-")
            .replace("−", "-")
            .replace("\u200f", "")
            .replace("\u200e", "")
            .replace("\xa0", " ")
    )
    times = re.findall(r"\d{1,2}:\d{2}(?::\d{2})?", text)
    if len(times) < 2:
        return "", ""
    start = normalize_time_text(times[0])
    end = normalize_time_text(times[1])
    return (start, end) if start and end else ("", "")


def clean_roster_name(value):
    text = clean_text(value)
    if not text:
        return ""

    if extract_shift_range_from_text(text)[0]:
        return ""

    text = re.sub(r"טרייני\s*[-–]\s*", "", text)
    text = re.sub(r"\bטרייני\s*ר[״\"]?צ\b", "", text)
    text = text.replace("טרייני ר״צ", "").replace('טרייני ר"צ', "").replace("טרייני רצ", "")
    text = re.sub(r"מש[׳']?\s*.*$", "", text)
    text = re.sub(r"עד\s+\d{1,2}:\d{2}.*$", "", text)

    bad_words = ["סידור", "יומי", "שלישי", "ד.", "שלנ", "שלן", "רצ", "ר״צ", "בידוק", "חוליה", "דיילים", "דלפק", "סיירת", "ש״ש", "שש"]
    stripped = text.strip()
    if any(word in stripped for word in bad_words) and len(stripped.split()) <= 3:
        return ""

    stripped = re.sub(r"[^א-תA-Za-z\s'\-]", " ", stripped)
    stripped = re.sub(r"\s+", " ", stripped).strip()

    if len(stripped.split()) < 2:
        return ""

    return stripped


def build_shift_map_from_excel(uploaded_file):
    """
    Scan the workbook and extract for each employee:
    - shift start/end (תחילת משמרת / סוף משמרת)
    - modified shift window (מש' עד / מש' מ / מש' HH:MM-HH:MM)
    - blocked time windows (רצ / בידוק חולייה / פיקוח TSA / מתדרכ/ת / ועדת היגוי / רענון TSA)
    - unavailable flag (SICK)
    - early end (עד HH:MM)

    Returns dict: name_key -> {
        "start": HH:MM, "end": HH:MM, "original": str,
        "blocked": [(start, end), ...],   # windows when employee is busy
        "sick": bool,
        "shift_end_override": HH:MM or None,
        "shift_start_override": HH:MM or None,
    }
    """
    shift_map = {}
    TIME_RANGE_RE   = re.compile(r"(\d{1,2}:\d{2})\s*[-–]\s*(\d{1,2}:\d{2})")
    SINGLE_TIME_RE  = re.compile(r"(\d{1,2}:\d{2})")

    BLOCKED_KEYWORDS = ["בידוק", "פיקוח", "מתדרכ", "ועדת היגוי", "רענון tsa", "רענון", "77"]
    SICK_KEYWORDS    = ["sick", "מחלה", "sick"]
    END_KEYWORDS     = ["עד ", "עד:"]
    START_KEYWORDS   = ["מש' מ", "מש מ", "משמרת מ"]
    END_SHIFT_KW     = ["מש' עד", "מש עד", "משמרת עד", "מש'"]

    def is_blocked_label(text):
        tl = text.lower()
        return any(kw in tl for kw in BLOCKED_KEYWORDS)

    def is_sick(text):
        tl = text.lower()
        return any(kw in tl for kw in SICK_KEYWORDS)

    try:
        uploaded_file.seek(0)
        sheets = pd.read_excel(uploaded_file, sheet_name=None, header=None, dtype=str)
    except Exception:
        return shift_map

    for sheet_name, raw in sheets.items():
        for col in raw.columns:
            current_start = ""
            current_end   = ""
            # Track if current header row is a "blocked" type
            current_blocked_range = None  # (start, end) if this section is a blocked type

            for row_i, cell in raw[col].items():
                cell_text = clean_text(cell)
                if not cell_text:
                    continue

                # Check for special inline format FIRST:
                # "NAME-תגבור בין HH:MM-HH:MM ואז בין HH:MM-HH:MM"
                is_availability_note = ('תגבור' in cell_text or 'ואז בין' in cell_text)
                if is_availability_note:
                    # Extract name part (before the dash)
                    dash_idx = cell_text.find('-')
                    name_part = cell_text[:dash_idx].strip() if dash_idx > 0 else cell_text
                    pn = clean_roster_name(name_part) if len(name_part.split()) >= 2 else name_part.strip()
                    if pn and current_start and current_end:
                        key = name_key(pn)
                        avail_windows = TIME_RANGE_RE.findall(cell_text)
                        entry = shift_map.get(key, {
                            "start":    current_start,
                            "end":      current_end,
                            "original": pn,
                            "blocked":  [],
                            "sick":     False,
                            "shift_end_override":   None,
                            "shift_start_override": None,
                            "available_windows": [],
                        })
                        if avail_windows:
                            entry["available_windows"] = [(normalize_time_text(ws), normalize_time_text(we)) for ws, we in avail_windows]
                        shift_map[key] = entry
                    # Do NOT update current_start/current_end — keep the real shift header
                    continue

                m = TIME_RANGE_RE.search(cell_text)
                if m:
                    s = normalize_time_text(m.group(1))
                    e = normalize_time_text(m.group(2))
                    if is_blocked_label(cell_text):
                        # Blocked section — save hours as shift AND as blocked
                        current_blocked_range = (s, e)
                        current_start = s
                        current_end   = e
                    else:
                        current_start = s
                        current_end   = e
                        current_blocked_range = None
                    continue

                # Not a time range header — try to parse as a name
                if not current_start or not current_end:
                    continue

                possible_name = clean_roster_name(cell_text)
                if not possible_name:
                    continue

                key = name_key(possible_name)

                # Parse per-name annotations
                sick            = is_sick(cell_text)
                shift_end_ovr   = None
                shift_start_ovr = None
                extra_blocked   = []

                # "מש' עד HH:MM" — shift ends early
                for kw in END_SHIFT_KW:
                    if kw in cell_text:
                        mt = SINGLE_TIME_RE.search(cell_text[cell_text.find(kw):])
                        if mt:
                            shift_end_ovr = normalize_time_text(mt.group(1))
                        break

                # "עד HH:MM" standalone — available only until that time
                if not shift_end_ovr:
                    for kw in END_KEYWORDS:
                        if kw in cell_text and kw not in END_SHIFT_KW:
                            mt = SINGLE_TIME_RE.search(cell_text[cell_text.find(kw):])
                            if mt:
                                shift_end_ovr = normalize_time_text(mt.group(1))
                            break

                # "מש' מ HH:MM" — shift starts late
                for kw in START_KEYWORDS:
                    if kw in cell_text:
                        mt = SINGLE_TIME_RE.search(cell_text[cell_text.find(kw):])
                        if mt:
                            shift_start_ovr = normalize_time_text(mt.group(1))
                        break

                # Inline blocked range e.g. "אילי סטמקר עד 00:30  18:00-19:30 רענון TSA"
                for rm in TIME_RANGE_RE.finditer(cell_text):
                    rs = normalize_time_text(rm.group(1))
                    re_ = normalize_time_text(rm.group(2))
                    # Check if the text around this range is a blocked keyword
                    surrounding = cell_text[max(0, rm.end()-30): rm.end()+30].lower()
                    if any(kw in surrounding for kw in BLOCKED_KEYWORDS):
                        extra_blocked.append((rs, re_))

                if key not in shift_map:
                    shift_map[key] = {
                        "start":    current_start,
                        "end":      current_end,
                        "original": possible_name,
                        "blocked":  [],
                        "sick":     False,
                        "shift_end_override":   None,
                        "shift_start_override": None,
                    }

                entry = shift_map[key]
                if sick:
                    entry["sick"] = True
                if shift_end_ovr and not entry["shift_end_override"]:
                    entry["shift_end_override"] = shift_end_ovr
                if shift_start_ovr and not entry["shift_start_override"]:
                    entry["shift_start_override"] = shift_start_ovr
                if current_blocked_range:
                    if current_blocked_range not in entry["blocked"]:
                        entry["blocked"].append(current_blocked_range)
                for eb in extra_blocked:
                    if eb not in entry["blocked"]:
                        entry["blocked"].append(eb)

    try:
        uploaded_file.seek(0)
    except Exception:
        pass

    return shift_map


def apply_shift_map_to_employees(employees_df, shift_map_with_names):
    """
    Apply shift times and annotations from the daily schedule to employees_df.
    Adds columns: תחילת משמרת, סוף משמרת, חסימות, חולה
    """
    df = employees_df.copy()

    for col in ["תחילת משמרת", "סוף משמרת", "חסימות", "חולה"]:
        if col not in df.columns:
            df[col] = "" if col != "חולה" else False

    def get_entry(emp_name):
        key = name_key(emp_name)
        if key in shift_map_with_names:
            return shift_map_with_names[key]
        # Fuzzy: 2+ shared words
        parts = set(emp_name.split())
        best = None; best_score = 1
        for _, entry in shift_map_with_names.items():
            shared = len(parts & set(entry["original"].split()))
            if shared > best_score:
                best_score = shared; best = entry
        return best

    for idx, row in df.iterrows():
        emp_name = clean_text(row.get("שם", ""))
        if not emp_name:
            continue
        if clean_text(df.at[idx, "תחילת משמרת"]):
            continue  # already set

        entry = get_entry(emp_name)
        if not entry:
            continue

        # Sick = not available at all
        if entry.get("sick"):
            df.at[idx, "חולה"] = True
            continue

        start = entry.get("shift_start_override") or entry["start"]
        end   = entry.get("shift_end_override")   or entry["end"]

        df.at[idx, "תחילת משמרת"] = start
        df.at[idx, "סוף משמרת"]   = end

        # Store blocked windows as "HH:MM-HH:MM,HH:MM-HH:MM"
        blocked = entry.get("blocked", [])
        if blocked:
            df.at[idx, "חסימות"] = ",".join(f"{s}-{e}" for s, e in blocked)

        # Store available windows (overrides shift for workers like נטע ונטוררו)
        avail = entry.get("available_windows", [])
        if avail and "זמינות" in df.columns or avail:
            if "זמינות" not in df.columns:
                df["זמינות"] = ""
            df.at[idx, "זמינות"] = ",".join(f"{s}-{e}" for s, e in avail)

    return df


def name_key(value) -> str:
    return re.sub(r"\s+", "", clean_text(value)).lower()


def flight_key(value) -> str:
    return re.sub(r"\s+", "", clean_text(value)).upper()


def parse_times(value):
    text = clean_text(value)
    match = re.search(r"(\d{2}:\d{2})\s*\((\d{2}:\d{2})\)", text)
    if match:
        return match.group(1), match.group(2)

    match = re.search(r"(\d{2}:\d{2})", text)
    if match:
        return match.group(1), ""

    return "", ""


def is_time_text(value):
    return bool(re.fullmatch(r"\d{2}:\d{2}", clean_text(value)))


def to_datetime_time(value):
    return datetime.strptime(clean_text(value), "%H:%M")


def time_to_minutes(value):
    h, m = clean_text(value).split(":")
    return int(h) * 60 + int(m)


def minutes_between(start, end):
    return int((end - start).total_seconds() / 60)


def short_flight_number(value):
    text = clean_text(value).upper().replace("LY", "").replace(" ", "")
    return text if text else clean_text(value)


def normalize_role_label(role):
    role = clean_text(role)
    if role.startswith("ראש צוות"):
        return "ראש צוות"
    if role.startswith("דייל"):
        return "דיילת"
    if role.startswith("מתאם"):
        return "מתאם תורים"
    if role.startswith("מפקח"):
        return "מפקח TSA"
    if role.startswith("שומר"):
        return "שומר TSA"
    if role.startswith("טרייני"):
        return "טרייני ר״צ"
    return role


def gender_role_label(role, employees_df, worker_name):
    """Return a gender-aware role title based on the employee's gender column."""
    base = normalize_role_label(role)
    if not worker_name or "❌" in worker_name:
        return base

    emp = employees_df[employees_df["שם"] == worker_name]
    if emp.empty:
        return base

    gender_col = next((c for c in emp.columns if clean_text(c) in {"מין", "gender", "זכר/נקבה", "מגדר"}), None)
    if not gender_col:
        return base

    gender = clean_text(emp.iloc[0].get(gender_col, "")).upper()
    is_male = gender in {"זכר", "M", "MALE", "ז"}

    gender_map = {
        "דיילת":      ("דייל",          "דיילת"),
        "מתאם תורים": ("מתאם תורים",    "מתאמת תורים"),
        "מפקח TSA":   ("מפקח TSA",      "מפקחת TSA"),
        "שומר TSA":   ("שומר TSA",      "שומרת TSA"),
    }

    if base in gender_map:
        male_form, female_form = gender_map[base]
        return male_form if is_male else female_form

    return base


def role_area(role):
    """Operational area for each task."""
    role = normalize_role_label(role)

    # These are flight/departure-hall roles.
    if role in {"ראש צוות", "דיילת", "מתאם תורים", "מפקח TSA", "שומר TSA", "טרייני רצ"}:
        return "שערי יציאה"

    return "דלפקי צ׳ק אין"


def default_area_for_employee(emp_row):
    """Default area when the worker is not assigned to a flight task."""
    if str(emp_row.get("ראש צוות", "")).strip() == "כן":
        return "שערי יציאה"
    return "דלפקי צ׳ק אין"


def employee_area_history(assignments, emp_name):
    areas = set()

    for task in assignments:
        if task.get("עובד") != emp_name:
            continue
        if "❌" in str(task.get("עובד", "")):
            continue
        areas.add(role_area(task.get("תפקיד", "")))

    return areas


def area_switch_penalty(assignments, emp, role):
    """
    Soft preference only.
    Certification does not lock a worker to one role.
    A TSA supervisor who is also qualified as team lead may still work as team lead / agent / queue coordinator.
    A regular agent may work queue coordinator or TSA if certified.
    This score only tries to reduce needless movement between counters and departure gates.
    """
    emp_name = emp["שם"]
    target_area = role_area(role)
    history = employee_area_history(assignments, emp_name)

    if not history:
        default_area = default_area_for_employee(emp)
        return 0 if default_area == target_area else 2

    if target_area in history:
        return 0

    return 5

def continuation_text_for_employee(timed_df, current_idx, emp, employees_df):
    """
    Returns the next operational text without using vague labels like 'המשך אולם יציאה'.
    """
    next_plain = next_task_plain_text(timed_df, current_idx, emp)

    if next_plain:
        return next_plain

    row = timed_df.loc[current_idx]
    emp_row = employees_df[employees_df["שם"] == emp]
    if emp_row.empty:
        return "חזרה"

    task_end_dt = to_datetime_time(row["סיום"])
    return return_text_by_shift(emp_row.iloc[0], task_end_dt)

def break_label_for_employee(emp_row):
    length = shift_length(emp_row)
    if length > 9 * 60 + 30:
        return "הפסקה ורענון"
    if length > 6 * 60:
        return "הפסקה"
    if length > 0:
        return "רענון"
    return ""


def required_break(emp):
    length = shift_length(emp)
    if length > 9 * 60 + 30:
        return 65
    if length > 6 * 60:
        return 45
    if length > 0:
        return 20  # רענון — shorter
    return 0


def shift_end_datetime(emp_row):
    end_text = clean_text(emp_row.get("סוף משמרת", ""))
    if not is_time_text(end_text):
        return None
    return to_datetime_time(end_text)


def minutes_until_shift_end(emp_row, task_end_dt):
    end_dt = shift_end_datetime(emp_row)
    if end_dt is None:
        return None

    end_min = end_dt.hour * 60 + end_dt.minute
    task_min = task_end_dt.hour * 60 + task_end_dt.minute

    if end_min < task_min:
        end_min += 24 * 60

    return end_min - task_min


def return_text_by_shift(emp_row, task_end_dt):
    """
    חזרה means leaving departure-gate duty:
    - If enough shift remains: return to check-in counters.
    - If close to shift end: return home / end shift.
    """
    remaining = minutes_until_shift_end(emp_row, task_end_dt)

    if remaining is None:
        return "חזרה"

    if remaining <= 30:
        return "חזרה הביתה"

    return "חזרה לדלפקים"


def gap_minutes_to_next(timed_df, current_idx, emp):
    row = timed_df.loc[current_idx]
    future = timed_df[
        (timed_df["עובד"].astype(str) == emp) &
        (timed_df["_start_dt"] > row["_start_dt"])
    ].sort_values("_start_dt")

    if future.empty:
        return None

    current_end = to_datetime_time(row["סיום"])
    next_start = to_datetime_time(future.iloc[0]["התחלה"])
    gap = minutes_between(current_end, next_start)

    if gap < 0:
        gap += 24 * 60

    return gap


def next_task_plain_text(timed_df, current_idx, emp):
    row = timed_df.loc[current_idx]
    future = timed_df[
        (timed_df["עובד"].astype(str) == emp) &
        (timed_df["_start_dt"] > row["_start_dt"])
    ].sort_values("_start_dt")

    if future.empty:
        return ""

    next_row = future.iloc[0]
    next_flight = short_flight_number(next_row["טיסה"])
    next_role = normalize_role_label(next_row["תפקיד"])
    return f"{next_flight} {next_role}"


def safe_sort_by_time(df, col):
    df = df.copy()
    df["_sort_time"] = pd.to_datetime(df[col], format="%H:%M", errors="coerce")
    df = df.sort_values("_sort_time").drop(columns=["_sort_time"])
    return df


def find_column(df, options):
    normalized = {str(c).strip(): c for c in df.columns}
    for opt in options:
        if opt in normalized:
            return normalized[opt]
    return None


# =========================
# LOAD FILES
# =========================

def load_daily_schedule(uploaded_file):
    excel = pd.ExcelFile(uploaded_file)
    sheet_name = "דוח שיבוץ טיסות - המראות" if "דוח שיבוץ טיסות - המראות" in excel.sheet_names else excel.sheet_names[0]
    raw = pd.read_excel(uploaded_file, sheet_name=sheet_name)
    raw.columns = raw.columns.astype(str).str.strip()

    flights = []

    # Original daily report layout
    if {"Unnamed: 8", "Unnamed: 7", "Unnamed: 6"}.issubset(set(raw.columns)):
        for _, row in raw.iterrows():
            flight = row.get("Unnamed: 8")
            time_text = row.get("Unnamed: 7")
            destination = row.get("Unnamed: 6")
            aircraft = row.get("Unnamed: 5")

            flight_text = clean_text(flight)
            if not flight_text.startswith("LY"):
                continue
            # Skip cargo flights — LY8xxx
            flight_num = flight_text.replace("LY", "").strip()
            if flight_num.startswith("8"):
                continue

            departure, boarding = parse_times(time_text)

            flights.append({
                "טיסה": flight_text,
                "יעד": clean_text(destination).upper(),
                "המראה": departure,
                "בורדינג": boarding,
                "גייט": "",
                "סוג מטוס": clean_text(aircraft),
                "רישוי": "",
                "נוסעים": "",
                "טרייני רצ": "לא",
                "סוג הכשרה": "",
            })
    else:
        flight_col = find_column(raw, ["טיסה", "מספר טיסה", "Flight", "flight"])
        dest_col = find_column(raw, ["יעד", "Destination", "destination"])
        dep_col = find_column(raw, ["המראה", "זמן המראה", "Departure", "departure"])
        board_col = find_column(raw, ["בורדינג", "תחילת בורדינג", "Boarding", "boarding"])
        gate_col = find_column(raw, ["גייט", "שער", "Gate", "gate"])
        aircraft_col = find_column(raw, ["סוג מטוס", "מטוס", "Aircraft", "aircraft"])
        reg_col = find_column(raw, ["רישוי", "רישום", "Registration", "registration"])
        pax_col = find_column(raw, ["נוסעים", "PAX", "pax"])
        trainee_col = find_column(raw, ["טרייני רצ", "טרייני ר״צ", 'טרייני ר"צ'])
        training_col = find_column(raw, ["סוג הכשרה", "הכשרה"])

        if not flight_col:
            raise ValueError("לא נמצאה עמודת טיסה בקובץ הסידור")

        for _, row in raw.iterrows():
            flight_text = clean_text(row.get(flight_col))
            if not flight_text.startswith("LY"):
                continue
            # Skip cargo flights — LY8xxx
            if flight_text.replace("LY", "").strip().startswith("8"):
                continue

            dep = clean_text(row.get(dep_col)) if dep_col else ""
            boarding = clean_text(row.get(board_col)) if board_col else ""

            if not is_time_text(dep):
                dep, parsed_boarding = parse_times(dep)
                if not boarding:
                    boarding = parsed_boarding

            flights.append({
                "טיסה": flight_text,
                "יעד": clean_text(row.get(dest_col)).upper() if dest_col else "",
                "המראה": dep,
                "בורדינג": boarding,
                "גייט": clean_text(row.get(gate_col)) if gate_col else "",
                "סוג מטוס": clean_text(row.get(aircraft_col)) if aircraft_col else "",
                "רישוי": clean_text(row.get(reg_col)) if reg_col else "",
                "נוסעים": clean_text(row.get(pax_col)) if pax_col else "",
                "טרייני רצ": normalize_yes_no(row.get(trainee_col)) if trainee_col else "לא",
                "סוג הכשרה": clean_text(row.get(training_col)) if training_col else "",
            })

    flights_df = pd.DataFrame(flights)

    if flights_df.empty:
        return pd.DataFrame(columns=[
            "טיסה", "יעד", "המראה", "בורדינג", "גייט", "סוג מטוס", "רישוי", "נוסעים", "טרייני רצ", "סוג הכשרה"
        ])

    flights_df["_flight_key"] = flights_df["טיסה"].apply(flight_key)
    flights_df = flights_df.drop_duplicates(subset=["_flight_key"], keep="first").drop(columns=["_flight_key"])
    flights_df = flights_df[flights_df["המראה"].astype(str).str.strip() != ""].copy()
    flights_df = safe_sort_by_time(flights_df, "המראה")

    return flights_df


def normalize_employees(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    if "שם" not in df.columns:
        raise ValueError("בקובץ העובדים חייבת להיות עמודה בשם: שם")

    aliases = {
        "מפקח tsa": "מפקח TSA",
        "שומר tsa": "שומר TSA",
        "טרייני ר״צ": "טרייני רצ",
        'טרייני ר"צ': "טרייני רצ",
        "ראש צוות חונך": "חונך רצים",
        "ראש צוות מסמיך": "מסמיך רצים",
    }

    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]

    df["שם"] = df["שם"].apply(clean_text)
    df = df[df["שם"] != ""].copy()
    df["_name_key"] = df["שם"].apply(name_key)

    for col in ROLE_COLUMNS:
        if col not in df.columns:
            df[col] = "לא"
        df[col] = df[col].apply(normalize_yes_no)

    for col in ["תחילת משמרת", "סוף משמרת", "חסימות", "חולה"]:
        if col not in df.columns:
            df[col] = "" if col != "חולה" else False
        if col in ["תחילת משמרת", "סוף משמרת", "חסימות"]:
            df[col] = df[col].apply(clean_text)

    return df


# =========================
# FLIGHT RULES
# =========================

def get_body_type(flight):
    reg = clean_text(flight.get("רישוי", "")).upper()
    aircraft = clean_text(flight.get("סוג מטוס", "")).upper()

    if reg.startswith(NARROW_REG_PREFIXES):
        return "צר גוף"
    if reg.startswith(WIDE_REG_PREFIXES):
        return "רחב גוף"
    if aircraft.startswith(("737", "738", "739", "E")):
        return "צר גוף"

    return "רחב גוף"


def is_remote_gate(gate):
    return clean_text(gate).upper() in REMOTE_GATES


def get_pax(flight):
    value = flight.get("נוסעים", 0)
    if pd.isna(value) or clean_text(value) == "":
        return 0
    try:
        return int(float(value))
    except Exception:
        return 0


def get_requirements(flight):
    dest = clean_text(flight["יעד"]).upper()
    body = get_body_type(flight)
    pax = get_pax(flight)

    req = {
        "ראש צוות": 1,
        "דייל": 1,
        "מתאם תורים": 0,
        "מפקח TSA": 0,
        "שומר TSA": 0,
        "טרייני רצ": 0,
    }

    if body == "צר גוף":
        req["דייל"] = 1 if pax <= 150 else 2
    else:
        if dest in USA_TSA_DESTS:
            # שומר TSA הוא חלק מצוות 5 — 4 דיילים + 1 שומר
            req["דייל"] = 4
            req["שומר TSA"] = 1
        else:
            req["דייל"] = 3

    if dest in TWO_TEAM_LEADS_DESTS:
        req["ראש צוות"] = 2

    if dest in QUEUE_DESTS:
        req["מתאם תורים"] = 1

    if dest in USA_TSA_DESTS:
        req["מפקח TSA"] = 1

    return req


def requirements_text(flight):
    req = get_requirements(flight)
    parts = []
    for role in ROLE_ORDER:
        amount = req.get(role, 0)
        if amount > 0:
            parts.append(role if amount == 1 else f"{role} × {amount}")
    return parts


def role_start_time(flight, role):
    departure = to_datetime_time(flight["המראה"])
    body = get_body_type(flight)
    remote_narrow = body == "צר גוף" and is_remote_gate(flight.get("גייט", ""))

    if role in {"ראש צוות", "מתאם תורים", "טרייני רצ"}:
        minutes_before = 60 if body == "צר גוף" else 75
    elif role == "דייל":
        minutes_before = 50 if body == "צר גוף" else 65
    elif role in {"מפקח TSA", "שומר TSA"}:
        minutes_before = 120
    else:
        minutes_before = 60

    if remote_narrow:
        minutes_before += 10

    return departure - timedelta(minutes=minutes_before)


def role_end_time(flight):
    return to_datetime_time(flight["המראה"])


# =========================
# SHIFT / AVAILABILITY
# =========================

# Early morning shift: starts 02:00-02:59, ends 08:00-09:30
EARLY_MORNING_START_MAX = 3 * 60       # 03:00
EARLY_MORNING_END_MIN   = 8 * 60       # 08:00
EARLY_MORNING_END_MAX   = 9 * 60 + 30  # 09:30

# Night shift: starts before midnight (21:00-23:59), ends 06:00-08:30
NIGHT_START_MIN = 21 * 60   # 21:00
NIGHT_END_MIN   = 6  * 60   # 06:00
NIGHT_END_MAX   = 8  * 60 + 30  # 08:30

# Late shift: ends by 01:30 — preferred for flights up to 01:30
LATE_SHIFT_END_MAX = 1 * 60 + 30  # 01:30


def classify_shift(emp):
    """
    Returns one of: 'early_morning', 'night', 'late', 'day', 'unknown'
    """
    ss = clean_text(emp.get("תחילת משמרת", ""))
    se = clean_text(emp.get("סוף משמרת",   ""))
    if not is_time_text(ss) or not is_time_text(se):
        return "unknown"

    s = time_to_minutes(ss)
    e = time_to_minutes(se)

    # Early morning: starts 02:00-02:59, ends 08:00-09:30
    if s < EARLY_MORNING_START_MAX and EARLY_MORNING_END_MIN <= e <= EARLY_MORNING_END_MAX:
        return "early_morning"

    # Night: starts 21:00-23:59 (before midnight), ends 06:00-08:30 (next day)
    if s >= NIGHT_START_MIN:
        # end is next day — e < s means overnight
        if e < s and NIGHT_END_MIN <= e <= NIGHT_END_MAX:
            return "night"

    # Late: ends by 01:30 (e <= 90 and shift goes through midnight, or day shift ending before 01:30)
    if e <= LATE_SHIFT_END_MAX and e < s:   # overnight ending early
        return "late"
    if e <= LATE_SHIFT_END_MAX and s > 12 * 60:  # evening ending before 01:30
        return "late"

    return "day"


def break_deadline_before_flight(emp, task_start_minutes):
    """
    For early morning shifts: calculate latest time employee must START their break
    so they can: break (45 min) + walk to gate (15 min) + arrive at gate on time.
    Returns the break deadline as HH:MM string, or None if not applicable.
    """
    if classify_shift(emp) != "early_morning":
        return None

    # task_start_minutes = when they need to be at the gate
    # deadline = task_start - 15 min walk - 45 min break
    deadline_min = task_start_minutes - 15 - 45
    if deadline_min < 0:
        deadline_min += 1440
    h = (deadline_min // 60) % 24
    m = deadline_min % 60
    return f"{h:02d}:{m:02d}"

MAX_CONTINUOUS_WORK_MINUTES = 4 * 60  # 4 hours max without break
NIGHT_BREAK_WINDOW_START = 0 * 60    # 00:00
NIGHT_BREAK_WINDOW_END   = 2 * 60    # 02:00


def minutes_worked_since_shift_start(assignments, emp_name, emp, until_time_minutes):
    ss = clean_text(emp.get("תחילת משמרת", ""))
    if not is_time_text(ss):
        return 0
    shift_start_m = time_to_minutes(ss)
    total = 0
    for task in assignments:
        if task["עובד"] != emp_name:
            continue
        ts_str = clean_text(task.get("התחלה", ""))
        te_str = clean_text(task.get("סיום",   ""))
        if not ts_str or not te_str:
            continue
        try:
            ts = time_to_minutes(ts_str)
            te = time_to_minutes(te_str)
            if ts < shift_start_m: ts += 1440
            if te < shift_start_m: te += 1440
            if te < ts: te += 1440
            until = until_time_minutes
            if until < shift_start_m: until += 1440
            te_capped = min(te, until)
            if te_capped > ts:
                total += te_capped - ts
        except Exception:
            pass
    return total


def would_exceed_max_continuous(assignments, emp_name, emp, task_start, task_end):
    """Returns True if this task would push employee over 4h continuous work."""
    ss = clean_text(emp.get("תחילת משמרת", ""))
    if not is_time_text(ss):
        return False
    shift_start_m = time_to_minutes(ss)
    ts = task_start.hour * 60 + task_start.minute
    te = task_end.hour   * 60 + task_end.minute
    if ts < shift_start_m: ts += 1440
    if te < shift_start_m: te += 1440
    if te < ts: te += 1440
    worked = minutes_worked_since_shift_start(assignments, emp_name, emp, te)
    worked += (te - ts)
    return worked > MAX_CONTINUOUS_WORK_MINUTES


def night_break_window_passed(assignments, emp_name):
    """Check if a break gap already exists in the 00:00-02:00 window."""
    tasks = sorted(
        [t for t in assignments if t.get("עובד") == emp_name and clean_text(t.get("סיום",""))],
        key=lambda t: time_to_minutes(clean_text(t.get("התחלה","00:00")))
    )
    for i in range(len(tasks) - 1):
        te_str = clean_text(tasks[i].get("סיום", ""))
        ts_str = clean_text(tasks[i+1].get("התחלה", ""))
        if not te_str or not ts_str: continue
        try:
            te = time_to_minutes(te_str)
            ts = time_to_minutes(ts_str)
            if ts < te: ts += 1440
            gap = ts - te
            te_in_window = NIGHT_BREAK_WINDOW_START <= (te % 1440) <= NIGHT_BREAK_WINDOW_END
            if gap >= 30 and te_in_window:
                return True
        except Exception:
            pass
    return False


def shift_length(emp):
    shift_start = clean_text(emp.get("תחילת משמרת", ""))
    shift_end = clean_text(emp.get("סוף משמרת", ""))

    if not is_time_text(shift_start) or not is_time_text(shift_end):
        return 0

    s = time_to_minutes(shift_start)
    e = time_to_minutes(shift_end)

    if e < s:
        e += 24 * 60

    return e - s



def is_within_shift(emp, task_start, task_end):
    shift_start = clean_text(emp.get("תחילת משמרת", ""))
    shift_end   = clean_text(emp.get("סוף משמרת", ""))

    if not is_time_text(shift_start) or not is_time_text(shift_end):
        return False

    ts = task_start.hour * 60 + task_start.minute
    te = task_end.hour   * 60 + task_end.minute

    # If employee has specific availability windows (e.g. נטע ונטוררו style)
    avail_str = clean_text(emp.get("זמינות", ""))
    if avail_str:
        for window in avail_str.split(","):
            if "-" not in window: continue
            try:
                ws, we = window.strip().split("-", 1)
                ws_m = time_to_minutes(ws.strip())
                we_m = time_to_minutes(we.strip())
                if we_m < ws_m: we_m += 1440
                ts_n = ts if ts >= ws_m else ts + 1440
                te_n = te if te >= ts_n % 1440 else te + 1440
                if te_n <= ts_n: te_n += 1440
                if ts_n >= ws_m and te_n <= we_m:
                    return True
            except Exception:
                pass
        return False  # not in any available window

    s  = time_to_minutes(shift_start)
    e  = time_to_minutes(shift_end)

    # Normalize shift to a continuous range
    if e <= s:
        e += 1440

    # Try task in both frames
    for ts_norm in [ts, ts + 1440]:
        te_norm = te if te > ts_norm % 1440 else te + 1440
        if te_norm <= ts_norm:
            te_norm += 1440
        if ts_norm >= s and te_norm <= e:
            return True

    return False


def assigned_minutes(assignments, emp_name):
    total = 0
    for task in assignments:
        if task["עובד"] != emp_name:
            continue
        if clean_text(task.get("התחלה", "")) == "" or clean_text(task.get("סיום", "")) == "":
            continue
        total += minutes_between(to_datetime_time(task["התחלה"]), to_datetime_time(task["סיום"]))
    return total


def has_room_for_break(assignments, emp, emp_name, start, end):
    length = shift_length(emp)
    if length == 0:
        return False  # No shift = not working today

    current = assigned_minutes(assignments, emp_name)
    new = minutes_between(start, end)
    return current + new + required_break(emp) <= length


def is_available(assignments, emp_name, start, end, emp_row=None):
    """Check if employee has no overlapping task or blocked window."""

    # Check sick status
    if emp_row is not None and emp_row.get("חולה", False):
        return False

    # Check blocked windows from daily schedule annotations
    if emp_row is not None:
        blocked_str = clean_text(emp_row.get("חסימות", ""))
        if blocked_str:
            ts = start.hour * 60 + start.minute
            te = end.hour   * 60 + end.minute
            if te < ts: te += 1440
            for window in blocked_str.split(","):
                if "-" not in window: continue
                try:
                    ws, we = window.strip().split("-", 1)
                    ws_m = time_to_minutes(ws.strip())
                    we_m = time_to_minutes(we.strip())
                    if we_m < ws_m: we_m += 1440
                    # Check overlap with buffer
                    if not (ts >= we_m + 5 or te <= ws_m - 5):
                        return False
                except Exception:
                    pass

    # Check existing assignments
    def to_m(dt): return dt.hour * 60 + dt.minute

    start_m = to_m(start)
    end_m   = to_m(end)
    if end_m < start_m: end_m += 1440

    for task in assignments:
        if task["עובד"] != emp_name:
            continue
        if clean_text(task.get("התחלה", "")) == "" or clean_text(task.get("סיום", "")) == "":
            continue

        es = to_datetime_time(task["התחלה"])
        ee = to_datetime_time(task["סיום"])
        es_m = to_m(es)
        ee_m = to_m(ee)
        if ee_m < es_m: ee_m += 1440

        buf = 5
        if not (start_m >= ee_m + buf or end_m <= es_m - buf):
            return False

    return True


# =========================
# ASSIGNMENT ENGINE
# =========================

def count_all_tasks(assignments, emp_name):
    return sum(1 for task in assignments if task["עובד"] == emp_name)


def count_team_lead_tasks(assignments, emp_name):
    return sum(
        1 for task in assignments
        if task["עובד"] == emp_name and str(task["תפקיד"]).startswith("ראש צוות")
    )


def tasks_in_window(assignments, emp_name, window_start, window_end):
    """Count how many tasks the employee already has that overlap or are close to this time window."""
    buffer = timedelta(hours=3)
    count = 0
    for task in assignments:
        if task["עובד"] != emp_name:
            continue
        if clean_text(task.get("התחלה", "")) == "":
            continue
        try:
            ts = to_datetime_time(task["התחלה"])
            te = to_datetime_time(task["סיום"])
            # Count tasks that are within a 3-hour window
            if not (ts > window_end + buffer or te < window_start - buffer):
                count += 1
        except Exception:
            pass
    return count


def sort_candidates(candidates, assignments, role, task_start=None, task_end=None):
    candidates = candidates.copy()

    if candidates.empty:
        return candidates

    candidates["_area_penalty"] = candidates.apply(
        lambda row: area_switch_penalty(assignments, row, role),
        axis=1,
    )
    candidates["_task_count"] = candidates["שם"].apply(lambda name: count_all_tasks(assignments, name))

    if task_start and task_end:
        candidates["_nearby_tasks"] = candidates["שם"].apply(
            lambda name: -tasks_in_window(assignments, name, task_start, task_end)
        )
    else:
        candidates["_nearby_tasks"] = 0

    # ── NEW: prefer workers whose shift starts closest to task_start ──
    # Workers with no tasks yet should start close to their shift start.
    # Workers already assigned are sorted by nearby tasks (already handled).
    def shift_start_proximity(emp_row):
        """
        For workers with no assignments yet: return gap (minutes) between
        shift start and task_start. Smaller gap = better fit = lower score.
        Workers already assigned get 0 (already in the area).
        """
        if not task_start:
            return 0
        name = emp_row["שם"]
        if count_all_tasks(assignments, name) > 0:
            return 0  # already assigned — proximity handled by nearby_tasks

        ss = clean_text(emp_row.get("תחילת משמרת", ""))
        if not is_time_text(ss):
            return 9999

        s = time_to_minutes(ss)
        t = task_start.hour * 60 + task_start.minute

        # Normalize for overnight shifts
        if t < s:
            t += 1440

        gap = t - s  # minutes after shift start that task begins
        return gap  # smaller = task starts right after shift start = preferred

    candidates["_shift_proximity"] = candidates.apply(shift_start_proximity, axis=1)

    # Shift priority: for flights ending before 01:30, prefer non-night workers
    flight_before_130 = False
    if task_end:
        te_m = task_end.hour * 60 + task_end.minute
        flight_before_130 = (te_m <= LATE_SHIFT_END_MAX)

    def shift_priority(emp_row):
        if not flight_before_130:
            return 0
        sc = classify_shift(emp_row)
        return {"late": 0, "day": 1, "early_morning": 2, "night": 3, "unknown": 4}.get(sc, 4)

    candidates["_shift_priority"] = candidates.apply(shift_priority, axis=1)

    sort_cols_base = ["_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_task_count"]

    if role == "ראש צוות":
        candidates["_role_count"] = candidates["שם"].apply(lambda name: count_team_lead_tasks(assignments, name))
        return candidates.sort_values(["_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_role_count", "_task_count"])

    if role == "דייל":
        candidates["_role_fit"] = candidates.apply(
            lambda row: 0 if str(row.get("ראש צוות", "")).strip() == "כן" else 1,
            axis=1,
        )
        return candidates.sort_values(["_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_role_fit", "_task_count"])

    return candidates.sort_values(sort_cols_base)

def has_required_mentor(assignments_for_flight, employees_df, training_type):
    required_col = "מסמיך רצים" if training_type == "הסמכה" else "חונך רצים"

    for task in assignments_for_flight:
        if str(task["תפקיד"]).startswith("ראש צוות") and "❌" not in str(task["עובד"]):
            emp = employees_df[employees_df["שם"] == task["עובד"]]
            if not emp.empty and str(emp.iloc[0].get(required_col, "")).strip() == "כן":
                return True

    return False


def has_trainee_available(employees_df):
    if "טרייני רצ" not in employees_df.columns:
        return False
    return (employees_df["טרייני רצ"].astype(str).str.strip() == "כן").any()


def flight_has_mentor_teamlead(assignments_for_flight, employees_df, training_type):
    """
    True only if the flight already has a real team lead who is חונך רצים/מסמיך רצים.
    If סוג הכשרה is הסמכה, only מסמיך רצים is valid.
    Otherwise either חונך or מסמיך is valid.
    """
    required_cols = ["חונך רצים", "מסמיך רצים"]
    if clean_text(training_type) == "הסמכה":
        required_cols = ["מסמיך רצים"]

    for task in assignments_for_flight:
        if not str(task.get("תפקיד", "")).startswith("ראש צוות"):
            continue

        worker = str(task.get("עובד", ""))
        if "❌" in worker:
            continue

        emp = employees_df[employees_df["שם"] == worker]
        if emp.empty:
            continue

        row = emp.iloc[0]
        for col in required_cols:
            if str(row.get(col, "")).strip() == "כן":
                return True

    return False


def has_trainee_available(employees_df):
    if "טרייני רצ" not in employees_df.columns:
        return False
    return (employees_df["טרייני רצ"].astype(str).str.strip() == "כן").any()


def trainee_already_used(assignments):
    for task in assignments:
        if str(task.get("תפקיד בסיס", "")) == "טרייני רצ" and "❌" not in str(task.get("עובד", "")):
            return True
    return False


def build_schedule(flights_df, employees_df):
    assignments = []
    flights_df = flights_df.copy()
    flights_df["_flight_key"] = flights_df["טיסה"].apply(flight_key)
    flights_df = flights_df.drop_duplicates(subset=["_flight_key"], keep="first").drop(columns=["_flight_key"])

    for _, flight in flights_df.iterrows():
        if clean_text(flight.get("המראה", "")) == "":
            continue

        req = get_requirements(flight)
        used_on_flight = set()
        assignments_for_flight = []

        trainee_needed = req.get("טרייני רצ", 0) > 0
        training_type = clean_text(flight.get("סוג הכשרה", "חניכה")) or "חניכה"

        for role in ROLE_ORDER:
            amount = req.get(role, 0)

            for i in range(amount):
                start = role_start_time(flight, role)
                end = role_end_time(flight)

                candidates = employees_df[
                    (employees_df[role].astype(str).str.strip() == "כן") &
                    (~employees_df["_name_key"].isin(used_on_flight))
                ].copy()

                if role == "ראש צוות" and trainee_needed:
                    mentor_col = "מסמיך רצים" if training_type == "הסמכה" else "חונך רצים"
                    if mentor_col not in candidates.columns:
                        candidates[mentor_col] = "לא"

                    mentors = candidates[candidates[mentor_col].astype(str).str.strip() == "כן"]
                    if not mentors.empty:
                        candidates = mentors

                candidates = sort_candidates(candidates, assignments, role, start, end)

                selected = None
                for _, emp in candidates.iterrows():
                    name = emp["שם"]
                    if (
                        is_within_shift(emp, start, end)
                        and is_available(assignments, name, start, end, emp)
                        and has_room_for_break(assignments, emp, name, start, end)
                        and not would_exceed_max_continuous(assignments, name, emp, start, end)
                    ):
                        selected = name
                        break

                # Fallback: if no ideal candidate, accept someone who exceeds 4h rule
                # (break will be adjusted — closing gaps is top priority)
                if not selected:
                    for _, emp in candidates.iterrows():
                        name = emp["שם"]
                        if (
                            is_within_shift(emp, start, end)
                            and is_available(assignments, name, start, end, emp)
                            and has_room_for_break(assignments, emp, name, start, end)
                        ):
                            selected = name
                            break

                if selected:
                    worker = selected
                    used_on_flight.add(name_key(worker))
                else:
                    worker = f"❌ חסר {role}"

                task = {
                    "טיסה": flight["טיסה"],
                    "יעד": flight["יעד"],
                    "תפקיד": role if amount == 1 else f"{role} {i+1}",
                    "תפקיד בסיס": role,
                    "עובד": worker,
                    "התחלה": start.strftime("%H:%M"),
                    "סיום": end.strftime("%H:%M"),
                }

                assignments.append(task)
                assignments_for_flight.append(task)

        # טרייני ר״צ
        if (
            has_trainee_available(employees_df)
            and flight_has_mentor_teamlead(assignments_for_flight, employees_df, training_type)
        ):
            role = "טרייני רצ"
            start = role_start_time(flight, role)
            end = role_end_time(flight)

            candidates = employees_df[
                (employees_df[role].astype(str).str.strip() == "כן") &
                (~employees_df["_name_key"].isin(used_on_flight))
            ].copy()

            candidates = sort_candidates(candidates, assignments, role, start, end)

            selected = None
            for _, emp in candidates.iterrows():
                name = emp["שם"]
                if (
                    is_within_shift(emp, start, end)
                    and is_available(assignments, name, start, end, emp)
                    and has_room_for_break(assignments, emp, name, start, end)
                    and not would_exceed_max_continuous(assignments, name, emp, start, end)
                ):
                    selected = name
                    break

            # Fallback without 4h rule
            if not selected:
                for _, emp in candidates.iterrows():
                    name = emp["שם"]
                    if (
                        is_within_shift(emp, start, end)
                        and is_available(assignments, name, start, end, emp)
                        and has_room_for_break(assignments, emp, name, start, end)
                    ):
                        selected = name
                        break

            if selected:
                task = {
                    "טיסה": flight["טיסה"],
                    "יעד": flight["יעד"],
                    "תפקיד": "טרייני ר״צ",
                    "תפקיד בסיס": "טרייני רצ",
                    "עובד": selected,
                    "התחלה": start.strftime("%H:%M"),
                    "סיום": end.strftime("%H:%M"),
                }
                assignments.append(task)
                assignments_for_flight.append(task)
                used_on_flight.add(name_key(selected))

    return pd.DataFrame(assignments)


def upgrade_teamleads(assignments_df, employees_df):
    """
    Second pass: for each missing ראש צוות slot, check if a qualified TL
    is assigned as דייל on a concurrent flight. If so:
    - Move that TL to the missing ראש צוות slot
    - Replace the vacated דייל slot with a plain agent
    Priority: close ראש צוות gaps first.
    """
    assignments = assignments_df.to_dict("records")

    def tasks_overlap(t1, t2):
        """Return True if two task dicts have overlapping time."""
        try:
            s1 = time_to_minutes(t1["התחלה"]); e1 = time_to_minutes(t1["סיום"])
            s2 = time_to_minutes(t2["התחלה"]); e2 = time_to_minutes(t2["סיום"])
            if e1 < s1: e1 += 1440
            if e2 < s2: e2 += 1440
            # normalize
            if s2 < s1 - 720: s2 += 1440; e2 += 1440
            if s1 < s2 - 720: s1 += 1440; e1 += 1440
            return not (e1 <= s2 + 5 or e2 <= s1 + 5)
        except Exception:
            return False

    changed = True
    max_iter = 20
    while changed and max_iter > 0:
        changed = False
        max_iter -= 1

        # Find missing ראש צוות slots
        missing_tl = [t for t in assignments if "❌" in str(t.get("עובד","")) and t.get("תפקיד בסיס") == "ראש צוות"]
        if not missing_tl:
            break

        for missing in missing_tl:
            # Find TL assigned as דייל on overlapping flights
            tl_as_agent = [
                t for t in assignments
                if t.get("תפקיד בסיס") == "דייל"
                and "❌" not in str(t.get("עובד",""))
                and tasks_overlap(t, missing)
            ]
            # Filter: worker must be qualified as ראש צוות
            promoted = None
            promoted_task = None
            for t in tl_as_agent:
                worker_name = t["עובד"]
                emp_row = employees_df[employees_df["שם"] == worker_name]
                if emp_row.empty:
                    continue
                if str(emp_row.iloc[0].get("ראש צוות","")).strip() == "כן":
                    promoted = worker_name
                    promoted_task = t
                    break

            if not promoted:
                continue

            # Find a replacement דייל for the vacated agent slot
            used_names = set(t["עובד"] for t in assignments if "❌" not in str(t.get("עובד","")))
            used_names.discard(promoted)

            agent_start = to_datetime_time(promoted_task["התחלה"])
            agent_end   = to_datetime_time(promoted_task["סיום"])

            agent_candidates = employees_df[
                (employees_df["דייל"].astype(str).str.strip() == "כן") &
                (~employees_df["שם"].isin(used_names))
            ].copy()
            agent_candidates = sort_candidates(agent_candidates, assignments, "דייל", agent_start, agent_end)

            replacement = None
            for _, emp in agent_candidates.iterrows():
                name = emp["שם"]
                if (
                    is_within_shift(emp, agent_start, agent_end)
                    and is_available(assignments, name, agent_start, agent_end, emp)
                    and has_room_for_break(assignments, emp, name, agent_start, agent_end)
                ):
                    replacement = name
                    break

            # Perform the swap regardless (even without replacement — TL gap is worse)
            # Move TL to missing ראש צוות slot
            missing["עובד"] = promoted
            # Update promoted_task with replacement or mark as missing
            promoted_task["עובד"] = replacement if replacement else f"❌ חסר דייל"
            changed = True
            break  # restart loop after each change

    return pd.DataFrame(assignments)



def next_task_text_for_employee(timed_df, current_idx, emp, employees_df):
    return continuation_text_for_employee(timed_df, current_idx, emp, employees_df)


def employee_shift_text(employees_df, emp_name):
    """
    Displays the exact shift from the daily employee roster.
    No automatic labels like יום/אפטר/לילה, because real shifts change every day.
    Examples:
    02:00-09:30
    02:00-11:00
    14:00-01:30
    """
    emp = employees_df[employees_df["שם"] == emp_name]
    if emp.empty:
        return ""

    s = clean_text(emp.iloc[0].get("תחילת משמרת", ""))
    e = clean_text(emp.iloc[0].get("סוף משמרת", ""))

    if s and e:
        return f"{s}-{e}"

    return ""

def build_next_task_labels(result_df, employees_df):
    """
    What the board shows per worker:
    - Current color = current role only.
    - Shift method and hours are always displayed at the end.
    - Break/refresher is displayed whenever the worker's shift requires it.
    - 'עזרה' appears only if there is a very large gap after the required break.
    """
    df = result_df.copy()

    if df.empty:
        df["טקסט עובד"] = []
        df["תפקיד נוכחי"] = []
        df["המשך אזורי"] = []
        return df

    df["טקסט עובד"] = df["עובד"].astype(str)
    df["תפקיד נוכחי"] = df["תפקיד"].apply(normalize_role_label)
    df["המשך אזורי"] = ""

    timed_df = df[df["התחלה"].astype(str).str.strip() != ""].copy()
    timed_df["_start_dt"] = pd.to_datetime(timed_df["התחלה"], format="%H:%M", errors="coerce")

    # break tracking per employee:
    # "break_state": None | "break_given" | "refresh_given"
    # "break_time": minutes when break was given
    # "refresh_time": minutes when refresh was given
    break_state = {}   # emp -> {"stage": 0/1/2, "last_m": int}
    # stage 0 = no break yet
    # stage 1 = break given, waiting for refresh (only for הפסקה ורענון)
    # stage 2 = all done
    MIN_BETWEEN_BREAKS = 4 * 60  # 4 hours

    for idx, row in timed_df.sort_values("_start_dt").iterrows():
        emp = str(row["עובד"]).strip()

        if "❌" in emp:
            df.loc[idx, "טקסט עובד"] = emp
            df.loc[idx, "המשך אזורי"] = ""
            continue

        emp_match = employees_df[employees_df["שם"] == emp]

        if emp_match.empty:
            next_text = next_task_plain_text(timed_df, idx, emp) or "חזרה"
            df.loc[idx, "טקסט עובד"] = f"{emp} - {next_text}"
            df.loc[idx, "המשך אזורי"] = next_text
            continue

        emp_row = emp_match.iloc[0]
        shift_text = employee_shift_text(employees_df, emp)
        shift_suffix = f" | {shift_text}" if shift_text else ""
        shift_type = classify_shift(emp_row)

        next_plain = next_task_plain_text(timed_df, idx, emp)
        task_end_dt   = to_datetime_time(row["סיום"])
        task_start_dt = to_datetime_time(row["התחלה"])
        task_end_m    = task_end_dt.hour * 60 + task_end_dt.minute
        gap_to_next   = gap_minutes_to_next(timed_df, idx, emp)
        break_label   = break_label_for_employee(emp_row)  # "רענון" / "הפסקה" / "הפסקה ורענון" / ""
        base_role = normalize_role_label(str(row.get("תפקיד בסיס", "")))
        is_agent  = base_role in {"דיילת", "דייל", "שומר TSA"}

        state = break_state.get(emp, {"stage": 0, "last_m": -9999})
        stage   = state["stage"]
        last_m  = state["last_m"]

        # Normalize for overnight
        te = task_end_m
        if last_m > 0 and te < last_m:
            te += 1440
        time_since_last = (te - last_m) if last_m != -9999 else 9999

        is_last_task = (next_plain == "")

        # Determine what break action to take now
        action = None  # None | "break" | "refresh" | "break_and_refresh"

        # For shifts > 9h: don't give break before 4h from shift start
        def enough_time_from_shift_start():
            ss = clean_text(emp_row.get("תחילת משמרת", ""))
            if not is_time_text(ss):
                return True
            s = time_to_minutes(ss)
            te = task_end_m
            if te < s: te += 1440
            return (te - s) >= MIN_BETWEEN_BREAKS

        long_shift = shift_length(emp_row) > 9 * 60
        can_break_now = (not long_shift) or enough_time_from_shift_start()

        if break_label == "הפסקה ורענון":
            if stage == 0 and can_break_now:
                action = "break"
            elif stage == 1 and time_since_last >= MIN_BETWEEN_BREAKS:
                action = "refresh"
        elif break_label in ("הפסקה", "רענון"):
            if stage == 0 and can_break_now:
                action = break_label

        # Night shift override — always give break after first flight (if can)
        if shift_type == "night" and stage == 0 and break_label and can_break_now:
            action = "break" if "הפסקה" in break_label else "רענון"

        # Agent with long gap
        if action is None and is_agent and gap_to_next is not None and gap_to_next >= 30:
            if stage == 0 and break_label and can_break_now:
                action = "break" if "הפסקה" in break_label else "רענון"

        # Build next_text
        def do_action(act, continuation):
            nonlocal stage
            label = "הפסקה" if act == "break" else "רענון" if act == "refresh" else act
            if act in ("break", "הפסקה"):
                break_state[emp] = {"stage": 1 if break_label == "הפסקה ורענון" else 2, "last_m": task_end_m}
            elif act in ("refresh", "רענון"):
                break_state[emp] = {"stage": 2, "last_m": task_end_m}
            return f"{label} ו{continuation}" if continuation else label

        return_text = return_text_by_shift(emp_row, task_end_dt)

        # After last flight — can also give refresh before returning
        if is_last_task:
            # If still owe a refresh (stage 1 + enough time) — give it now
            if break_label == "הפסקה ורענון" and stage == 1 and time_since_last >= MIN_BETWEEN_BREAKS:
                action = "refresh"
            continuation = return_text
        else:
            continuation = next_plain

        if action:
            next_text = do_action(action, continuation)
        else:
            next_text = continuation if continuation else return_text

        # Early morning break deadline annotation
        task_start_m   = task_start_dt.hour * 60 + task_start_dt.minute
        break_deadline = break_deadline_before_flight(emp_row, task_start_m)
        deadline_suffix = (
            f" [הפסקה עד {break_deadline}]"
            if break_deadline and stage == 0
            else ""
        )

        df.loc[idx, "טקסט עובד"] = f"{emp} - {next_text}{shift_suffix}{deadline_suffix}"
        df.loc[idx, "המשך אזורי"] = next_text

    return df

def build_counter_continuity_rows(result_labeled, employees_df):
    rows = []

    if result_labeled.empty:
        return pd.DataFrame(columns=["עובד", "משמרת", "טיסות", "טיסות משובצות", "תפקידים", "הערה"])

    for _, emp in employees_df.iterrows():
        name = emp["שם"]
        shift = employee_shift_text(employees_df, name)

        emp_tasks = result_labeled[
            (result_labeled["עובד"].astype(str) == name) &
            (result_labeled["התחלה"].astype(str).str.strip() != "")
        ].copy()

        if emp_tasks.empty:
            rows.append({
                "עובד": name,
                "משמרת": shift,
                "טיסות": 0,
                "טיסות משובצות": "",
                "תפקידים": "",
                "הערה": "לא שובץ לטיסות. נשאר בדלפקים או לפי הנחיית אחמ״ש.",
            })
            continue

        rows.append({
            "עובד": name,
            "משמרת": shift,
            "טיסות": len(emp_tasks),
            "טיסות משובצות": " | ".join(emp_tasks["טיסה"].astype(str).tolist()),
            "תפקידים": " | ".join(emp_tasks["תפקיד"].astype(str).tolist()),
            "הערה": "רצף טיסות" if len(emp_tasks) >= 2 else "טיסה בודדת ואז חזרה לדלפקים/סיום משמרת",
        })

    return pd.DataFrame(rows)


def build_workload(result_df, employees_df):
    rows = []

    if result_df.empty:
        return pd.DataFrame(columns=["עובד", "משימות", "דקות עבודה", "הפסקה נדרשת", "סה״כ כולל הפסקות"])

    timed = result_df[result_df["התחלה"].astype(str).str.strip() != ""].copy()

    real_workers = sorted([
        worker for worker in timed["עובד"].dropna().unique()
        if "❌" not in str(worker)
    ])

    for emp in real_workers:
        tasks = timed[timed["עובד"] == emp]
        total = 0

        for _, task in tasks.iterrows():
            total += minutes_between(to_datetime_time(task["התחלה"]), to_datetime_time(task["סיום"]))

        emp_row = employees_df[employees_df["שם"] == emp]
        break_min = required_break(emp_row.iloc[0]) if not emp_row.empty else 0

        rows.append({
            "עובד": emp,
            "משימות": len(tasks),
            "דקות עבודה": total,
            "הפסקה נדרשת": break_min,
            "סה״כ כולל הפסקות": total + break_min,
        })

    return pd.DataFrame(rows)


def build_output_table(flights_df, result_labeled, employees_df):
    rows = []
    flights_df = flights_df.copy()
    flights_df["_flight_key"] = flights_df["טיסה"].apply(flight_key)
    flights_df = flights_df.drop_duplicates(subset=["_flight_key"], keep="first").drop(columns=["_flight_key"])

    for _, flight in flights_df.iterrows():
        fnum = str(flight["טיסה"]).strip()
        dep = clean_text(flight.get("המראה", ""))
        boarding = clean_text(flight.get("בורדינג", ""))
        aircraft = clean_text(flight.get("סוג מטוס", ""))
        reg = clean_text(flight.get("רישוי", ""))
        reqs = requirements_text(flight)

        tasks = result_labeled[result_labeled["טיסה"].astype(str).str.strip() == fnum]

        management_lines = []
        agents_lines = []
        management_roles = []
        agent_roles = []

        for _, task in tasks.iterrows():
            role = str(task["תפקיד"])
            base_role = normalize_role_label(role)
            worker = str(task.get("עובד", ""))
            text_value = str(task["טקסט עובד"])

            # Gender-aware role label
            display_role = gender_role_label(role, employees_df, worker)

            # Add role in parentheses right after the worker name
            if "❌" not in worker and worker and " - " in text_value:
                name_part, rest = text_value.split(" - ", 1)
                text_value = f"{name_part} ({display_role}) - {rest}"
            elif "❌" not in worker and worker:
                text_value = f"{worker} ({display_role})"

            # Add exact shift hours at the end of every real worker line.
            shift = employee_shift_text(employees_df, worker)
            if shift and "❌" not in worker and f"({shift})" not in text_value:
                text_value = f"{text_value} ({shift})"

            item = {"text": text_value, "role": base_role}

            if "ראש צוות" in role or "טרייני" in role or "מתאם" in role or "מפקח" in role:
                management_lines.append(item)
                if base_role not in management_roles:
                    management_roles.append(base_role)
            elif "דייל" in role or "שומר" in role or "בדיקת טרייני" in role:
                agents_lines.append(item)
                if base_role not in agent_roles:
                    agent_roles.append(base_role)

        rows.append({
            "מספר טיסה": fnum,
            "יעד": clean_text(flight["יעד"]),
            "זמנים": f"{dep} ({boarding})" if boarding else dep,
            "מטוס/רישוי": f"{aircraft}\n{reg}".strip(),
            "תפקידים דרושים": " | ".join(reqs),
            "כותרת ניהול": " / ".join(management_roles) if management_roles else "ניהול",
            "כותרת דיילים": " / ".join(agent_roles) if agent_roles else "דיילים",
            # Agents on left (c1), management on right (c2)
            "דיילים / שומר TSA": "\n".join([f"{x['role']}||{x['text']}" for x in agents_lines]),
            "ראש צוות / מתאם תורים / מפקח TSA": "\n".join([f"{x['role']}||{x['text']}" for x in management_lines]),
        })

    return pd.DataFrame(rows)


# =========================
# AVAILABLE IN HALL
# =========================

def build_available_in_hall(schedule_df, employees_df, flights_df):
    """
    Returns employees who:
    1. Are assigned to at least one flight (in departure hall)
    2. Have a meaningful gap (≥ 20 min) between tasks OR after last task within shift
    3. MUST have shift hours — without them we can't know if the gap is real
    """
    timed = schedule_df[
        (schedule_df["התחלה"].astype(str).str.strip() != "") &
        (~schedule_df["עובד"].astype(str).str.contains("❌", na=False))
    ].copy()

    if timed.empty:
        return pd.DataFrame(columns=["עובד", "תפקיד עיקרי", "משמרת", "פנוי מ", "פנוי עד", "פנות (דק׳)", "משימה הבאה", "הערה"])

    timed["_start_dt"] = pd.to_datetime(timed["התחלה"], format="%H:%M", errors="coerce")
    timed["_end_dt"]   = pd.to_datetime(timed["סיום"],   format="%H:%M", errors="coerce")

    hall_workers = timed["עובד"].unique()
    rows = []

    for emp_name in hall_workers:
        emp_tasks = timed[timed["עובד"] == emp_name].sort_values("_start_dt")
        emp_row_df = employees_df[employees_df["שם"] == emp_name]
        emp_row = emp_row_df.iloc[0] if not emp_row_df.empty else None

        shift_start_str = clean_text(emp_row.get("תחילת משמרת", "")) if emp_row is not None else ""
        shift_end_str   = clean_text(emp_row.get("סוף משמרת",   "")) if emp_row is not None else ""

        # Skip employees without shift hours — gaps would be meaningless
        if not is_time_text(shift_start_str) or not is_time_text(shift_end_str):
            continue

        shift_text = f"{shift_start_str}-{shift_end_str}"
        main_role = emp_tasks["תפקיד בסיס"].mode().iloc[0] if not emp_tasks.empty else ""

        # Parse shift boundaries (handle overnight)
        try:
            shift_start_dt = pd.to_datetime(shift_start_str, format="%H:%M")
            shift_end_dt   = pd.to_datetime(shift_end_str,   format="%H:%M")
            if shift_end_dt <= shift_start_dt:
                shift_end_dt += pd.Timedelta(hours=24)
        except Exception:
            continue

        task_list = emp_tasks.reset_index(drop=True)
        gaps = []

        # Gaps between consecutive tasks
        for i in range(len(task_list) - 1):
            end_i      = task_list.loc[i,   "_end_dt"]
            start_next = task_list.loc[i+1, "_start_dt"]

            # Handle overnight tasks
            if start_next < end_i:
                start_next += pd.Timedelta(hours=24)

            gap_min = int((start_next - end_i).total_seconds() / 60)

            if gap_min < 20 or gap_min > 300:  # ignore tiny or absurd gaps
                continue

            next_task_text = f"{task_list.loc[i+1, 'טיסה']} — {normalize_role_label(task_list.loc[i+1, 'תפקיד'])}"
            gaps.append({
                "from": end_i.strftime("%H:%M"),
                "to":   start_next.strftime("%H:%M"),
                "gap":  gap_min,
                "next": next_task_text,
                "note": "פנוי בין טיסות",
            })

        # Gap after last task until shift end
        if not task_list.empty:
            last_end = task_list.iloc[-1]["_end_dt"]
            # Adjust for overnight
            le = last_end
            if le < shift_start_dt:
                le += pd.Timedelta(hours=24)
            se = shift_end_dt
            if se < le:
                se += pd.Timedelta(hours=24)

            remaining = int((se - le).total_seconds() / 60)
            if 30 <= remaining <= 300:  # only sensible durations
                gaps.append({
                    "from": last_end.strftime("%H:%M"),
                    "to":   shift_end_str,
                    "gap":  remaining,
                    "next": "סיום משמרת",
                    "note": "פנוי לאחר סיום טיסות",
                })

        for gap in gaps:
            rows.append({
                "עובד":         emp_name,
                "תפקיד עיקרי": normalize_role_label(main_role),
                "משמרת":        shift_text,
                "פנוי מ":       gap["from"],
                "פנוי עד":      gap["to"],
                "פנות (דק׳)":  gap["gap"],
                "משימה הבאה":   gap["next"],
                "הערה":         gap["note"],
            })

    if not rows:
        return pd.DataFrame(columns=["עובד", "תפקיד עיקרי", "משמרת", "פנוי מ", "פנוי עד", "פנות (דק׳)", "משימה הבאה", "הערה"])

    return pd.DataFrame(rows).sort_values(["פנוי מ", "עובד"]).reset_index(drop=True)


def build_unassigned_agents(schedule_df, employees_df, shift_map):
    """
    Returns agents who appear in the shift map (working today) but were NOT assigned
    to any flight. Grouped by shift type.
    """
    # Workers assigned to at least one flight
    assigned_workers = set(
        schedule_df[~schedule_df["עובד"].astype(str).str.contains("❌", na=False)]["עובד"].tolist()
    )

    rows = []
    for _, emp in employees_df.iterrows():
        name = clean_text(emp.get("שם", ""))
        if not name:
            continue

        # Must be working today (has shift hours)
        shift_start = clean_text(emp.get("תחילת משמרת", ""))
        shift_end   = clean_text(emp.get("סוף משמרת", ""))
        if not is_time_text(shift_start) or not is_time_text(shift_end):
            continue

        # Must not be assigned to any flight
        if name in assigned_workers:
            continue

        # Must be a qualified agent (דייל column)
        is_agent = str(emp.get("דייל", "")).strip() == "כן"
        is_tl    = str(emp.get("ראש צוות", "")).strip() == "כן"
        if not is_agent and not is_tl:
            continue

        role = "ראש צוות" if is_tl else "דייל"
        rows.append({
            "שם":           name,
            "תפקיד":        role,
            "משמרת":        f"{shift_start}-{shift_end}",
            "תחילת משמרת": shift_start,
            "סוף משמרת":   shift_end,
        })

    if not rows:
        return pd.DataFrame(columns=["שם", "תפקיד", "משמרת", "תחילת משמרת", "סוף משמרת"])

    df = pd.DataFrame(rows)
    df = df.sort_values(["תחילת משמרת", "שם"]).reset_index(drop=True)
    return df




def get_qualified_candidates_for_swap(schedule_df, employees_df, flight_num, role_base, task_idx):
    """
    Return employees who:
    1. Are certified for role_base
    2. Are within shift for the task's time window
    3. Are not already assigned to an overlapping task on a different flight
       (being on the same flight is OK – we're replacing)
    The current assignee is excluded (they are the one being swapped out).
    """
    task_row = schedule_df.loc[task_idx]
    start_str = str(task_row.get("התחלה", ""))
    end_str   = str(task_row.get("סיום",   ""))
    current_worker = str(task_row.get("עובד", ""))

    # Map role_base → employee column name
    role_col_map = {
        "ראש צוות":    "ראש צוות",
        "דייל":        "דייל",
        "מתאם תורים":  "מתאם תורים",
        "מפקח TSA":    "מפקח TSA",
        "שומר TSA":    "שומר TSA",
        "טרייני רצ":   "טרייני רצ",
        "טרייני ר״צ":  "טרייני רצ",
    }
    col = role_col_map.get(normalize_role_label(role_base), role_base)

    if col not in employees_df.columns:
        return []

    certified = employees_df[employees_df[col].astype(str).str.strip() == "כן"].copy()

    if not is_time_text(start_str) or not is_time_text(end_str):
        # No time info – return all certified except current
        return [n for n in certified["שם"].tolist() if n != current_worker]

    try:
        task_start = to_datetime_time(start_str)
        task_end   = to_datetime_time(end_str)
    except Exception:
        return []

    # Build a quick assignment lookup excluding this task itself
    other_tasks = schedule_df[schedule_df.index != task_idx].copy()
    other_tasks = other_tasks[other_tasks["התחלה"].astype(str).str.strip() != ""]

    results = []
    for _, emp_row in certified.iterrows():
        name = emp_row["שם"]
        if name == current_worker:
            continue

        # Shift check
        if not is_within_shift(emp_row, task_start, task_end):
            continue

        # Availability check (no overlap with other tasks this person already has)
        person_tasks = other_tasks[other_tasks["עובד"].astype(str) == name]
        conflict = False
        buffer = __import__("datetime").timedelta(minutes=5)
        for _, pt in person_tasks.iterrows():
            try:
                ps = to_datetime_time(str(pt["התחלה"]))
                pe = to_datetime_time(str(pt["סיום"]))
                if not (task_start >= pe + buffer or task_end <= ps - buffer):
                    conflict = True
                    break
            except Exception:
                pass
        if not conflict:
            results.append(name)

    return results


def do_swap(schedule_df, task_idx, new_worker, displaced_action, displaced_target_flight=None):
    """
    Perform the swap on schedule_df (in place on a copy).
    displaced_action: "unassign" | "move"
    displaced_target_flight: flight number string if action == "move"
    Returns the updated schedule_df.
    """
    df = schedule_df.copy()
    old_worker = str(df.at[task_idx, "עובד"])

    # Set new worker
    df.at[task_idx, "עובד"] = new_worker

    if displaced_action == "unassign":
        # Mark the old worker as missing in their original slot (already replaced above)
        pass  # nothing more needed; old slot now has new_worker

    elif displaced_action == "move" and displaced_target_flight:
        # Find an open (❌) slot on the target flight with the same base role
        role_base = str(df.at[task_idx, "תפקיד בסיס"])
        target_mask = (
            (df["טיסה"].astype(str).str.strip() == displaced_target_flight.strip()) &
            (df["תפקיד בסיס"].astype(str) == role_base) &
            (df["עובד"].astype(str).str.contains("❌"))
        )
        target_slots = df[target_mask]
        if not target_slots.empty:
            first_slot = target_slots.index[0]
            df.at[first_slot, "עובד"] = old_worker

    return df


# =========================
# DISPLAY
# =========================

def line_style_by_role(current_role, line):
    if "❌" in str(line):
        return "role-missing"

    role = normalize_role_label(current_role)

    if role == "ראש צוות":
        return "role-teamlead"
    if role == "מפקח TSA":
        return "role-inspector"
    if role == "שומר TSA":
        return "role-guard"
    if role == "טרייני ר״צ":
        return "role-trainee"
    if role == "מתאם תורים":
        return "role-queue"
    if role == "דיילת":
        return "role-agent"

    return "role-agent"


def render_line(line, current_role=""):
    line_str = str(line)
    style_cls = line_style_by_role(current_role, line_str)

    # Extract shift hours badge — pattern: (HH:MM-HH:MM) at end of line
    shift_badge = ""
    shift_match = re.search(r"\((\d{2}:\d{2}-\d{2}:\d{2})\)\s*$", line_str)
    if shift_match:
        shift_badge = shift_match.group(1)
        line_str = line_str[:shift_match.start()].rstrip()

    badge_html = (
        f'<span style="float:left;background:#e8f0fe;color:#1a3d7a;'
        f'font-size:11px;font-weight:900;border-radius:6px;'
        f'padding:2px 7px;margin-right:6px;white-space:nowrap;">🕐 {safe_html(shift_badge)}</span>'
        if shift_badge else ""
    )

    st.markdown(
        f'<div class="assignment-line {style_cls}">'
        f'{badge_html}'
        f'{safe_html(line_str)}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_flight_card(row):
    aircraft = str(row["מטוס/רישוי"]).replace("\n", " / ")
    reqs = str(row["תפקידים דרושים"])
    left_text = str(row["ראש צוות / מתאם תורים / מפקח TSA"])
    right_text = str(row["דיילים / שומר TSA"])

    required_line = " | ".join([part.strip() for part in reqs.split("|") if part.strip()]) or "לא הוגדרו תפקידים"

    st.markdown(
        f"""
        <div class="flight-card">
          <div class="flight-head">
            <div class="flight-row">
              <div class="flight-name">✈️ {safe_html(row['מספר טיסה'])} ← {safe_html(row['יעד'])}</div>
              <div class="flight-meta">🕒 {safe_html(row['זמנים'])} | 🛩️ {safe_html(aircraft)}</div>
            </div>
            <div class="req-line">תפקידים דרושים: {safe_html(required_line)}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── ניהול מעל ──
    management_title = str(row.get("כותרת ניהול", "ניהול"))
    st.markdown(f'<div class="panel-title">👔 {safe_html(management_title)}</div>', unsafe_allow_html=True)
    if left_text and left_text != "nan":
        for line in left_text.split("\n"):
            if "||" in line:
                role_part, text_part = line.split("||", 1)
                render_line(text_part, role_part)
            else:
                render_line(line)
    else:
        render_line("אין שיבוץ")

    st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

    # ── דיילים מתחת ──
    agents_title = str(row.get("כותרת דיילים", "דיילים"))
    st.markdown(f'<div class="panel-title">🧍 {safe_html(agents_title)}</div>', unsafe_allow_html=True)
    if right_text and right_text != "nan":
        for line in right_text.split("\n"):
            if "||" in line:
                role_part, text_part = line.split("||", 1)
                render_line(text_part, role_part)
            else:
                render_line(line)
    else:
        render_line("אין שיבוץ")


def render_flight_card_with_swap(row, schedule_df, employees_df):
    aircraft = str(row["מטוס/רישוי"]).replace("\n", " / ")
    reqs     = str(row["תפקידים דרושים"])
    left_text  = str(row["ראש צוות / מתאם תורים / מפקח TSA"])
    right_text = str(row["דיילים / שומר TSA"])
    fnum = str(row["מספר טיסה"]).strip()

    required_line = " | ".join([part.strip() for part in reqs.split("|") if part.strip()]) or "לא הוגדרו תפקידים"
    aircraft_short = str(row["מטוס/רישוי"]).split("\n")[0].strip()

    has_missing = "❌" in left_text or "❌" in right_text
    missing_icon = " ⚠️" if has_missing else ""

    expander_label = (
        f"✈️ {fnum} ← {row['יעד']}{missing_icon}"
        f"   |   🕒 {row['זמנים']}"
        f"   |   🛩️ {aircraft_short}"
        f"   |   {required_line}"
    )

    with st.expander(expander_label, expanded=False):

        c1, c2 = st.columns(2) if False else (None, None)  # unused — kept for compat

        def render_lines_with_swap(panel_lines):
            for line_i, line in enumerate(panel_lines):
                role_part, text_part = (line.split("||", 1) if "||" in line else ("", line))

                worker_raw = text_part.split(" - ")[0].strip() if " - " in text_part else text_part.split(" (")[0].strip()
                role_base  = normalize_role_label(role_part) if role_part else ""

                # Find matching task index
                flight_tasks = schedule_df[schedule_df["טיסה"].astype(str).str.strip() == fnum]
                match = flight_tasks[
                    (flight_tasks["עובד"].astype(str).str.contains(re.escape(worker_raw), na=False)) &
                    (flight_tasks["תפקיד בסיס"].astype(str).apply(normalize_role_label) == role_base)
                ]
                if match.empty:
                    match = flight_tasks[
                        flight_tasks["תפקיד בסיס"].astype(str).apply(normalize_role_label) == role_base
                    ]

                if match.empty:
                    render_line(text_part, role_part)
                    continue

                task_idx = match.index[0]
                # Unique key includes flight + task index + line position to avoid duplicates
                uid = f"{fnum}_{task_idx}_{line_i}"
                popup_key = f"popup_open_{uid}"
                if popup_key not in st.session_state:
                    st.session_state[popup_key] = False

                # ── Assignment line row with arrow ──
                style_cls = line_style_by_role(role_part, text_part)

                # Extract shift badge
                shift_badge = ""
                shift_match = re.search(r"\((\d{2}:\d{2}-\d{2}:\d{2})\)\s*$", text_part)
                if shift_match:
                    shift_badge = shift_match.group(1)
                    display_text = text_part[:shift_match.start()].rstrip()
                else:
                    display_text = text_part

                badge_html = (
                    f'<span style="float:left;background:#e8f0fe;color:#1a3d7a;'
                    f'font-size:11px;font-weight:900;border-radius:6px;'
                    f'padding:2px 7px;margin-right:6px;white-space:nowrap;">🕐 {safe_html(shift_badge)}</span>'
                    if shift_badge else ""
                )

                col_line, col_arrow = st.columns([11, 1])
                with col_line:
                    st.markdown(
                        f'<div class="assignment-line {style_cls}" style="margin-bottom:0">'
                        f'{badge_html}{safe_html(display_text)}</div>',
                        unsafe_allow_html=True,
                    )
                with col_arrow:
                    arrow = "▲" if st.session_state[popup_key] else "▼"
                    if st.button(arrow, key=f"arrow_{uid}", help="החלף עובד"):
                        st.session_state[popup_key] = not st.session_state[popup_key]
                        st.rerun()

                # ── Popup panel ──
                if st.session_state[popup_key]:
                    candidates = get_qualified_candidates_for_swap(
                        schedule_df, employees_df, fnum, role_base, task_idx
                    )

                    st.markdown(
                        f'<div class="swap-popup">'
                        f'<div class="swap-popup-title">🔄 החלפת עובד — {safe_html(worker_raw)} ({safe_html(role_base)})</div>',
                        unsafe_allow_html=True,
                    )

                    if not candidates:
                        st.warning("אין עובדים מוסמכים ופנויים להחלפה כרגע.")
                    else:
                        st.markdown('<div class="swap-popup-label">בחר עובד חלופי:</div>', unsafe_allow_html=True)
                        selected_new = st.selectbox(
                            "",
                            options=candidates,
                            key=f"swap_select_{uid}",
                            label_visibility="collapsed",
                        )

                        st.markdown(f'<div class="swap-popup-label">מה לעשות עם {safe_html(worker_raw)}?</div>', unsafe_allow_html=True)
                        action = st.radio(
                            "",
                            options=["השאר ללא שיבוץ", "העבר לחריץ פנוי בטיסה אחרת"],
                            key=f"swap_action_{uid}",
                            horizontal=True,
                            label_visibility="collapsed",
                        )

                        target_flight = None
                        if action == "העבר לחריץ פנוי בטיסה אחרת":
                            other_flights = sorted(
                                schedule_df[
                                    (schedule_df["טיסה"].astype(str).str.strip() != fnum) &
                                    (schedule_df["עובד"].astype(str).str.contains("❌")) &
                                    (schedule_df["תפקיד בסיס"].astype(str).apply(normalize_role_label) == role_base)
                                ]["טיסה"].astype(str).str.strip().unique().tolist()
                            )
                            if not other_flights:
                                st.info("אין חריצים פנויים מתאימים בטיסות אחרות.")
                            else:
                                st.markdown('<div class="swap-popup-label">בחר טיסה יעד:</div>', unsafe_allow_html=True)
                                target_flight = st.selectbox(
                                    "",
                                    options=other_flights,
                                    key=f"swap_target_{uid}",
                                    label_visibility="collapsed",
                                )

                        bc1, bc2 = st.columns(2)
                        with bc1:
                            if st.button("✅ אשר החלפה", key=f"swap_confirm_{uid}", use_container_width=True):
                                displaced_action = "move" if action == "העבר לחריץ פנוי בטיסה אחרת" else "unassign"
                                updated = do_swap(
                                    st.session_state["schedule_df"],
                                    task_idx,
                                    selected_new,
                                    displaced_action,
                                    target_flight,
                                )
                                st.session_state["schedule_df"] = updated
                                st.session_state[popup_key] = False
                                st.rerun()
                        with bc2:
                            if st.button("✖ ביטול", key=f"swap_cancel_{uid}", use_container_width=True):
                                st.session_state[popup_key] = False
                                st.rerun()

                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom:7px'></div>", unsafe_allow_html=True)

        management_title = str(row.get("כותרת ניהול", "ניהול"))
        agents_title     = str(row.get("כותרת דיילים", "דיילים"))

        # ── ניהול מעל ──
        st.markdown(f'<div class="panel-title">👔 {safe_html(management_title)}</div>', unsafe_allow_html=True)
        left_lines = [l for l in left_text.split("\n") if l.strip()] if left_text and left_text != "nan" else []
        if left_lines:
            render_lines_with_swap(left_lines)
        else:
            render_line("אין שיבוץ")

        st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

        # ── דיילים מתחת ──
        st.markdown(f'<div class="panel-title">🧍 {safe_html(agents_title)}</div>', unsafe_allow_html=True)
        right_lines = [l for l in right_text.split("\n") if l.strip()] if right_text and right_text != "nan" else []
        if right_lines:
            render_lines_with_swap(right_lines)
        else:
            render_line("אין שיבוץ")




def to_excel_bytes(output_df, workload_df, schedule_df, continuity_df=None):
    output = io.BytesIO()

    try:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            output_df.to_excel(writer, index=False, sheet_name="שיבוץ")
            workload_df.to_excel(writer, index=False, sheet_name="עומס")
            schedule_df.to_excel(writer, index=False, sheet_name="פירוט גולמי")
            if continuity_df is not None:
                continuity_df.to_excel(writer, index=False, sheet_name="רצף אזורי")
    except Exception:
        output = io.BytesIO()
        output_df.to_csv(output, index=False, encoding="utf-8-sig")

    output.seek(0)
    return output


# =========================
# UI
# =========================

with st.sidebar:
    st.header("📂 העלאת קבצים")
    daily_file = st.file_uploader("קובץ סידור יומי", type=["xlsx"])
    employees_file = st.file_uploader("קובץ עובדים / הסמכות", type=["xlsx"])

if not daily_file or not employees_file:
    st.info("העלי קובץ סידור יומי וקובץ עובדים כדי להתחיל.")
    st.stop()

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
    '<div class="small-note">השלימי כאן גייט, רישוי, נוסעים וסוג הכשרה. טרייני רצ נקבע מטבלת העובדים בלבד.</div></div>',
    unsafe_allow_html=True,
)

# עמודת טרייני רצ יורדת מטבלת הטיסות.
# טרייני רצ נקבע מטבלת העובדים בלבד.
flights_editor_df = flights_df.drop(columns=["טרייני רצ"], errors="ignore").copy()

# Merge saved edits (גייט, רישוי, נוסעים) from previous session
if "saved_flight_edits" in st.session_state:
    saved = st.session_state["saved_flight_edits"]
    for col in ["גייט", "רישוי", "נוסעים", "סוג הכשרה"]:
        if col in saved.columns and col in flights_editor_df.columns:
            # Merge by flight number
            merge = saved[["טיסה", col]].dropna(subset=[col])
            merge = merge[merge[col].astype(str).str.strip() != ""]
            for _, mrow in merge.iterrows():
                mask = flights_editor_df["טיסה"] == mrow["טיסה"]
                if mask.any():
                    flights_editor_df.loc[mask, col] = mrow[col]

edited_flights = st.data_editor(
    flights_editor_df,
    use_container_width=True,
    num_rows="dynamic",
    key="flights_editor",
)

# Auto-save edits to session_state on every rerun
st.session_state["saved_flight_edits"] = edited_flights.copy()

# Clear button
if st.button("🗑️ נקה נתונים שמורים", help="מחק גייט / רישוי / נוסעים שהוזנו ידנית"):
    st.session_state.pop("saved_flight_edits", None)
    st.rerun()

m1, m2, m3, m4 = st.columns(4)
m1.metric("טיסות", len(edited_flights))
m2.metric("עובדים", len(employees_df))
m3.metric("יעדי TSA", edited_flights["יעד"].isin(list(USA_TSA_DESTS)).sum())
m4.metric("עובדי טרייני רצ", (employees_df["טרייני רצ"].astype(str).str.strip() == "כן").sum() if "טרייני רצ" in employees_df.columns else 0)


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

# ── Display (runs every rerun as long as session_state has data) ───────────────
if "schedule_df" in st.session_state:
    try:
        live_schedule  = st.session_state["schedule_df"]
        live_flights   = st.session_state["flights_snap"]
        live_employees = st.session_state["employees_snap"]

        labeled_df, workload_df, continuity_df, output_df = recompute_from_schedule(
            live_schedule, live_flights, live_employees
        )
        missing = live_schedule[live_schedule["עובד"].astype(str).str.contains("❌", na=False)]

        tab_schedule, tab_gantt, tab_missing, tab_available, tab_unassigned, tab_breaks, tab_workload, tab_continuity, tab_raw = st.tabs(
            ["✈️ לוח מבצעים", "📅 גאנט", "❌ חוסרים", "🟡 פנויים באולם", "🏠 לא משובצים", "⏰ הפסקות חובה", "📊 עומס עובדים", "🧭 רצף אזורי", "🧾 פירוט גולמי"]
        )

        with tab_schedule:
            st.markdown('<div class="ops-rtl"><h3>✈️ Assignment Board</h3></div>', unsafe_allow_html=True)

            search = st.text_input("🔎 חיפוש לפי טיסה / יעד / עובד")
            only_missing = st.checkbox("הצג רק טיסות עם חוסר")

            display_df = output_df.copy()

            if only_missing:
                display_df = display_df[
                    display_df.astype(str).apply(lambda row: row.str.contains("❌", na=False).any(), axis=1)
                ]

            if search:
                mask = display_df.astype(str).apply(
                    lambda row: row.str.contains(search, case=False, na=False).any(),
                    axis=1,
                )
                display_df = display_df[mask]

            for _, row in display_df.iterrows():
                render_flight_card_with_swap(
                    row,
                    st.session_state["schedule_df"],
                    st.session_state["employees_snap"],
                )

        with tab_gantt:
            import json as _json
            import streamlit.components.v1 as _components

            timed_g = live_schedule[
                live_schedule["התחלה"].astype(str).str.strip() != ""
            ].copy()

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

                flights_g = safe_sort_by_time(live_flights, "המראה")["טיסה"].tolist()
                flights_data = []
                for fnum in flights_g:
                    dest_r = live_flights[live_flights["טיסה"] == fnum]
                    dest_v = dest_r.iloc[0]["יעד"] if not dest_r.empty else ""
                    ftasks = timed_g[timed_g["טיסה"].astype(str).str.strip() == fnum.strip()]
                    tlist = []
                    for idx, task in ftasks.iterrows():
                        role = normalize_role_label(str(task.get("תפקיד בסיס", "")))
                        tlist.append({
                            "idx":    int(idx),
                            "worker": str(task.get("עובד", "")),
                            "role":   role,
                            "start":  str(task.get("התחלה", "")),
                            "end":    str(task.get("סיום", "")),
                            "color":  ROLE_COLORS_G.get(role, "#9fb7d7"),
                            "missing": "❌" in str(task.get("עובד", "")),
                        })
                    flights_data.append({
                        "flight": fnum,
                        "short":  fnum.replace("LY", "").strip(),
                        "dest":   dest_v,
                        "tasks":  tlist,
                    })

                gdata   = _json.dumps(flights_data,  ensure_ascii=False)
                rcolors = _json.dumps(ROLE_COLORS_G, ensure_ascii=False)

                # Build the full standalone HTML page
                gantt_page = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>גאנט טיסות — סידורומט</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:Arial,sans-serif;background:#f4f7fb;padding:12px;
     -webkit-user-select:none;user-select:none;}}
h2{{direction:rtl;color:#071b3a;font-size:20px;margin-bottom:8px;}}
#legend{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;direction:rtl;}}
.li{{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:800;color:#071b3a;}}
.ld{{width:13px;height:13px;border-radius:3px;display:inline-block;}}
#gantt{{overflow-x:auto;-webkit-overflow-scrolling:touch;
        border:1px solid #d9e2ef;border-radius:14px;background:#fff;}}
#inner{{position:relative;}}
.hour-line{{position:absolute;top:0;bottom:0;border-left:1px solid #e8eef7;pointer-events:none;}}
.hour-label{{position:absolute;top:5px;font-size:11px;color:#8a9ab5;pointer-events:none;}}
.frow{{display:flex;align-items:stretch;border-bottom:1px solid #eef2f8;position:relative;min-height:48px;}}
.frow:nth-child(even){{background:#f8fbff;}}
.frow:nth-child(odd){{background:#fff;}}
.flabel{{width:96px;min-width:96px;display:flex;flex-direction:column;justify-content:center;
         align-items:flex-end;padding:4px 8px 4px 4px;border-right:2px solid #e0e8f4;
         z-index:2;background:inherit;position:sticky;left:0;}}
.flabel .fn{{font-size:13px;font-weight:900;color:#071b3a;}}
.flabel .fd{{font-size:10px;color:#8a9ab5;}}
.timeline{{position:relative;flex:1;}}
.task{{position:absolute;height:30px;border-radius:8px;display:flex;align-items:center;
       justify-content:center;font-size:10px;font-weight:800;color:white;
       white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 6px;
       cursor:grab;box-shadow:0 2px 6px rgba(0,0,0,0.15);touch-action:none;}}
.task.missing{{background:#ffcccc!important;color:#9b0000;cursor:default;}}
.task.dragging{{opacity:0.3;}}
.frow.drop-target .timeline{{background:rgba(99,179,237,0.12);outline:2px dashed #4299e1;border-radius:8px;}}
#ghost{{position:fixed;pointer-events:none;z-index:9999;border-radius:8px;
        display:none;align-items:center;justify-content:center;
        font-size:11px;font-weight:800;color:white;padding:0 10px;height:32px;
        box-shadow:0 6px 24px rgba(0,0,0,0.3);white-space:nowrap;opacity:0.92;}}
#toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
        padding:10px 22px;border-radius:22px;font-size:13px;font-weight:800;
        display:none;z-index:10000;direction:rtl;box-shadow:0 4px 20px rgba(0,0,0,0.2);}}
.tok{{background:#071b3a;color:white;}}
.terr{{background:#d32f2f;color:white;}}
</style></head><body>
<h2>📅 גאנט טיסות — סידורומט</h2>
<div id="legend"></div>
<div id="gantt"><div id="inner"></div></div>
<div id="ghost"></div>
<div id="toast"></div>
<script>
const FLIGHTS={gdata};
const DAY_MIN={g_min},DAY_MAX={g_max},HOURS=DAY_MAX-DAY_MIN;
const HPX=96,LW=96,HDR=26;

function h2px(s){{const[h,m]=(s||"0:0").split(":").map(Number);return(h+m/60-DAY_MIN)*HPX;}}
function h2f(s){{const[h,m]=(s||"0:0").split(":").map(Number);return h+m/60;}}
function lanes(tasks){{
  const L=[];
  return tasks.map(t=>{{
    let s=h2f(t.start),e=h2f(t.end);if(e<s)e+=24;
    let p=-1;
    for(let i=0;i<L.length;i++)if(L[i].every(([a,b])=>s>=b||e<=a)){{L[i].push([s,e]);p=i;break;}}
    if(p<0){{L.push([[s,e]]);p=L.length-1;}}
    return{{...t,lane:p,sh:s,eh:e}};
  }});
}}

const inner=document.getElementById("inner");
inner.style.cssText=`position:relative;width:${{LW+HOURS*HPX+16}}px;padding-top:${{HDR}}px;`;

for(let h=0;h<=HOURS;h++){{
  const x=LW+h*HPX;
  const ln=document.createElement("div");ln.className="hour-line";
  ln.style.cssText=`left:${{x}}px;`;inner.appendChild(ln);
  const lb=document.createElement("div");lb.className="hour-label";
  lb.style.cssText=`left:${{x+3}}px;`;
  lb.textContent=String(DAY_MIN+h).padStart(2,"0")+":00";
  inner.appendChild(lb);
}}

FLIGHTS.forEach((f,fi)=>{{
  const asgn=lanes(f.tasks);
  const nL=asgn.length?Math.max(...asgn.map(t=>t.lane))+1:1;
  const RH=nL*40+12;
  const row=document.createElement("div");
  row.className="frow";row.style.minHeight=RH+"px";row.dataset.fi=fi;
  const lbl=document.createElement("div");lbl.className="flabel";
  lbl.innerHTML=`<span class="fn">${{f.short}}</span><span class="fd">${{f.dest}}</span>`;
  row.appendChild(lbl);
  const tl=document.createElement("div");
  tl.className="timeline";tl.style.cssText=`position:relative;height:${{RH}}px;`;
  asgn.forEach(t=>{{
    const x1=h2px(t.start),x2=h2px(t.end),bw=Math.max(x2-x1,8);
    const top=6+t.lane*40;
    const d=document.createElement("div");d.className="task"+(t.missing?" missing":"");
    d.style.cssText=`left:${{x1.toFixed(1)}}px;width:${{bw.toFixed(1)}}px;top:${{top}}px;background:${{t.missing?"#ffcccc":t.color}};`;
    if(t.missing)d.style.color="#9b0000";
    d.textContent=t.worker;d.title=`${{t.worker}} | ${{t.role}} | ${{t.start}}–${{t.end}}`;
    d.dataset.fi=fi;d.dataset.idx=t.idx;
    if(!t.missing)addDrag(d,f,t,fi);
    tl.appendChild(d);
  }});
  row.appendChild(tl);inner.appendChild(row);
}});

const ghost=document.getElementById("ghost");
let drag=null;

function addDrag(el,flight,task,fi){{
  function start(e){{
    const s=e.touches?e.touches[0]:e;
    drag={{el,flight,task,fi}};
    el.classList.add("dragging");
    ghost.textContent=task.worker;ghost.style.background=task.color;
    ghost.style.display="flex";ghost.style.width=Math.max(el.offsetWidth,80)+"px";
    mv(s.clientX,s.clientY);
    e.stopPropagation();if(e.cancelable)e.preventDefault();
  }}
  el.addEventListener("mousedown",start);
  el.addEventListener("touchstart",start,{{passive:false}});
}}
function mv(cx,cy){{ghost.style.left=(cx-ghost.offsetWidth/2)+"px";ghost.style.top=(cy-16)+"px";}}
function rowAt(cx,cy){{
  for(const r of document.querySelectorAll(".frow")){{
    const b=r.getBoundingClientRect();
    if(cy>=b.top&&cy<=b.bottom&&cx>=b.left&&cx<=b.right)return+r.dataset.fi;
  }}return -1;
}}
document.addEventListener("mousemove",e=>{{if(!drag)return;mv(e.clientX,e.clientY);hl(rowAt(e.clientX,e.clientY));}});
document.addEventListener("touchmove",e=>{{if(!drag)return;const t=e.touches[0];mv(t.clientX,t.clientY);hl(rowAt(t.clientX,t.clientY));if(e.cancelable)e.preventDefault();}},{{passive:false}});
document.addEventListener("mouseup",e=>{{if(drag)finish(rowAt(e.clientX,e.clientY));}});
document.addEventListener("touchend",e=>{{if(drag){{const t=e.changedTouches[0];finish(rowAt(t.clientX,t.clientY));}}}});
function hl(fi){{document.querySelectorAll(".frow").forEach(r=>r.classList.remove("drop-target"));if(fi>=0&&fi!==drag?.fi)document.querySelector(`.frow[data-fi="${{fi}}"]`)?.classList.add("drop-target");}}
function toast(msg,ok){{const t=document.getElementById("toast");t.textContent=msg;t.className=ok?"tok":"terr";t.style.display="block";setTimeout(()=>t.style.display="none",3000);}}
function finish(tfi){{
  document.querySelectorAll(".frow").forEach(r=>r.classList.remove("drop-target"));
  ghost.style.display="none";
  if(!drag)return;
  const src=drag;drag=null;src.el.classList.remove("dragging");
  if(tfi<0||tfi===src.fi)return;
  const tF=FLIGHTS[tfi],role=src.task.role;
  const mis=tF.tasks.find(t=>t.missing&&t.role===role);
  if(!mis&&!tF.tasks.some(t=>t.role===role)){{toast("❌ אין תפקיד מתאים ("+role+") בטיסה "+tF.short,false);return;}}
  const wn=src.task.worker;
  src.el.textContent="❌ חסר "+role;src.el.style.background="#ffcccc";src.el.style.color="#9b0000";src.el.classList.add("missing");src.task.missing=true;src.task.worker="❌ חסר "+role;
  if(mis){{mis.worker=wn;mis.missing=false;const te=document.querySelector(`.task[data-idx="${{mis.idx}}"]`);if(te){{te.textContent=wn;te.style.background=mis.color||src.task.color;te.style.color="white";te.classList.remove("missing");addDrag(te,tF,mis,tfi);}}}}
  toast("✅ "+wn+" → "+tF.short+" ("+role+")",true);
}}
// legend
const lDiv=document.getElementById("legend");
[["ראש צוות","#8e24aa"],["דיילת","#5b9bd5"],["מתאם תורים","#f0a000"],["מפקח TSA","#d32f2f"],["שומר TSA","#2e7d32"],["טרייני ר״צ","#f9a825"]].forEach(([r,c])=>{{
  const d=document.createElement("div");d.className="li";
  d.innerHTML=`<span class="ld" style="background:${{c}}"></span><span>${{r}}</span>`;lDiv.appendChild(d);
}});
</script></body></html>"""

                # Option 1: Download as HTML file (opens correctly in any browser)
                import base64 as _b64
                encoded = _b64.b64encode(gantt_page.encode("utf-8")).decode()

                st.download_button(
                    label="⬇️ הורד גאנט כקובץ HTML (פתח בדפדפן)",
                    data=gantt_page.encode("utf-8"),
                    file_name="gantt.html",
                    mime="text/html",
                    use_container_width=True,
                )
                st.caption("לאחר ההורדה — פתח את הקובץ בדפדפן לתצוגה מלאה עם גרירה.")

                st.markdown("---")

                # Option 2: Show inline fullscreen
                st.markdown("**או צפה כאן:**")
                _components.html(
                    gantt_page,
                    height=max(600, len(flights_g) * 55 + 160),
                    scrolling=False,
                )

            st.subheader("❌ חוסרים")
            if missing.empty:
                st.success("אין חוסרים 🎉")
            else:
                st.warning(f"נמצאו {len(missing)} חוסרים")
                st.dataframe(missing, use_container_width=True)

        with tab_available:
            st.subheader("🟡 עובדים פנויים באולם היציאה")
            st.caption("עובדים שמשובצים לפחות לטיסה אחת — ולכן נמצאים באולם — אך יש להם פער של 20 דק׳ ומעלה בין משימות.")

            available_df = build_available_in_hall(live_schedule, live_employees, live_flights)

            if available_df.empty:
                st.success("אין עובדים פנויים כרגע באולם היציאה 🎉")
            else:
                # Summary cards
                total_free = available_df["עובד"].nunique()
                long_gaps  = available_df[available_df["פנות (דק׳)"] >= 60]["עובד"].nunique()
                sc1, sc2 = st.columns(2)
                sc1.metric("עובדים פנויים באולם", total_free)
                sc2.metric("מתוכם פנויים שעה+", long_gaps)

                st.markdown("---")

                # Role filter
                roles = ["הכל"] + sorted(available_df["תפקיד עיקרי"].dropna().unique().tolist())
                selected_role = st.selectbox("סנן לפי תפקיד:", roles, key="avail_role_filter")

                filtered = available_df if selected_role == "הכל" else available_df[available_df["תפקיד עיקרי"] == selected_role]

                # Display as styled cards
                for _, r in filtered.iterrows():
                    gap_color = "#fff3cd" if r["פנות (דק׳)"] < 60 else "#d4edda"
                    gap_border = "#ffc107" if r["פנות (דק׳)"] < 60 else "#28a745"
                    st.markdown(
                        f"""
                        <div style="direction:rtl;background:{gap_color};border-right:5px solid {gap_border};
                                    border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px;">
                            <strong>{safe_html(r['עובד'])}</strong>
                            &nbsp;·&nbsp; {safe_html(r['תפקיד עיקרי'])}
                            &nbsp;·&nbsp; משמרת: {safe_html(r['משמרת'])}
                            <br>
                            🕒 פנוי: <strong>{safe_html(r['פנוי מ'])} – {safe_html(r['פנוי עד'])}</strong>
                            &nbsp; ({r['פנות (דק׳)']} דק׳)
                            &nbsp;·&nbsp; הבא: {safe_html(r['משימה הבאה'])}
                            <br>
                            <span style="color:#555;font-size:12px">{safe_html(r['הערה'])}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with tab_unassigned:
            st.subheader("🏠 דיילים וראשי צוות שלא שובצו לטיסות היום")
            st.caption("עובדים שנמצאים במשמרת היום (יש להם שעות בסידור) אך לא שובצו לאף טיסה — ממוינים לפי סוג משמרת.")

            # Initialize break tracking in session_state
            if "break_log" not in st.session_state:
                st.session_state["break_log"] = {}  # name -> {"start": HH:MM, "end": HH:MM or None}

            shift_map_ref = build_shift_map_from_excel(daily_file) if "daily_file" in dir() else {}
            unassigned_df = build_unassigned_agents(live_schedule, live_employees, shift_map_ref)

            if unassigned_df.empty:
                st.success("כל העובדים שובצו לטיסות 🎉")
            else:
                st.metric("סה״כ לא משובצים", len(unassigned_df))
                st.markdown("---")

                from datetime import datetime as _dt

                shift_groups = unassigned_df.groupby("משמרת")
                for shift_label, group in shift_groups:
                    start_h = shift_label.split("-")[0] if "-" in shift_label else "00:00"
                    try:
                        sh = int(start_h.split(":")[0])
                        if 5 <= sh < 12:   emoji, label = "🌅", f"משמרת בוקר — {shift_label}"
                        elif 12 <= sh < 18: emoji, label = "☀️", f"משמרת צהריים — {shift_label}"
                        elif 18 <= sh < 22: emoji, label = "🌆", f"משמרת ערב — {shift_label}"
                        else:               emoji, label = "🌙", f"משמרת לילה — {shift_label}"
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
                        role_color = "#8e24aa" if role == "ראש צוות" else "#5b9bd5"
                        break_info = st.session_state["break_log"].get(name, {})
                        on_break   = bool(break_info.get("start")) and not break_info.get("end")
                        break_done = bool(break_info.get("start")) and bool(break_info.get("end"))

                        # Determine break duration based on shift length
                        emp_row_match = live_employees[live_employees["שם"] == name]
                        if not emp_row_match.empty:
                            bl = break_label_for_employee(emp_row_match.iloc[0])
                            if bl == "הפסקה ורענון":
                                break_duration = 65
                            elif bl == "הפסקה":
                                break_duration = 45
                            else:
                                break_duration = 20
                        else:
                            break_duration = 45

                        # Build status text
                        if on_break:
                            start_display = break_info.get("start", "")
                            start_ts_disp = break_info.get("ts", 0)
                            status = f'☕ בהפסקה מ-<strong><span id="start_time_{btn_key}">...</span></strong>'
                            status_color = "#92400e"
                            status_bg    = "#fef3c7"
                        elif break_done:
                            start_ts_d = break_info.get("ts", 0)
                            end_ts_d   = break_info.get("end_ts", 0)
                            status = (
                                f'✅ הפסקה: <span id="bstart_{btn_key}">...</span>'
                                f' – <span id="bend_{btn_key}">...</span>'
                            )
                            status_color = "#065f46"
                            status_bg    = "#d1fae5"
                        else:
                            status = ""
                            status_bg = "#fff"
                            status_color = "#333"

                        st.markdown(
                            f'<div style="direction:rtl;background:{status_bg};border:1px solid #e0e8f4;'
                            f'border-right:4px solid {role_color};border-radius:8px;'
                            f'padding:6px 12px;margin-bottom:4px;font-size:13px;color:{status_color};">'
                            f'<strong style="color:#071b3a;">{safe_html(name)}</strong>'
                            f'&nbsp;<span style="color:{role_color};font-weight:800;">({safe_html(role)})</span>'
                            + (f'&nbsp;&nbsp;{status}' if status else '') +
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        btn_key = name.replace(" ", "_")
                        col_start, col_end, col_reset = st.columns([2, 2, 1])

                        with col_start:
                            if not on_break and not break_done:
                                if st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}",
                                             use_container_width=True):
                                    import time as _time
                                    ts = int(_time.time())
                                    st.session_state["break_log"][name] = {
                                        "start": "",   # will be shown from JS
                                        "ts":    ts,
                                        "end":   None,
                                        "end_ts": None,
                                    }
                                    st.rerun()
                            elif on_break:
                                st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}",
                                          disabled=True, use_container_width=True)

                        with col_end:
                            if on_break:
                                if st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}",
                                             use_container_width=True):
                                    import time as _time_end
                                    st.session_state["break_log"][name]["end_ts"] = int(_time_end.time())
                                    st.session_state["break_log"][name]["end"] = "סיום"
                                    st.rerun()
                            else:
                                st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}",
                                          disabled=True, use_container_width=True)

                        with col_reset:
                            if break_info:
                                if st.button("↺", key=f"brk_reset_{btn_key}", help="אפס הפסקה"):
                                    st.session_state["break_log"].pop(name, None)
                                    st.rerun()

                        # Build status + timer as one self-contained HTML component
                        if on_break or break_done:
                            import streamlit.components.v1 as _comp_brk
                            s_ts = break_info.get("ts", 0)
                            e_ts = break_info.get("end_ts", 0) or 0
                            is_done_js = "true" if break_done else "false"
                            timer_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;font-family:Arial,sans-serif;direction:rtl;background:transparent;">
<div id="box" style="padding:7px 14px;border-radius:8px;font-size:13px;font-weight:800;border:1px solid #fbbf24;background:#fff8e1;color:#92400e;">
  <span id="msg">מחשב...</span>
</div>
<script>
(function(){{
  var sTs      = {s_ts};
  var eTs      = {e_ts};
  var dur      = {break_duration} * 60;
  var isDone   = {is_done_js};

  function fmt(ts){{
    var d=new Date(ts*1000);
    return String(d.getHours()).padStart(2,"0")+":"+String(d.getMinutes()).padStart(2,"0");
  }}

  var box = document.getElementById("box");
  var msg = document.getElementById("msg");

  if (isDone) {{
    box.style.background = "#d1fae5";
    box.style.borderColor = "#10b981";
    box.style.color = "#065f46";
    msg.textContent = "✅ הפסקה: " + fmt(sTs) + " – " + fmt(eTs);
    return;
  }}

  // Active break — countdown
  function update(){{
    var nowTs = Math.floor(Date.now()/1000);
    var remaining = dur - (nowTs - sTs);
    if (remaining <= 0){{
      box.style.background="#ffe4e4";
      box.style.borderColor="#ef4444";
      box.style.color="#991b1b";
      msg.textContent = "⚠️ זמן ההפסקה הסתיים — חזרה לעבודה!";
    }} else {{
      var m = Math.floor(remaining/60);
      var s = remaining%60;
      msg.textContent = "☕ בהפסקה מ-" + fmt(sTs) + " | נותרו " + m + ":" + String(s).padStart(2,"0") + " מתוך {break_duration} דק׳";
    }}
  }}
  update();
  setInterval(update, 1000);
}})();
</script>
</body></html>"""
                            _comp_brk.html(timer_html, height=44)

        with tab_breaks:
            st.subheader("⏰ עובדים שחייבים לצאת להפסקה עד שעה מסוימת")
            st.caption("עובדי משמרת בוקר מוקדמת (02:xx) שמשובצים לטיסות — חייבים לצאת להפסקה לפני הירידה לשערים.")

            timed_br = live_schedule[
                (live_schedule["התחלה"].astype(str).str.strip() != "") &
                (~live_schedule["עובד"].astype(str).str.contains("❌", na=False))
            ].copy()

            break_rows = []
            if not timed_br.empty:
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

                    first_task = emp_tasks.iloc[0]
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
                st.markdown("---")

                for _, r in break_df.iterrows():
                    st.markdown(
                        f'<div style="direction:rtl;background:#fff8e1;border-right:5px solid #f59e0b;'
                        f'border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px;'
                        f'color:#1a1a1a;">'
                        f'⏰ <strong style="color:#000000;">{safe_html(r["עובד"])}</strong>'
                        f'<span style="color:#333333;"> ({safe_html(r["תפקיד"])}) | משמרת: {safe_html(r["משמרת"])}</span>'
                        f'<br>'
                        f'<span style="color:#333333;">חייב/ת לצאת להפסקה עד: </span>'
                        f'<strong style="color:#b45309;font-size:16px;">{safe_html(r["הפסקה עד"])}</strong>'
                        f'<span style="color:#333333;"> &nbsp;→&nbsp; טיסה {safe_html(r["טיסה ראשונה"])} | כניסה לשער: {safe_html(r["שעת כניסה לשער"])}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        with tab_workload:
            st.subheader("📊 עומס עובדים")
            st.dataframe(workload_df, use_container_width=True)

        with tab_continuity:
            st.subheader("🧭 רצף אזורי")
            st.caption("הטבלה הזו משקפת מי אמור להישאר בדלפקי צ׳ק אין, מי באולם היציאה, ומי קיבל טיסות בודדות בלבד.")
            st.dataframe(continuity_df, use_container_width=True)

        with tab_raw:
            st.subheader("🧾 פירוט גולמי")
            st.dataframe(labeled_df, use_container_width=True)

        excel_data = to_excel_bytes(output_df, workload_df, labeled_df, continuity_df)

        st.download_button(
            "⬇️ הורדת אקסל מלא",
            data=excel_data,
            file_name="SIDUROMAT_OPS_BOARD.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("הייתה שגיאה בהצגת השיבוץ.")
        st.exception(exc)
