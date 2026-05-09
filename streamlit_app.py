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

    BLOCKED_KEYWORDS = ["בידוק", "מתדרכ", "ועדת היגוי", "רענון tsa", "רענון", "77"]
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
            current_blocked_label = ""    # label text e.g. "פיקוח TSA 18:00-01:30"

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
                        current_blocked_label = cell_text  # store the label (e.g. "פיקוח TSA")
                        current_start = s
                        current_end   = e
                    else:
                        current_start = s
                        current_end   = e
                        current_blocked_range = None
                        current_blocked_label = ""
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
                    # Also store under yod-normalized key variants
                    shift_map[key] = {
                        "start":    current_start,
                        "end":      current_end,
                        "original": possible_name,
                        "blocked":       [],
                        "blocked_roles": [],
                        "sick":     False,
                        "shift_end_override":   None,
                        "shift_start_override": None,
                    }
                    # Also index by reversed name so lookup works both ways
                    key_rev = name_key(" ".join(reversed(possible_name.split())))
                    if key_rev not in shift_map:
                        shift_map[key_rev] = shift_map[key]

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
                        entry.setdefault("blocked_roles", []).append(current_blocked_label)
                for eb in extra_blocked:
                    if eb not in entry["blocked"]:
                        entry["blocked"].append(eb)
                        entry.setdefault("blocked_roles", []).append("")

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
        # Try exact key (with yod normalization)
        key = name_key(emp_name)
        if key in shift_map_with_names:
            return shift_map_with_names[key]
        # Try reversed word order
        key_rev = name_key_reversed(emp_name)
        if key_rev in shift_map_with_names:
            return shift_map_with_names[key_rev]
        # Fuzzy: 2+ shared words (normalize each word with name_key for yod matching)
        parts = {name_key(w) for w in emp_name.split() if len(w) > 1}
        best = None; best_score = 1
        for _, entry in shift_map_with_names.items():
            orig_parts = {name_key(w) for w in entry["original"].split() if len(w) > 1}
            shared = len(parts & orig_parts)
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
        blocked_roles = entry.get("blocked_roles", [])  # parallel list of role labels
        if blocked:
            df.at[idx, "חסימות"] = ",".join(f"{s}-{e}" for s, e in blocked)
            # Store role labels for each blocked window
            for i, (s, e) in enumerate(blocked):
                role_label = blocked_roles[i] if i < len(blocked_roles) else ""
                df.at[idx, f"_blocked_role_{s}-{e}"] = role_label

        # Store available windows (overrides shift for workers like נטע ונטוררו)
        avail = entry.get("available_windows", [])
        if avail and "זמינות" in df.columns or avail:
            if "זמינות" not in df.columns:
                df["זמינות"] = ""
            df.at[idx, "זמינות"] = ",".join(f"{s}-{e}" for s, e in avail)

    return df


def name_key(value) -> str:
    """Normalize name: no spaces, lowercase, double-yod = single-yod."""
    text = re.sub(r"\s+", "", clean_text(value)).lower()
    text = text.replace("יי", "י")   # שיילו = שילו
    return text


def name_key_reversed(value) -> str:
    """Return name_key of the reversed word order (בר שיילו → שיילובר)."""
    words = clean_text(value).split()
    return name_key(" ".join(reversed(words))) if len(words) >= 2 else name_key(value)


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

    # Normalize all column names to strip whitespace
    df.columns = df.columns.astype(str).str.strip()

    aliases = {
        "מפקח tsa":          "מפקח TSA",
        "מפקח Tsa":          "מפקח TSA",
        "פיקוח tsa":         "מפקח TSA",
        "פיקוח TSA":         "מפקח TSA",
        "פיקוח Tsa":         "מפקח TSA",
        "שומר tsa":          "שומר TSA",
        "שומר Tsa":          "שומר TSA",
        "טרייני ר״צ":        "טרייני רצ",
        'טרייני ר"צ':        "טרייני רצ",
        "ראש צוות חונך":     "חונך רצים",
        "ראש צוות מסמיך":    "מסמיך רצים",
        "ראש צוות מסמיך ":   "מסמיך רצים",
        "טרייני ר״צ ":       "טרייני רצ",
    }

    for old, new in aliases.items():
        if old in df.columns:
            if new not in df.columns:
                df[new] = df[old]
            else:
                # Merge: if new is empty/NaN, fill from old
                df[new] = df[new].apply(clean_text)
                df[old] = df[old].apply(clean_text)
                mask = df[new].str.strip().isin(["", "לא"]) & (df[old] != "")
                df.loc[mask, new] = df.loc[mask, old]

    df["שם"] = df["שם"].apply(clean_text)
    df = df[df["שם"] != ""].copy()
    df["_name_key"] = df["שם"].apply(name_key)

    for col in ROLE_COLUMNS:
        if col not in df.columns:
            df[col] = "לא"
        df[col] = df[col].apply(normalize_yes_no)

    for col in ["תחילת משמרת", "סוף משמרת", "חסימות", "זמינות"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].apply(clean_text)

    # חולה must be real boolean
    if "חולה" not in df.columns:
        df["חולה"] = False
    def to_bool_sick(v):
        if isinstance(v, bool): return v
        s = str(v).strip().lower()
        return s in {"true", "1", "כן", "yes"}
    df["חולה"] = df["חולה"].apply(to_bool_sick)

    # זמינות must be a valid time-range string or empty
    if "זמינות" not in df.columns:
        df["זמינות"] = ""
    def clean_avail(v):
        s = str(v).strip() if not pd.isna(v) else ""
        # If not a valid time-range pattern, treat as empty
        import re as _re
        if not s or s.lower() in {"false","true","none","nan","0","1"}:
            return ""
        # Must contain HH:MM-HH:MM pattern
        if not _re.search(r'\d{1,2}:\d{2}', s):
            return ""
        return s
    df["זמינות"] = df["זמינות"].apply(clean_avail)

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


def get_terminal(gate):
    """Extract terminal letter from gate string. E.g. 'B12' → 'B', 'D1A' → 'D'"""
    g = clean_text(gate).upper().strip()
    if g and g[0].isalpha():
        return g[0]
    return ""


def is_available(assignments, emp_name, start, end, emp_row=None, role=None, flight_gate=None):
    """Check if employee has no overlapping task or blocked window.
    Exception: TSA inspector can cover multiple parallel flights in the same terminal.
    """

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
                # Format: "HH:MM-HH:MM" or "HH:MM-HH:MM:role"
                if "-" not in window: continue
                try:
                    parts = window.strip().split(":")
                    # Parse window — last part may be a role label stored separately
                    ws_str = window.strip().split("-")[0]
                    we_str = window.strip().split("-")[1] if len(window.strip().split("-")) > 1 else ""
                    ws_m = time_to_minutes(ws_str.strip())
                    we_m = time_to_minutes(we_str.strip())
                    if we_m < ws_m: we_m += 1440
                    # Check overlap with buffer
                    if not (ts >= we_m + 5 or te <= ws_m - 5):
                        # This window blocks — BUT if role matches the blocked role, allow it
                        # פיקוח TSA block allows מפקח TSA assignment
                        blocked_role = emp_row.get("_blocked_role_" + window.strip(), "")
                        if role == "מפקח TSA" and "פיקוח" in blocked_role:
                            continue  # allowed
                        return False
                except Exception:
                    pass

    is_tsa_inspector = (role == "מפקח TSA")
    new_terminal     = get_terminal(flight_gate or "")

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
            # Overlapping task — check TSA terminal exception
            if is_tsa_inspector and task.get("תפקיד בסיס") == "מפקח TSA":
                existing_gate     = task.get("_gate", "")
                existing_terminal = get_terminal(existing_gate)
                if new_terminal and existing_terminal and new_terminal == existing_terminal:
                    continue  # Same terminal — TSA inspector can cover both
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

    # Dual-qualification penalty/bonus:
    # Workers qualified as both מפקח TSA AND ראש צוות →
    #   preferred for מפקח TSA (bonus = 0), deprioritized for ראש צוות (penalty = 1)
    def dual_qual_score(emp_row):
        is_tsa = str(emp_row.get("מפקח TSA", emp_row.get("מפקח tsa", ""))).strip() == "כן"
        is_tl  = str(emp_row.get("ראש צוות", "")).strip() == "כן"
        if is_tsa and is_tl:
            if role == "מפקח TSA":  return 0   # preferred
            if role == "ראש צוות": return 1   # deprioritized — save for TSA
        return 0

    candidates["_dual_qual"] = candidates.apply(dual_qual_score, axis=1)

    sort_cols_base = ["_dual_qual", "_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_task_count"]

    if role == "ראש צוות":
        candidates["_role_count"] = candidates["שם"].apply(lambda name: count_team_lead_tasks(assignments, name))
        return candidates.sort_values(["_dual_qual", "_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_role_count", "_task_count"])

    if role == "דייל":
        candidates["_role_fit"] = candidates.apply(
            lambda row: 0 if str(row.get("ראש צוות", "")).strip() == "כן" else 1,
            axis=1,
        )
        return candidates.sort_values(["_dual_qual", "_shift_priority", "_area_penalty", "_nearby_tasks", "_shift_proximity", "_role_fit", "_task_count"])

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

                # Find the actual column name for this role (handle case variants)
                role_col = role
                if role not in employees_df.columns:
                    role_col = next(
                        (c for c in employees_df.columns if clean_text(c).upper() == clean_text(role).upper()),
                        None
                    )
                if not role_col or role_col not in employees_df.columns:
                    candidates = employees_df.iloc[0:0].copy()  # empty
                else:
                    candidates = employees_df[
                        (employees_df[role_col].astype(str).str.strip() == "כן") &
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
                        and is_available(assignments, name, start, end, emp,
                                        role=role,
                                        flight_gate=clean_text(flight.get("גייט","")))
                        and has_room_for_break(assignments, emp, name, start, end)
                        and not would_exceed_max_continuous(assignments, name, emp, start, end)
                    ):
                        selected = name
                        break

                # Fallback 1: relax 4h continuous work rule
                if not selected:
                    for _, emp in candidates.iterrows():
                        name = emp["שם"]
                        if (
                            is_within_shift(emp, start, end)
                            and is_available(assignments, name, start, end, emp,
                                            role=role,
                                            flight_gate=clean_text(flight.get("גייט","")))
                            and has_room_for_break(assignments, emp, name, start, end)
                        ):
                            selected = name
                            break

                # Fallback 2: also relax has_room_for_break — close the gap no matter what
                if not selected:
                    for _, emp in candidates.iterrows():
                        name = emp["שם"]
                        if (
                            is_within_shift(emp, start, end)
                            and is_available(assignments, name, start, end, emp,
                                            role=role,
                                            flight_gate=clean_text(flight.get("גייט","")))
                        ):
                            selected = name
                            break

                if selected:
                    worker = selected
                    used_on_flight.add(name_key(worker))
                else:
                    worker = f"❌ חסר {role}"

                task = {
                    "טיסה":       flight["טיסה"],
                    "יעד":        flight["יעד"],
                    "תפקיד":      role if amount == 1 else f"{role} {i+1}",
                    "תפקיד בסיס": role,
                    "עובד":       worker,
                    "התחלה":      start.strftime("%H:%M"),
                    "סיום":       end.strftime("%H:%M"),
                    "_gate":      clean_text(flight.get("גייט", "")),
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

            role_col_t = role if role in employees_df.columns else next(
                (c for c in employees_df.columns if clean_text(c).upper() == clean_text(role).upper()), None
            )
            if not role_col_t:
                candidates = employees_df.iloc[0:0].copy()
            else:
                candidates = employees_df[
                    (employees_df[role_col_t].astype(str).str.strip() == "כן") &
                (~employees_df["_name_key"].isin(used_on_flight))
            ].copy()

            candidates = sort_candidates(candidates, assignments, role, start, end)

            selected = None
            for _, emp in candidates.iterrows():
                name = emp["שם"]
                if (
                    is_within_shift(emp, start, end)
                    and is_available(assignments, name, start, end, emp,
                                    role=role, flight_gate=clean_text(flight.get("גייט","")))
                    and has_room_for_break(assignments, emp, name, start, end)
                    and not would_exceed_max_continuous(assignments, name, emp, start, end)
                ):
                    selected = name
                    break

            # Fallback 1: relax 4h rule
            if not selected:
                for _, emp in candidates.iterrows():
                    name = emp["שם"]
                    if (
                        is_within_shift(emp, start, end)
                        and is_available(assignments, name, start, end, emp,
                                        role=role, flight_gate=clean_text(flight.get("גייט","")))
                        and has_room_for_break(assignments, emp, name, start, end)
                    ):
                        selected = name
                        break

            # Fallback 2: relax break room check too
            if not selected:
                for _, emp in candidates.iterrows():
                    name = emp["שם"]
                    if (
                        is_within_shift(emp, start, end)
                        and is_available(assignments, name, start, end, emp,
                                        role=role, flight_gate=clean_text(flight.get("גייט","")))
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
    daily_file     = st.file_uploader("קובץ סידור יומי", type=["xlsx"]) or st.session_state.get("daily_file_obj")
    employees_file = st.file_uploader("קובץ עובדים / הסמכות", type=["xlsx"]) or st.session_state.get("employees_file_obj")

    daily_file = st.file_uploader("קובץ סידור יומי", type=["xlsx"])
    employees_file = st.file_uploader("קובץ עובדים / הסמכות", type=["xlsx"])

if not daily_file or not employees_file:
    _logo_b64 = "/9j/4QDKRXhpZgAATU0AKgAAAAgABgESAAMAAAABAAEAAAEaAAUAAAABAAAAVgEbAAUAAAABAAAAXgEoAAMAAAABAAIAAAITAAMAAAABAAEAAIdpAAQAAAABAAAAZgAAAAAAAABIAAAAAQAAAEgAAAABAAeQAAAHAAAABDAyMjGRAQAHAAAABAECAwCgAAAHAAAABDAxMDCgAQADAAAAAQABAACgAgAEAAAAAQAAAsCgAwAEAAAAAQAAA3ukBgADAAAAAQAAAAAAAAAAAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYYXBwbAQAAABtbnRyUkdCIFhZWiAH5gABAAEAAAAAAABhY3NwQVBQTAAAAABBUFBMAAAAAAAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLWFwcGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApkZXNjAAAA/AAAADBjcHJ0AAABLAAAAFB3dHB0AAABfAAAABRyWFlaAAABkAAAABRnWFlaAAABpAAAABRiWFlaAAABuAAAABRyVFJDAAABzAAAACBjaGFkAAAB7AAAACxiVFJDAAABzAAAACBnVFJDAAABzAAAACBtbHVjAAAAAAAAAAEAAAAMZW5VUwAAABQAAAAcAEQAaQBzAHAAbABhAHkAIABQADNtbHVjAAAAAAAAAAEAAAAMZW5VUwAAADQAAAAcAEMAbwBwAHkAcgBpAGcAaAB0ACAAQQBwAHAAbABlACAASQBuAGMALgAsACAAMgAwADIAMlhZWiAAAAAAAAD21QABAAAAANMsWFlaIAAAAAAAAIPfAAA9v////7tYWVogAAAAAAAASr8AALE3AAAKuVhZWiAAAAAAAAAoOAAAEQsAAMi5cGFyYQAAAAAAAwAAAAJmZgAA8qcAAA1ZAAAT0AAACltzZjMyAAAAAAABDEIAAAXe///zJgAAB5MAAP2Q///7ov///aMAAAPcAADAbv/bAIQAAQEBAQEBAgEBAgMCAgIDBAMDAwMEBQQEBAQEBQYFBQUFBQUGBgYGBgYGBgcHBwcHBwgICAgICQkJCQkJCQkJCQEBAQECAgIEAgIECQYFBgkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJ/90ABAAs/8AAEQgDewLAAwEiAAIRAQMRAf/EAaIAAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKCxAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6AQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgsRAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/gDP36THpQ/LGgZ6LQJAOtNo+lLjtQMSiil9qAFC8Zpdo7UnAHFL7dKAE203pxSmkoASiinAA0AKFB6U7aO1Nz3paAAIKaeOKOhpKAEx6UoIoFLgUAJjsKdtx3pBTgM0AGwetG3PejsKMUANBxTaWnDAoAaBTwtN/pTxigACCkAozQOvHFACbcGm0ufSlAyPpQA0elPC56Uh9qcDj27UAIEGcUuzmk3c8UD8u1ACY6U3inc9aMCgBAKFGaTk08egoAVVXr/Kk2rQccUuAeg6UAN29qb2pfajAoAbSikp+ATx0oANtLs44ozg0vB5NADQtJ2wKQnNLt5xQAhOetJRTgKAF2g07aBxTVpwxQAzbxR7UdqXAoAZS9qSpAoxQAirmnbR0qMVIMce1AAI+1JwBxTenFOA7UAMopKeAO9ADQuaf5dMqUEUAN20u0E8U3AI44pwHNAEYz0oopwGKAGgU/YKZ0qQAZ9KAAIMU3A6UoIHNLgfSgBmMYpKOKUAGgBtSADFMp3GKAFwOAKTbS8E00DPBoAWm5pKdgUAJilAzSU/jHFACBKXbyKaB7U4DPtQABecUn0o60ACgBRha/Wf/ghcqt/wVr+AJP8A0Oen/wDs9fkz96v1l/4IX8f8FbPgCMf8zlp//s9J7Af/0P4Am4ak4pWHNAoEhOKM8YFGKUAUDGgUCl60tAC+w4o47U09qXrQAnWkop2BQA3HalGelA45pyjsBQAigYp3yjtTMHsKcVz2oAT3pvSilAFADR6U7ik+lPC880AJ9adxgcU35umKdg+lAAe1MoPXNKoGeaAGiiin4FACY9acMU0UvXpQAnGOlHbIoyelGBQAgGKQe1LxgYp4HPAoAaAKXgCky2KUBsdOlAC4HQUw4+lL83alAoATHOKb9KdwaBjOKABRzinAgdKbyeV4p3PegAx0pDgdKTnpTgMcEUAM70maKcAp9qAEHanAeopoyOacASelADh2Jppx2oy3agA9KAG45o74o+lOGKAGYpR0xR24pwB6L/nFADuBikO3mk+b0pR05FADfak4o+lLgdKAGgc0v0o9KcBzwKAFUAUHAHTFJz/DThnP6UANFNOBx6Uue1AxxQA0cHFLtOKXv6Uo9KAFACnGPalwMU0Z4xThu9OlACcYx+FMp3WkwKAG4wcUv0opwWgBoHbtUgApOd2QKFyO1AC/L0qPNHOKMCgBMUY7UU/GDQA0Yp+AKaN2c04bqADIFN7U3Bp4GeKAGYpKX6U4D/CgBAMtgU4AdKbyOlPwQeKAFHpTSPSlbdikA55oAFHPNJ7CjNKAM0AA44r9aP8AghYN3/BWv4Ak4/5HLT//AGevyXGM4r9af+CF/wAv/BWr4BD08Zaf/wCz0mB//9H+AM/eptB60o/+tQAneik604CgBBxTwSBio885p+D0/CgAzzzTSaQ04AUANxRxRSgUAKOKUHg4poGelO29qAFyQcGmlz2pMZOKMDNADaWkp2KAADnFOBI+7TRjNSBcmgBN3tSFqCKQce1ACD0pOO1FKAKAAcU7tgfSm08elAAvXBoDHoKbgkcUq0AJ25pv0paXaKAEA5wacAe1N69KeMelACj72DQGI4HQUm3jik2gNigABOcU3rRS8CgBAOcUfSjrTsCgBeQcYpP6elGOKXHagBMnOKaefal6cCjgUAIBzigc8Cj6U4AUAAyD+lLnpSdqUD0FAC5PAphOelFAHNACCjFJ1p3FACgYOKM8UYytOC4OBQAgPakLZGBSdRRgflQAnfFFKOeBSjGaAEA5pc446YpBz0pwHNAC7iDTS2Rik4xSjigBvGcUn0p3bAo4z0oAABnFOG400DI4p/t6UAG4g4pu49qOvSg4BoAM5PNNo+lLx2oABijoMUn0p46jtQAA84/Cl3HoKTvxRjmgBN3ODTfpRn0pRgUAIBzSj2o7elLgdPwoAdkjjFG44pucnrRjnHpQAuTnH4Uw8nij6Uo7YoAaBzQBS0/jgnpQAgOMClyccUuOee1NGMYoATJHHpSdelSZ5B9BTR/KgBuO1KKOelA6UAPGBX6yf8EL/wDlLZ8ATj/mctP/APZ6/JlRlsV+s/8AwQw4/wCCtXwC7D/hMrD/ANnpPYEf/9L+AJh83FJj5c0EmlGRwOKAEpenSm0/AzigBAD+FAxmj2o4FADcYpSMUpYim9qACnbTxim+1O64/KgAxzSjGeKAB0FBKgYFAB0/lTcelKc9TScj8KAExx9KdtPWj2p27AIIoATC44ox6UpHFJjGKAF9hTcce1KQcYoIYcUANwKBkdKUZ3dKXnpigAAAo6ClIPSl6Hjp/SgAxnAUUzHpUoAH4/yphPYUWAChxx0FM2mn7cetGADRYBAvANG3PNP8r/61KB8gosK6Ggcgdqbg9RUhXjcxpo3qM54osCY0qwHTpSYPpTi0jdTQA/QfpTsMAPakXJpdjt+FSiNuB0FHKxXIwClIFP5VIytupAr4+lHKwuM2t1xxTdrdqcN45zil+dTiiwxu3b1FGw0BTjGaeQ4wD09KOUBAMHFGznbSmNs7e/tTcN+VHKwAIevpSbG9KVlkJ5pMOKOUA2YpNppwV6ftcDB5pWFcAOeaZg9adsYcn0pxDYHHSnysLkew9uaaFJ6CnZek/eCiwxMY7Uu3ngU/Dj8KXJpWFcZjp+tLtIGKdkk0fOF9KdgGbSMUeWw4xS/P3pwaUjA70JDGbSDg9qTYemKd8+MN+VLt5osAm2lxzj1o2Y55pwAzjmjlFcTZzioipqUgnuaYVPSlYLiYI6dqNp7UuJAcHNJg9+1AwwAKAMnAo2k9ak2D8higBhxgUhUjtxTtmOaViyjYRxQAxVz0pNpAo2uPalO9jk0AAHGaQDsKk2YHuKVRtBJ6UANOBio/pS5KmkwVwaAFwQaTHpRkj2peeKAADmjAwfam5p4oAcGX7uKZhSOKBjGKBxwKAExg0ewpQT0FKPbigBAMdqUDJx2ptKBQA4fLz6V+s/8AwQvCn/grV8AdvX/hMbD/ANnr8mMZI/pX60/8EKx/xtu+AK9v+EysP5PSY0f/0/4AW+9xRxSdTTh7UAJ900vaj2oAGaAExz6UlOxngU0dqAFA5ANTKFxjAppQdadtHbtQS2gwvoKcqr6CgcHmpQoTmjoZ8wpVNpAABpoUMeFqTA2jfx9KB7dqmIrjdqcY6DpVgIh6gflTAq/d9aei5B3joKUY3Ycw0xptD4qVI0ZdrKB07VIkYZst1qaWNlbcp6V0KlczlU7B9nXGVAH4VMkdui8op/CmAbeSam27f3kmSDW0aKRk2xrRRj+BevAx0qVII2OzYvHtU3lfL5rZIApyKqrzxW3ImguyIQQO2BGoA9qseXbj70S/lUi7UbP4U7LDGehpqw7sFihC7BGvT0FKbS2P3Y1/KpFPHld/X0FWIYxF8rH2quTTQamxn2SAKPkX0HFH2aBSP3S8/wCyKtbCzcHpUbRhirHp0Bq+UcXYX7LbMo3RqRjuopVs7bd/qlJ/3RxUw8wYKj5TVlR+72547noKfs4iZXWxtjn90nHbaKkFjaZ+aJMnj7o61YSF1Cs5GB09KuR7iMqu0g4z0oVNdiblJdMtRnzo4wD0yo6dqYLWxRQBCn/fI/wrTER+XPb26VKYx1AHrzWyoX6DuZxsbQAMYk+m0f4Uq6faKcNFH/3yKsgMHIBzu/L2q8sION3XjgcVSw8U9QcmZ4s7MDHkRn/gIpV0+3ZsiGP2+UVp5jB2jrQkXz7m49KynBLZEOWtjNbTbI9YkP8AwAUyPT7H/nlHj/dFbBhwPn70nlxggp2rSlT8hoz/ALDYgZMKAf7gpVstPY8QRj6IK0fMPO8Uu4DjBpTh/dByZn/Y7RxsFun/AHwBSjS7Qf8ALCP/AL5Fa23I44oEcueoxSjGFthqRk/2ZZryIYs/7q00abbZ/wBTF+CL/hWqYpufmHtiovs7f3vbpVqhARS/sy1xgxR/98CmNYWwbb5Ef/fC1oC3fPDU4ROv8dV7CA7Gd/Z1tnb5EX/fApDYWyDmCPHsi1ppbyBtwIwaXBzSjRixIyjBZn5TAn/fA/wpGsrFTzDGP+ArWk8gAyR0puYW4ZfpTWFj2M3e5ntp1gBzCg/4AKj/ALPs/wCGGPj/AGBWm1uHICEj6VCbfaflb8KTw8TW7KH9n2iA5hj/AO+R/hTPsVp18hP++RWn5MoOMYxTd3OHx6Vm6OuiM7SMk2No3SJOf9kVE1hbnlo0x/uitWa3AXK4DetV2VsArkkml7ASnK5Qe2tdgSSFBx/dFRNYWf8AyzjXP+7Wqckgz8+ntUMqrkuMewFdHsVy6o1UjKmsokO14044+6P6VX+xQDIWNMdhtHFapVkbBPBpjRn73TOK4+RPoDmZzQWoPMS/go/SoZbeLoqR/wDfI4FazNjOR8vYf5FVpY12DPP4UnTiguzKNtasNgRP++faqyQRjLGNMf7vbtWsYON8YGO3vUPkmRQAMEf0pOBopFLyY1yBGntwOKjaKJfmCJjA4wBUxV0YbWwc/pQqgDis/ZroZ6lVrVZRkqox0GBUBit92GVemBxWns2rsqEpEx3AdBUuKDmZnmONSFZBz04pksELMVwAR6CrOxVG0Z/CqW3y+uQO1Hs1sVfsRtFErFGAqLyohlgoxwKv+WD9771N8qTcdprFpIXOUHVl5Cj2GKYVA4IAP0rUdAnzYP8ASqEnDfXgVy1blwqXK3lKflI57UGJSxU9BVghh144qr8y/IKlLqaxkNKgj5QMCo2jC8YqZsL0pPvHBHTpVFPyINg9qbt5yKssoHWoegoHFkHGKT2p5XNN47cUGgo64pMdhRQBQAo64oHNHUUvFADgccV+tP8AwQs+b/grd8Af+xysOn0evyU6mv1o/wCCFx2/8Fa/gCw4x4ysP5PQCP/U/gB/ixQKTHNOAFACDikPtS9elC4yKAF5XmnKVHJoC5GKUD1oAk49KPwpR83apEULSbsYDB2wB6VaVAFpEVTwAKXkcLUXuSwx+VIdu0Yp3tQqpIw9/SriONhqFFIXH9KmiUA569ABTxD/ABnqMYqyY9o+UcnBFdUIrqZykCkt8wGMU5lO7inqv93p3oAZRz+lbJJGY4Kg9aniVNpL9KZEpP3iCKsAYXA7VatsAO4X73+RTwylVHcf4VGqPsO/vwMdqnUKvIGOMcVSsA5DgbiMg9KkXf0Xt2pyLlPLTgA/57VZt1JAx90jFO3QTdkRiJugG1W+mauBU2jj7vSnRQNEo7571Myhh5Yxx1qo26DuIMZyP/rU4bOvXOBTRH+9BGDkfyqcRlQOOODVxjcAVhkBeB044o24+WrMURB+VeMcU9lKbT0zXRSo2AjTcpzx+lSA4O3b271KsCE5JOPenqFXLAZrpjEQ0oRgMe3b/CnnyuBzxUqq0wDYAxVhUVPvYquYZCF4OB6e1SJE+PmI/Cnoo3EKDUvlZH8qyqRvsJq40wrj5h+VPVT0Ax+FWAgHLZNI6yfdXpxURp2QETKwXDdPyqPbAOelWFjmQ/vOlSrFFuyx59q0WgyFHhwAoqTO8fKtTkLGowMU3ex4rGpF7iItjqaXYw/GpkG7naKPL6fKKuEl2GQGJgvpSYcdTVjypWIXgGgxSdRt4x0pSs3sS7kAV+AOc+lIEfd/+qrPlP7YpFgYHJx6VEUuwtblfyJCcZAH1pqxPGe36Vd8uTp1+lG1x1XitkSpMpsGA6flUR8v+MYq2xcdVxUJ2ydcDHSqTL5iEJFjb0qMxL/Cuea0VjjC9s+1RfZ1BJBOO1Tzai51sVjFcAY2/lUTRK3+sFXSJUFIUSVRu5NFyVJmfJbjgrxUbp5JxjjjgVf2MV+SgK33SB/hSW41YzyyR/6xfeoHSJs7E9+OKtSJ85VabHE4OVOV6VEoxbI5VczWRomz2/LtUflbwHUfdxgDpWmVBG1sewqF4Wb5UwoXqO/FW4I2M8/L94d8VE4KKMcA88VdaPGVf6jFVvIJcmMYHcdKzdJCsVgEk+aI/wCTUbbCeBg8VaMSkYUdPTio/Kw+044PSprRQ2ZkgjRgFH09BUSoEOP4T0q+YDgh8Y/pULxjonGPWuOw7lVo2zs6VAQqg4FWHQg5Hf19Krlu2PaoaAg2xvwo6YzVJ/JjJQDK5/KrzJ/dwB3pjxJKuT2oQFRXQHGKlVtvPtxTnjGcPVaRWJ3dFFTVp8xnKNx0u5F4rPZGDkfnV0szDOR9KZMm/HqK5pRSWpcfdM8qU+/TMjI9qtuCzBG74x+FVCADjArPY3gxco421AQUfB5qxsC9qYeTkVkmNMYysR6Yqv7VZAOCR0qJx3qikRHGMVCQAanpjgAA0GkGRDrigelBGKVcUFjsfpxSDnij3pf6UAAOOK/WP/ghpz/wVn+AYHGfGWn/APs9fk394gV+s/8AwQuX/jbX8Auf+ZysP/Z6AR//1f4AT1xR7CkxzS9KAFOABik9KUe1PKjoKAHdsCjB9KVODUnU7TUtkSmIoJNSHgbaNoQbvwp6tkU2jNj1AXBowGwe1KoGQ36U7a3CDrSpwREpDSORjtT0UcDGDTxCFGKnjiRW2j04xWyRPNpYnX5ugzj6U/IPT+VOI8tS57gAU13dU56cdq1ox5tTBakRwvJHWplTzCAKXDB1/CrWGZcDgZrcL20GRIu3OKe6bBu6Z/SpI13Ebe3NS+XlNi/5xVxRaGjlsfw9KsLCCfm4HaiK3G7YOo59qth/4cdMfoKrlsA3yeitx0HpVwRLgEMAOOlRqCzYHbnFW4E3cAdOuR/ShPsSJHGYwQ/zAfdqZdgI4wOlOVVH+q6jr6VMFlD4fkZHTpXRGi7CSIljDEGLt6VYUInzNyT2p/lqpBi4NSRIf4hXTCNkWhyBiMA4pWVEwzCpiqAbgfyoCAtv7VSERFAr5BOTUqofvfeI6ZqRFLLkDipfLK/e44rRMZGmW6LipFhXAZulTbgeVpVV3OT0xUvTYB4TnIp6p60ikQ9Dmj/W4C8VzPnbEhUiiU4YZHtRGXII7VZC7UGeKcqDHy1rGNhW1IBGc/McUKozirQgI6nFARAQQadiiLK7cH6dKlSJ8ZABqVDt7GhFkJyg5FNEjNjKuQM+1MVGJy521YKyMMYxSLbAqHAqX5Cb6EO35uT09qGBCjaasmNVGSoqLah6Jj8xVqbtsNaaEe1m6tSFFXG4nmrWI1IOz6c0BIz2GKUm7bDZEFKnKc0wo3JNTNBjlOKeFc8ZqIu5km2UW3LgOvXsKZIkWcYq1IjqOaYVXIZsVoi3EgEMarzTNoVsVbaNHGBx0qHasbEMKyUWpXDlSK7FkQ0hEbKMcVaHy8KP0pXiUgbht4pqTMlUSdij5WOQdv0qIjCDGSe9W5EIWo496A8Yq2XKmiqFL5C8EY//AFVGIGRcjnOP0q/tG/K9KbuO7aBnisZu01YLJFSUAD94M1VdWwGxkelaLbWG0DHrVcgxY9/Sug0M/wArcOarlHU7X59MdRWkUD/Mvymqzqwb6dxQBRIDMUA+7UDqM/MMjPHbFaTxO3PAzVbJTsfwqJxAqm1SNSWP+fpTXiHmHHarAj4w/IH0qB4xGcDHrxiuK7W4GbMhKnYNw6D2x9Kztmzk9ya2GRt3y8Cq5jfAB57iiUbAuxlHzEbA6CgwtkFvwq9LCM7wT+FU5ANyo3JPFc7QyGQAgle3WqrKGxj6/lWl5R39M4H4VVKpk9AP1oWxHUq7REQ2AKCFK0Orbv5CnAEDisqkBsgaMFc9xVIxg9KvbHDbgePSmlOWKjGelYOKsVGRn5HQ03aFfHrUrYz0xUZw6nHaufRbGkRpG0Y6CoccVIvowpGUCqLRWwd3NIcE1ORkYqAgg4NBVxhXP4Co+Km+tMBxnAoNkCgUwUA07HpQMUHB4r9Y/wDghgR/w9q+AIPH/FZaf9P46/JnGeK/WX/ghgM/8FafgF7eMrD+T0Af/9b+AE8HigEYxig0q9zQA9Pu040i9BSnigVxQM9Kk27D6imqD2qT7px60GTHL98ccVLx0HHFM2FBxUmOBmkQxwOGGeKsKAi5PtVcJvbI7VaBLjC7cela0tEZSJAQflfj0xT49qncPpSCMl89MYGKslQqZPPQ1vZGcmNLljgDp6dqRgcben0pwaVPm7deBUpVkAdxkGtUrAo22FT92vHFToQxylMWPktx6VbSMLk46VUUUJsRh83fpUyq7bfLB/kKaQCRDkEsegq9FFu+7268D6VfQmTsh0VsWweckc0NuVi+MA16R4U8Ex+IrWaaScxLEQuAMkkjt2GKi1L4YazbyFbCVJowON3yn/CvYWR4idFVYrQ4nmEFLkOLtonyBIMKcflVzYr58vOB2q5/Zuo6aRZ3MZicDkH+YPcU4RRxLnA7VxUsNKEuWasa0p31M9gOi9eMmraRHAJ4GOlOEAH38DPT+lO2uhCv2/KulPoauougnlsoG4Dmpo9xfavJqTyRN8wGFWrCv5K7VGakx9sxsaoijjGaVEDDjgH8KspG8g3kjGM0iRu/y8AdB2oBVmtxflwSvHamG3D49qf5BjO88jt6VJk7d6YAArRtJHTGS6ESrGMBRwetTBeAB07cVMke1QHAqbY7INmFGODipZLvfQqlE3bj9KmVNo+XFOQMF+bHbFSLHsO09TRoUmtgWMHg08QEcDigxPj6U+Pex8sjOO9KxQ0Qqv0FSRRRgZHepo440PPPbipwig9OccUaE86KYZ8fdpSsmcPV0K2BgYxTmEiE56fSnymbq9iiLbg8k0hiVcbePpV0RjopNKqqVCg88VEZxuZxqFTaRyen6VIAmMk4qwUQ/K4/I/yqPy4gSCDz71r7RbClPsNURDHT3xSNFE3Ht2q35KDIX2p0YiHygjijnI5+hQMCABkPHtUbwOp4rSkiiOefSo/LP8JzWUI6mtG9zLKyx/Ln+VRSfMBuGcVpvHheOKg2LnAFVY6EU8bjgAcU4pvUEjGKleAEjbgYp/luAAMYxRFDKn3enFQt8xAfirvB+9SNGrClJaaGEqfYqNEcduMflTcYX5hVkRYxtGaiaR1JRhijUhxkV9nYGmY2H61M0PmqGOBS7CBz6VNiWiIwhj8rVXMYU9Kt7dn096Y4QHHvxQHLJbGc4DkbKrPuHHStIwAHcgqBvm+UgAirOlSKYUEALj8agcn2Hb0FX/LWB9x5FRssch3j8ulJ7kSbTMhg4+Ukj246VGUEg3KeB+FaDhj8owPb2qjKFXGzgUpQTVjWxRkCyMWAxjiovLIX5egxnNX3j35Yj/CoQXYMhxgVzezaMqqfQomMjhT25qoUJO0gHHIPt61pSpvQLjjtVWWGRWC/5xWU1YqE7meCUHzfd9qhfbxwOtWXjH3NvGc+wqLcFJjk9fyrJFFGUADcowAaTZngjBqaYYYxE5z+VV87vlHbrUtdCLaDtv7vj0xUGVxhjzVrAVNn/wCqoWiLcdPpXPsTF6FZkjYfMMYqkyqpynStAq3VeR0rPkQjnjFZyiraHRBEJ6AjrUWHYfN+lWOVAGOtJ91cmsjVMr7dvBNNb1FSsoxv6U0cjIoKIl44xzSEAUrJtptI0RBx26UnWnsOKZTNBc45FfrN/wAELV3f8Fa/gCv/AFOVh/7PX5L1+tv/AAQnX/jbh8AOM/8AFY2PH4SUCZ//1/4AW605QCvNNIHapVA29KBN2FFFLmp8D0oM29QXHSlG0SZPSk2E429qmKKBWTl0IuO6j0pGLBttOVMJzSqgI3/lWlNXI5h6hk5A6VIkYDBxSln24UYFThCoJ/KtrbWMmTRsT94YIqQj94MHGPTpUbyf3eOn6VKEEjAL/hXRTgZpCgAgIPpxj+lWPKZj5YOcc/lS/ZYgAozjtUixAR4H41vYsVVXJCde9TorDjpxilRcNnHWpiCMVSQIcoBAyAB7VfgVFbe/Sq4Vido9KtwpuTZ16UnHQicbqx3vgXxF/Zur/YZTthuQI+n8f8J/pX6Vfsr/AAL8D/tHXms/DnVr+TRfEkcAv9Lu1xJHIiHZPBLDwHC5R12srY3dQMV+TbwSoVZflbII9v5V94fs6/FHWPh14v8AD/xb8PlZr/RrhZ5IjwsuBsmgb/ZmiLL+NffcLY+c6UsP1Wx83muHUWpo6z43/s1eO/grrf8AwhfxOsEjklVns72A77e5jXALwSYGSDjchCsvdQCK+JPFmhXXh64FvL80bH5HA+96dOhr+zP4g+G/hR+0p8HYrDUANS8Pa7bx31nOhAmi3jMc0T/8s5ovukc9CjAjIr+b79pL9mvxd8C/EbeHPFEYv9HvWP2DU1XbFcqMZBAz5U6jhkJ7ZXK812zdHHU3TmrVEY0akqTTWx+cnk5IPOB/KrkCxiTe43f5/wD1V2Gv+EL7SXNzbKZbTHB/iQdtw9PeucaEbFKcD2/Kvi62DqYduFVH0FCvCcdAypOfuimYQyCTt7e1I7FSUxwcYzUkNsVcM3QdK4YVrsfL1Bi/Kp3q2SuWVRgipUhfOFGRV3yhAod+/GTXZGQ5yvqZ7RMw5xhaSIYGwgY7Y71YCs6jjge1M2B3EPP4VnOF0ar3VclVYAg2ndkU9tyrtj7+npUsFkwDMeFq+nl9O3t+f6U5eQ5T7FGKBogWkGaEjCDIHWrP2eN2KAngjGOBT8KF2LUqJNKPUgjXeeRip0gPUnA7VNtcgDoKckZz7Vp5G9tCusYA4q0HHDBaVVPYdKVY5CvFCijF0kMzJKdq4xipDFK8gRW4qRLZh0FTJC6fNnj2omtdDKpFJ6FEQFQSTmlYRbclfu1ewvPTFI/kg9s+lKyRmZ6+Wo2Ff51YXy/TFWliEh3KvA9qe1v8uSh9uKTsBULRnk4+lNzGr7h3q2IRjDL19qkW3PBKHnpgU7qwGO6hstwMVIsJAGD/AErSls3X5NhB+lUjEyMVHUcVVOXc3otIg+zleai3yD+HirixFe+aeYsYyetJGntUUBHHIcHK96iERU4H4Vea2BPJqJreQcK1KxnzO9ik+QM4z7VHsbqMfhVlgVOGFRbUf+HGOlNo6SB42AyKjzxirzB8cD8qhaKPOWJH8qCJRuZ+35sDhc0/JYc4AxipngwwVeam8kqvzDH9KzaRz1Iq5m+SUG4GoyiOcsOlX2jdV55/z6VXeMk8ce1N00bSlpYrFGXmq7qH46EVfYug+YcegqNkUncvSqjGxMIWZmOjq5z0o8pDwQPw4q+0StwTzVdoCvynp0FNGpmTxh1AZd2DgbefpVVlZGwx6/8A6q0XhIYvH19R6VEUViGTgj9aq1hpFB7Ybc85qlLtOG+7t9PaugZZBh1Gayp4MnL/AC5PasMRJGc3rYzw/nDy1yGA71TkHmKuOqnnjjtWoICBubqBUsdsrDLk57YrhnUWyOdy5TDlh+XgZ4zWexjX58dOMD1rbvLQqpbOOentXMy3CQvuY8Csot9jenJNEkrKGww6cfnUSrGF7cjrzQrNMPQVG6Mv3cYrCrOotohzxvYkMkasFYZ9qgZmycdDQybD7Y4qESR569TXNCp1kEYLoNmYrg9c1QkGZcJ0P41eZOKhMYPQcURqrobR00KDlgQCO2OKDnbVnb5Zweh6VXbjgDNI0T6ATxmoguw7SalZTj2qNxlfcYrJSNCKTnkVFmrGzIqAgA1qWmRsN3NRHj5al5HPakZd3Tig1GCv1t/4IS4/4e5fs/j/AKnGx/k9fkiK/W//AIISgf8AD3P9n89v+Exsf/QZKBM//9D+ATaRyaevTFFO6dKCJPoKq556VJ90c01OFp5UsMCgiQ+Nh0I61MACcGmoFVaehw+Kx3Zm2K4AAApeG4HWk2468VNHHtw7dK1ppmdy2ibFyKeuS2MfL6dqYzEr8nfGKkh3D8BzXoU6dkZxXcfmNv8AV9+v9KnhjBIfbj1qNY4zjaMMOc1bDFWH8XbpVoom77gafhDnnFNjUqpQinxhS29sY6VrcQ+OMsnmjr2qzErjlsc0oUAjbwewqdEAbc30q4jJYogoyepq5CFjG56jUMhCN1q2Y49o79M0p7WMqmugG3DtubI9MV6d8PNe/srVBYOxWK4wD2w46E/XpXnG0F9np2qeF/KOc4/SurLsRLDVo1UcmKwqlDlZ+9f7A/7Ulp4euB8AfHN1Hb2V3M02iXMzBY4rmQky2jMeESZvniJ4Em5f4xj9ZvF3gjwr8RPDl34Q8bWKX+nXYCXFrKMglT+DKyn7rLggjgiv49tG8UQX8I03UyqvgKAfusOgHoDX6w/srft6eM/hnLa+D/i35viDQYdqpdlt+oWUY4AUk/6REo6K/wA4A+VsYWvssVg/rD+sYZ69jw+X2fuSOg/aE/4J9eNvhjDP4o+GaTeIvD65doAu6+s09GUDNwgHRkXP95eN1fmF4g8C6ZdhriwJtZByRGvy/ivbHfHSv7D/AAL488GfEfw1b+LvA2ow6np12MwXMDfLuHG1h1jcfxIwBHoK8H+O37I/wL+NrS33jHSPs2qyJj+1NNItLwf7TnBjm/7ao3sRWdPPo29hjYXK+qv4qbP4/NZ0DVNOnPnL5iJ/Gg6fUdRUVlmaMbOSO2P/AK1ft58Q/wDglD8dLPfdfAe+tPiBGv3NO3Jp2tgdMR28x8i7b0W3maRu0Nfmz4k+Eeq+F/Et34O8Z6XeeHdfszturDULaSzu4WH/AD0gmVGX2yoyOhrmlklCu+fCz+R3Rxk4K00eCxwvGeB1xUsscToC54Pp2rttR8F6jYZEX75VHJC7WA6dD1/CvP7oFZjbqCCo5GOmK82tl9WhpNHTRrQnsKYQAY1PHrTokEPyLx0NLApP3v8AOKvCLocDHTA/SuFrsdLiyPyfN+c8CnNG4OwKNvTt+FaYUpBjqDVTKs23HPYj2oUdQprUhEZCkE4xUoEXRQcmrEcOfmckjpTAgX7vHatOXQ6Ul0G+X8uOlSxxc9ccU8JhRn8KdbRzXVxBp1nE81xcMEihiUySSMcYWNEBZmPYAVlKolsYOpfSIihFxvFLEGd9iDcT0AGf5V+xn7JX/BDr9u39qBrTWdZ8Pw/Dzw9cbW/tLxYzWspTjmLTYw12x9PMWFT/AHhX9Sf7Jf8AwbG/sK/Dy3ttZ/aE1TWPirqa4LQTyHRtJz7WlkwnZen+suWB7jtXDWzCEWaQw8pH+fvpmk6prGqQaDpML3OoXBCxWsCtNPITjASGMM7HnoFr9Pvgd/wRU/4Ki/tBw2954B+DPiG1spxlbvXootCt9vrnUnglK+m2M+1f6WXwn+CH7JH7GHh5dM+EPhLwx8ObJECn+y7K3tZXH+3IiiaU47szE+tecfGH/gpt+zr8H9KbVdTu3ugmcSzOlrCxHYPOyk/8BUmsaVetW0pxM8TVw9JXqSsfxt/C3/g06/bp16CK++Mnjfwd4JjcgyQ2/wBr1u5Re4wkdrBkY7Ske9fcPhP/AINOvgtpUMbfE/4y+J9XlXAdNH0yw01D9DL9scV9EftF/wDByfqWhI+nfATwvpV5IOBLcG5nQenzf6Mp/AEV+PfjT/gu3/wVU+Nfi+HwL8MNXW01DUH2Wmm+GdFiuLuUnGFiUx3U2fcV60chxjjeo7I8D/WvC35aSufsX4c/4Njf+CdOjW4i1ODxt4glU9bzXfK3f8BtbeHr7Yrpr7/g3p/4JwaJC3lfC28nVejXet6q59O1yo/TFfGHwZ/Ya/4La/tIeR4i/an+NPiD4Z6PdgObSTU5ptUZGxx9hsZYYYDxjEsysvePtX6g/Dr/AIJP/s4+ALOOf4h6l4o+JmqqAz3firW7yeNj3ItIZIoNv+y6ufc15WJpQpaOZ6eFx1WrHSFkfEviT/giT/wTt0tjaxfC21VhwB/amok+33rrrXjetf8ABGX9gLBW3+H7WnHBh1bUUI/O4Nfti3wU+GvgKHyvAvhzTNHjQbVWzs4YSOP7yoGP515hrMEcLtuwuOBnHFef7Xsz1aMZL4kfgr4z/wCCKH7HUzM2iReINKH8P2bVmkA9OLiOWvkHx3/wRJ8DQiU+CvHmsWZ6ot/aW12oHoWi8g/pX9Qlt8P/ABP4rUnw/pt3fE9Ps9vI4/NVxVLWP2TvjlfxbrfwxeAN3lCRf+hsprZYhmkqVkfxd+Pf+CSHx48OO7+Ddd0XXkjH3JDNYTMfQB1kiz/20FfFnjz9k/8AaU+GUUk3jDwXqkVvD964toheQAevmWpkAH1xX93HiT9kX432gKzaA4Iwf9dbk/8AoZr578T/ALOnxa0uUyzaBdr7xrux/wB+ya6IYqRzNQsfwifu/PNsp+cfeU8MMeoPIqVoCOR6fhX9hPxK/ZO8HfEUSp8V/BtvfyICvm31mVmUf7M+1ZFx7NX50/Fb/glR8PNQje5+FmrXfh+UZIt5/wDTbXHphts6/wDfbfSt6eLXUTprdH4BFSO2QPSo2iHAUV9i/F/9iv8AaB+DsMup6zo39q6ZDkvfaQTcxqo7yxBRNH9Sm33r5CnEZQyg/L7V2RqxkDcluVMS7v3eDj8KaGV+lS5CZI/ipViTk9Cce1aKxKnpcrPFsYOOaHOQNn6VKICv3e1ACNkdx61nCCJ9ncosfLXaOc/lUO3cxJA4q28TRffpTHvGIxirt2LVFFR8xJ84GDUDRAqDHxVlsRjZLyvFSrDsw3OD0q4tdTRuxnNGiqQ3yk9BVd0khGxhj9K2pLcAfdx6VnoZGby2G4D0obsroSmrXMyVQo4PXrVBk2v7da6VtOuLpSltGZHPoPxq9p/gm/llzeP5Y7qoBYD+QrbD4DEV/gjY5quNhE5lflhDcADvWhBoeparb/6BbtKfphfz4Fe4eDvAVnf61beHNIs5NT1S7YR29pbxvd3UrHoscMQZmPsqmv3a/Zi/4N8f+CoX7S1vaajF4Ci+HuiXGCNQ8Z3H2BgnHI06FZbzp0Dwxj3xXpf6u4egubF1LeR5/tqtR/u4n831p4D1GRt99PHD2wvzN9OOK7fQPhto7fu7kTSnvuYIP0r+8n4J/wDBoZ8LLBoNQ/aa+L2ta9KFBlsfDNnb6TbKe6+fc/bJmHuBGfpX62/Bf/g3g/4JIfCEW7H4UW3ia8hGDc+I7281V392jnlMH5RADsK5Keb5Vhn7seY3jl1eXxOx/l/jwT8OtPj2XgtUcDpLKN35ZrLj8FeFryfZoeni7Hrb2zy8e21GFf7Fnw1/YH/Yb+DlukXwr+EPg3QvKOVez0WySQH/AK6eVvz+NfSen+D/AA7pkSRaXZQWsSjhIokjUfQKBXVLjiha0KCRrDJGvtH+LTY/DK3ZAD4fuhgZ50+bH6xVjax4M8GRoV1C0htdvH7+Iwn9QmK/2yotM0+BDmJADzyBX5Rftp/8FVP+CT/7KWqX3w8/ae8baBNrloCLnQ7aybWryNv7k1vawz+S3P3ZtlOlxep+4qCYqmUJRu5H+SbrPw88JX0Jayh2bhhXgcsD79xXhuu/DPWNKczabm7hX5vlGGH1Xv8AhX9yX/BST9rD/gh58XPhXoHxd8Gfs06nr2jeM/Pt7bxp4TWy8LTWWpW74lsZzHnF8kYE4gvLZ0khYOgkUNj+Sa8TRrjxBdjw3FcR6d57m0W8MbXK25b92J2iCxmQLjcUVVJ6ADAHo0MooZj/AMu+Q5HVnh9nc+EXilhJSQFSO2MYxVWOYDjvX2/4i8BaF4kjZ9QgKzlcCWMAN9Tjj8xXzL4v+Fet+H5fO03/AEuDGdyjDAf7v4dq+bzbg6vhdYaxO3C4+FTR6HnMrc4PbioZMYoYSK22TOR2IwRSMw6EV8fVjy6NHoomfaw96qlSG2087t/PSmyZVixrlirFRK/+9TWjP3hUzYYGkZl2ha6jVFTBBwaT2p5+8QaZQaJkWNpr9av+CFOB/wAFcPgBx/zONj/6DJX5MHDDPpX60f8ABCcD/h7j8AAf+hwsv/QZKCj/0f4CKTAz6CnMPmxTlXI6UGKZKFAxiljy4/pTBxwPwqWMFVxQJj1hYjig4JHoKljO0baAioKyhuZcxIkZK7m4FX0j3YHYU0LhAnAqTDBSq9+K3p7nPcj2qWB7dh2qwkUZ57HBqsINwwucjj9K0YYVC/LwF616Jq1oSgKF3jv0p0Zbh14z2psYLZWPjnpU24I5V1zgdcVSJJBsXDMOKkWLcAvcc4zio/8AWEB+Aeoq6iYw/Y421cSkSwRBcNjNW402EkdPQUQo34dKlRNzGMfjV2ViWTBIywWM81chDYKDpUcQXblfpVxBjmlFJhYi2rGRuAq3sRlBb5fpUIXzenRatBVkRSgxzW9fSIFeaHcu3HB/KvSPDHiS60eIRXRMsAA7/Mg/2T7elcTsCDBPI6D69q0FH7oAcD24rpy3FVqEuemzmr4ZTVmfavwM/aF+InwR1o+K/hdqW2KRlN3aSgtaXQHRLiLI5A+664ZexFfut+zp+3B8Nv2gVj0G5A0TxFtBk0ydwd/HLWkpx56/7OBIB/D3r+Wezvbmxk8yycpgAH0PsRXeWXiG1uLiFiTb3cbB49jFTvHIaNhypHb07V9TTxmGzBctRWkeHUoTo7bH9lSQh4v3B3pJ6cjAPf6V7BrmoeDPir4Ug+Hf7RHhrTPiF4dt12Q2uvQGeW2B5P2K+jaO+sj6G3nUD+6RxX8+/wCyn/wUP1vwhLB4S+O7y6hYj5U1pRvuoh0Auoh/rkH/AD0X94P9uv3K8P654c8a6Ra+I/C97Dd2V4nmW9xbSLLBMvqjLx16jqOhA6V89mWTVsLLTY68DiFJWPjH4x/8EY/g58TLOXWv2L/iB/wjupkbo/CPjmVXs5H/ALllr8MahM4xHHe26t6zd6/Az9pf9kX4/wD7Lvi4eEP2mvBOo+Db+U7YJb6L/Rbr0NnfxbrW5HPHlSPx1xX9V+oG6tZ3jhdonOQcHHB/mPwr3bwB+0n408LeGpfhx4ttbDxf4OvE2Xnh7XoEvdLnX0MEwZY/bZ8g/umjD59XppQq6o6KtCDemh/CJJ4MvbaQvp2ZF/utww7fSsyazng/dzKVb0Ix0r+2H4hf8Eh/+Ccf7XVq+pfsxeIG+AHji4+ceH9UBvvDFzM3RLdncS2wY8ARTbR/DbcYr8G/21/+CT37b37EC3WpfHnwDcTeGrZtqeJNEzqmjMvQO9zCge1B7LdRw57cV6NCWCxOkXyyMZRr09d0fj7ITjZjniiGFt+1RnPP0/8ArVq3unoEM9m4KPymz5lI9vaoLKO6kukto1Z5HwqhV3FiTgABc5J9BXHVyqrS13RrRxK6Ey2xdcovIA/Kui8OeDvEHjDW7fw54YsbnUNQvTst7S0haeaQ8cLGgLH64wO/Ffoh+zV/wTf+J3xWntdf+Kjv4R0R8MEkTOozr6RwNxADjAaX5h1CEV/R5+yr+yr8MfhJbp4M+BXhxIbq6UC4nA829uAP47i5bnb7ZVF7KK8TFY7k0R6tKi5as/D/APZm/wCCLHxD8by23iD9o/Vv+ETsDhv7K03y7nUpB6STHNvbenAlbnoDX9OX7G/7FPwB/Z1gS1/Z88E2mnX20JPqrqbnUZM/89b6bdIFPdUZU9Fr6s8L/s/6H4Vs01f4h3SSsmMwIcQqfQvw0jey4B96479oX9tb4PfsyeDU1PxfqEWhWbqVtLeGMNe3e3jba2oxxnjecBf4mWvPw1KtinaJhjMZQwseeoz7N03+xvBSRzeJrzdc8bbaH5nOcd//ANQ9K+S/2nP+CtXwW/Z2tZ/DZ1Qf2tGpH9l6UFur/OOkzZ8qD33sregNfzHftV/8FRvjh8dHn8O/DIyeC/Dc4MZW2l3ahdKeP9IuVwVz3ih2jsS3WvHPAn7JfjVvAMvxY+Mt2ngfwtEgm+1X6k3t0W5Vba04dnkP3S5XPUZFfcZZwYlrXPy/O/ES3u0D6V/ad/4K9/tBfFCWa3+H0UfhWzfI853F9qDA9zLIoiQ/7keR2Nfk/qnjvxb4314an4qvr3XdSvZFRGuHkuppJHICpGMlix6KqjrwK9W8M/Bnxv8AtIfFyx+Dn7NGhXmr6pq0m2ztZXXzBCmN91eSgCOCFB80rnCRjjLHGf7G/wDgnB/wTA+B37DNpb+M9TNv4x+KLp/pPiGaIG3sCww9vpETj90g6G5YedJ/sL8lenmOOwmWwtBanFlOW4rM3zTeh+TX7Cn/AAb9/HH46zWXxC/a+vLn4b+GrhVli0WBUfxBeRnkeYrhotPQ46SK8o/55Jwa/rP/AGc/2Fv2a/2RvCh8K/s3+D7HwykqAXNzEpmv7vA63N7Lunl+hbaP4VHSvZPBl6s8u/JLN1J5JJ6mvTfEnjXwt4C0kXfiS5CPKv7qFMGR8ei9QPfivzbNOIcRinvZH6plnD2GwkLJHkGq+FYrVWYLnsRjNY1l8OdW1wlYVSBT0eU7R+Q5r5n+PH7c/wAMvhP4VufHfxT1q08MaFESPMmfG88YjUD55nP9yJSfav54f2jf+Djf4gSm68KfsbeH4bGLlV8R67HumI6brbTw3lr7NOze8YrHLcgxWI2RGYcR4TDLVn9ZWqfAX4daXo8mv+PtV3WlsheZ2kS0t41HXfIx4A9SwFfmv8R/+Cof/BJH9nC8l05fG2halqcBKmHQYJNducjsZbZZowf96Va/jK8W+I/2+/8AgohqEmseOdR8TfEdVfGbuQxaTA3UhEPlWMOPRErz34ufsOftC/s9eC7P4heNbKybTLmb7NKdPnFz9jkb7iXG1cKr9FK5XPBYHAr7XB8GU0/3svuPi8dx7Nr9zGx/UV43/wCDmP8AZy0maWx+Fnw98V+IQo+WS8az0mBvTjzLiQD0ygNfJni//g5d+LmsBv8AhB/g9odomcA6jq9zdN+IgggH61+bH7Gf7Hf7J/xx+Gs3jvx/4nuzrmmyGPVNKvL630u3g3H91LG/DSxOAMMGGGBVgOM9H8dPg1/wTp8P+FrjSfB3iKPSdctVbyH0iW41bzJFAxHOGMkRRuhKvGR6nGK9WGQ4KEuTlPn63FWMnDmUz1XxN/wcL/tnatLtt/BHgqFckhfJ1FzjtybsfyrkIv8Agu7+1VfTAar4F8JTKOvlfb4j79bhsV+cHwy8RfC7wtFc6b8S/BNr4rWdd0Di7nsrqGTj+KE7Hjx2Kbh2btXd+HfgN8QfjjjXvgZ8Mr2203zWj821lnuody4+Qz3DLGCo6jj6V2LJ8Mvs6HmR4jxT0T1P0y0P/gtj4pmg2+M/hlatn7x07VZI/lH+xNA4/Wu+tf8Agpx+yL8QkMfxA0DU9AkI5aazhu4x/wBtbZ/Nx7+XXwFF/wAE1v2r7rQ7nUF0/S0vY0EkOltqEX2247bYVAMRcf3TID2ANfBOsaNqWj6rc+GvEFpPYajZyGG4trlGjmikHBRkYAg+xFEMjwNbSDOn+3sxoK89j+ijRPGH7J3xcG74U+O9NS8b7lpdS/Z3J9FS5EMme3y5+lfC/wC1D/wT/wDh745nm1fxP4f+xX8wz/a+lYilbvuYgeXJn/prGTj+Kvyvg/s63Bivk3xjhlBAb8j/ACr6K+CeqfF2bUI9K/Z88aTR30p2po0s5hMhH8K28+63l9MLyfauLF8IQj/CkethfEGpD+NHQ+CvjN+wl8VPhrO+qeDT/wAJRpcfzZgTZeRr/tW/O/HrEW+gr4xKFXMbg70O1gQQVI6gjtj0r+kTWvjV8VPCdwNH/aQ8Ey2lxnH262jazkyOMlD+5kP+4Vryr4j/AAH+An7SFq+rRObfVXQbdQtoxDeKB08+JvlmA4HPPowr5/EZZVo7o+wy3irB4vSEkfgsYlK4x9OKhaKPr6fpX058bP2XPiB8ES2oatEL/R2bZFqdqCYc9llX70T+zfLngMa+ZpAsS5kIwfTH5VxUmuh9By8utyBtnbGKrvhceSOfSpFMRO1evT2qykG0lmOOKqTtsV7S2pmS7TH844H9KdZyCVWhk9vyqZ7O6upRHChYHv0H510eh6Hb28olvD5oHPXCCvTwuTVcRa+iOWvi1bQrwaTc3/FvGXGD82MAVZsvCkEFz5l8d/qBwoH1r9dP2Fv+CTv7bf8AwUJvLab9n/wg9v4UZwsvinWd9josQ4yYpChe7Zf7tskuDwxUc1/Yt+xT/wAGwn7FH7O15Z+NP2lpJPjN4qgKSbNUj+z6FbuvOItMVmEwB73UkoPZF6V6OIxGX4FWvzSMqGHrVddkfxFfsgf8E7f2uP23rxNI/ZX8Aah4jsg22XVtos9GgI/566hPsgLDn5Iy8h7Ia/p8/ZH/AODTDw5a/ZvEX7dPxBm1OUYaTw74QBtbQEfwS6jOn2iUdj5UVufRq/tb8P8Ah/w/4U0G18O+GbK307TrKNYbe1tY1hgijUYVI40AVVHQAACvz5/aX/bd074b/Db4u6t8CvDl98QvF3wo0j7bLollHIv2y8cN5VhFJHHK7Skqdwjicr0xnivmMx4yrztCFopnqUMohFXO1/ZH/YL/AGNv2ItH/sb9mf4faL4Q/d4lvLeESXsy9/PvZi9zKP8AflPHoK+f/jz/AMFtP2Bvgv8AGDRf2cfDXiY/ET4j6/q1rotr4e8JhNRlS7u5VhRbm5VltINpOXR5vMCg/uziv5Pf2mdT/wCCjv7WqeHvEX/BZ745wfsofDHx5era6L4D0mC4k1PUEaSNMPp1oXm8pDIgkm1O4ZY9wJt1yFr+rH9g3/gjp/wTq/4J5TaXqnwf8JWt74xi3RW/ibX5EvtWeTYd/wBmZlSK2OzO5bSKIbcgg149aP2qsrs6qVl7qP1f1u9sNMsp9Tv5Ut4II2kkkkYIiIgyzMxwAoXkk8Ada/GHW/8AgsN4N+J2tXfgz/gn38NvFP7Qmp2kzW0mp6DCmneFopkOGWTxDqLQ2bY/6dftHHSvdv8AgtHJcw/8EvfjF9mkaNJdGjiuthKl7OW7t47uMkchZLdpEb/ZJr7+8O+EfC3gvw/YeGPBthb6XpNhClvZ2dpEkNvBDGNqRxRoAqIq4CqAABxXlVIqKudNj8oP2Iv25v2t/iR+2l8QP2O/2yfBPh7wbreg+F9I8X6RD4ev59SAsNQuJ7SSC6uZo4UlmikiXLQxInJA3ABq/aRCNvFfhJqVv/wjH/BwNp142Ej8W/Ae4hjPA3SaR4ijcj8Eua/daDaYx7impK6YkfJv7e/xl8Qfs8fsXfFT43+FI5pNW8L+FtU1DTxbxmV/tkVs/wBnIRQchZdrHjoD2Ff5Jfwx/ZX/AGtv2ptXlh+CfgDxR4+1C8kMt3c6dp1zcrJcSndJLPdlRCrOxLMzyDnnNf7Nu1W4YZ7UyO2ghiEEKKiAYCqAAB9BX0uTZ7LBKXJFNs5MVg1Vtc/gF/4JP/8ABA7/AIKH+D/E9/a/teaR4e0H4Q+NrUWni7wZq15/aN5qkKZNtJEliXis76zkxJa3S3KyxHK4Kkiv1m+Dv/BqB/wTp8J6rNqHxC1vxp4uh852gtLnUYrGCOEn5Ij9hghmcqMAv5o3dcCv6hPsUSHKgDHcDpUnmKpx+VcdXiTEyk2na4U8BTXQ/jm/4Kv/APBGX/gmt8IPDnwt+AH7K3gq70D4xfFnxHB4d8Mta6tezokEe2bU9T1CC8kuVmtrC2G9wojcs6AOBnH4sftzf8G2P/BQf9mAXPij4WWVt8X/AAxb5f7R4dRodWjjH8UukSlnc45xay3B/wBkV/Vz4seH4pf8HMnhXSdXYtafCv4IXmr2asflhvdX1Q2ksgHQFrdwpPoBX7qeIvGXg20O24vovMHZPnPT/ZyK9HBcT4vD6XuiKuXUpdD/ABMfFvwug1S5u9O1a2k0/VLV2hkE8TQzRSIcNHNE4VkZehDAEV8ka3ot3oOpy6XejEkJxx09iPwr/SE/4Ohf2Zf2evEfwQ079srwTZ29h8QNG1Gy07VbmKIRNqelXhaGMXPTzJYJhH5Lt8yxl15G3H+fF8cbaHzrK/Xh23xH3C4I/nX0GbUaOMwf1yEbSR52FlKnV9k3oeC7mpHbKYxThwfakAwcN+Ffm56owKAME1DsAbHarLqvmbfSoZCuacGaRZE4Haos8VK44qGti4CDAB3V+sn/AAQvO3/grf8AAHH/AEONiP8Ax2SvycNfrF/wQwJj/wCCtvwAfr/xWVh/J6DQ/9L+Ag5Jqdenp6VGQAMinD5QO1BnMmVB3qbaQuTwKhTjj1qZS7krWMtzKdwBIO2rMUWXw3OKhTg5xVqEqBjvXTGyRhJ9idOFy2KkXbMNqdup/pSfIpAxnNHlHG0dMjP4V0U49WSl1J1Vz93HH+fSrABIHPXFR42YLngjjHoatKsa8juK6kuxoJDy3occ47VM8bsev5VIkfybsY9qEWVOSOv8qW7MZr3rIcv+t8s9R/L0q7EEUFE5poiw4kIHzCr0UWBngjHT06VtTNb6WJ4I5MCNfr+FLznjgVLGhj5PccVMFVPlf8P8itItW1ESIxVQF7VLtygHSmxho0+bvU8Ub5yemKtSikJtIlJEKgAdeKsoy8Z6cYpI42HLjPH/AOqrQhIIJHGOKwlPndkTzdiZUXDMw7U+J9xBkpiKzDb+P9KtbY3jG35enau+m3yjSEQDcSozx0p43vMnfFQJ877B19a1bSLKHaenpWMoa6GEl0Z3mieIZrdfKvWZlGAHH3h7H1FfWXwN/aj+Jf7Puq/a/h/erPp07B7vSrjd9iuuOrKCDHJjpJHtce44r4jV1jOAORirceo3EDZXgHqvYivrMuz5+z9hildHm4nLV8dLQ/p4+Ff7fvwF+ImkwT69rMHh29JCy2Grt5Txuf8Anlc7fJlj7Ako3qoxX3FpB0zxDbQ3+kzJPDMN0boyyJIPVJEJVh7g1/Gxp+oC5XbE5DYxs6n/AOuK+mfgb+0f8Xf2drxJfh/qTLZbt0+mz5ksp/XdFn5GP9+Mq3v2rtq8MUq8PaYZnn/XnTlaaP6sRHLBG0Y75BU/d/Kvo74S/twfH74BQppnhjVze6MnytpOoA3VmVxgqoJEkQI4xG6rjsa/I79nD9v34W/HVYfDPiFk8PeJJAFFhcODFKf+nW4OA+e0b7ZPTdX2FdLBdTHyMjbwQe2K+IxGVSpScaisevHFae4ezfFv9kz/AIJD/wDBQtpL74j+FT8BviHf7v8Aif8Ahfy7awmlbo9xCE+xsGbG4zW8b/8ATxmvyL/ah/4Ntv27P2frR/HnwBFl8a/CQHnwXfh0+TqqxDozaazt5p9DZzzk9lAxX3tNpsjPmElT6E459q+ovgR+1H8b/wBnC7E3w21iW1ty26TTpv3tlL67oHOAT/eTa3vWmHzDFYb4HdFwVKppNWP5TfhJ+1/+0D+zb4rfwX4k+1XsOlzbL3QNfSaG5typyyb5AtzbSegYFR/dNf0y/ssf8FmP2JvFWg23gs2P/Csdcl2oLTV3VrKaQ8Bv7UQBHOen2hYeOK/S7x58Wf8Agmr/AMFItCg8H/8ABQj4cadZ65GnlW2vKGDw5BwYNSt9l5ajPOx2MX94npX4u/tj/wDBrj47ttOn+Iv/AATp+INp430KdTLb6D4gmhhuGQjhbXVIF+y3GR0E0cPvITXpU8dgMXpiIckivY1aa/dSuj0j9tH/AIKx+Dvh3LN4J+Ct3a+MfFygxyX6sJdI05iP+WZQlLmQdljPlL/Ezfdr8HPB/wANf2kP22vireeIvNude1GZwdQ1jUXIt7dewklxtRVH3IYxnAwinpXw98Xfg1+0Z+yR44Hw5+PfhXV/A2sdEstUtmhjnCnkwSH9xcJnA3QOykdGr9bfgr/wVq8P+DPhlF4I8c+CLfTpdLg22B0ICGylcDC+fATmMseXkVnJ/uivvspyrD06V6Fmfi/GkMz1lTjzP8j7E034V/s1/sDeF7Xxx44I8WeL5DssDIgLyzjjbZW5yIYxlc3DhnHG3BISvgf4g+Lf2i/20fjvpnwxhtZLzxDqd8bLS9Gifbb2kj8uWJyEESKXuZ35VVJY8YHO/wDC6Y/F+l6j+074o1y11fxdeymy0W2ikVhpyIMvdGLOYRCpxbqw+8d/Lc1+0H/BMn4A2fwH+Da/HzxfDjx18Q7XfaeYP3un+HpDuj68rNqLASuev2cRDOHYVx5tmv1ak5y36HhcHcK1MRikq+r6/wDAP00/Yw/Zf+EX7D3wtfwH4EePVPEmqKjeIvEWzZLqE6ciKDPzQ2MR4iiGN333y54+5fDWuxuRyPavh/RfEjXMiqzDjGK+jdCi1O08NP4ikBQS5jt/9ojhmGOy9Pc8V+IYmvUxVXmluf0zhqFLC0rR0SPetZ/aDt/AYOlaLtuNWxjn7kOcYz/eb0FfiP8Atuf8FS9H+Dmr3/hTwtKvi7x42VnjaQ/Y9PYjg3UkZ+Zx2toyCP4mTofib/gob/wUHvPB2vX/AMB/2ftQA1iItDrmvQPlrNj961tXBI8/H+tlH+q+6nzcr+b/AOzF8BIvi38efBnwp8ctd6RY+Jb2BJ5tpW4MFwhlV08wHmUAFZGB4bdyK/RuG+E48nta2x+TcZcd8l6VBnhXxh8f/Fj9oj4hjxt8Z9dm1O9lbZ9pus+RaRE8rBbxjEcYHRI1BPuea1fEvhD4KWVvpmlfDS+1fU74bxqV3fwxW1vLkLsFtbozyKBzkyNk8cCv6M/+GRP2LPhzqVxomlfD241240+R4Gn1WeWcM0ZxnBlSMjjtGPpXsvh/wf8ADbxZptz8Fx4L0jwvoniq3l0p5rO3t0khe4QpBJlIgfkl2HO7tX21CklrBaH4Ti+MqblySlqfm/8ABj9oX9trx58LNO+G/wAD/AUOutokEdgdTt7KWUDy1zGJAHS2jk2cnpnGSOtdLrv7I/8AwVA+M+jzaH8Y/EVj4a0S++S5tL28ggiZQQdrw2aSZAwMbm6gV73/AMEpdY1LwD8ePEn7L3jOWSwTxda3Nh5StsMOtaXvKbcYwzxiaPd6hRzxX6s337PdiZpHvy07oSuZdzcjj+I9a+Xz3Olg63uxP1Dg/IlmWH53Pbofy5ftI/sKeO/2YotJufFUtlrmla1D/oWraeGNsZ4/9ZbNuG5XAwQTwy8rnBA/VD9lv/gn5+wf8UvhXpPxb8N6XqHiY3a+Xcw6teNm1vYgBPbSQWqwp8hwy7shkKkdeP1duv2f/AnxL+FuqfAT4jRk6BrK/uZABv0+7HMN1D6FG59CMjoTX4KfBH4keOP+Cbf7VmsfCv4uRs3h25nSy1+NFJjaEf8AHrq1suAG2K27A+/EWTqoxMM2eNwzVJ2kgxOULKcdH26vTkfqR44/YU/Zy8ZfDe6+GU/g3TNN0ufDI2l2sVtdW0w4SeGcDeWT+65KuOGGK/GzVPhx+0P/AMEyfilFLZsNe8Iay2ElwyWGsW8Y5WRRn7LeRjt95T03pX9WWn6daX9nDeWc0dzbzRrNDLCd0ckTgMjoV4ZWXBHtWD45+Fvgn4n+ENQ8AfEHTE1TRNUQLd2r8ZK/cljfrHLGeY3XlT7cV81l3EE6NT2WI1R+hZtwjSr0ViMFo1sflPpmueDPjB4Bi+KHwzma40y4YJPE+FuLG4Ayba5RejKPuv8AddeQcV85fGn4DfDj9ou2XTfioj22qWiiOw8RWyD7fYqv3VkHH2mEED9253L/AAMprgvi/wDCr4w/8E2/i5H4n8FynXvBusE28TzfLBqNsvzNZXoTiO7jzlGH++ny7lr7h8E3fgP4u+C4vir8Prxf7FkOyf7SyRNYTj79tdZICsnY52uuCOK9DFYKdFqvhHozycuzujiYvB49JSifhh8RPDNp8IPF0Hwb/br8PWes6Pqa79F8b2EZEksIwqyNcQBJJEXgOHzLCcb0dcVxHxc/4Jt+JdG09PFP7P2sL4gtpFW5t7Cd0S7eNuY3tLmPENwCBlceW3oGPFfrb8b/AItfsbXHgy/+FXxj1u38T6NfN5kmnaQpu7m3uQMJd2k6fuoZ4/8AroAw+V1ZSRX5JfCL9ovxt+z/AGupeB/CATxL4TmklbT7TWlaNoGY/JcRiCTMTsMebErmNjzjPNfS4KWJrQU1oz5HHVsHh6jot3j5CfAb/gof8WPhM7fCL9pPRj4z0O1P2W4s9YTbqVmFwCgeZfnCjokyn0BWv1J8Mfs1fsR/te+F38Yfs56m2gaqi+ZNa2/7uW2c/wDPayckhf8AahOz0Nfln4v0j9q39uO+tL7TfByav/ZjGKO90zTlt1jAAzDLfyH5lUc7JJTjsBWB42/Z6/aq/Y0uNM+KGq28mlJE48nVtIuhOLKY4xHNJCT5ROcfP8j9AT0r6LD1oL91Vtc+CzThv2r+s4BuD8tvuPrX4yfs2fHH4EW083iizTX9E2mM39snnIY+hWePGQMHlXXHbdX4f/Hj9kjQvE8k3iX4EKtleudz6K/yxSZ6m1kf7jn/AJ4scdlI6V/RX8Fv+Ct/w9/4RKTRP2uJv7JvI4XMes2cHmpelFz5ctpGCRMw4DIPLY9dnWvwY/bW/bm8EfFfxlcTfs5+F/8AhENOLOZr+Uhbq5B/iNuhMNv9V3P79q8bOuFqMvfpaH3Xh7xJnHP9WxsLxXU/J46RrelaxJo2q2ktreWzbJobhDE8bDsysBjFejafpFv5X2i5PmKoyeQEX69q+8/2Jf8AgmD+3V/wUo8TDWPgb4ZuZ9DmmAu/F2uySWukR4xk/aXUvduo/gtkkPrtHNf3Q/8ABPP/AINqv2J/2W4bDxz+0Ov/AAuTxrbbJRJq8Aj0W1kXn/RtLyySYP8AFdNMehUJ0r5t4rBYFWfvSP2qNCrX8j+Ij9jD/gk3+3B/wUDv7e6/Z88HSp4ZdwsnifWN2n6HEvGSk7IXuiP7trHIR0bbX9mn7AX/AAbI/safsyzWHj39pqT/AIXH4utisqx6jCINAtZFwf3Om5cTbT0a6eXPUIlf09SQaL4f0XYkcVnY2EXCqFjiiijXsBhVVVHsABX8s3iv/g4z+G3x/wDiL8Sf2d/2GNCu73VND8DeJ/EGheLdVjEdhd6joVm1ykdvYMBLNA/lviR2jyV/1ZXmvm8ZnmLxT5aeiPUo4CnTWp/Rj8Xvi/4K/Zq+C+p/EvV7GU6L4ZtVb7Jp0K5EalY0jiiG1VUEgdlA9hX5P/GH/gtV4LtYlj+BHg+98RSR+X9pub5jaWsTP0jG1XkY5+UbhGCemRUX/BH/AONeo/8ABRr/AIJNeDPGP7Sd2/inU/E1vqel+JJpCIXuZYL+eI58nYE+RY8bAoC4xjFaX7c3w/8AAemeOfgh+x38KtGtdE0zXNdTUbuzsoljXybZljDuFALkI0zFmOflr804jqYuj8L0PostjSk7TRifEn9u34wfszftheING8cX0viLwldW1tcR6XtjR7Bbm3WSJYmVV+aOTKtvPzp74qX4b/tUfs0/8E6/2Fbn9sT9qjxL5P8Awn2tTXlxLYxve3dzfTiQw2cUcWSZFjjd23bUQltzKOa9d+BPwHuPjf8AtA/Hzxh8bfDs48OeIrqHQNOS9jaEXFtZfKZ4Cfm2qYo2jkXA3cqeK5z43fsw/wDBOH9g/wDZNufiT+2xFH4u8E+CNdHieD+37db0JqtxGLK2S2sI0Ec8rhgiI6MNxLnGMrx5Bh8RUrqdXWJrjKtJQ5YaH88vxe/bk/bj/wCC0XxS8OeKf+Cd37LGnQWHg6SdNC+JHj+zt7z7D57Rs8tqbsHTIpMxq2FXUZUZQUVWr9gf+CcH/BGv45/Bj9pLT/25/wDgoJ8adU+MPxZ061ubfT7cyytpGkfbYzFM1v5+GdvKZkXy4baJQzfuidrDv/23f+Cltt4j/wCCI3jH/goH/wAE3r3b9m0+OHTJZ7IRzaUq38VjeFrNgyJLZoXZVYNGMBsMmM/Mn/Brb+1v+1r+1r+yn4/8RftR+JdQ8ZjQvFpstI1nUyHuJY3tIpri3Mm1fMWGVht4+XftBwoA/RK7n7J8qtY8CEdT9kP+Csfha58c/wDBMr47+H7NN87eBtanjX1e2tXnXH4x8VgfsTfBfxe/jXxV+2zrfj++8T6V8a/D/hW90jQbiMrb6Fa2unb/AC7dvMKOJ3uGkJSKLn7248190/FDwZafEr4ZeIfhzeKDB4g0u80yQN023cDwnPth6/GT/glt+3T+z98IP+CSvwk1v9qTx1ong658K6fP4Pu49VvYoZmu/DdzJpjxRRM3mzSbIEby40ZsMOK8qGsLHRY4/wDb78Qf8KO/4K0fsd/HnUoX/svxNN4p+G15MvASfWbaC405WHcNcQEfQH0r+gKylVrdQMV/Kr+1Z+2f4D/4Kr/tB/B39nH9ifw5q3iSy8A/EfQPHWveNrm3ex03SLLQ3eaXCTBZy9xGzRxiRIS5IEayDJX+i+/+NGlwQtHosBuCCcMx2L/Un8hWc4e6ogfRiMjfcPTisXV/E+gaEP8Aia3kUB7Bj834KOf0r5A1D4m+KdXzGbloY8f6uH92v5j5v1rjmlLHJH498/Wt72Vhn0j4h+OGh2S7dJt5rv0Y/ul9Op5/SvG9W+M3i/UT5dmI7NegMa7mx9W/wrjnjlmzmuD8XeKPDvgew/trxNcpa2wOAW5Zj6IvVj6YFZqnd6Bey1PxJ+JHxNuPhT/wco+CtQ8YzMtl8XvhA/h6wuJWwsl9aXU1wIQRxlmtAqr6yKMciv2d8Z/F/RdGjbTPDJjv74DBZT/o8JGPvMD8zD+6PocV+Df/AAVo+D+pft5+DPDviH4L/wDFOfED4ZXjat4Q1NpBFcPMSjyWzy/dhErRRyROciOaNC3yFxXxN4J/4LlWHw/+Cer6b+0Z4KvNP+MmgoLYaQsTQWWo3mdhmmLENZ4IDyoA6kH9w7Ajb9NgMoniEuRHmYnFqJQ/4OE/2mbdvAPhr9luzvvtOsa3fx+JtcwfmitbQPHZowH3fNldnVeywg4wwr+LT4x6ol1rUGmL/wAsELOPRn/+sBX3H+0D8dfGnxX8Z+IPjp8X9ROoa5rk/wBpuZSAoLkBY4Yk/ghjRQkSDhEUV+Zmo3txquoS6hcHLysWP49B+HSvqOI1HBYOOFT1Z5mX3nUdVlBVORTpY+cjj0qeKMkY/SkmjCjOK/N4x01PZ5tSswDjI4xUexRyBUqlgCp70w7gcVm00aIhGKgcZO01Lt2nPbpTWFa3RcdCM1+sP/BDUBv+CtPwAXp/xWdh/J6/KALtJWv1a/4Ic7l/4K0/ADHT/hM9P/8AZqGa3P/T/gOAHU1INpGOuKTkDtxT0wB0xmolsYyYqJhsn0p/A6UoX5uenSpAFLY6VEVdmTkSIr9gKsKn71e30pI0KncTxVlVTcT+VdvKrGLGbm3ZxwKmi37N5xz29qaQGTip1wEQKOBXTfRAtiU7VBZRk4x0q15e3AX2qKPkkDoOTVqJNzBlHBHT2qnK2iInUsSAHPlEYJ/lU67jhf7opkXzjAHsO1TwbcsjfePFa0+5SS3HJ935V5fjp27VcXLr5ceB+XapECxAlwDx0HFSxgNFkdD0NV9m4Jlm3x5mGAwP0pww3zHofShFKKSev9KnigdiFjUk+mK0pxu/dG5JbhCUdsnjAxitAqdoAP0+lWLfRdVnIEVu5HXJXA/XFao8P6qV3uqR+xYV0f2ViZu6gcNXEQvuYRJPCdRxV4HIVR97jNbFj4Y1GZ/9YoGOm0/4Vpah4cvtHRZrpRtbHK8//qrq/sfE0o8/KWsXHYxmAVMv6f5FK5ZSqEccYNIyunD8dOP5VKFO/wDedsD8PwrKLutToVRDFhLuu0cjtW3FGYoMtweP/wBVVLVCrAsQM1pN06/do5dTCpdvQhSLy9zSnjHr7VEQztl+AMcGrDSZYg8Yx+VNjbyz7dR+FKSuJXL1iJI3SZTjHQ9x+Vdlaa4g/d35xxw/b8fSuXsohKykqdpxwPwr+j7/AIIc/wDBFa7/AG7vE8X7Sn7RtlLa/Bnw7deWlu+UPiS/hPzWsRwD9giIxcyKRvYeSp++y64XO54KXNF/Izr5fGtufz6m6tLmAy27LNG/ORyOPp6V+hf7M/8AwUL+InwpWDwv8Tkm8VaBGAkcjuP7QtYxwFikY4lQdklOR2YdK/Ur/g5I/wCGC9K+O+h+Av2ePDNppPxL0WNU8U3mirFa6YlosYW2s7i2hXy5L1RtYMgRoodqSFyVCfn9+zD/AME8D4i0K1+I3x+Sa3s7kLNZaEhMcs0ZGUku3G1o1PG2FcORyxX7tfeLG08Rh1UrxsfPOl7OfLBn0Iv/AAU/0bxFejR/hH4C1fxDdZ4WQhDjjrHarcN+eK6KL9oD/goP4yjafw38L7PR7Y8g3qbCqqM5b7TcxcAck7AABX1HLr/wg/Z18CK+rS6b4R0S3XEUSKsO7HaKCMb5m7fKrH8K/JX9ov8Abg8R/Ha/Hwm+Gkg8O+GNQmS1mub2XyJLxJGChrtxkQWw6sgJJA+ckfLXHg8BGb92noXVq26n1h+yJ+098dPj/wDE3WdC8Xf2cdE0ayeS5ks7fy83LuI4VSUMwIba7cHBVeOK/Wf4OftCfGf4A6v/AGt8LNdudKVnDTWoIktZj6SW8mYmz0yAG9CK+Wf2evgN4N/Z++Htt4E8LSLeySlbq9v1wft07KB5yEEjytuFiAOAgGOcmven0+L5sjdXyuc4ejOq+VWSO/D1JRR+wPg3/goX+zz+0t4QPwe/bu8C6ZqekXi7JpHtBqOmsTwGks5Q8sJHXdGXI6jGK+K/2mv+DYz9j39o/wANz/FX/gnN4+XwbLcKWi0yeU6voLtj/VrJuN5accEF5gnQRDpXyVDp6wv5kfB6A+leofD34tfEn4O62fFHw21q60a/4BmtWI8wDoJUOY5F9nVhXj4epicPK9CR3RqU5r96j+Yv9sT/AIJh/t4/sDatc3P7QHgS9s9FgcxjxLpBOoaPJHnAZruFcRBv7l0kJ9q+rPgX/wAFifjBo8dta/H20i8Y2IWNP7QtvLs79Io0CIMIBby7VUADbGcDG6v7JPgJ/wAFZBfIPDP7TOircQSJ5cmp6agbcrcf6RZMeQR94xkj0jrgv2k/+CHv/BJ7/govol18TvgC8PgDxJcZZ9W8GeVBB5rY/wCP7SHHkZz97EcEp/v19DDiinWj7LHQMllcVLnw+h8F/sO/tMfA39s34maH8OPhj4lgTUtVkxJYX2LS9hiQF5CIJCPNIVcDyi4JwM175/wWj/a+T9lv4bWHwY+FUv2Hxb4hga2szGw8zS9NhPlSXYA/5aO2Y4D/AH979UxX8+37ZP8Awbvf8FFP2TRN4z8AabH8XPC1i3nR6l4WEg1OAIcq8mlNm4Vh1/0VrjHcivyG8R/H/wCLninxK8/xR1zVNd1axij06Q67LNPeQRWo2x2zPOTKnljhUb7vPAr1Mk4dwVSuq1Gaa7HjcR4rF/VnTitT9Tf2If2T5PjBrbfELxrblvDekzbRG+T9tuRhthz1jXgynPzH5fp+qfxk0uPwn/wVH8D3EOEVX8Kk8AAK0EUOAAAAB0GB0rwn9kP/AIKRfsc674b0T4XX/wDxby6s4I7WO21JlaybaOWS9UKvzNliZVj5PU19GftkXmiyf8FEvBXiDw/cwXlpPa+GLiKaCRZInVZsbkdCVI47cYr7Cv7vux2P5NzH+0Hi5/WYWj0P0O8feHWi8da7bhc4v5CBjpuwf61xeo6NeW9obq0GyWLEqEcYZCGB/MV9+eOPgbqVx4v1TxLqV3ZabY3M29ZLl9mBtVTnOAOR614B4r1j9m7waPL8VeP7K4ZR80VkVlbjtiESkHH0rkw2NtHksfnGOymqq3tLn5v/ALZnhfW/gx+1bpH7Q3gJBG2tx2PiyyZOAL63K/aU/wCBOm5vaWv6JrefRfiDo+n/ABD8NYbTfEFlBqdrj/nndRiQA+65wfcV+I/7V/xy+BHxh+Fvhzwb4CkvrnVPDd232aea2McJtZk2yoXkYN1VNvyfw9s1kfDj/goZ8XfgX8GNK+Enhqw0iVNGWWK0v9QEssghklMixiJXjT92W2rknjAxxXzuf5JUxtNOG6P3Lw74/o5VWlCtrFpH7Yf2ErSFApbBxhRX5xf8FS/2YND+LvwZg+KzPb2Pi7wdCdjzskJv9N4MtoA5G6SL/WQ9f4lH3hXxiPjV/wAFA/2jZfL8L3XiW9tpuNuiWbada89jNEkQxj1mrsfC3/BMj9qLxheLrPxDgsdHLkM1xq98by4B/wB2Lzj+bivPyjh36nNVJ1D6fifxJWaUnh6NH0Jv+Cfn7c3hD4PfCaf4OfHue6+yaDGJPDtxBA1zK9u7EvYFF4HlMd0TMQNhK5G1a9b+If8AwVS0u0EsXwy8Hfd6XWuXaxenW3tRIfp+9FfFH7Xv7HvjD9mG60y9Oox61o+sRnytQhhMMcd4vLwMjFiOMMjZG4Z6Yr9Jf2ZfBX7I/iz4Cad8V/hR8PdKvdfjkFhqaa5K939h1BFywdphN+7cbZI2SNcqR0INenmOAwMf9qcbo83hziTN6rWWqfLY/Jr4uftS/tSftd6bJ4BtLaTVtJuZI3k03QNJaSItE2UYy7ZpQVPfzF/LIr4r+KHwg8e/C3XIfBvxZ0i58NTXyRXXl3yNt8hztFwUTdvC4OQMsMYwDxX9aEvg74y6rbJaa14ptdAs48YsvDFiluq47C5ufNbt1RI68c/aT/ZI0L9of4LD4YzXU/8AbWmmS50HVdQla4miu2+9DPK3zG3nACuOinawHGK5sHxZQ51RirI+izLw7xrg8VKd5H48aZ+wT+zt4Q0m0174ieL9U8VrNDHcRweHrVbW1mikXcjLPJ5rFGHcbD9DxXo2meB/2QrHT7nwTb/CeCHRNUjNteX0s0lzrNujDAntppGcJJHgEYwDjB4rxT4G/tc/DL9ki01v4H/tp6k3hWDw95slgksTz3cNyjZmsI4I1Z5ElJ3wkDywc/MqsCPgf9qD/guX4o8ZpceFP2O/Clt4MsPu/wBv6pDFdavMp/iS3O+1tQeo3ee47Mtb1MLmFavy0nofQcO5XgZ4bmnDU+tfDnxgX/glx8ZLj4ZfG3UJL/4aeLIRf213bqTJJCQRb6jbQD5vOGPKuIR/7Kpr8+/2rv8AgtV4r8Xy6t4E/ZV0FPD2h6gklrcarrSRXV9cwSDa22zbzLa3Vgc5czMOxU18tfsz/sXft2/8FOPiPdXvwZ0DVvG15cyY1HxLq0zpp9ueM/adSuPkO0ZxDDvkxwkZFf1z/sI/8Gtv7MnwMu7L4ifto3y/FnxRblZRpe1rfw3ayDHHkH97fFTj5rgiNu8Fdea47A4SSqVZXqLsfSZJkMoQdOPwH8h37Ev/AATk/bY/4KK66ifs6+ErrVtM8wRXXiXU2a00a2xjO+9kUiVl7xWyySY/gxX9l/7DX/Brv+yT+zw9j8Q/2tbgfGHxdAVlFrdReR4etHGDiOwyTdEH+K6Z1bj9ylfvb8Sfj7+y5+xR8KIvEHxj8RaD8OvCOlItvbm5khsrVAvCw20K7d2OgiiQn/ZwK8l/Zd/4KFfCv9sv4xfGL4GfC3TdQtbn4PahaaXfX12sSwXkt2kxD2qqzN5aGEjLhS3BAxXwed8WYzFQbjpE+1wOU0KWiR6PbftDfsv+BfhePGtp4i0fT/CemyTafA8Dxx26SWbGKS3t4kA3GMgqEiU+wxXiH/DxDwC3xk+HPgTwzZNfeGfiLBI1l4g8zy41nR2hFv5DIHDiVVRgxXG9eK/LD4r/APBMjQ/2f/2evGHxr+NviP8AtvVtMtpm02z07NvaRXV3MFidnfLyHdIGKKEX6isP47n4Z/Cn9h34N+ArvUyvxNsZrfxDpWn2wM10Pt8jXD+Yq/6pPmQrxl3QBQecfimMz3FQm7rY+yw+XUWlZlv/AIK+/tfeKvg34A/aN+LOk6vcJHonh+z+Hvh2280rCur+IwouZY4wQvnQ2q3D78EjaK/nF/Z8+Mv7Neo/t3/sW+Gv2ebHVU8NaT4fPwz13WtSsTYWOtahrYu49RlsmbmVEn1VwxbDAeWMBcE/0Y/Ez/gkh8dv+Ci1h8Ibv426nH4c8DSeJdR8d+PbC5R11HULqUxQWVhDbj5Y0a0SVXeRwYVnbajMAB+nfxs/a2/4JXfAP9q34V/safE//hH9P+JCBYvB1gNIWVNE+34jgWOdIDDppujEqRgNGzYXopUn9E4YxbjhVK15PU8jHQXPZbI/lR/4Jg/sNf8ABfqb9mub9jj4Z6tH+zp8K49e1G8ufEeqW7L4iuVnZIpI7CAN58cJ8rejj7KW3kiYjAr96fib8R/+Cd//AAQ++HHwn139r7xrrfirxfpekzeHNF1O7SbUtUu4zcSXV/qBtlZtiq90RLM7ErGUiQseD+W3/ByV/wAFUf2yv2M/2u/hn8Fv2afEs/hbRrHSLbxfqC2satLrU/8AaMlutlKxRs2wjgIaJdokMnzZ2qB75/wcE/8ABHz9qf8A4KgeKvhD8Yf2Yjp/2vTtOm0TWLDV7kWq2drfSR3CXi5Vt/kt5izIo8wjZsDYOPWxOHhXcZYjSLOWE+XSJ6B/wca/8FG/2jf2V/2Z/hTq/wCxt4ofw9F8SdQmlk8SWCRyTfYre1juYIrdpUdUFz5gcts3FIyowCa9u+OXwB/aI/4La/8ABBb4dxzXVlpXxN8SadoficG+DWtleXlocSeZ5aP5SXURaRCIyqsy/KF6fpXqn/BPH9nP4r/sm+Af2SP2l/Dtl8QvD/gXTtKtoBqSMA1zpVstslwuxg6F1DBlDYKMUbK5FfoD4b0TRvDWgWXhvw/axWNhYQpbW1vboscMMMShI440UBVRFAVVAAAGABXJDFUoJQorVBFNu7Pyj/4JWf8ABNM/sRf8E7LT9jz47S6f4uutZm1G98SWwTz9MkbVDiWzRJUXzYFiCo25BvO47QDgfoJ8Ifg/8KvgN4Hsfhj8FvDuneFfDumAi00zSreO1tYdxLHZFEFUEkkk4yScmuy8S/Efw7oUbwiQXU448qL1Hq3QV8n+JPiR4n16dozKbSDkCKAkZHu3U/oK4sRUlOTdzRJdD6R1z4neHtClNq0huJ1P+riwcN/tEcAfjX4kT/8ABIL/AIJwzfH/AMQ/tJ6l8O5NT1zxNfT6nc2d/qEz6XFc3beZcGO1h8ssksmZGimd4gSQqgYA+9rdvLjAP1/OteO4wMnoKVOPKrIdjP0Pw14V8DeFbfwR8PdH0/w3odrkw6dpNrFZWifSGFVX8cZ9arg9NwxjGK1GkLrg9Kzrn90y4+bd0FN9xEIdY32k/wCf0rSSSKGFrmRgkajczOQqqPVmPAr50+IHx98F+AblrBZP7S1NePsluQdvtJJ91B7dfavi3xv8ZvGfxCna38QXHkWAPy2NuSsI/wB/vIR6tx6AVqqcnsiHVij64+J37UGj6Ax0nwAiandD7122RbRnp8o4MhHthfc18MeK9d8R+MdQ/t3xLdyXt02Bvk7Z7Ko4VfQACljtnuSMADjjtgfyr5Y/a+/bC+Dv7G3w/XxB4/lGoa3qCP8A2ToFuy/a7904Jz/ywt1OBJcONo+6oZ/lr18Bl8qslGCPPxWItG7Jf2k/2mvhd+yd8L7r4rfFi7MVkmYbOzgIN1qF2VyltbIf4j/E33Y1+Z+OD/GN+0t+1f4+/al+Kd98ZvitKlqETybKyiObfTbJCWS2i7sQSS7nmRyT6AZ37VP7SvxV/ai+JFx8WvjRqC7oUMVnaQkrY6XaE5FvaoTkD+85zJIeWJ7fnl4r8WT+Irs29vlbKI/u17sRxub39q+8U4ZXSu/iPHUHXfkWviB40n8VaiRFlLOPPkx/+zH3P6dK88WIkjA4q5HG0h9xUoH7sKK/NsbjamJqOrVZ6tNRguWJR2sjlE5qspcHY/5dq05Iw6ZIxjpiqEuT83pxXL0N4SRVYEPhelR87+fSrbgMAU4qDbnkdqHE0UiCXBUAdaMfLz7UpGWxSdDilJXNFsV++K/Vv/gh1k/8FZ/2f/8Asc9Px/49X5Uyr8/HIxiv1b/4Iaru/wCCtnwAB7eMrD+T07G3of/U/gN6nFPlBVQVqMq56d6mUMVw3TtWTZlsP5K+uafyDkDvTeF4qwrZJUHBIxj8KqEepkyZJCy9ParUYd+B8vpmo4liReMHHNTcE/SuimmYPyLQ4AAqxGxWMMPp7VDEr4O4cCptrE4Xsc12ISfcnUkHGOKfsKoApx/hTgu5unFP2E49uKrciVnoizEXDeWvUjNS7g0gbHXFC/wsegGKuQ8vtGfX0rWJqklsTtDuX5Oo/wA9Kco2R7PcH+VSxrg5JJqYLvxs46UTleJL0LEZTHzc/wCcV6d8O7vbNPpkij51DoRjOR1rzWOGT+HgcVu6bfSaXfRXsXHlkEj27j8q9fIMXGjiYyexw4+DlTsj9EP2Vf2VdW/a2+Is3w60jxZoPg/7LDFPLe+IDdeR5ckgjyotIJj8pxuLbFGRzX9M3wR/4NJtJ8baBb+J/G/7RkN/azjP/FK6NE8B9dlxcXcgP/fofQV/Lf8As3/GBPgT8btF+JjpLc6em+C/ityFeWzukKuq7uNyna69BlBX9Hv7OX7fnhLw1ry3XwT8f3HhfVZm2/Y7pjYF2J4BSTNrNnjgF66vELNs3w9bnwlO9LyIyGhhakeWrK0j9K9K/wCDQD9jpdOXzPiz4+e9VSFnzpYi3evlCy6e278a/n7/AOCqf/BDP9oT/gmfaR/EcagnxA+GFzKkH/CRwW32aewnkO1IdTtQ0giV2+WO4RzEzYVvLZkU/wBfXwE/4K5eLNCitdE+PekJqiEDdqVltgnK/wB4wn90+f8AZZPpX6c6X+0V+yb+1b4Jv/h++q6Xren63aSWd/ouqBY2nt518uWGS3uMb0ZTggAj0r4rJvEaUZr2svkz6DG5CraL7j/HE8VaCdLn+0wLiHoUPVPp/s1zC5ZRjnIzxX9Cn/Baf/gkT4q/4Jw/FpPGPgFJtV+Dniu6dNDv5CZJNLuGBcaTevyTtUE20zH99GMH94jE/gbqmkNp85kgH7gnHTG0+n0r9DxeGpYml9cwm3ZHy0Jypy9lUMa2ibIcdAP8KviJX4HA9c1IwSNFVOc9+2KqkmJCNuN1eHBtnoxbaHn/AEhi69E459qqSOqgEdccfWtKBMqp7Yr0P4Q/BT4l/tBfFfQPgn8ILA6l4i8SXaWlnD0jVjy00zY+SGFAZJXPCoCazrVVFXZ0KKtY/Q//AII8/wDBNjxn/wAFM/2oLb4cn7RpngPQfKvvF2sxAAwWbE7LKBiMfa70qUiAyY0Dy4ITn+6H/grL+3L8Pv8Aglr+x/ofwB/Zc0+10nxfqdkmjeD9J09FK6TZRAQi6EXO51JEduG/1s53NuCvU37I/wAKfgB/wR5/YXi8I6G66g+mR/adTu0VYrnxBr1yu0t/s+YQEiXlYLdBn7rE/wA4/wCzVrfjH/gpp/wVm1H44fFeUano/wAN/wDibTDrbte27eRZQRqeFiimI8pf7lsxPzO5PBlWH9tN1p/DEzxlbkiqcN2fmt+0L/wTk/4KB/DP4pxeNdQ8E6t4suZxaakup6RCdV2XZVZJUuU+eTz4p9wlaSPEjKWGVIr0zSPhp/wW1+M876ZongvxvGH6yPptroqjPczzpb498OK/tSh04z6luc5yetfUvwj8KRa34htNNm5QEyyd8pHyQfTJ4r0lxzVS5ORabHOsjhuf5+P7U3/BGj/gol+zL8A3/a3/AGltO05NPEsUeoKdajvtTs/PkSKIy7vlk8yRwoWCSVh1KqATX5CXamIScZ3cAV/al/wdM/tMXcniz4b/ALH2hTgWlrBL4s1iCM8tM7PaacrgY4RFuXwfVT6V/NfJ+yvp3jH4Y2WuW87WWt3MZm3tnyZFY5SORcfLhQPmUfge361wpjqlbB89bqfmvE2cUcHiFTk9Dw79mj9tj4o/s53sehHOv+FVbD6VcSbPI/vNZS8+Q3+xgxMeq55r+hT4B/tFfDL4++HP+Eg+HOoC6SLAuraUCO8tCf4Z4MkhfSRcxt2bsP5W/Hvw88XfDbxJN4V8c6fNp9/Eqt5cq7co4DK68YZWGCpBxipvhz4r8Z/DbxPbeOPAmoz6Vqtkf3F1bvtkXPUc/KynoyMCpHUGvPx3D0K93TVme3g81TipJ6H9l0lpHLEJIhj+tZM0QTcAPavzS/Zf/wCCkPhH4hPaeCvjd5Hh3X5dscF+Ds068c8AOW4tJWPqfKPYrwtfS/xK/bG/Z0+EmpPp3jnxZZC+Q82Vift1wPZo7YOE/wCBFRXwWKymvTqezaPdhXTinE+m7Szwyvj3Hbn8Kvab4w8X+AfEkXibwTqNzpWp2/8Aq7m1kaKVQO29T8y+qtlT3FfmFf8A/BVHwBeXo0j4W+C9a8R3GcKjGOEn0xFELiT/AMdFeKfE/wD4KTfH7wPd2L+IPhF/Yy6uxGnxalJdRy3BQhSEBjjY4JC/cxkgVDySpJe8i44mzSif2Gfs7/8ABW3xv4Wjg0P4/aZ/b1sPvanYhIb5F6Zkt+IZvqhjPsa+mvjZ+x3/AMEq/wDgrvoT63440HSdd11Y9v8Aa+nE6X4is+OA8kfl3G1eMJMskX+yRX87em2WoXGh2smqQra3bwxPcQq24RSsgLxgjGQjZAOO1TWN/wCIvDesQa74fuprO9tGBgubaRop4iO6yIwZfw6189UwVSjLmpOx6MMcpe7NHkH7bP8Awak/tCfDi4u/Fn7DPjG3+IGlKSy6B4gMen6qq9liu0As7hgP+ei23pya/nO1fS/2p/2Mfisngb4r6JrXgPX7FlcabrFvJCriM5DRCQeXLHno8LMvcNX9737PP/BU34w+C5IPD3xijXxjpy/KbptttqUY/wB/5YZsccMEY/36/WyDX/2G/wDgoV8O5vhx4707RPG1hcLmbQ9etYmuIyRjcsE4LAjtLCeD91q+gy/jLE0bLEq6PPxvD+FxcXGx/AF8DP8Agor4N8b6/ZaN+0tfXOh28rAT6vFFLqcUY6b2t/MEoHrtL/Sv6LPhP+zD+xf8XPBMPjvwf8W5PGemOgJbQlgjCk/wyKfNkhfsVkVCPSuI/bN/4NTPgh40lu/GP7B/jCfwDqJy6eHdcMmoaOzdkiueb21XA6sblR0CgV/Lb+0F+xR/wUb/AOCYnjA+Kfih4V1zwYls22LxRocslxpUi9j9vtP3aBv+edwImxwUFfcYfPMHjbeynyvsfjue+D8I3qUFr+B/ZZo/7Kv7KE9rdeDdA0K/l1C9tp47XUr64mdo5ihEUgTcqZDAfw49q+M/2APGNv4R/adtvB3jCzgm/teG407FzDHK0V3ADJGyblOxiY2TjHUe1fhZ+zr/AMFyfjh8L7q0g+NNgni/Tg6O2oW7LbXqp64H7iU46AopJHLV7N8Qf+Co/wCy5pnxbT4+/DjUbuZzqkOrRaWtpIl3DMrJJJG4bEQy25QRKVxXrTwz5XFH5DPgvMqGISlTv6H9X3xE+IvxWg8X3nh59YlgtomBiSALGBE4yuSoz3x1rxHxj8cvBPwOgXxT8XvHdl4ZjJVkfVtQjhZv91JZA7/8AU1/Kh+2T/wXl/aO/aR16Sx+BVjH8LdCm/0aFrST7TrNypPAa5KhYm54W2jDjoXavBPAf/BKr/got8d9Oh+MXi/whdaBpWszKI9e8bzvZSXTSDO+O3mEmoTArk7xCFxj5ua4XTowh+/kkfb5b4WYqpW9rUnZdkf01ftC/wDBZH/gmB47+F2q/Cbxj4vvfED3cDGO40jSLuZIL2M5hnWSWOBCQ/8AdJBUkd6/L79iP/gp98AfhD8dFtNY1/7J4V8WBNM1mK8ikgSJTnyLwZ+UNbOeeR+7Zx6V558X/wDgi58Bv2Of2Uo/2pv21/jhfWEd9ItrpGieG9Gia71S6Zd6xWhvLjLYUMzyukcaKMt2B/BOPwn4O8f+L7rRfhtqRtYrmYR6ZZ+IpYoZ5g2AqPdxqlmkp6ASGJOwbOK6Msw+DxNOVOjqvwPuq/BEKNWFZv3kf6K/xI/bh/Zc/Zf+Hh8TftAeONO0qwRd+nSxyLdT6lA/MZsreDzJbgEcBo1KdMsBX81n7aX/AAcU/Fn4gW154H/Yj0U+BtIdTGfEWqLFPrEqHjdBbnfbWfsWM0g6qUNfzWeNvCHifwb4muvDXivTrnT9Y0hvs1xZXiyRT25TkxlWG5AAchQOV5XNf3z/APBKL/g3F/Ye/wCFUeEv2nf2hNft/jlca/ZQarp9vb7ofDMccyh0xb8S3jDo32rC5BUwKRXymPyXA5W/bVVzN7H6Vl9atXpqmmfx4fsxfsM/t7/8FPviVda/8H9B1TxpcX9zv1XxbrU0kenpJxlrjU7jd5rqOsUPmSYGAmMCv7Rv+Ce//Brl+yz8EbSx8cftm3//AAtjxNHtkbTNr2vh+3k44FuCJbzBH3rhhGw/5Yiv6evD3gfwt4K0W08MeENOttK0zT41htLOzhSC3gjXokcUYVFUDoFAFdTGYofQf4V8jmPGFer+7g+WJ7WEyalSMXwl4M8JeAfDln4O8DaZaaNpOmxiG0srKGO3t7eNeiRRRqqIo7BQBX57f8Fb/wBon4m/sk/8E7/it+0d8Gki/wCEn8MaIZtNeaMSxwzSzRwCdoz8r+SJDIFYFSVwRjiv0naVfpXxV/wUb+BXiD9pf9hH4tfAbwdbC71jxT4V1PT9OgLCMSXbwE26bmIVcyhRkkAd+K+ahOMppyPVcVax/no/s86x4Y/ap8XaN8V5fBPjD9tT44XVpa3et3/jSebTfAXhQuVeaCc7kEyWwyrNLLb2eR8kbAYP6e/Cb/golpH/AATA/wCCwP7XvhS18D658QNZ+It9pMnhvw34aiEr3d95QuQMpvMcIjuzh0ikOAAExXr/AOyp/wAG8X7dvx3+BPhb4P8A/BS/4xX3hb4aeHLGG2svhv4OkhQNHGcj+0rmFFtZJic7nMd1Ic/LMuBX9cvwl/Zs+Bnwo8TXnj/wL4T0rS/EWqW1raX2rRWsX9oXcNlAltbpPdbfNcRxRoqgtjAHFe3jcfQUuSGtzmpU3uz8zvhF4D/bu/4KD/swJbftyeHLL4QTal4si1D+wbX9/c/8I7bRK0VvKfNkxcyXG7cZNhCqCYlOFruvhH+0d/wTM8Zf8FCfG37P/wAJr3TLz45aLbpJrGbeVpI1s0jgktrS6lXyA1qmxZYbZvkz8wyGx+wIX9K/lD/Yo/4IR/HT9mP/AILMeNv28vGPiPTbjwK17r2o6DHbSu2o3kviEuTFdIUVYltVlkBbzH8xlQqAM4+f/s3DTlKpUR2utUUeWLPCT/wWM/bCuv8Ag44sf2LrW9EHwrs9efwcfD8dvGRP5lh551GWXZ5xlE2HQhxGsI27eST3P7fP/BD39qz9qH/guH4b/a58GvZW/wAMrm68PazqusS3Ua3Fk+giJJLOO1P755JhboYmQbAXO5l28/0JaB+wL+yToX7XV5+3Ta+CrEfFTULRbKXXSZGk8tYxBvSIt5STGECJplQSNGAhbbxX2+91bwRNPO6xovVmICj6npXpUsxjCzoK2ljJRvufEv7Qn7BH7JX7Tvxb8HfG349eBtO8UeJ/h9O1xoN5eBybV2ZZOYwwjmVZEWRElV1RxuUA19bLFAqB3wAmc56D615R40+NHh7S5WtdFX7fKO4+WMf8C7/hXz9f+NvEviyc/wBpzfuV6Qx/LGP8fxryZVJTfK9iran0b4o+K+gaKvlaOv2+Tp+7O2NSPVu/4V41qHxF8U69D5V7N5UQ/wCWcXyJj3xyfxrjzCrR88Y6VQEW18dAOKcKaW4KxoSTzOdpJAHpxVNohv3kc1Y+YYLd+lKchgp79K3UUthplHydqfLwBT0DCURxDJbtXkvxC+N/gX4cv9l1C4Nxe8/6JbYeTI7N/Cg+tfEXxA/aN+IXjoNZaVJ/Yli3BitmPnMp4w83B/BNtFOLnoZVa6gj708f/GHwJ8PUNpqVx9pv8Y+x22Hkz6OekY+v4CvhX4mfHrxv47tX023b+ydOb/lhasQ7g9BJLgMfouBXj1uHmg3KfzPUn1q3Dp8rjbjj8hXdSpxRzuvzI5CKySHgjag6beOtX4kVphEwGTjbx+Vc58T/AIg/D34NeD7z4jfFHWrTQdCsgPPvLxgqKeyRp96WRv4Y0BY9lNfzI/tqf8FgvHvxVivPhr+zAbrwl4YmzFPrLfutY1CI4BESgn7FERx8pMzDqyD5a+ky7JalbpoeRVxKi7H6v/tw/wDBVL4afsux3nw1+Fy2/in4hxZjkh3Z0/SGx9+9ljOJJV7WsZ3D/loyDg/yefGL42+Lfib4v1D4qfF7W59b1zVGBnu7kgyTbRhI41XCxxIvypGgCIBgAV4DrvjGDRiNPssPIOqZ4Uk5y5/ibPX1715Ze3t3eT/a76QySt/ET0HoPQfhX0ksdhsvp8lLWRyyjOq7vYv+NPEN/wCJWU3A8qBOUhHQdsk9z/kV52xCtuAx0BropFlb5FHPr09qxDFng18HisRUxE3UqM9KjSsrLYiBEfyqoxkVCy7cqfXFWfLZeO3tTWAVA55FclWnZHR7NXKR8wZjWq4QHKY6VYJUuD+gprA79o61lylWS2KIOAV6VV2jBz+FWWGw7Saqqp5J/wAisJs1RGgO48U1utTv1yO1Vj98E9KnmvobLUD3PTAr9XP+CGmD/wAFbv2f8jj/AITKw4/B6/KUycFSMA9K/Vr/AIIZEj/grV8ACOn/AAmdh/J6tG6eh//V/gSGRz0x2qdWDDJ7UkkeGI7ewpmTjFZRs0cz1Q5gSOfwqxFDIZAvp1qBQpbnoK0Ivus/XgVrCOyMm7Ekf3MY249KmjAI9qiJwq8dathVXAUf5Fd0Y2Rml1JY0VVOTzxjFWYVQcvx2qNV2Ll/UdKsKq4+tXyXQOF1YmTdGpLcZHH0p6DKlSKVirdMcDFWIQxOF4xTpqyFThyokhXgEdO2OlaSqQm8DjoKqo6o4B4zVtgIhvIJwR0raPYpstxERLnHBx/Sn/Kr57f0qKMF2+nTFW4ok273HJ9PStIxM5Rd9C2m9VxnhsU8sU+cDjsKVl+4mOvH6U/ejcDp0Ht2qpwstOg4q5654I1BbnRha3B3SW7bPqh6dPSvpTw+w1bQ47ibBMY8qQHkHZ04+mK+MvC12LXUwj5Ecy7Dj9K/Sf8AYh+A3iz9qv47aP8As1eBNR0zStc8VGWKwl1eSSK1e6toJJ1ti8McrK86IVjOwjdgHqK/c+Cc9o/VebE7RPgs8wEnK1Pc1/h7+0H8YvhFtg8Ba/dWdpEcCzkIuLQj/rhNvRc/7AXivqzw5/wUq8X28scPjzw3bX2Os2nTvZv/AN+pRMmfoV9q6H45f8EaP+CnvwFE114t+EGq6vYxDP2zwy8OtwkD+LZaM1wF/wB6FfpX5U+KrDV/CGqSaH42s7nRL6NsPbalBJZzKR2Mc6owx9K5824b4bzb3lGN/LQrCZlmeF0u7H75Wv8AwU2+EfxY+FurfAT4wanr0Xg/XoRa6hpGpxvdWbpkMvltA05heNlV45Y0RkZQwIr8LfjL8JfDngDxfPpfgvX7XxZ4fugZdM1G3IJeBukVzHgGK5j6OpAB+8vykY5+08y5jjlh5Ujgg5GK7e1jjkt3tbhP3cgw3GPTke4/pWvDXhrhMDN/Vp+6+nQzzPiSvVSVWOp8na1oz6a//TInjj7p/umubnZMD+tfSni7QxYw/Z7kb4pPuS9jxgfQivnHV7B9OuPLk5B+5x2r4rjHh+WEqOdJaH0OS5j7SFmRG6WCHcOCOeewGOfwr+yT/ghb+xpYfBX4cj9pzx7apH4s8ZWyjT/NGHsNGfDoCWA2PdbRLIe0axrx8wr+bP8A4J6fsxp+0z+0Fp+n+JoS/hjQNmo6tuHyTIh/cWhP/Tw4w3/TMPX9i3xE+Jb6V4Z/4QnRZDFcahH/AKRsG0R2542ADp5nT/d+tfl+KrObUGfRr3Y8x8v/APBTT9r641vR9Z8UafdOPD3hS2li0eFjgXF3NiIXBXu00pUL/djHGMtWP/wQA8MW/hb9l/xb8Srhg994i8QtA0hHzmLTYECjPXmW5lP16V+K/wDwUU+M8PjPxpF8IvDEok07w9KXvXjPyy6ht2+XxwVtlyv++W/uiv3u/wCCTNrFoX/BNjw3qluATdXmrzuVGME6m8XP4ItfW4rAvC5VfbmPBwVdVcVZdD9q/DPiJZLjIbPIr9HP2VoY73UtRvvlPlWyLx/00Y//ABFfib4U8X/ODG3AP6V+sX7CfjW31XXdc0TjzPscE34JIyn8t4r86o7o+tZ/A/8A8Fk/iBqPxr/4Kw/Fy6kZmWz16Dw7bA87ItMhhsyi+g81ZHx6sa+q/hV8PtL1XVYpPEH7vQfD9s1/qUh6La2iZ2+xbGAK+MP219KFl/wVk+KVprkixofibqbSSSkKqpJfNIrMTwBsIOTxivtL9oH4ofDfwL+y/ceAfBGsWWoa/wCKrxItQ+yTLI0NpD+8KHYfunaq+h3N6V/ReSJRwUEux/I3iX7WrmEaaXU+Zvhl8NPD/wC2J8WvEfjL4sWH27TH8ydodzRhHm+S3SN1wUMUY+XaQPlAIx1+V/2xP+Cfeofs0eHz8SvCOprqHhl50tyl0yRXtvJLxGm3gXAIH3ohkAEsigZr9Ff2Tvil8D/hX8OYovEfiG0i1K+me6uY9ruyD7kaNtQjIUZ/Gvhj/gpL+0Fo3xl+KWj+D/Dmou3hTRYYj58Ubcy3BBuZ0ifaXZEwiqcD5cZwa9zAy5Y3PG4dx+YPNVh4aUl+nY+Dvg/+z98Vv2h9ek8K/C7S/tfkjdd3U7GOytUPQzy4wCRnbGoLt/Cpr9cvgB/wSo+C3gq5ivvi5eSeLr4bWe3jzaacp9PLRhLKOmNzgH+5XLaX/wAFKP2bPgV8M7b4a/s++BtXuLGwH7sXRgsvOkP3p53Vp3eWQ8u2z2GABj4Z+I//AAUn/ae+JUz6b4avIfB9i2QYtHBNyVI6NdybpOmP9UI6+YxyxOIqWtZH9GYepSjGyP3F+Nn7QfwC/Yn8J/2DptnZ2eptFus/D2lJFBI+B8pn8ofuYueZJOSPuqxr4s/Zd+C3xI/aQ+LUX7a/7Si70DLL4d01l2xsEz5MqRn7ltbnmEH5pX/etnALfh/dXd5qFxNe6g8k1xcHdLLKxd3Y/wATMxyxPqa/ZL9l/wD4KdWdzJZfDz9paSO1aNIre18QQxgREKNqJfQxgCMAADzo1xx86j71Y5nk9TD4f3NWaU68ZyP2c3XGw5PXkZ/Wo8M0vGQRjFJYX1lqFql1ZSxzwzqJIpInEkciN91o3X5WBHQqcY6Vdht8tuHINfnU7pWkeorXVhogCRbJVyCasjU7zS9lzYSvFJasHhKkqY2HRkKkMhHYqQRVrawGTj2FZd8gKZx7Ej9KzSjPRo2ScNUfoD8A/wDgqL8dvhQ0GifEFx4u0lTyL19l4ij/AJ53YBLYHTzkYn+8K+lf2sv+Dhj9hb9nL4VtPrVnqXiPxlqMB+z+DFhjE8iMuPMup2L28Fq3TzHLMw/1cT4Ir+TT9uz9tKL9m3S08A+ADFP431SDzVMgDR6VbHgXUqnhpX/5YxHjje3ygA4X/BJ//ghT+1H/AMFM76P9oT41ape+B/hnq0v2qTxDeL52sa6xILNp0Mwx5bYwLuYeUP8AllHKBx30Mjw1Ne3xDtE3p4ytL3Yo/OD9qz4y+IP2/f2i11v4QfCLQvCGr65IUsPDPw/0qXzrksR80qQ/NdTf3pVhiTqdoFfsD+xV/wAGsf7aHxyis/F/7V+tW3wi0Cba7afHs1PX5VIBwY0b7LbEjj55JHXvFX91H7Fv/BOb9j39gLwP/wAIf+zJ4QtdGmuI1S+1ab/SNVvyMfNdXkn718kZ2ArGp+4ijivYvjz8S9B+BXwn8QfFbxEHax8O6beanciNSzGGyge4lCgfxFYzgUsw41qKKo4RWiaUMninzVD4h/YG/wCCN/7Af7Atha6p8G/BUOo+KYECv4n13Goau57sk8i7bfP922SJfauF/wCCgmsX3iz49+HvhpFIyQxWMCIo7Tajc+UW47hEXHav1F+DXj3Tvih8JfC/xQ0jiz8S6TZarAAc4jvYEnQcdcK46V+SP7dlxJ4a/az0nxLIMx/2ZYXif9udy7N/ID+VfJTxVSrK9R6nq8sYR0R/Hr/wdAfHbV/GX/BRe3/Z/hkaLw18KPDWnadYWuf3cd1qUYvLiVVHG5oWtoif7sQFfz128ieRscbkYYOeQQR0r+kb/gtt4K0bw1/wX307xl4riik8P+PbHQtUs5JlWSCVZLBtOTcGBUqLi3GQeOlfiV+1/wDBzTPgb8b9R8J6Avk6ZdxxajZR/wDPOK5HMf8AupIrqv8AsgV+68HY6lGnDDJbo+Jzii2+c+2vAnhZv27P2KvFn2uNrv4p/s66VDrVldj5rnV/A/meXd2c5PMsmjSbZbd2yRbsYv4Vx+9v/Br3/wAFM/CXw58JeMf2Jv2ifFNjomiaPC3ifwve6tdRWttBBLIF1GyEs7Iqqsrpcxpn/lpNjha/G3/g3j1azk/4Ki+DPA2qx/aNK8aaH4h8PanA3KTWk+myzsjDpt3W68V+XeqfCqTwp+0lcfAwS2zPpPia98PLJduscH+jXMlmryO3yoP3YJPQUZhllLF1auCquyVmn2MsJXnRjGpBH+nn8Vf+C4n/AASx+FpkttV+MuiX86Z/d6QJ9VP4GximX/x6vz+8b/8AB0Z/wTq0JynhWHxd4hKk4+y6N5CnHobuaHj8K/kb1L/gn18cbWxDXM+kxrIoKf6Q2Cvqp8sZHpjI968dvP2GPjdb3DhJdKkK8AC4f/41Xxs8o4aw7tiMRqj0frmZT1hTP6tfEX/B2P8AAu3cr4W+Evii/TPBubnT7Xj6LJLXnV//AMHZ+o3MDJ4X+B3f5GvdfRfzEVo386/l8n/Ys+PVriUW2myd/kvAD+G6MVFbfsmftBW0JZfD3mhe8FzbuP8A0MGvVwK4Plp7ZfeceKrZvFX5LH9FHif/AIOuP2kbhG/4R34Q+G7Yf9NtUupiP++II68if/g6l/bjEw+x/D/wbGgP8cl6x/8AQlr8GNT+A/xm0hC2p+FdUQL1KW7Srx7xbhXj2saFqOgzkaxbT2fbbPE8X/oYFfa4Th/hmok6Mov5nh1M2zFP30/uP6WB/wAHS/7fkqeYvg7wQoJ4BjvzgfhOP5VHc/8AB1D+3PAwF74C8Ezrjopv4/8A2o2K/mfiu4yAImDjp8pzxUU8u8bB+dezHgPJ5q8Io5nxBi0/eZ/T/o3/AAdbftS2xUa78JfDFwA3zfZtTu4Tj23xOP0r3Dw3/wAHQnh/xXKk3xX+D+rAdf8AiWa5aXCIP9mKeG3H61/IekKlR3zxircTRIdnQegrnl4Y5ZL7JsuKsTHZn9sGif8ABwP+wN4maNfFtl4y8MsduTd6THeRJ/wKxnnOB67K+6vg/wD8FOv+Cc3xSKReGPjF4ctriQ7Vt9WlfSJs+hW/SD9P6V/ndyW6S/dUA+oqeOeWH92XZlH8LHcPyNefi/CfBf8ALt2NI8W4hvU/1QPC+qeF/HOlf274G1Sz1yxPSfTbiK7iP0eFmFOitS85UZ469sdq/wArOw+I+s/CzUf7a8D6td6FqKHcJNJuJbK4DjnPmW7Iwr6o+Hn/AAWt/wCCjvw8jGk3XxFufFWkof8Ajw8SqNRUqONv2jMd2OABxNXxGa+GjpL93K56+E4jqT+JH+it43+L3gHwE5s9Qn+1XoH/AB62+Hf1+Yj5UH1/Kviv4hfHrxr4wElnYP8A2TZHIEVs3zsD03ycH8Biv5lfgZ/wXa+Hmr3Edj+0D4IvNDkJxJf+HZhfW/8AvNaXJjmUY67ZJT0xX7EfB39qT9nH9o22EnwV8Zadrk7HBsg/2e/TP96yn8uft2THvXw+L4Xr0HecT6elmkJKx6ZeKJBvAx6465+tNgtR/EOeorbvLAxk8Y2DLbuNoGCc5HAA6noK/KL9qb/grX+zR+z4tz4b8DSj4heKrfKmy0qVfsNvIvBFzqPzRDHdYVmfsQnUZ4PLqtR8sYjq4iEdz9VLW5sLQPNqMyQpCpdy7Kioq8lmZsKqgdWJAAr8kv2rv+Cyfwb+Fa3PhH9nKCHx34hTMbX7M0ei2jr/ANNk+e8YY+7CVj4/1vav53/2mv29P2kf2rppLH4iasun+HC4ZPD+lM1vpy45BmyxkumHZp2YD+FV6V8cXvjk2yBLLEuOMrwg/Dvj06V9bgslw2HXPiX8jyqmInL3YbH0z+0f+0l8XP2kfE3/AAnnx88Sz6zc24K2yyYis7NT1S0tY8RxAjH3V3H+Ik18H+KfFs99utdL3QwPwX/jbj0/hFXta1C/v5fOv5TI46E8BR7DoPwrjbhCybuOuK5cz4j517LDqyOrDYJbyMPYkSZbkj1/nQSH4zjGMVdZfMTOMYwKrzRpjeoAwMV8m49WelGCRTfePkHcflVCRQjYz1rRKeY3H8OOPwFV5E3oOOMgcVRVig2EYjtVecYGByeKtOVK76rSOvC96icboUloRPskUFRtA/zxVWX5MNxirTnJI/8A1VTceahA6j+lcXK0iIp9SrJHvffzzxUcsQQgg9f5VfC5t1B/Kql1hQGrNJWNYvWxQcOOD09KjKA4NS7nbbjqP6VDnmsmrI6UKvl96/Vj/ghuT/w9s+AK9v8AhMrD/wBnr8qI417n2r9W/wDgh0wX/grb8AXYf8znYdPo9KKNIn//1v4GZGViSKaMcetNyd2D0FIy85rOMbKxy26D15Hy1dhbbEFH8X5Cq2Mr6VoxBNqAdu1bRi9EZTegqRMdhkGcc1dDOPmGB9agRs8jjHarKqr7dpwDn/P9K7Yu6MlJ3HLIN209Bj86vxLnKx8EflTEIAUEdcdKsKo5IH3ea0RrYe0abOn41Zj/AEJA/IVFtdk5Oc//AFqsIu3BUcY4x1pRRJahRJGAYdKtNl1wwyPT/PpUEAKDP6VbiZkGTyDjHtXS7AyePEa9B6VbiJHypjCgcCoAr8Mw/CriFShkGMg1StYRZjyX/D+lMwVx61L8yRMcDHH60RIWAblQcUqkrqwRSRo2SGL96p2lcYPYGvq/4SfE/wAVfC3xn4e+Mfw8nNvr/hm+tdY0+Tsl5YTLNHnpwWXafVcivlmPCLsX2r0zwjfmNHtW524lUDjPrX1HB+LSnLDT2kjxs0pNWkuh/sUfs7fHzwl+1D+zr4N/aJ8BNnS/GmjWusQKpyYjcRgyQt/tQSbo2HUMpFafi/wN4K+Jtg+heP8AR7DXrRxhodStYbyMj02TIw/Sv5gv+DWb9ruXxV8AfHP7GXiO6DXXgK9GvaGjHk6TrDMbiJB/dt75WY+n2hfav6hNQ1y30G0udXu0kkjt4nmKQxtLIyxrvKpGgLO5A+VVGScADpXwebUKmFxTpwZ72FlGpTu0fDHj/wD4I+f8E0PixI1x4p+CXhaOZhtM2lWz6RLn136e9ufxr5D8W/8ABsx/wTv8Vb5vBh8YeFGYAqNP1oXUa9ONmowXR/AtX138P/8Ags3/AMEtPGNvJPY/G3w1BJbxu8lrqMkum3Y8obnTyL2OBy4xjywM54AzxX87/wDwT5/4LCfE34W/tVaz+1z+0T4ksP8AhTv7Q/ji+0y50eS9je/8JzWiRx6TqMlpvMkVnLBttp32hMQ+afuqH+hyytmqg6kZNWOHEUsM5JNI95+N/wDwateF5dKmt/hZ8X9Wt8qdsWu6Pb3Ue7tmWzltmX6iM/Q9K/j/AP2zv2MPjl+xR8ZL74CftE6QLLUYVNxZXcBMtlqNmTtju7KbC+YhxhlOGjPyuqniv9ebR/if8OfGVtu8N65p2oBhx9luoJuP+AM1fAn/AAUh/wCCb3wX/wCCkv7PFx8I/iB/xLtUs2a88P69Age60m/K4EkfTfBJws8OdsiejqrDpw/F2J51TxusTOrlVK16Oh/Dv/wSSvvhhovwR1Wy0W5Da/aXj3WtQMAspZspbMnXfB5YCqy8B9wOCRn1r9sj9oy4+Cvw5uPElpLjxL4gdrbSh3ibaPMuMf3bZCNvbeUFfkb8Rfg7+0z/AME2f2pb74bfESz/ALC8Y+GXPzDc9lqdhJ92aFuBNZXSj/eUjaQsiELxX7S3xs1r9pD4qp4gW1ays0ghsNPsnfd5CAZlJPQl5S7Zx93aO1ezguEo1MUsRT1gePj849nRcJaNHkMmi67deHJPFb20z2CTrDLdMCU85xu2ljnLNyTX9UP/AASJ8V/8JN/wThuPC0LBrjw/q+tWhQHoWaO/j/MSnFfzs+Mdc1iH4Yy/Dqxlzp0KRMsYUfehJbcDjIySc89/wr9P/wDghZ8Z7bw7488Z/ATWX2x+ILWHWrBXPDXVgDFcxgHjL20gb6RV9Hxhh/bYJxgtEfL8I5pzV7yP2F0Tx0sLFmkwGxiv0S/YV+Ntn4V+PWjJqMwjtdVD6a5z/wA/AHlf+RlQfjX4+/Euyu/h341vPDsxYRK3m27Ho1tJzGeO4Hyn3GKh8L/EW70+8S6t5ijIwZWHBVgQQR7ggEV+CKLUj9ePjD/g4i+B+ofBX/gpZ4i8aW1sY9L+I9hY+JLR1+40yRixvI8/3lmtw7D0lXivz/0zwRFPf6B4e8M3S6nPr1rayoFXaEmujtEJAznacA5/Kv6pv+CjPwvi/wCCq37CFl4u8HRCX4qfDiZ7+zt0AMt3IYwL2wX/AK/oo1ngwMGeIRjHNfy8fsKax4fsf2ivCcfiuUW1vHdkq0vyqtx5bCFGzjafNwPY9a/cuD8wVWgodtD+fPEnByo81eC7s/Vjwn/wTY+FcMgk1rU9TumU7WMZijXd3wNhP613Hij/AIJo/sw6pDGdY0+9u5FAUSNdEHHp8irx9K/QqwijVAyjD/x1V1F3Em0mvuYxS0SP4unxlmLrcyqNWPhL4U/8Ev8A9jS48d6fo+peEIryGSUeZ9puLmVdi8nK+YB0Hpx9K/Mj4a/sf/A/9pv9oHUfAw0//hH9Dmk1O5tH0xESS1ijZvs4TIKsikplG6juOo/oSh8Qp4Q0PxN4xfj+x9D1C7Qg4Idbd9v8q/Lb/gnLpbP8QdV10cC10pYyx5w00qflkJXkOVqisfoOS8V4+OEq4mdRtq1j8Xv2zf2APjL+yHqIvvEMQ1bwvcSFLLW7RD5EmDwkycm3lx/AxwedjMBX5tXUis7YyueMf5xX+jD4i0rQ/FPhq98M+JLOC/0/UITBcWlyglhmjbqjowwQfp9K/mt/bk/4I5XegxXnxQ/ZRtp72yTdLc+GifNuYEHO6ydsvOg/54tmUfwl+3pV63MkmtD9N8PfF7D4q2Gx3uz6dmfln+yt+2/8VP2a72PQYg2ueEGkzPo00m0RbvvyWUh/1En+z/q2xyo6j+mn4KfFnwB8cfA1r49+G9+t7p1x+6JPyTQTD70M8XLRSL6dCOVJXmv48JdJubGVra+QpJGSjAggqV4II4wR6V9Kfs1/tFeNf2bPHqeMvCX+k2swWLU9OdtsF/br1Rz/AAuvWKQDKH2JB+dzbhaNaHtKe5/QGFx60fQ/rbEHy4ztHv6ce1eBftBfHn4ffs7fD248deO51Z/Lf7Bp4YCfULhB8sMSj5gu4jfJjai5J7A/mL8cf+CuML6ONI/Z+0CW3vJkGdR1oJ/ozHGUhto2YSsvQPIwXv5ZFfn78M/AHxS/bB8dXXjn4i61dXFoj+RqGsXb+ZK8m0FLW2BwqnpkIBHEvbOAfkqGS+y/eYp8sT1ZYjn0gfW//BJT9mKz/wCCnP8AwVO0bRP2gh/a2kkXnjLxLA/+qurew8tYbEj/AJ92nkgiZAR+4Vl71/qieGdIsND0yDTtMgS3t4IlijhiQIkcaDCoqjAVVAwqgYAwMV/mLf8ABuP8d/DP7PX/AAVG0y4+IkxtLLxJ4Z1nQHKo0jLcx+VdogVRu5+yMowOvFf6E2vf8FAfgHodqPsA1O+IHHk2hQHt1lMdfNcZSm6yjD4baHr5TJKGp95dV2rx/KvHPjj8PNM+Kvww1r4e6ou+01qyutNuBnA8m9t5LZ847BZP0r86/EH/AAUs17UI5LfwF4ZitMcCbUJTIf8Av3FtAP8AwM18j+Ovj58XPinLLb+L9cuJ7WTP+iQ4t7fH90xx7dw6Y3E18zCm9D1XVTWhvf8ABIr9u3wBon/BNDwR4A+Jd68njL4YG78B6tp0Cl7hLjw/M1pHu6Kga2WFwWIznjpX5vf8FqP2yPjqND8FftO/B2yWw03wLqqwa9ZArLJeaXdsgAkcjCBZVCZQfKZQScCvgL4oeM0/4Jyf8FALzxl4hb7L8Gvj+yXF7cYPkaR4htxtllYD7qsW8x/+mUrMM+Qa/XrXPDPh/wAZ+Gr3w14mtodT0vVbWS2urdyHiuLWdNrLxwVdT1H4dq936nCFRVHqmcjk5R5T8qv+CiHwVg/4Ke/sJeFfjx+z476z41+GVvPfaOIATdal4fl2Nc2KL977Zp8sYkSLlvlkUAs61/LX8Zv2hvFH7QutaV4u8aRRDUbDS7fTZZYc/wCkNAzkzuv8LyFssOmenpX9CGl+Df2rv+CRnxIvvFfwhhm8ZfB6/uPtKK/mSCyfoouTDmS0uIxhBdqPJmQDzF3fKON+Nbf8Ep/25Nfl+Lvi7wN4p8AeMtRYT6nceErvTo7S/lb78s0M6mDzWP3pYoYixO5wxr7bJcb9XknGN10PDxkIyXK3Y5H/AINlvh9ceK/+Cm1n8XNQUw+Hvhf4a1fXdVvX4gtvtFubGESMcBSwmkcDP3Yn4wDX50eD/gt8bv8AgpB+1p4i8N/s3aB/wkPiPxpqeu+JYLFpo7dDatNLeMWklKxr8jqi7mUM5CjkivtH4uf8FNPgx+zP+yf4h/4J/f8ABOPwUvhDSPFwMXjLxbc37apreqRkGKS3a4SGCPdJEWhbylMUUTtHCA0jsf2P/wCDcvwv8IP2GZPEHx9/abs7rTvF/jeygstMKw+aulaQG81o51H7xJrmQI8gCnakaKcHcK6a+bVKCq42StJ6JBSw0JctOOx/OLqWi/8ABSf/AIJneIwni3QvFvwz8l87NSsjdaLKV4xtuI59PlTt8pbjpivvn4E/8F/NOtZYNL/a5+Afgf4k2OPn1LQ4U0HUyuOpi2y2rt/uiAZ7iv8ASJ8H/Ez4IfH3w9KnhHVtM8S2Fwm2WFWjl+U9pIXGR9GUV+Sv7Xf/AAb+f8Evv2qpbjV9c+Gtl4W1yYf8hTwwx0e4Df3ilsBbuf8ArpE9fD4rMcBil/tlFfI9+jSq0v4Uj8g/gp+3r/wbv/tJx22ma61x8JNZudqiz8Rm80yNHPHF5HNcWAAPTdKucdBX6gaX/wAEpP2afil4STxt+zz4uuNS0y7G63utPv7TU7Nz22yKMH/vuv5vf2uv+DVH42/DN57/APZM8dxeKdOTcYdJ8SxfZLkKOgS+tFaF2I4G+GIds1+B3gf4v/td/wDBMz42a1Z/DbxHf/Drxv4WmMWp2+j30VxaNMgDGG6jheS0uAM4eN1fHQhWGB4VTwuynHU3UwjtbodEeI8RTajUP7e/iP8A8Ew/jJ4GkkGlala3ag/It5FJas30dPNjPtyB9K+K/iZ+y18ffDFq51nwvdXNuv3pLQi8jwO+I9xx+Ar+wj9lfxj47+Lv7LPw8+IPxq02Oy8TeIvDWl6hrFlswkV5dWscs6bGztAdiNp+707VX+I37Pvh/XLKW98JILG7VciJf9VIR2x/CfTHHtX5piOA1Sv9XquPzPfjm0ZfxIJn8C/iX4O/DjV7h7Lxh4a09rjOGW4sUimHTqwRHFeM+IP2GvgtryySaLFe6RIR8v2O5LJ/37uFlH4DFf19+N/BvhnxJ5mmeLtLtdRXJBS6hSTGOvJXII9q+RvGf7Evwf8AEe658Libw7P1Bgfzbce5jkPH/AWGK8/n4mwHvYPENnQsNlOI0q00j+T/AMX/APBP7xtpUTXPgvX7W+VRlYdRie2c/SSLzoyfqEFfIfjv4O/Fv4YM11448PXdrapjN3EBc2gz0zPBvRfo236V/V142/Z38ceAZWtdPuLbXbVf4rMguB0+aEjIOOwzXytr0Ulncy4ia1nQ4O0GOQfVf6fhXv5T9I7iLLpqnmVPmRwY3wzy3Ex5sLKx/NUfE2jWVqtxJMsgI+VI/nJHtjpXnOr+MNQvnK2g+zxEY+X7x+vp+Ffvz4+/Y3+BnxlFxqepaOun6tIPm1HSAllc59ZIwv2ebty0e7/aFfmd8Yf2AfjH8N0n1rwVt8X6VApZzZxmO+iUd5LM7i2PWFn9wtf0bwf9ILK82tSqS5Jdj86zXw9xOD95K6PgG4k3g9dxrJS3ViHI5HpWm8iOxjTqD34wR2I7H2qeKPJ2jg4r9c9vCouaL0PmYw5dGhlpaovTjnqOvFbltLIk8dwMiWLmN8lXQjoysMEEdiMVnqsa5bdkfpWZc+KrC3AitR5znHThePevLzDNMLRharY6KOHnJ+6fRPi39or9oXx54Gj+GvjLx54h1Tw5CpX+zrzUZ5LcrxgSAvmRQAMLIWA7AV8j65rmmWCCCwAm28BUG2Ncds/4Uup6zeX5xcPiMcbBworjb13xzjae3t9K/MMz4ohfkwsLH0GHwEt5sy7/AFLUNTkBumwgGVReFHp9aitrn5AijpSyDPGOn/1qikG0suMFR/P/AAr4+rOdR3mz2o0VbQJpzKPUHjHYenFZsiKz+T3/AMOKtfu0crj7+PoM1VdSDuXkYxUTSSSRcY2KE4LNlemBx9Kz2DbPKxya2GGWC47ZrPlyfnHQ1lI0KVxggMRjtVCQHZtTjnjpWlOoQYrPlVnXavGDUoRQkHRGxj/CoCkZBRh83Yj9KtMkjOQO39Krp85IHBHWobByQ2RsflWaXeLcr9K0AAqEf3SR/nFVpI94y3euarJ20EpFTzQvyP0HSqrsZYw7Z4qfyyzbfT1qBA3MfpXPB9GWkQA5AXp2FIv6GnfxZpoAVsDpSSRomNICnZ61+rH/AAQ3zJ/wVr/Z/X18Z6f/ACevymYfPkelfrB/wQyGf+CuH7P+eP8AisrD/wBBes09mjeG5//X/gUxlifSnYzj8KRVYcmngEnisoy6HLcnWNQuB3xVuEKFIqsmQQDVuMNnp+VdEJaowmW18sADFOWOR2DcDHSkAwucVbT5Ex9K7IsikupNGrxZUcZAI6U9Uwig9cjJpsYYDJxtPHSrIHA3D2P6VtbsbRLCgcKo7VZXyxtXHHGMVFGp2qfYUqgZ3dgeO3T/ADiiLsVY00UgDHXirBBWPkZqNFfJkfpnHFW1bbhR09K1k/euZtaEittiAIxmrCtt2nGAcUxk6KMAirSgEj2xVu3QCxtAIj9cVcwhZQD0x+FU1+acbhnaMVdhxu6fh9KS8hF9FCqDjPTH41sWeomwuUvfuhGwcehwDWXG3mLuOMDsDTZcuhVe/StYVfZyU47oxxFNSjY/Wj/gkZ+11/wxb/wUK+Hnxg1K5MHhzU7z/hG/EDZwg0rWCsDSv22203kXH/bKv9SdLVpbvy+hhfgg8ZB/Kv8AGV00LqeiPZ3AJUK0bAcZRv8ACv8AUr/4Ilftej9tb/gnn4J8e61d/aPFXhaIeFfEm45kN/paKiXDD/p6tvJuPq7DtXo8WYVVIQxcTDKalm6Z/Pj/AMHAf7Jnhf8AZH+Lep/tF/DfQfC9zof7RNvJo+qW+sW0TTaL4hgaOZ9Y0xyA1ubiLd57qNquXLD5o8fub8Pv+Der/glZ/wAM7eH/AAv4y8EWfiTxDJoNva3fiu1vrqOe7uJYPnv4TFMIfmdi8OEKbdowRXzd/wAFY/2Ov21/2kv2xvCPxR8HfCHw/wDGD4W+DPDd9psGganr0WlNcX+sI8d5csJMMjxL5XksvIMYYEECvzG/Zs/4KH/8FWv+CU934N/4J4fGH4DyeMBqs1zJ4Jsr7Wo11A6aGJ/s+0v4fOtbn7NxsUqsighduzYB20ZVsRhacKU9UROKhNtx0Pza8Lf8Ev8A/hDP2+vB/wDwSe8c+E2s/G8vjNdUm8fWep3EMWr+BFhlujssfM8hLho4XXeihg6+WRld5/06PD+l2OmaTBplhEsVvbxrDFGo+VI0UBVHsAAK/wAv3xV8Q/2if27fjf8AFz/gop4Z+HHxFn8bQ6vYN4E1bwbBLqVl4Z1DRyjrYX3lKDMPsojUlFADOzlGDEH/AEBv+CXn7Zuvftt/ss6L8VvHnhu/8G+LrX/iW+JNG1KznspLXU4FXzjFHcojtbzArLCwHCMFPzKwrz+MMPL2cJStpub5bO0rHD/8FWv+CVfws/4KY/A1fC2ovFofjrw8JJ/DHiHy97WkzY3W06gZksrggCZOqnEi/MvP+Y18bvhT8Yf2UPjRq3wd+NGjS6F4v8LXJgvbKf5hyMq8cn3ZLeZCGhlXKupBHpX+yUPavwp/4LW/8EifA3/BSz4SLrHhY2+h/FXwxbufDusuuI50OWOmXxUfNayt91uWt3O9MqXVnwnxNLByVKfwP8DPOcnhiIH+dzoWoWPiqxS8tDvV/lZT/Ce6n6Ve025+I37JfxX8L/E3R0Nrqdl9n1zTd/3JrdyV2HH/ACzlTfE4/uk4FeQz+HfiL8BviXrHw1+J+k3Wh6/4cu2sNY0u5XbNDLCf3if3Tx80TrlHUhlJBBr3L9rz4w+H/jh8WIb34fgnRNO0+z0zTE27Cscce51Kk8ESMy/hX7ElCpS/us/GvqNfCYxJL3T+oy517wB+2L8DtE+J3w0uFT7dC01gzkboZRgXGn3P91o3G056EBx8rc/GlvbaroWpS6Nq8UltcwPslSQYKkY4/wACOPSvxK/Yk/bb8ZfscfEG4sdTtpdV8HaxIv8AbGkhtrpIg2reWpbCi5jX5cHCyp8jYwpX+p7wbqXwQ/a0+Htt8Qfh3qcGvadhUS9tMR3lq3XybqJvnhcd45R/ukrg1+FZ/kdTDVXKC90/aMqzenWgk3qeUfBT4w+LPhJ4lj8ReGpPlKiOe3diI7iMHPluVIYEEbkZSGRgGUg14h+1p+xl4F/aV8VXfx6/Zo8nSfF9+5n1Xw9ctHBFqE7YLz28nyxx3LH74AWKc/P+5kJVvqG+/Z+13TJzJpEqXsI6AfI+P93oenY1vaJ4B1XTYwNQtXUcfKy5FedlGdyws1JEZ3ktPGUuSR+fvwZ/bJ+JnwjnHw0+NOl3V42mkQvHdBoNRtQoxtzIB5igfd3gHHRiK+0bf9rz4E+IMTtq7WDsMlLu3dMfim9OPY16f4l+F/hv4l6euleOtHh1eOEYjFym54h6RSjEsf8AwBx9K8a1j/gnf8K9biaTQ7rVNGY9ESZLiNfosyb/APyJX6jheOcNONpOzP5f4j8CJOq6tGP3D/il+0H8Ib34BeOdM8P+I7G51PVNJNlbW6OfMlaaVFZVTHZCT7AV8u/sTfEH4e/C+28Q3vjHUotPmuXtY4kkyWdUDlioA5AYivadS/4JraJ4W0a78X+IvHsOj6Jp8e+5vtUtoraCBPWSV7hY09BkjPavxT/aS/aT/Z/+GWrP4e+Buuz/ABBuIfke+Wzaw03I4xFJKxmmGRjKxIpH3WIwa9vB5nTrLmpnzcfDPFQovBKDsz+h2+/bQ+Cem27TSa1uVfmbZE2AnU8kDivlP4r/APBZr9n/AMD6WYvhfZXXirVwcIrAW9pGw6b5ssT7CNT/ALwr+bLwzbftVftreP4fhd8KdD1Txdq8zB49E0G2eURKcfPLs+WNB/z1uHCAdWxX9RH7Bf8Awam/F3xnb2njH9vPxYvg7T22ufDXht47vUmX/nncaiwa1t+nKwJP14kU1liOIKOGV60vkfXcOeAWHjKNStufzAftA/FjxH+0R8YtV+KXiGxtbfV9bbz5bbS7fYmyFAGcRpuZsKu6SVsseWY189yr5akp904IxxX+v7+yt/wTs/Yw/Yp8MHwx+zd8PdJ8P+bF5Nze+V9p1G7UjaRc31wXuJVYdVZ9o6AAcV/K5/wWq/4NxfKGp/tS/wDBOXQ3cybrnWvAVkqqB/FJdaMpwAeMtYjg8/Z8ECI8eW+IlKdT2c42j0P3uPC/sKKjT6H8U3h8+ELrxRaRfEGe7g0bfm8awjWW5KKM+XEHZVUvgLvJ+QHOGwBX6V+HP2xf2e9GtbHwz4Ys9U0jSbFBHaWy2a7IUXsMSsxPJJY5ZjknJr8rb+3uNOvJLDUI3guIHaOWKRWjkjeM7XR0YKyspGCrAEHjAra8HvoVn4ks7zxVbT3emrIv2iC3mFvLJCPvCOVlkCtj7uUYZ6jFduc5NSzD+I9PIWFxM8PqkfSHiX4iaL4G/aPg+OXwAvtzWmpweILHzYpIPJvAwklgdXAyrOG6ZBR8V/an8EP2hfhr+1L8GNK+Mnw2uFNpfIFubQsDNp94B+9tJ16h0OdpOA64ZeDx/Oz4D/YF/ZM+Pvw9j8dfAnxzra27Dy5IrxbWWWyuMZEV1CqxOu32bDjlGIr4C1u1/bN/4J1/EK58R+F7+/8ADaz4h/tXTwLnStRhU/Is6urQsP8ApncIsi9vWvKzXLMPXpRo03aUdC8Lj587bW5/a3Zho5uTlenPSuxtIcMsxbiv44rH/guP+2jaWcUc7eErt1XmeTTWVifUqlyq/kAKqT/8Flf2/PGKfYtE8Sadppf7v9k6Nbs/4GRZzn6V8z/qnVfVHtRzCmlax/Wl+0X8Avht+1J8JtT+CHxWtXu9L1NQ6SQ4+0Wd1H/qbu3YjCzRE8DlWUsjAozCvwa+HP7X3xp/4JWeLo/2Vv2s4/8AhNPA1qSuga5pssb3sFon3QLd33bEBGbaYo8JBWJ5I9oH5r+J/GH/AAVD/aQtvs+p6t8QNctLr/lmrXFhZMpx94ILaDH14pnw5/4JWftFa9Ol74ym0zwpHK37xppvtt1/3xb5Qn/elHvXrYbKqdGPJXkrHLWxvMvdP3K+K3/Bd79lzwPocifBvStZ8baq8fyiSL+y7JSw/wCWk06tKSO4SBh6Hoa/DPxh8Tv2xf8AgpR41nbwt4bsdN0XzCJItHtk07S4s4z9rvmHmXDAdVZ3P92MdK/Sj4Sf8Etv2fPAfk6j45a68b36YbF+VgsgR3FrCfmGccSyOPav0R0rQbDSLO30rTLeK0s7ZdkFtbxiGKJR0VI0wqgegGK5ljaGG/gI5WpTtzn5yfswf8E7Phr8DtRs/HXjqVPFPii1IkhkKbbGykHe3hbmR1PIlk5H8KpX6g2F1L5ZaTr69M571Qm090UHrtH8qjhmEG+Z2AjQZJJ2gKO5J6D36V5eIxE8RrI6VywO10e+1TTb+PU9JnktrqLmKaBmidSOMqyEH9a+v/C//BSP9pX4KadJqviDxJb6tolhH5lx/wAJBtaOOFf4jdbkkQe7uQPSvwi+N/8AwUw+A/wdWXQfA5XxxrsJKNDZShbGBh/z1vMMrY/uwhz2ytfEHgH4M/8ABQj/AIK169HdwgaV4EhnBN7dCSz8P2x/6YxjMt/OB02+YQcAvGK2hkKceetojX61LaJ+kn/BST/g52+N3x28I/8ADP37Fmk/8IjLqZ+xah4ntGee+uWkOzyNFjMayRCToJypmP8AyyVPvH2f/ghb/wAG/wA/jbxfZ/tOft72HmW+g3CXdh4Om/eL9t4kV9Yc/fmjbEhshnaSPtDbsxV+j3/BML/ghb8F/gjfp4x0RZda1y1/dXfjHU4kF0MjEkGlQfNHZhl4ZlLyqOGlOdlf0Han8X/2e/2dPD8Hgq0vYIF09AkdjZDz5uOpcJn5mPLFyMnk142PzeNCDoYRWPRoYVu0pn1dDMtvEIweleXfF740+GPhNohmvXE+pTITa2aH52I/ibH3UHcn6Cvzm+I37ePinWg9h8NbIaPEeDdXJWS4x6rGP3afUlvwr8lP22P28PA37IPwuuPil8S7s6tr+p710jSZJM3WqXSjHzMcslvFwZpsbVX5VyxUV4GAwlWtLlSOydVRR698Sv2yPB2gftKab+zZBA2peJ9R0G/8S3pjYBLKCF40g83rj7TI7bV4IVc/xLXPah4x8SeJWE+qTkRt0hT5Y16du+PevyO/4JffDf4meOLHxp+3V8e3eXxZ8V5VSyZxtCaTC2Q0Sf8ALOGV0RYU7QwRn+Kv1bhVYvkPoBz6V6OKwUacuRdDCFeVrmssgG1e3GCOMVzHirwP4c8a25g8Q2cdxhcByMOg/wBlxgitzUtT0LwzoE/ivxZqFppOkWS+ZcXl5KlvBEvYvJIVUfTIz0FfjT+0x/wWw+EPw5+0eGf2ZdK/4TjU4/3f9r3wktdJjbpmKMbbi6x2/wBSnozClDhJ5j+6dO6MP7b9g7xZ9s+NfgLP4I0q88YaTch9JsVMs/nusZt4l/jLnau0epxX5K/GL/gor8GPh+kmn+Bon8Y6nE20NARDZo/bN1tO4f8AXJGHoR2/Mr4tftMftT/tla7Dp/xH1vUPEPmNvtNFsYjHZxnr+6sbcBCQOjuGfjk1pfAb9lVPin8RLfwf8SdUl8P28sLTrHahJLiYJgtEHb93CSP9lyMY21thPo/5Zg6v13Ey26I5MV4m1Z/7LFrU+cvjh8bdY+N/xBl8eeKtP0zS76dSGTTLfyd4XkyTNkvM6jrK/OAOgHHjDeIoYmItl8zb3/hHH61/az+yN+y3+zB4M+EGsfDjwt4PsbNdShn0fWrwp59/fWN9E0bebdSZlwULDYhVAQCFFfxi/Fn4T658B/il4l+DXiXm+8Kanc6VI/TzPs0hRJOO0iBXHs1fXS4rcIfVsIrJHIssv+8qHBapqV1dx5lOV7AcAZ9q5tppuCccdK2blQg2txn8KwW2+YY/SvmMRXnUfNNnp08PBbEvmXE8DOQMjpjp6VWmjZY98pHbH0pYmJBiHQippvukemMUUrOxskkZd1kqDnA9aoFSAH98e1aLD5M9vSs9lbjJ6YrZxu9BjHVSMdh+VUnwQvGOq1LJI/lhD0zz60mAV5HQ1hVXK7CKsuTjd/DWbKMIxXp3rVkjZ0O3FUH3iPaTztrL0AoupBx68CqTxpjaOeM4qzKzA+WwBORVSVHDggdOM9hxU+TGVmkUuWBGBg8egFVWCo+Uz81WHRN/yDaSP84pkjBVGevtUCtYpBWRsH5QfyqnOvBjxg8VpvluM8dKrSqXjJ6HvWUzN6MzDE0Rz7VTPzNkdK0JQYymO3FV5iqyZ/LHSsPZrc2SIpVCtsXpVdhtPNTybhMB60yVcsMVzzfvWLWmhExC8mv1e/4IXAt/wVz/AGfv+xysf0WSvyeI3RYFfq//AMELJVi/4K4/s/O/T/hMbL/0CQUQRvTWp//Q/gd3KclelMjPNDKWQ7PWliUj73pWcYnFoPU5JZh7cVpQDdjzBjjtWanznKVpwIG+TpWqepD21LQwUy3SrLKgAwCu7jrUCpGyhUqzjGM9hjj1HFehHZBHYej7NqPxg/pVyP532MMioVG7bkce3pViEIXDA5WrWxppYt7iyjapU5HFO2ceWDgE5zRtPUcirEQUPuOMUoktl1U4UehyKnjYBs1Eit0znHOO1ThcfLjpzWktbESehMm1Zdp6/wD6qvwLjLDpVeIc56VZTLD5eM1oMsQZVAFHXmtKMhlXjr6VUjXCZFW1j/dhD1ByBVc3QTLJi43LxzyKr47H2q2TsKr1qEbncMOnTFKcbxBvQ3NAuFtrsLKTsf5cfXpX9NP/AAbv/wDBRv4a/sP/ALQfif4YftC63HoHgD4kWVuDqFyG+y2OtWDMLaWcqD5cU8MkkTyn5VKxFsKMj+ZiytmC56u2MV6LZXjPaLKD8+Oceo7V9zw1h4Y7DSwdU8HGVXQqKrE/2KtB8X+EvH2gw+LfAGp2Wv6Td4aK90u4iu7Z19VmgZkOfY18bf8ABQf9gz4Vf8FC/wBnS++CHxDf+ztRt2+3eHtcjXbdaRqkakQ3ER4O3nbMgI8yMkcMFYf5i3gn4l/Ef4VX8XjL4LeJNW8IXzhW+0aBf3Gmvv8A9o2zxhufUV+j/wALf+C5f/BVz4TxpZ6b8XLvXrWPkQ+I7Cx1QHHQGZ4UuD/3+zWX/ENcVQlz4aY/9Y6U1yyR/fl/wSo/YW0n9gH9iTwf+zncvb3Gu2Ucl9r15aljFdateNvuZEZgrFF+WKLcAfKjTIzX6d2NhHbqG+9jpzX+fN8MP+DpT9ujwzDDb/EPwT4J8RhPvPAt/pUrkfSa6iHHogHtX6CeBP8Ag7V077Mi/Eb4GXsb4G5tK1y3uF/BZ7eA49BmvEx3A+bObnKNzpw+fYVabH9lO7HTjH5Vm3iRTJg8g1/Ltof/AAdZ/sdX1kW8U/Dzxtpb4/5ZQWN0B+K3S/yrudH/AODor/gnNelY7vTvG9tnru0Mvj/v3K9eXU4OzNf8umdX9v4e9kz1j/gtB/wRO8I/8FEPBJ+MfwaS10P4y+HrUx2V3KBHb6zax5ZdOvmH3ef+Pe4IJhY4OYydv+cj418L+PfgJ8Wb3wF8StDudE8S+G7trbU9J1GMxzQyj7yOOnzAgo6ZR1wykgg1/otD/g5v/wCCZItTJJP4ujC8HPh+5FfkJ/wU5/b1/wCCHP8AwUx8JK3jpvFug+ONOgaPRfFmneG5ftlqOT5M6syrdWueTBIeOTE8bnNfZ8NTzLCr2Fek3D02PFzZYTEx916n8saeDfDXxRt/7S8MttuVP7yAf6+H2Kn76D1FQeBtV+OH7OXjL/hPPhRrN94f1OH90b2wkZd6j/lnKvKyIe6Sqy+1ec3Gl3ngzxdcP4X1Fr2CxmKWepwRy2wnQfckWGYLJCSPvI44PGSBk/Q2i/tBafcWxtPiTZG5O0L9stgFk4HSSPhWHrjFfojyJShzW07H5dilisJK9HVH6c/Bj/guF460W1g0b9pfwPbeJQAAdV0KVdOvGx3e1cPbSNjr5ZgHtX6h/C7/AIK0/sAePUW1vPF1z4TuHGPJ8RafcQhe2DPbC4gwPXzBX81nxO1D9jPUPB+g634bm1WPWGDHVktkwoHQBUl4Vy5ABD7Aq9MnFfA3ijxTpUd/PN4cWW0sUA2m6dHkGP7zKETHsBx618vjeC8BU96UeU+tyLiXFVI25bH96c37cv7AGkaDN4u1v4w+DhZQf8+uoJc3DY7JZxBrhz7LGTX5ZftJf8F8/AOgxzeGf2NPB7azdAFV1/xIrW1uPRoNOjYTSD+6Z5IR6x4r8YP2Jf8Agkt+3x+33qMOqfAvwVPD4bmILeJte3aXpKqSMtFPIjTXePS1jl6YOK/tE/YN/wCDWf8AZE+B8Nn40/bB1Kb4weIo8SGwlRrDw/C4xwLNGMt1gjrcylGH/LEdK+Lr4HKcDJt+8+x99SqYmrFdEfx7eEvCH/BSz/gr98R49P8ACth4g+Kdzay4yira6BpZb1fEOm2eB2/1rY/iNf0ofsaf8Gl/hqw+x+Nv+CgPjFtbm+WR/C3heSS2shjB8u51J1W5mHZhAkA9HIr+zLwX4G8FfDjwzaeCvh7pFloOj6egjtbDTreO1toEHRY4YlVEUegAFdHKVK7vSvIx/FdZx5KC5I+R0Ucrpxd5anzL+zt+yZ+z7+yp8P4Phf8As7+ENL8HaFDhvsml26Qh3H8czj55pMcF5WZj3NfS1uixR7APw6Cqkl3HGh3dB3p1jf297kW7BgvpjjFfIwnOcueR6SiktDS+vSsTWLiLyvJPXGfyr8gv2Ev+C3n7K/7fH7Uvjj9lD4dadquja34UN3Jp8+prEsOs2unzi2uZrYI7NGY5Cp8uQBjGwcdGVfw2/wCCW/x2/wCCpek/8F3Piz+zx+05qHifXPCl02v3F/BqS3D6TYQw3Pm6NeacXHkQQzQssMSQkB1c7gShx6McM9b6WC5Y/wCCn37KH/BM7/gr38fvHHwz/Yw8baJpP7VnghJ2v7aOKW3s9fNjiO4s7uYxrBPNbtiM3UDPLB0mDxKdn8SXjr4ZfEb4NeP9X+FfxZ0W78O+JtBuDZ6lp1/H5c9rKmMqy9CpGCjqSjoQyEqQa/0Yv2Zf+DfPwv8As4f8FZdY/wCCjXhjxxLLoN3davq2n+GfsflzW+oa2kiXSyXgkxJax+dK0SeUrZZQxOzJ+3v+CpH/AARn/Zx/4Kb+A0uPEY/4Rb4jaTAY9F8WWkSvPEmdwtbyLKi7syf+WbMGjJJiZCTn63IOK1hZKMneP5HlY/LVUV0f5d3wj+OnxH/Z88Yx+PPhpfG2ulASeF8tbXkHUwXEf8cZ7dGU8qQa/oj/AGY/2s/hx+1XoE8egf8AEu1+3hDapok7h3jHeSEt/wAfFt6MBleA4HGfwm/bk/Ym/aK/YA+Ntz8B/wBpLQ/7L1KNGmsbyAmXT9UtFbaLqxn2qJEP8SkLJEflkRTXy/4H8TeIfAfiey8beDb6fTNX0yRZrS7t22ywuOMqffoQRgjgjFffYvC0sbH2lFnyyhKm7SR/X5efCvwLNIb2Tw7pbyuv+sOn2pJ/Hyq2tK0uLR2EOlRpa7MYWCNIgPwRVxXx9+xn+3R4Z/aNtIvAHj5rfR/HUS/LCmEt9TCjJlttxwk5x89v+MeRwPty6kjhkOBj1zxyO2K+CxmHr0Z8kj1qdaLV0akjSXC5mLMemWY9Kx3jEUn7sKoHBx3pmq+J/DXhXSjrHi7ULXSLLH/HxfTJbxjH+1IwH4V8FfF//gpZ+zP8O0kg8J3N14xvY+Nmmx+XbZHY3U2xce8ayVxxwlWfwo05on6IWtukkgfPBHHt7/SsH4ifEn4b/B7Qh4i+J+t2Wg2J+693KqNJjHEcf35D6Kik+1fh1Zft1/tz/tV62/g/9lPwjJpySHaX0eB9QuEGP+Wt9Oot4PXdtjx68V9AfDb/AIIrfH34uayPGn7XHjX+yZpyDPDayf2vqjDuj3Up+zw9ONpmA9K745dThrWlYtXatEh+Pf8AwV5+GHhe1ksfgXocviS6GFF/qW6xslPAG2If6RJ7ZEP1r5U0H4Lf8FRf+CjcUd/rcE+ieDbpg4l1Hdo2j+WeQUtgPtF2MZw2yUf7Yr+jP9nr/gnh+yN+zfLb33gPwlBe61b4xrGskajfZH8SNIPKhP8A1xjSvs+aM/aDPdEuc53N1/w/Ss55tQpe7RidMMA3rI/JL9kn/gjP+zP8F7m18R/GJj8R9cg2NtvovI0mF1/552QJ87BxzO7g/wBwV+/XgnUPCul2sa3sJNraqscFhZqsKlF4EeQNkMY7BBnHAr56t5fLk83PUcew/nV3xP8AFf4c/Cbwi3jT4qa9p/hzR4+Dd6lcR28efRd5Bdv9lcsewryMVi6+IsjppUYQPsHxN8a/H/iTSU8O2l2dL0O2XZDp1ifJgROoVivzSe5YnNfLXjTV/DXgjRLrxT4pv7TSdJsl8y6vLyWO2t4V/vSSylUA+pGa/FD9pD/gut4A0W+/4QD9jnwzP4+8QXLeTbajfQzQWRlOAv2ayjAvLvrwMQD/AHhXx3N/wT3/AOCjf/BQrWLT4gft0+K5/C2iZ823067CPNCrfw2ujwFLe1PbdOwlH8StSw+T29+s7Iqpi1tE+jf2sP8Agut8KvBHm+Af2P8ATG+IPiS5b7NDqs8UqaVHM2FX7PEoW4vnz90II4z2dxxXiP7K/wDwTi/aD/at+KI/aj/4KVX11N9pKSxaDdsFvLuNf9XFcRx4Sxs06C1QK5HDCPnP6ofss/sAfs3/ALJ0UMnwp0H7T4gKbJNe1DF1qcoIwQsm0Jbqw6pAkYI6g1g/tI/8FF/2WP2UrmfR/F+u/wBu+JIOP7B0Tbc3Qf0uJAwhtvfzHDgdENevSnb93hYnFUmvtM/RWx0yHyINH0i3SOKFFihghUJHHGgAVFVflVUUAKBjAHoK/GL9uL/grd8JP2eLu6+HfwLjtvHXjKBjFLOsh/sjTpRxtkmiP+kyj/nnCwUd5Aflr8l/2lf+Cof7Tn7Xm74a+EY5PCHhjVCIU0DRGklu74NjC3VyiiWfPeKJY4T3U9a1/gV/wSt8ZeLltvE37QU8nhvTeGXRrRlN/Mv92WTlLVexUbpMf3DXq4Xh6nh4+3xb+R59bHyk+SmeAaX4k/bl/wCCo/xosPhxpq6t8SPE1yxNnotmqxWFkuAWcRLstLSJR1lkIOOrE19Zf8FH/wDgjN8dv+CZf7O/w/8AjN8ffEumXmseNdafSZtF0mN5YdPUWjXKF719vnSkxsjKkQRcfK7V/RD/AMEzvDvgP9nj9pT4f+FvhxpdroGinUvsv2a0XCubmGSFWlfJeWQswG+Rmb36V9Af8HdPhh9Z/wCCc3grxdAuTofxD01mP91Lmyv4D+G4qKrDcUyWLp0qK5YBHK4ypOctz+cv/gjj4k0S08E+LPDZSFdUivEvFk2KJngK+WUMuNxRGVSFzj5+led/tJaXefBX9ow+JtBj8uG3vI9SgAwB5Mxy6cdgdyfSvnL9hn4iD4Sa34Z8bu4W0n1a/wBK1AD/AJ4utucn2UTBh/uV+lH7fHgr7d4X0zxlCvzWU8ljKwH/ACym+ZDx6MpAx61+lZtBTpOJ/MeYzqYTP/aX92X6H6Q/sya/bXniG0ubc7rXXrby19yw8yI/0H1r8CP+C63wbHgf9qzTPizYQ7bTx5osckxA4OoaURaTfiYPszH3Nfp/+w542utY+C+m3SODfaFOYOOxgbfF/wCO4HpSf8F1vANt45/Y60z4s6ZHvk8Ja7Z324clbLVUNrNn0AlNv+VfgeIpeyxLif1PluIVXDRkj+Qe7PyAvznpjtWG4zKGHGRV2eckiNhhg2PTp+FQNHwrdulJx6HbSehRRjHORjmlz5ZYHnk1Ylj2nzBj39qqj5mwMcjJqqNrluxVLLu2rxVRjhmwMH6VpXG5bjdxkr+lVHUifP4VrUqa6BYooF654Paq/wDCVFT8EhCO3FQSDYxA4rmswKXKt1+X2/Cq/wDDk9+RVqTAdowATmqpQ9B7VVhGXJ+8DDjpVLz25ReAf8K0ysiSmPg5FZsir8wUcrxWciiAk7FfGOcD9KjeIhSXOcfhU2GGEP8Ae/So5skbFOc8jPtSbBlFkO8KxqLeY8oBnsP5VO+VYE9BVJzulY8gjjHapmtCZIhmkGd5HHFZ8ztuU4rUuInkGTjA6+gFUJUGPlxheormuNEMnEYY884qCU5X61bnG6INjuKiZBjFZVCkQbhsOB2r9VP+CGuf+Htn7P4H/Q52P8nr8qwDyBX6q/8ABDlSn/BW39n8D/odLH+T1hA6Ybn/0f4GWGDt6VIMAe1NY5Yj1oAAAA69KVOPc4nsXVjXHpVmDKnjp2qjDu3bc8VfiXKn/ZppK5M/ItRACIZHerilAcN0PSq0f3sBuvUVajUKCEPA59K9BS7AiVBlgPVeKuLC4OSAnP8An8KiCgENxjFTRbTHvUAA1aexSLIVVHXHbgfSp40yhYA5LdKiiMiIHHI9KsRcAM//AC0IP8qF5EmjGOGOAPlGMVIu1SGA6impkoeMVbjPRZOmKFKwNEsGQhq0gCD61FEG2begq5HGZFBrb2mhKjYmUfusMKtxn5wD7cU2NW2D8OKnCMpqo2aJv0GySEuNvHYn6VbgjUt34xVXafNHAwf0rVs1TaZHPHp9a3prUir0NOJGxjGOmD0rXsbhoJTbtxz8uPWm6ZZvczLboCzP046flX9JXwB/4JwfCf4H/sPeNPjD+1d5eman4m8OzGJ7mMF9GgcB7U7Dg/a5phEdo+YLiPuwr6nhjD1IV/bbI+F4s4nw+EUadTd6JI/ADwtdm5hm0ubjy/3sY/2W6j8DiuuhtmKYZcGuT+FWr+DdC+KOhap8SrVr7w/BewrqsCSNEzWUhCTMrJtZWRSXXB6r71/Rpr//AATM/Zxhmb7G+uWiH7rJdZVlIyjL5sL/ACkYK89K+wz3xJwWT2+tJ2fY6cDw5WxutI/AiOJchsYAwOelaksqKdoAx16V+4dl/wAEvvgjd/6rVPEsg/hWOSA59uLY13On/wDBIL4farKsenaJ4x1bGOFklCkH3itk/mK8D/iY3JkrxTfyPT/4hvjXu0fz43MvnIEUflxT7GNLeXdPcLH6ZfH9f8+1f1ZfDf8A4Ia+Hb/y5V+FchX/AJ665qUqjj+8j3IP/kOv08+FP/BGfwr4E019avIvCPhC2s0Ms89nYxzPDGo+Z2uJEhVVUDljJgda8qf0h4Vp2wmGlI6l4dygv3tRI/hW0bwF478aqI/Bmj6trO/j/QrWeVOP9tV2j8xXsPgf9hf9q3x/fw6fpHhc29xcP5aR3d0DLz28i28+X8Ngr+kL9rb/AIKJ/wDBI39ju0n8N+EbvUv2g/GVllDaaZdJBocMq8fvtQjUW2M8YgW7PY7a/m6+Nn/BS/8Ab2/4KAeLx8B/gzpU/h3SNXJitPA3w6spkkuIzj5bmWENfXYx97zXSDvsVa9KHGuf4z35U1SgR/YGCpaJ8zOq+IfwO+CX7NgfQ/j940i1TxPD/rPDfhqKK6uI3HBS6m8xorfHcTtFIP8AnielfC3jHxH4b8Vaza2XgvQTpKSt5cFvFNJe3VyzH5AdqoruRjCwxCv6MP2CP+DVz9rr4w21n4n/AGwNZtPg94ffY50my8rU9elU4OCFJsrQn+8zTup+9HX9n37EP/BJv9hH/gn9YxXX7PXge2TxCI/Ln8S6p/p+tT8YO68mBaNWHWOARReiCpnxt9WVufnl+BUchjPpZH8I37Dv/Buf/wAFBv2uY7DxV4/00fCPwfdbX/tHxNFJ/aUkZxzbaQpWfOOhuWtxjkbq/ra/Yp/4N1v+CeH7HlzZ+K9X8Pn4l+MLXEi634sEd4I5B/Fa2AUWcGDgqfLeVcD94a/f0DHAHFVriSOAGSQ4FfCZvxPjMSvelp5Ht4XLKNL4UYVjotpp0apbxhQoCrx90DsuOg9AOK3ofkwleO/GD4z/AA8+Bvwu8QfGT4o6pFo/hvwzYzalqV7MDsgtrdN8j4ALMQBwqgkngAnivz5+G/8AwVB+GP7Xv7EvxF/al/4J+zDxxq3g/TNTNpo99bT2dydVs7Vp4Lae2YLMBN8jJt/1ithTnp83To1JPmO9ySP1rllgtojNcMsaqMsxwAAOSc9uK+eLD9qT4GeOfhj4o+Kfwd8TaZ470zwjDdvqH/CN3cGpOslpC0zW4Fu7gTMq4VDgkkYr+eX/AIIff8FEvj9/wWM/Z5+O37O37Wd1bT3kOmJZRa7pNotkwsvENtd27QtFGdgltTEWjIwxVgGyV3Hqf+Dfb/gkL+1p/wAEx/iT8WtZ/aEv9I/sfxDb6dpelwaTctOt9/Z8lw3290KRiDckoVEbL8sDgKufRlh1G6m9UCZd/wCCMv8AwXU1P/gq38RfH/wS8b+DIfAmt6Lp41vRnsrl7pJ9LklFuwm8xU23Nu8kO4r8jh/lC7Tn5B/4N7v2Uf8Agpp+yj+3f8YND/afsdfi8EzWNzFc6jq1y89jq2rLfKbO9smdz5pktzMzyJ91WCSYbCj+lL9nj/gnJ+xX+yZ8U/F/xs/Z28A2HhXxL45bOr3dqZTvUyea0UETu0dtE0p8xooFjQtg7eBj64VLeBzIOCP0qamLjCLjCOjFyn5F/s6/8EVf2Sv2Xf27PEv7fPwum1eHxB4gGoNFo0s8Z0uwn1Zw99LbIsSynzSDtSSRkjDMEA+Xb+tcNnEsoLcjtngCuI8UfFLwj4eJhuLkSzDjyYvmP0OOBXhetfG7X9UbytChWwj/ALx+eQj+Q/KvMdac/iKR9eahq2j6HafatVnW3Xp83f6Ac15D4m+MDqTZ+H4dpY7UkcZZu3yp2/GvnqXV7qVH1LUJwSEZ5ZbiQKqoi7mZ3b5UVVBJY4Cj0Ffzv61+1J8eP+Czf7Tuo/sQfsC6xeeEvgh4cKf8LE+JljmG8v7RiV/s/SJSP3C3W1o4pB+8ljDTfLAoWb0MPhW03skRKXQ+/Pj98I/g9/wV/uNd/Zc8R6UPFHhbwvdyLrHjGORQuh6yqYW00W4AYT6ony/atuba3j/dT75HEK/wif8ABST/AIJcftFf8EwPi0PAfxZg/tXw3q0jnw74ntoillqkMfJVx832a8jH+ttmOR96MvHhq/1aPgN8CfhX+zj8K9C+CfwZ0a38P+GPDdqllp1hbLiOKJPXu7uSXd2yzuxdiWJNeIf8FC/h58APiz+yj4o+G/7ROhWfiTQNUgEKafd8eZeN/wAe7QyDDxTRN86SRlXTbkHivbyHiWphanufCcmJwMasdT/Hwt9UazuobyKVreWB1kjl3GN45E5V0YEFWU9CPTiv0d8G/tCf8FNv2ltGtPBfwWTV9ZFvGIZNT0vTkiklx0e51KRfKV8dXDxk4z1r+l34X/8ABP39ib4N6lFeeCvhro7XcQAS71JG1SfI/i33rygH/dA6V9pySxf2emn26LHBGAscUYCRqPRUUAAD0FfWZhxbCqtIHj08r5WfyzfC7/gi3+018VdXi8UftSeOLbSJJCN8Yll13UR6qXZkgjPHaSQe1fq78Lf+CRv7FfwmWC+1HQbjxnqEWD9q8QzCeLI9LOLy7bHTh0fHrX6LNL9lJ2cewrTafz4FdOeK+Yr5xWasnZHfTwkUc54a0PR/DGnQeHvD9rBYWFuNsVtaxJbwRDsEijCoMfSu6G5k8teBjoOK8s8WeNfCfw+0STxb481Sy0PSbYfvb3UbiO0t09vMlZVz6AHn0r8yPiV/wWc+A9lrJ8Bfsu+HtW+MfiRvkjj0uGW3sd3b94Y3uJl/65W5QjpJXBGnUqs6rxhofsBDBK1ziIZLcKAOv5V8aftK/t6/spfsvRzW3xR8WQPq8I/5BGlL9v1A+zRRHbD/ANtnjHoa/OTWfhJ/wV//AG4oNnxY1q1+CPgu8HzaXZu0Nw0R/geK3druU4H3bi5hX/YHSvov4C/8Ecv2PfhGsN94q0+f4h60hD+dre0WfmD+JNPhxCR3/fmU+9ehDBUoP33dmVSu2j4S1D/gqL+3H+2FrEvg3/gnj8MrjTrLdsOu3aJdyoOxeaXZp1qcc4ZpmHbpXovwl/4IvfF/45eI1+Jn7fXxQvNX1ST5pLHTpjeXKj/nn9vuh5UQHTbBBtAPyt0r9FPjJ+3Z+x3+yxZHwn4l8T2KXGnr5cWg6BGt3PFtHCeRbYihAzwsjRgV+SHxd/4LqfFrWGuNH/Zs8L2nhe25VdT1Yi9vcdAy24xbRH2czYr3cFl9ep7tCFjzKmLiviP6BvhJ+y/+yd+xN4SuPEPw/wBF0nwXZRx7LvXdSmX7TIv/AE21C7ffg/3A6r6IK+A/2jv+C2H7LHwvhuNE+DNrdfEfV0BUSwbrPSg3vdTKXkH/AFyhZSOjiv51LuX9r39uvxcNX1OXXPiJexEgXV25+w2uQMgPJ5dpbjHRUA9hX3L8Gf8Agk7cXc0Op/tB+IvLQYLaVoh5P+zJeyLx05EcfTo1el/YmHormxU7vsczx7elNHyT8ev+Cl37bv7Vepv4FsNVn0TTtRzCmgeFYpY2nB/gkkQveTg9wXCH+6BXT/AP/glN8Y/GzQ6v8XrlPBOmsQ32ZQtxqTr/ANcwfKhJx1kYsO6V+93ww+AHwh+B2m/2N8KNBtNDikULJJApa4l4x+9uHLSyf8CbHtXoJ8uLMSVx18+pU1y4aNiI0ZyfvHiv7PH7NHwW/Zx00Q/DjR1t7uRNk2pXJ8+/nHT55jyoI6pGET/Zr6TuHbyTFjA6YHv9awIAUA4O0e1biksMtz/kV8xi8VVq+9NnbSpRirIk8IeIJ/A/jXSPGVsNr6TfW16pPH/HvKj/AMhiv1r/AODlPwlD8Rv+CMXxA8QWi+cNDvdA1uMjn5U1S2jLD/tnK34V+PeqWZkj2TD5XQ8ex4r9K/8AgoL+29+x1c/8EZfEXwU/aE8faZovi3xt4FuNJ0zRQ5udSm1K3iMdsws4A8yxtcxRnzXVY1ByWrGjRft4TguqPQpzjyNM/h0+BmlNr3wD8bwRIA+haxpuog+kF5HLayf+PCOv2oi1PTvjH+xD/wAJHr1zDAf7NNvNcXEiRxreWB4y7EKC2wcZ/ir+czwJ8YfGXw08Ka/ougNbQW/ijT4bDUXuUWQrHE4kHlEnajBuN2OnSvrL9mb/AIJt/wDBRX9vCztm+B3gHW9Z0B33pq2qsdM0NN2N0kc93sikPHIt0kb2r92xtelSheo0tD8Ozjgipj8Rzp2s7o+g/wBlz9tz4MfAaLXLTxld3d5b3ojlgi0yH7Q3nrlWByyRrlCOS3610X7SX/BXDwZ8Z/2bPEP7M9r8PL6WDxBYTacmo3l/FEYAZBLbyiCOOXcYZFDbTIM4xmvvG3/4NkvEvwU+HcHjT9q34sQxandzR29rofhO08xXkPzPuv77bwiAklbYex5FeWftb/sS/wDBNn/gnl+zfpnxZ+J3hHVPG3ifxTcT6f4U0e91e6he/e32m4vbprdohDZ22UB2R7pJHVFxksPzytUy+viPd1Z+kYDC1cNRVK+x/LvceG3Zy1tJuYAcFcfN+H6dqzJrC4tZvIuQVft3H4GvsW31r9nn4k6v/ZPiHQU+Gkty37rUtJuLu/023J+6LuzvXnuPK4G6WC43IPm8l8Yrl/iJ8I/FHw08RXPgDx3bpFeRIksckLrLBPBKoeC5t5l+WWCVCGjdeCPcED2KvCMK0f3ejKp5rKLsz5Zu0UW+D97txWSXKurnGOK6XXrM6bePZyHJTgHsR25rmnwCVPB44FfnmJoOlN05LY+koVlKKaFkJkZfRRxVRwxOcZ6VaDDaPaqzHBGB1Nc7NvIqyDayjHaqlwAWBHHatC4DEqgGcVRuFIde/wDSoGVGjVWLetUSW+Ujptq+0e51x1J4qsoXaBjoMU1HoJMx5lMbl92P88VX2NJuXGCxzWtJFGfTtVGYb2+TgrWUyylIi446cfhVMhnO5fStJiFRnIGCMVScLsBHcYH6VCEVWIVufTgCqDI6OWxgMOO1aLpsj3dPaqjHb8mcg/SmOexU5yUWqUq7Y/c1oOwywA61TlUGLHFcTvexmiCcDyFB68VFIMcj0qeViq5YnnAAqsc4x2NKUdDQjUYPNfqt/wAEO+P+Ctn7P23j/itLH+T1+VPNfqz/AMEOE/421/s/DsfGlh/J6xgjaif/0v4HTEAc+nFJ0B4z2pST355pUWQqQvTpilGT2OGxKnyc9K0ItmSR17CqgDk846dPSr8AKD5qtR95EtFwF5PvY6fTFPRNgyfSmQhWYkYX2q0CCpYj29K3StIpaFhFGwdCtPhCbVVRimbiqAY/yKls9r7c9MV0NdhyetkaYVlhj4GcGr1lGXjUgcc49qppHuijCHGOn0zWhBmJU28jB/nUX0M4pp2kO3nGxa0FiEm1VzgfyquBiMy4zjjj/P5V1mh6Xa6kqG4uR7xr978c/wCfyrqw2DlWlyQMq9flRkQx7yIoxk9hj+grqLDwxrN4q+RARnB+bA4r0bQ9K0iznjTZsTIDsoDSKvcgErzjoMj61+oH7Pfwd/YJ8e/Z7DxZ8QdWt9VlOwWV5Fb6OpPQbZZFuYyc9P3uT6V9hDhunShzV39x5MsylJ2ij8m18B6+qgqIx6/MOMVm3Xh3WbMfNBvAGcqQR+lf1Gz/APBMD9lfUrGNrLWvFNgGj4mhvbG6jLY4YJNZKGX02yY968L8Tf8ABGLQ9QeST4ffGGKD+JI9f8PSKv8AwK4024uP/RH4Vy1MNlz0u0axdZan85ex9+yZSD6EYrZtYCGCKeT2/Kv2wv8A/giv+22GcfDi28L+P41x8uga7bx3Ley2mrLYT59lVvSvlD4ufsMftXfAgNcfGv4R+L/C0UQy1zd6Ld/Zhj0uYY3tyPcORXTg8owsvgqoVfEVlH4T9Jf+CNv7Atr8RNYi/ag+Ldis2g6PPs0ezuF+W/v4/wDlsQeGgtmHT7ryYHRWFeQf8FkP26Z/jp8Uf+GffhreGfwt4WumN3LE2V1HVOjtkffih5jj/vHcw4K48ptv+Cvv7Smh/BiT4DeFJfD9rZw6edLtZ7K1+y3djBt2fuVhdUD7Scs0edzFvvc1+angHxJ4d0PxhHrvim1nuI7ZS1sLfY5E/Z2DFcheox3xX0GPpuFNUqGvofkmW8M4mrmU8xzDp8K7HT+Jvh9f+EDY/wBoN532613SAc+XKOJYj67Rt/pX9+H/AARF/ayT9qb/AIJ/+HdD8RTi88RfDVv+ES1Lfh5HitUDadOcjOJLMome7xPX8PnxC+IXwu8U/DWW2tL+VdVtpUuLSKW3kRmk3BZVLYKcqeDnquK/Qr/ggF+2BoP7OP7bkvw58e6vb6T4S+KOm/2VLNdyrFbQ6raFp9OkeR2CLvJltgzEDMq54ry+I8nWMy5KcbtH6Tw/jpQqXeh/oCeG7hm5hCoU+XaqgYx9BXoM8Mk0bSM/yopdyzbVQLySW4AAHXsBX42ftof8Ffv2O/2FbabTdT1dPG3jd0DReGdAmjnkyeVa8uhuhs488/PmTH3Ymr+P39s7/gqN/wAFAv8AgqD4ph+DcD31roOuziDTfAHhBJ5EuySNsc4izc6g+ME+afKHJWNRX59lPAsqkeeUFGKPsK2dJaJn9U37dn/BxD+xn+yNc3fgP4FmP4xePLXMTwaZOI9Ds5hx/pOprvWVlP8AyytBKeMF4zX8qnxf/bN/4Kl/8FnPigvwjs5NZ8ZfaXElv4K8LQPBo9rHn5XnhRtmxc/8fF/K2P7w6V+s/wDwTj/4NSvih8Rk074lf8FDtUk8FaPlZE8G6JLHJqkycYW9v03Q2i8YMVuJJNpOZI24r+5v9l/9kz9nL9jn4Y2/wm/Zn8HaZ4N0GLDG30+La8zj/lpcTNuluJccGSV3c+te9HG4HL1yYWClLuczp1a3xuyP4zv2Gv8Ag0n8V67DZeNP+Chfi46PB8sh8JeFZVkn/wBy61Vl8tMEYZLWM8fdmFf1zfsvfsI/so/sR+Bv+EF/Zg8DaX4NsHCrM9lF/pVzjgNdXcm+4nb3ldj6V9omMB8cYqtfJ/o+5CB0/p2r53Mc8xGJXvyOulhIQ2R+Os37b/7SP7TXjTxF8PP+Cc/hHSrvRPDOoz6LqnxF8XyzQ6Amo2TmO7ttLsbX/TNWe2dTHJIJLa2EilRM5Bp/7NfxS/bR+Cf/AAUBi/ZD/a8+Ilj8S9H8eeCLnxX4e1K30S30I2eoaRfRWuoafFFBJL5kBguoJozLI8gwctXxH/wT/wD2o9E/Yj+Hnjn9kvxXo2p6/q/hX9oDUfAek2OmQ+bP9j8V3h1uwvZuyW0Vrdyyyux+7EQOa+u/+CquszfAX4o/sy/twRDbY/D/AOIcXhvXpeixaH4yt20m4lc9NkVz9lf6gV5sVbQ6D9Cv23v2t/BH7C/7LPi79qr4hWF3qml+EraKZ7OxC+fcSTzR28MaFyqrullUFmOFGT2xX5SeNf8Agoz8S/8Agot/wRh+Jn7VH/BN7T9S0X4k6fZ3mnwaTKsc2pWN9aNE12luE3JLObJzLaMoyzMmFD/KP2s+O3wN+Gv7THwY8SfAT4x6eNV8M+KrGXT9QtyShaKQYyjDlHQgMjDlWUEdK+af+Ce3/BOn4C/8E1/gVdfAT4CzaneWF/qc+r3l5q86T3dxczIkWWMUcUYVIoo0ULGowuTkkmuqEoqN+oj+er/ghW/7TP8AwUe/4Jg/Gf8AZi/b2ufEeq6DqlzdeH9J1/X45v7SltL6zzOgkugsk5sLj5kdwQGYR5wmB+iP/BEj/gj34i/4JR+D/Hmn+MfHUfjTVfG97ZyM1paNZWtvBp6SRw4jeSRmmk81jI2QBhVUYGT+4d/Pp+iJ9ov5khT+85CCvJNY+OvhLTRJFpO+/kT/AJ5jan/fTf0BrGvmVRpqKshKJ6d4A+Ffwv8AhiuoP8NfDml+HjrFwby//syzhtPtVy33pp/JRfMkPdmyfeu11HVdM0i3N1q1xFbRj+KRgo/Wvy5/at/b8u/2bPgtqXxb1CwaZYLiz07T9MsyhudQ1LUp0tbK0SWbEcRlmcBpXGyNcsc4xXxvqfwu/wCCgP7Qc/239ob4nW3wu06Xl9C+HiC91YDp5c3iTVI2EbDGGNhZQj+6+OamM7q8hn6eftIf8FAf2bP2Y9Ih1P4peJdP0cXfFot9Lsmum4AW0s41e8u2J4C28D5Nfk18dv8AgqB8Z9L8HX/x11P4P+MLb4S6KIrnVdcv2ttEu4dPeRI5b230GZn1K4gtwfMk88WzeUCwQ4r6c+An7H/7OH7P+qTeLvhd4ZgTxNdqReeJNUll1bxBdZHJm1S+eW5IbuquqeiivePHvgfQvG3hzUfCXi+zW+0nW7SfT9Qt5MkT211G0U6N/vxswpQrQ6oZxujSWWq2MOp6ZMlza3EaSwyxnMckMgDRurDjDqQR7V21raQrGJjwowSelfmN/wAE8PHX/Ctfg/rn7Jnxh1NIvEfwD1U+EZZ7ptr3uihPtGgX4HVhc6e8acDHmQuOor6z1j9pPSPIlsPB9obpidn2mfKxgeoj+8fbpWkoNOyI5lY/Bf8A4L1ft4ePtb8VaT/wSw/ZfWa68S+MDZW/ic2r4knOpug07Q0ZeU+070lu/wDpkUjOAziv6Uf2Cv2Z/wBnb/glN+xvoHwBfV9Pt9Tt4/t/iC/ZlE2p6xMq/argIPnK7gI4E2/JCkafw1/n76X8X4vhZ/wW11r4uftK3gsfsnxA1iS7v5gdlo9zHPDp10P+ecUQkgZHBwkYDDha/rFuxJeQR6g7+f56Bkn3iUTI3IZZcsHVuoIOCOhr6TN8BKnQpwgtGjzsLiLzlzH6NfE7/gpLo+nM9h8KNIe/kJI+13+YIR2+WJf3je27ZXwD8QfjV8R/jJqSav4/1F7xod3kRqoihgDdRFEvA47nLepNeMXdjJFds3B+laVlFPswnGO1eRRwyjGxvKqWdypzip4SOcDjGSew+pqGZZYwM4z35/D+Vc5qHg/TPFsX2DW9PXUoTx5M2ZITj+9ETsYdPvLWvLJrRGLxHKfNPxT/AGuvhJ4F1CTw54aF/wCOPEEeQdI8L2x1GUMMcTTqRa2/v5sykD+GvCX1b/gpX8ekNh4GtNC+C+l3HSecrrmtiM8A/dFlE30Vip/ir62+JXxv/ZY/Z00drH4ieL/D3heO3HyWEcsXnr7LZ2u+bjsBFX5rfEP/AILi/AHwUJtP+CnhXU/GlzlglxqBGk2GexAIluJF9vKiOO4rswuU4mvZRgc8sfCD1PQLf/gj/wDCrxf4mg8dftUeKfEXxX1uLGG1y+k+zhv9iGJlEaeiBgMdsV9hSeMP2Jv2C/DS6Jrt/wCHfh3bEblsLVI47uXb6W1uGuZuOAdnPrX81f7Q3/BVz9t743RS6bZ+Il8E6bNwLDwxGbRyDxtN0xkvG99sij2r5H+G/wCyn8dPifqH/CRPpktlDdtvk1HVWaNpM9XO/M0pPPIHPrX2eF4QqR0rux4eP4nw9GPNKS0P6Avjj/wXH+G+lRS6Z+zf4OudenIONR1x2sbXHTK2sRedxx/E0P0r8QPj/wDt6ftaftCzz6f8Q/F91BpUxIOlaV/oFjt/uukREkoH/TZ3r7B0L9hX4R+EvC8utfFTxLfXAjXMklvstokY9NilZGcnt6+lfn/49+Dtpc+LP7J+Fhu71LmURWdvPGrXUpOAoxEMZPpjgV9JTyrBYdJpHyOF42hi6jhTeh85SWaGNYrdFRP9kYFfQ/7N3j/4ZfCnxyPEnxS8D2fjuxVVC2d5M0YgKkZkjQboZGxxtmRl+lVPGv7Ovxy+Fdqbjx/4avbS3XA+0InnWw/7bRb0H5149IhiRh+WOlfS0adKpT93Y7/ra5rXP6Y/hd/wUB/ZT+Ilta+GdP1aPwlKAIrfTNUiSwhT/YhkQm1wOgw6/TtX2Zb6hpf2Fda+1Q/ZCMifzU8nb6+ZnbjHfNfxg2mmapr+q2uhaTbyX1zdyLbwW0StLJNK5wqIigksc4AAr9PPhT/wSa+M3jS1guPi9qMHg/TXIY6fAftt6c9jGrC3iPbl2I/u18HmeQ0ou7me1RxOmx+sfxS/b8/ZQ+FFvJBe+JE12+iODaaIn21t3o0ylbdPTmUH2r4Ss/8AgqL4y+J3xS0TwD8GPANsU1vUILKN9RvHlnZJGAZ9sCrHGEXcxO5wAPSsz4m6N+wH+xT4ek8MeFtBtvH/AMRbZcRrrEov4bJsD99doAtpHs6iBIvMPRtq817b/wAE9P2VPEWjTT/tR/FyDHiPxBFIdMgkjVDBaXP+tuWjUKInnX5Y4wB5cPGBuwPPnl2GpUHUfyNo4mcp2R+nELeYN0RO1TgZ9O1TeIfFnhvwF4T1Dx54zvY9P0nSYTcXly/3Io14z0+Yk4VVHJJAAzWrHpwig2MMZ/MgcACvwf8A+Cpf7TUWs+J0/Zq8K3Qex0JlvdekibKSXgGYbQ7Tgi3U73H/AD0YA8x14GV5Y8VW5eh3Va/JHQwv2q/+Cq/j/wAX2k3hT9nO3bwxpUh8pdWuFD6pcZwB5MfzJbbv4cB5fQqeKT/gn/8A8EUv23v+CgPxQim1aL/hCNK1Jftt7r/ijzGvZYMjMsVkSLmdjn5TKYo2/vYr9m/+CYf/AAT++HvwG+Deg/HH4gaTBqXxH8T2keprdXSLIdItLld0FrbIwxHKYirTS48wsdgIVcH+h/8A4J+alb2Px1vbO44lvdLlCdMsUkRj+lejmud0sJelhVt1LweElPWYv7DX/Bvt/wAE8P2M47DxRf8Ahz/hZPjSzCsdf8Uql1tlA+9a2OPsluARlcRtIv8Az0Nft3JZQrbrbwqERQAqqMAAcYAHQYrn/Eo1S58Lalb6Cdt89pOtsQcYlKEJj0+bHNfO37B3xsg/aL/Y/wDh/wDFsSM91f6TFBfCQ7pEvrMm0vI5O+9LiKRWz3FfB18ZUr+/OVz6CnSjBWij4A/4KU6vPH8R/DPh4uwgtdKu7pVB+TzJZkj/ADATH41/F5/wca6x4k8U/wDBQnwb8EdDilvIfDPgHQdP0uzhB/eS35luZmReBvclAfUIOwr+un/gs98Wfhl8Cvip8Jde+JOqJpcPipdV0GAupYyXB+yyQqoXpliVycAZGcV/Kt/wXjsv7D/as+An7atmhk0rV9AttF1CXHCX/hy4aK5Qns32a5Qj12HHAr3OGpOjVU7HlYyN7xP50o7G8066ktdSheC5gkMcsUg2srrwysp6EHjH4V+hPgwf8Lv/AGQfEGiagom8QfBwQaxpkxGZG8N39yttfWZ9Y7O8lguYR/yzWWYDANeU/tceHtO0f4nWuq6ewDavYpdSBed2GMaye/mIoI9cV7T/AME5bdNZ+JnjvwpcZ+x6p8L/ABpDcg9NkelPOh/4DLChHuBX7llWJc8N7Vo+HxdP95Y/Nb4g2od47iLGVOPqG6V5VJGFyWJzXqOuyvP4ehmk+8EU/wBa8wlLjdu9c5H+FfmvGVGKxXMup9TlGkLdiuT8pOOeOlR5+RW/Cp+SG21CqnywBzzXyB7A5AcelU7lTtDelW8hSQO1QS8xkjp7VKQzJVy03TG0ioiqqNzDvxVxvkbnnJWqLr+6H+9/9atZbiRVdUMnuKzrltsp57AD/P0rTnAEmAByOc/hWdIoD5bAHXmsZLqDRUbEcTfT8KpH5kX8KvzRhQwcAZ4/Piqi7QmSOOlZbFJlK4ZEJ28Y61QClhjHIPUdPatKYkYLjjOMYqOQfN0xx+FZ1J2SJnKxRZUYMDxgDpVKQAIfT2/lWkVZtzD+6Ko+WrRtnniuWY4tFWUqY8kcY61AOR8oq1L8kIT6dKaThdg6+9KUtB3KzYUZNfqv/wAENsf8Pbf2fV/6nTT/ANA9flRkFTur9Vf+CHDFf+Ctn7Pj+njSw/k9ZQ2NqWh//9P+BwYwWNNTJGV4xTwY9hUcUsMYPJxxRSbtY4my4u4EN2xg9Kuwr8mffiqe0IwXqCBVyDnHGccYpx+KxJoxf7VTqDsOOwqCDirCthDu7iu1rUC0CFdc1atmTAJwOtVmwVB6YGalt0C7WPQjtSje/kVF2ZpgqR8nGBirS/L5aj8KoBIVAI4BxWlEVUIfUUThpYJK7uXBIMEHpgYp4Ckq4Own04qskZEJkBxU8eSqgnPf+mKqm3H4WY8p01nr2p2pVQ/mLxw3P616BZeLrSdPI1CPbxt5+Za8stfuByOCBWqV24Z+/wCVe5hOIcTS03Rx1cFCR9TfDP8AaH+MXwhmEnwo8S3ulwBgxto382zbH9+2l3Rc/wC6D6Gv1A+C3/BWHV7Uw2Pxw8P+aq/e1DRW+bH957SVsH32Sj2WvwlhjPmfu22kdxxxXVWWq3SyjO1+nXjH4ivbo5ng67Ua8bHDWwtSmrxZ/Yl8Iv2svgh8Z1it/AXim0u7l8H7DcEW90G/695wrk/7mR796+9fBH7Tnxr+FsezwT4k1HTUGD5CzsYRj/pjJvjP0Cj0r+Nb4L/sf/tD/tC+GB4o+Enhp9eVFllFvDKguTHAQrSxxuVLqGOAEyxI4Xium039p/8AbB/Zl1V/A1/qup2MtkAJNF8RQPL5a44Hl3IWaNT22MvHSunH8Gxa5qEjz8v4npTqOinqj+uj4gftCfDj42LJb/tP/CLwL8Sd67WuNY0O0+149RdRLvU+4Ar5b1T9gb/giX8YLk/2x8KPEXw3vH63HhHXJ3iU+ot7t5oxjrgQY9q/Gf4cf8FZNNnmFl8ZvCUtnj717ocokX/eNrOVYfhM30r9CfhV+13+zB8WLqC08JeNNPjvJSAtnqJNhc59Atx5Yb0+QtXzssBi6OiPeWJjLc9J8Xf8G937CXj6FpP2f/2mNQ8NyFP3Vl4x0i3nAPZWnhOnfThWxXxn8Qf+DYH9vrToHv8A4K674C+KNljcBpWrtZTyA9vJvIhCD/28e2a/W6KK9t7ZTveNH5Xup+nqPStOy1G+06cXNkyxyDpJHmN/ruQg1dHOsdDqL2VB9D+V34xf8Env+ClX7PayDx38B/FttbRfM9xpVh/a9sAP4jLpZuUx9SBxWv8AsJf8FNv2jf8Agld421e7+F/h/wAOQapqzD7cPF+hvHqHlKNv2dLrzLS7igzgmJDtLclTiv64NG/az/aJ8ISR2/hrxVqcaoAoje4NygHpsuRIuOnSvUfFf/BTjWvB3ho337U58IapoWOW8UW1uiuvTCqzKrk+ixMfQdq9efEtetT9jVp3XkYrCUoO8Wfm78Nf+DwHx3Z2Ef8Awt74G6fqDcbrjw9r0luG91gu7ST8B51fXfhr/g8J/ZguofL1r4PeNLeULkrDcaVMnHYMbiM/+O/hX5Kft0/8FYf+CbPjfwxd+Hf2cf2VPhxqniWUFf8AhKL/AEGC202DjHmQWohguLpu4M3kxDAJWQcV8Nf8Epf+CJH7Qn/BSX4iWHjfXNPn8I/BoXwk1XxFPF9mbUIt26W00aEqPMZ8FPORRBAOjMyhK55ZVg1SdavDlOmOMnzKMNT/AEb/APgnf+23Zf8ABQj9mfS/2pdB8I6t4N0jXLq6h0+11gwNcXFvav5Rul+zsy+U8iuqdzsJHykZ+6J1Ei7TXnXgHwv8Lvgj8OtE+F/gGzttD8P+HrCDT9N0+34S3tbZBHFEi8nCqoHqe/NY+q/FW1h3ppVv5zDvIdo4/wBkZNfmldLmvDY9yOx+OrI37LP/AAXbaW6/0fw9+074AwrHhZPE/gpiGX03SaVP9Ts9q+0/+Ck/ww8AftE/sH/FH4DeOtWstFtfEHh67hh1C9njt7eyvo1E9jcPLIypGIrtInzkdK+Z/wDgpb+z78Wf2vfAPhDxJ8C/Eln4J+KXwv8AE1t4p8Ja3dWzT2cMyRvb3Ntcoqu7QXEEjB12kFlUEben5W6b/wAEWdU/aG8YwfEn/gqd8ZfFHx+1KGTzY/D8bNofhe3bOdiWds/mOF4AKGDI4ZTXTFRspNgfvN/wT0/bMsv2iP2C/hN8cvEO+fWvEXhqzkv1jwVN/bqba8+bOMfaYZMEdRivoLXPjF4kuwyaXGllH0DD53/M8D24r5y+G3gvwX8MPBmmfDn4faVa6FoOh20dpp+n2UQhtrWCMYSKKNeFUfr1616SISygdm4GPpWXtb7DRwuvG/1e6+26lM9y3rIxbH07D8Kx7eziZfm6duK7PX7zw9oNsbrXbuCzQAkGZ1jH/jxr5j8SftMfCbRWkg064m1SVT921j+Tp03tgY+ma15eiM51Yx3OK/bO/Z0i/as/Zc8bfs9+Z9nvfEOnt/ZNxkA22r2pFzp1wDxt8u6ijOey5rov2Bvj9P8AtcfsleDPjfqkP2bXLyzNj4htMYaz17TXa01OGQdVK3MTkDj5GXivE/EX7VXiy/3f8IzpcOnnPEkx86TH0+VRX5a6J8TNQ/ZB/aC8Tnxxqg0f4WfGrUv7cGoySfZ7DSfGDRiO8guiCIoIdWjVJopHIT7RGycbhWlLDtwsyfap6o/oy8TfEz4ceBwzavfpJcA48m1/fSZ9wOB+JFfP/ir9p3Wb5WtvB1pHp6fd86f97MR/uD5F/Wvyf8dftffD9NQuPBPwTtrv4m+JYMCTTfCix3cMXcG81HeLG0Hc+bOHx0Q1y+ieDv2wfi+u74m+KbT4WaOx+bR/CJTUNYK9Ns2sXaeRC2Rg/ZbVv9l+hreGXpLmZjKvLaxm/tK6ofBP7a3wu+L1xfLPrHxDM3gTW7J5F+1Xdo0U1/pl6IQckafcRSRs4XasVwQTgV9p6XcLHk9ewOR2+npXBfC/9lj4L/COe88V+BNAT+254iL7X9Smkv8AVp4yPm8/UrxpJghHVUZYxj7oFfDf7QX/AAVN/Yz/AGeZ7nR5fEn/AAmOuW/ynS/DIW8AYY+Wa8DC1i6c4kZh/c7V6dDC1K3u04nLVrqOrOc/4KM/8EyfCv7ZMqfFT4f6jD4c+IltbpbPPOrGy1WCPiGK88sNJE8a/Kk6I3yYR0YBSv8APdrniz/go9/wTH1u1+G2o65qvgmKUNJaWKXltqOlzhcZkht3M8Cocj/llGfUdRX0F8ef+CzP7Vfxhgn0P4SfZ/hfoUoKA6bJ9o1SRTgfvNQlQeUf+vaKIjpk1+U0/g/4heL9Qk8ZalBeXZ1CY+bqd8ZGaaQ8ndPLlpGxnvX6VkuU14U0sVbl7HzGNzejF72Z+jmnf8FoP28Le2SDUL3w3qbp1kudEhEh+v2d4l/IVtJ/wWo/bft1VR/wikBPddGGfb787D+lO/Za/ZK+FPiPww3ibx7DJq1zBMYhAZPKgxtBB2phj/31X2uPgp8GNDRItJ8H6PGI+m+2SQ8e7gn9a9ytleAjtA/Ms18UqdGq6SV7H56eI/8AgrT+3/4ltvLh8a22mKen9m6Tp0RHphmgkce3PFfOevfEz9tf4+/6J4o8ReM/FdvK24w+feNbjJ6eTHsh/TFfuzoWkeGdMTGk6VYWgXp5NrEmMemFFdZLK4QSkkAds4H5dKKOFwytywR8rifF2pbljA/C/wAHfsJfH/xREs6aBFo0Ug5lvpo4Dj3Rd0v1+Wu/8UfsGn4W6FbeI/FeuDUnknWKaCzjKRoCCVPmP8zcjH3R1r9tfDYutZlWx0q3kupT/BChkOPwrE/aD+BfjW7+DHiLxJqSR2i6dbrdeTI2ZT5LqfujhOM/eI9q9H6yvsrY+Xh4k42tiFTbSTPi79lfwD4D0Sw1NNJ0m0ivIDG8dy0ayTKrArhZGywHA6GvR/il450j4Y6b/bHiff5twN1rb9Jrgj+6P4Uz/GRgdsnivn34KftDL8GLjUtX03TLTV7y8sza27XgLQ20pdWWfy+A7LtICH5fUEcVh/Df4DftG/t8/Gm48PfD63k1fVZytxqurXrFLTT4DgeddTAEIg6RwoC7/djU9B5uZYnTmex6NLKK+JxblVfunkk/jj4g/HXxpa6Dp0LXt1dvssNOgOUjz1x6AAZeVuAOSQK/Tz4Tfs2+Fv2f9DfxLrcsV/4onjK3F6vKW6N1t7XODt/vPjc/svFfs1+y5+xB8CP2FPBD2+kBdd8S6igTUdcuol+03jDnyYE+b7PbA4xGCexdmbGOo8YeEvDXjSaS41rSbVkbpGYkwoPfIA55r5V+0xcko6RO/OeM8vyOLp09anl0PxYHiK41GeSDPlW5+7GD192B+v4V8t/Hf9nr4DeKNJl1zxFpSWNyeBc6di3nd/QKo2MfdkNfsH8XfhT8FvBOntrN/ZfZpHysENs5V5nGOB2AHdiMAflX5bfEDwTrWtXEmqQStdDGFgPDRr/dTscD8a+soQVKHJE/P8s4qr4qv9ZU2j8r/AuifFj9lrx9/wALW+DUFjrk6W8luE1C28+aGKQjcUCsjb9o2l4iG2kjGDUHxb/4KF/tWfFHS5vDtzrsWgWE4KTQ6HB9jdgRhladmecA9CFkUdsV+gvw++EmteONaaW5ja20u0bFxORglh1ijyPvEdT0X8hXzz+3l4F+A1xrGm6Z4Ct0tPGFrtS7+zbfJ+zgfKLz1uDxtYfPj7/8OPKWYYeVdU5K7P6M4ex+IqYf2tbRH5f+FdRn8K65Y69axxSy6fcxXSRXCCSKR4mDhZVbh1Yj5gRyK/rg+BP7UXwx+Nvwcb4zPqFtpNvYpjWo7uZYxp1wOWSRmx8h6xMfvr05yB/JjqWjXmnTNaXkZjdPvAj+XY+1ZbExh7ck7GKllyQrbeRuGcHHbPSvos0ySli6cUtLHu4TH2fMfsh+15/wVFv9at7vwF+zHPJpum4aO68RspjuZ0+6Vs4yMwR+kzDzD/CEr8bvGvgjxR4C1C1tPHNjLp8mowWuoBJ/9Y1rdnIkYHkM4BYg/N619qfsbaZ+zPbayfiF8e/E9ha3dhP/AMSzR7tJfL8xMYu538sxkKceVHuxkbm4AFdj/wAFE/8AhA/ihHpHxW8Da/pmtCGJ9Lvxa3cMsqpIxlt5TGG343M6scADcua+fShhp/V6cOm56qk5q7P7TLOa38qOCyOYFRFjA+7sVFC4xxjGMV1Xw28fXnwo+Juk+P7OMyrp8v72Icb4nG2Rf++envX5mf8ABMz9pey/ab/ZY8O+IZ7hJNf8OQRaBr8W4b0vLKMJHKR/duYFSVT0zuHVTX6FXlqJBubtX5HmdGUarTPr8G7wVj9UfF//AAUR8D6TbmPwDpF3q1wF3Brki1hVvQn52OPZfxr8FP2Qv2wfjL+zN+2X8YP2L7DUo9I8PeNNRuPiL4QiESSCNNXJn1K0t3kBwsc4kIQjgxSkYzge+uFiJJHt7V8RftyfAXx18RvDnhz4+fAQEfE34XTtqGjrGuWvbNiGubED+I/L5kSfxnfEP9bWOBoJS5H1FVqOx23/AAVq/Zw8Y/tv/sz6hp1td3Oq+NfDdyPEGgPNIzSSzwIyz2iEnCm5gLLGBj96sXTFfkz+zb8Yvhv/AMFRf2StQ/YN/aQ1mPRvHCSJfaHqN4jH7Pq9knlJfbfvPHPEzW+owoN8YPmhSPmX9yv2Xf2nPh7+1l8Ibb4leCpFtbuHbDq2mFsz6bej78brw2zIzE5A3L/tBgPyV/4KJ/8ABMLSfiD4h1H9pz4AajZ+FPEqub7VbS9nXT9Pu7hTkXkN5uVbG8J5JZljkb5t0b7mP0+TxX8Cat2PLxcrrmifzpfH34G/HX9mn4lT/Cn9o/T7vSdd01EhjN3IZYZ7RBthksrj/V3FoVwY5IiVxxwcgfXv7J1je/B79mn4v/ta62PstpqXh24+H3hd3G3+0NW14xpefZsgb0s7BJXldcqpdFJ3MBXSaR/wVX/bR8HeAk+FPi3U9C8d6Tp0jLDD4t0bT9e8h1OCY55FPmcjh8vu67jmvif4+ftP/Gr9o7XbTxR8bdcbUE0mI2+m2cMMNnp9hbk7jDZWVqkcECkjJ2ICf4ia/VaVepSpezqaI+clSUpXPn7xU6WmnRWicZwmO+BXmUoUq23p2re1K+fVLwyv8iqMIvYCsBgAnsa/LOIMzWJxHNHZH1GX0VCFiNn4O3sKoMR5H41puoMZNUGRfJIHqK8E7xuN/I/SqlzkQ8euKu/dbaepqlcBthC+ta05W0AgbDnJ7EVSlB4A6Z6VfYbQxPQ4/SqfmIDluQaJ67CuVpdu7aKypsI7YI6gfnWlcFfNJ64qhJtM5RemRWew4oozAY2RknGKrbZEj2Z4zV3Kx5JwOMVRc7yVU8cVithlV0yxXuCOTTDI27b2H+FTthc8d/5cVA43DAHA/WokugpIqMwYv64FVMHa3PFX32bnDdSAOKpME8siuOSJiyrcKUg+b26VA5I+9V+4VfIOPwrNbdjFKUFYqJHkHtxX6rf8EOuf+Ctv7Pq+vjSw/k9flWqgKQelfql/wQ4j/wCNuH7PrY5/4TXTx/6FUWskjopWuf/U/gdCcFD2705F2/MelNQkN60svLDGOvaiVS1kjit0LO7fIBjBH/1q0Lc/IS/XNZ0JDSjcD0q/DwTwOelUldks0oW55qdTvXIqtAcnnjFWlQRqV6/Suq/vCL6BCFV1HIFOh+6yISCDj0wKgDuIxkY44qwmWQFcCtEBeMi5BUYx+HSr8LAiPjBxj6VRG9WD56jgcCrKZ3owPQ1pbQ1TtuaCqfK+g9PpV2DGzI444qgu8Jsz7Y/zircAKDC8DGDWFroyqU9U0aSyBIFYD2qQ3Yk2rH+NUyP3Ptjj6U90VApAx0ra/YTNmCQ+YYh6CvTfht4H1T4ieN9M8FaGD5+pzpCCBwqn7zn2Vck/SvKI2VCMCv17/wCCYfwil8XeMZ/Fyw7riSWLSNP/AOu05Akb2wpUd+DXs5FhFWxC5tkfH8b50sDgZ1vI/qK/YR+E/h34GfAZ/FcgFlbS25iiduPK06yU7pCe29g7se/Ffxj/ALZXx81z9pX9o/xP8XL4yOdYvGFkh+ZorVMRWkK9eEiRR9fqa/sN/wCCrfxMtf2df2CdZ8O+HZRBPqNtbeG7AKcNtm+Wcjp/ywR8/X3r+NH9mbwwvjz49aJbTAfZrGdtRlBHGy0G9Qfq4Vfxr7LiDMfZLlpn4t4K5fOvKrmVb7T0P0C+LX7BHwU+D37G9p8fvHnim+0TxE2LO00+OOO7XVb8KAY4422PH+8Em6QOUjiTO0syg/mV8Lvg/wDFL48+OrL4WfB/wzqPi7xFqCloNK0m1kvLhkX7z7Iwdka5+Z2wi9SRX61/8FkYda0H4q/Db4Xzb00zR/BtveW6HhTc3s8guJAOgY+Qik+1fuJ/wQu+Lfw1+AX7GGnWv7O1npreOPEkk1z4w1Rljn1I3kc0iQWvln5kt4IAgiUjYSWcAlzjz4YytSwSrNXbP3iFKEqnLex/OTN8NP8Agpb+xHdLoGseGvH/AICMa7/s82nXkunlR7GOazZckZ2k46Vv2v7cP/BSHU0/s/SpNTuJjjb9m8MpJL2A4W1PP4V/bv4g/aE+N2v7oNc1zU/LY7mjEhiT/viIKPwxXjWu+PvFOpBkvdTuZGk6hpX/AMa81cSuXx0UelHAxitJH8dr+HP+CzPx1uVEFh46gtp+AzpH4et8H1ZhZ8V6j8O/+CJv7UPjvWItd+OXijSPDkkp/eM002t6hz1GR5cef+3giv6iHie5cyO29j13MTmtC2gWMbEI+meKyq5/K94QsX9UT0bPiX9k/wD4I7fss/DrXrIy6PL8R/E0bK63niTy3sYGH/LQWEYW1VRwQZxMRjiv6dfC72Xwy8NweGk1iM7FAkd540BYLjao3YSNcYRQAAO1fj7DPJGpjDjaRg4b+lUNTtxff3M/hXyuYYqviPiO+hRp01ofthafFzwFbBk1PxDp649bqMnj1wc1i33x0+DFnl5vEVq3f90Hlz9NqmvxesrY6fOvK474Ar0qzt5JVGGzx2/+tXEsHU7G/t47H6Rap+078HrSForW5u7rPaC2b09X2ivBNb/a58O2zsmk6LeTEcAzPHEv6bjXzUmhXs3MMUrY6gKTXnviiytNFia61eaO0T+9cSJCv5uQK66eWzl0IliUkfSd5+1x46u2A0fTrGx923zt+pUZ/CsXUvjb8UPEkPl3utXCK/8ABBtgX6fIAf1r4O139o39mjwRn/hLPiL4W0sp95bjV7MMP+ALIx/IV5hqH/BU7/gnx4Vgb7b8TNP1KRONul2l7enj3ig2/rXVDIaz0jEwljoLc/QG6hfUD5t4Wmkz9+Qlzx7tXO3GlCJt23jr6V+V3iX/AILk/scaLCT4X03xV4jcH/ljYw2cf/fVzOrD/vivkP4lf8F9NTksmHwr+FttFJ0WXW9UeXHpmG0hj/Lza9rD8K4x/YPOqZpRXU/oCe1ZYznCscYzxxWhZ2FtcaXcJrMcMumuhW6W7RGtWTv5wl/d7PUMMV/HT8SP+Cyn7d/i+M2mh65pXhGE8FdF0yHzB24lvTcuPqMfpXwX44+K/wC0D8eXl1P4oeJfEPjGKD55DqFzcXVtCCQM7CfJjHTooHavXo8GVV/EdjlnndOK3P7a/ip/wUQ/YA/Zz0T/AIRzVPHGlzNaD91onhGBdRdCBwoSxH2SI+zyR1+Pfxj/AOC//iNLiXSP2X/h7b6au4qmq+J5vtE3oGSwtWWND6BriQf7Nfij8NfhDr3jS2dtOe3tYbbajliRt3DIwqjnp9OK+g9F/Zg8J6fcJdeI7mbUmHPlD9zD+nzHkeor6ejwpg6MVKbufJ5lxxSpy5TlfjN+15+1x+1rP/ZXxa8X6t4ihlbKaTb4gsAfRbG0EcP0LIT71x3hX9kT4ja7JHNrvlaBanH+u+ebb6CJeB/wLFfor4H0/wAO+GbJbDw9Zw2MI/hhQKT/ALzdT+NdzPJFL85HQV7kHShDloxsfl+acfYiU2oaHifwv/Zv+GPgLbei0/tO/T/l6vcPgj+5F91fbjIru/jboTar4Ie9+99juIpB6AH5DgdABn0rq7I3lxItvCu53YABeW/KvpXR/wBn3xt4t+HesanqdotrbRWM0o8/h5PJXzAFTqM7eprKMZVGfA4zPpxqxqVpnzx+zPf4sr7SFU5zFKMck8FTwB9K+y7f4afEPxEgl03R7kq3Id18pf8Avp8CuA/Yl8nQfjLZ6dCioupWk0AAHJO3eP8A0D2/Kv1f8TfFD4YeCYGi8ZazbQSgZ+zo3nT/AIRR5I/HArqqUFa58VxJmNRYq1KF7nxT4Q/Zx8V3cgPiO7is1HLJDmaQD9FFfQ8XwR+HHhjRjqmvFZI7YZkudQlVIV9MjKIPx47V84/EP9tu7j1JNC+Efh9priZxHBNdgvK5OABHbQ5JPoCx/wB2vMPil8HfjTqfhmH4oftpeJn8IaXOGax0ycCfVrkjHyWumptSEHp5km0L3HauJYiEfcRWA4cx2K9+t7sTpfid+3n8LfhVato/wsshrc68FlU2tgjD0KAPJ/wEAe9flF8df2l/i98dIwvjPVJHs4m3RWUP7q2jHYCJTg49WycVleIvDl98QvH1v4X+FGj391Nqksdvp+nRk3t5cSHAXHloN0jdcIgRfoM1/TV/wT8/4IVeD/BunWvxg/bt8jUdRh/fxeFBIr2Nt3DalMpxO64GYI28ns7SDKjzMbmUaPxb9j9W4c4SwtBe0XTqz8R/+Ce3/BLr44/tp6hb+N9eaXwj8N4ZNs+uyx/vb0jrb6XC+BMxwVac/uIu5dh5df1q+HfA3wV/ZJ+F9v8ABT9n/RYNOsrT52gQ75JZtuDdX1x96edu5POPlUKmAPTPiJ8VoHjXwt8M4FstPtUFss0MYjRIkGBHbRgBY0UD5cAYHQDivB/sBCCKMEluRjkknvXBDD1sS1Krt2Pl+MvFGjh1LB5dv3/yPN9SN3f6g+q6nI0079WbgAdlUdAB2FeXfEX4iaP4DtCHUTX7qDFbA8gdnk/uoPzPb2yvjb8abTwkJdC8KbLnUVysko+aK2xweOjv7dB39K+BrvX7i9upbvVJnllnyzyOSSxPXJ/z6V9DCjGK00sfhOEwlbEVHWrO9zm/ibrmreLdWl13WJDLO4weMKq9lQdFUdq4DwN4D1HxjdC8uN0Omq21nH3pCP4I+PzPQfXivozw/wDC+/8AGHkajfRlbJ8eWnRpx2I9E/mOlfmf+2n+3hpnhC1ufgf+zpcIbyIG11HW7YjZbbfle2sWHyl+zzjheic/MPCx+ZOT9nRP6I4H4NcoKtilaPRE37Yv7VWkfDFJfhB8IGjbXrdTDdXUWGj00f3E6q9z65yI+p+fgflb4H8MXmtakdUvC7KWLyysSzO5OWOTyWbu1ez/AAL/AGR/jh8YtAh8Z6Bobvo8zHy7m4lWFZz3Kb/mcZzlwCCehr9Yf2YP+CTHxn+MOtta63qNpoGkWQQXV1bRvdCHedsabv3ab2btn7uT2rgw1bDUHq9T9azCniqlP2VGFoo/KDx54E8OeONCTTIFFtf2q4tZiM/9s5P9knv2/Svz81/QbvQtQn03UY/LuIG8uRD/AAsO3pjHSv2c/Z48F+GPEH7SugfCj4oRBra71ObS545XeJPtEW9Y/MKfNs81QMDBI4r9e/8Agrv/AMERNV0/9mRP2oPgtZafP4g8KWkcl/puhWpihudFUfNIqkky3FsPnyBueLcDkotfSR4jp0asaM9mLhXBYicJdkfyNfAz4Sab8bPiTafDHUfEUPhm61VCmnT3UBmgkuuq28pV1MfmAEI3I3YXjIr6v8Uf8Elf2lNPle60a/8ADes7BkYnmtn/AClhA/8AHq/Py9BgC3FtIwxh0kjJDKRyrKRg5BwQR09jX6FeDv8Agp9+1xqWm2nhPQdH0zxJqNpGsRu1sLq6u5imAJJlt5QpcjG4hACecV155CupqVJqx91g7WszzH4PePv2tf8AgmD8dIPGNxo5sjqUQt77T7xjLpesWqnd5X2iAlPMjY5ikRvMiPVcEg/vl4O/4Lufs06xoSy+O/B3inQ7vjelqlpqMAP+zIJbdyPTMQ4r8V5f2of2ufjn8VNH/Zw+JFlp6/2tq9nZ3+i3WjRxkI5V5POE6vLHti3PkFZEAzkV+rHiL/gk5+yb4gunu/C8uu+HY3JCw2d6k0Sj/ZF1FM4AAHG+vksyhhLp4xa+R7GHrVUrQPQfEf8AwXC/ZCs5gNK0TxffsV3bRZWkAPtlro14drf/AAXv0C1Z4/AfwsvJ8NlG1TVo4RkdCUt4JD+T/jSeG/8Agjn+zLqfxA0jw/4g8UeJ5LO/u0tZWWWzjdd3CnItTj5sAnHGenFfj78Rvgf4O+D37bOrfs86t5l7ovhzxw2hv57/AD3FlHfCFfMdApy0JGSuOTxioy3A5bVb5Vsc+JxNaC5meq/E/wDbw+Jvjj42SftCfCzT7X4WeIb2Jlv5fDNxcIt+znl7pJnaJ3P8REahj87KW5ryHTfC37aP7fHxMsvBvh+HxR8VddvHK2tvJJNcRAqu5iplZbaAKgJ3ZUADngV9GftO/Dj4b+Ev2gfEHgP4baNa6RpttPZ2UNvAuVVnji3EFizZLMc5Y1/WT/wTM8IwL+1roghQJb6NpmoSIirtVdtuIRgDAH3hW+fZ/QwVKHsaaucOQyeMqST2R/Gt+3p+wl+0l/wTuTwVof7Slnpuna3410671G306zuxey2kVlLFCVuZIh5O5mk+VYpJAMHLDgV+adzdXN8TJdHJzwBwB9BX9Vn/AAds60b79sf4X+HSdy2PgaeYeubrVpBz9RB0r+Ul8qmQODXxuI4gxOLj+8Z9XHAQpvREokCgnrnj6VTcFUAqcK4TFNZ/3Y9BXnxRuyGbK4A6H0qky8AfSrcrDdz0xUDDpTKIGO19w7VVuiV249asvndz0qrcZwuOMUgIQFdDzWZgLkD1x+HtVwLtJB4B9qhn2DDgYzyPqP8A9dVG72JRnM2xvM6Z7VTfmTdjuOlX3Y7GUqOnHFZ025ZDtbIHQelZzkCepFIEMbEE9OePpWe6hflGOcVfJCRsDgkf/WrMcSFsHge3pWSNXuMZmYbUAABxjiomB7jpU6hjliMCq8hbqnQVDZHQhBky23pj2rOkf92232rRdDyDgenaqE2Fiyv41xyZnBjZf9WRnFZuQq5NW7r5owy9KrSFdg9ugpVXsawWghAwBX6q/wDBDnA/4K2/s+7RyPGdhx+DV+VHQHNfqx/wQ3Xb/wAFb/2fnXOB40sB+j0peR0UlbQ//9X+BlR+9wO3FOlIRuaVCEPzcf54pjsQxPaob95HGlqXI3XdlvrV+P5YxzkdPyrMChNmavQSHkSDj0FaqSUiJq5o9ZABwD0+lX04XArOVWiI5+lX03YGM10q1yktLlxCxix/kVciQhB6VSRxtJTjmrKbwgOa1M6ctS8DIgH4Yqyn8BPcgiqo5HzcjgVbR0VRxx/kVVijQQNySOePapFT2xjmqqB0YDsy1L5jA5bjPSmlY0aL0b/II2+8tX3Jdl9KzoCVU5PNWoWwmCO/FaxSSMZLsX3yFORkY4Ff1Z/8EjvAcPhnxL4V0O7QK+kWUupT8dbiRf5q0gA/3a/mc+D3hdfGHxK0Tw7Ku6O6u4hIP+mcZ3v/AOOrX9an/BOm2e38da3rLjaPKitwT2V2JP5AA19vwnhZKDqWP5/8c8zthXQXY+af+Dhn4xM2reB/g5aOdtrbXWr3Cdi87/Z4T+AR/wA6/IP/AIJ+acs3ibxP4kON1pZW9kuRwpncyN+kQr3P/gtx40uPE37cOt6QXJTR9P0+0Uf3QsQkZf8AvqSvMP2CbGRfh74qvYf9ZPqMcefaK3yPT+/xXh5/WvNrsfZ+FmVrD5PRSW6P6Kf+CsH7IPh39oHRPBOtQXX9m65YWVxBaX+wyRlA0b/Z5l/ijO7IK/Mh5wQStfy9/FT4GfGX9mrxFaT+OoBp0l55n2G/s7nckwhI3lJI9si7dw4cKeRxX9qn7QU8fjf9nfwT8QrL/V/6M5x0C3toDn/vpAMV/PF/wVZ0aP8A4Vj4L1tV5tdVurcsOuJ4AwHH/XKvYyHM7YWz1SM8Vj60M0+rS2Z+cPhj9sf9qzwmotfC/wARfFFsBgIkerXUg7YAjZmB9hiuji/4Kkfty6JdeSPifrLeX/DcrazY6dfNhJr5d+GPjH/hBPiX4Z8cAhDoms6bf5PYWt1FLkfQJX+h/wD8FEPDHgDV/g3c6/b6NpsrQ63BOj/ZISWiuVdcklckHK+3SscZxVShZOmj7qhl8mtz+KzTP+CwX7dSwoYvGq3I6Zl02wbP1IhFdja/8Fh/29fLBTxNp7D/AGtJsj/7TrzP/goz4M03R/jhpus6PaQ2ltqejRNsgjSNPMt5ZI2+VAFzt2ZPfivN9N0vQrrwRY6nDawCTYFchBzjIP8AKvsMow+GxNNVXBHzGa5nLDSUT6Sf/gsF+3wR/wAjVYr7DSLEf+06wr3/AIK6/t9+WS3jS3jz026XYDHp1hr5ivLewiDfuE7fwj/CqLrp5jLtbRMqjOCq9B26V3zy/Cx0UEcX9uztc951L/gq9+39qu1/+FkXMK4/5dbOwix7cQCsyf8A4KK/tz63ABqPxa8SAAYxDdCDg9v3Kr+FZX7cfgXwx4G+P+jan4PsYLHTdX0TStSjhgjWOLLx7JPlHHJXJ9TzWZp8+nQDCwxjB7Iv+FZUaOHUtYEVuIJezjOPU5jXP2jP2jvFqlfEXjvxPqQbnEurXrDn2EmP0ryfWdF8TeLSTf2t5qB65n82X9XzX1tBfxlQRgY6YAFaKXqSqT7evT2rslUoJe7BHiVOKKp8YaV8DviFd6PqnifTdBZbDRIFuL6XaiCGJm2hjnk8nHA/KtrwF4B1/wAYGVtOlhhihZY2MjEckZGABX6F/DS4W88G/EfwtJj/AE3wvdMg9XgIkH8q+LfgRqoi1K+tTlQ0cUgH0yM1xU8U4+8lY1WeVatKb7Homkfs5XQTOqasgPcRRE/kWOB+Vd9p37PfgiOEDUZ7u8x1DMsa/kozXd6VqPmv5TEFemP8a763tZp8CBSxPQKpNdjzGq9j4jF53iL6yPKdL+GXgHSHC6dpFsHTo0i+awx7vmvbdIsYdU8H+KPCUaALqGkXASNQAN8a7kwFwOoqi3gzxZeS/wCjWbID3kwnp64r1TwR8O9Q0LWbXXPFOp2emWQYpI8sgA2MMEbm2r+tebUcm9TzqmZSlZ8x8Ofs2aoF1G909zhpIUkA9Ch/+vX15LY3F4wit1Lv/CFXcT9AK+LPhVrvhD4W/HUy+JnjvtAtru5glkjy6PCdwR12HLDhWGK/TNf22vgj4csPs/gvRrm6I/55xR2a+3z/ADPit8NGMo++x8RUcR7ZTowvcxvA3wn+IWsTo8lp9lgPJe6PlDH+6fm/IV9t+Cf2Z9NmgV9dupb+RsZjt12R/wDfbcn8AK/MPxN+338Qlumfwvo+naQvQSy5uJB9S5Vf/Hfwrpvhx49/a2/aonHhnwDF4j8Yux2/ZdBs5548+hFonlge7EAVf12hTVm9jwsRwrmeItZcp+ol9rnwE+CEmzWtR0/TJE+XZERPdZ9wu9wfYgVzt9/wUE+Gun202ieB9Hn1WSaJ42kvWEERDrt+6N0hHPT5a1fg9/wQN/4KCfFyK31jxjo+mfDzT5wHeXXrwS3O3/r0s/Obcf7sjxn6V+v/AMEv+CBv7HH7OenxfED9q7xfdeNHt2DmGcjStK3f3Rbwu1xKemFM53dNteHX4qoQl7rv6HsYLwfnUtPEX+eh/Of8LPhz8Svi54hi0P4W6XqGrXwwEj06GR2XPBy0f3R2yf0r9RPhn/wSV+KenaW3jL9prXrH4f6OuJJFeRLi72DrnkQoexLMx/2T0r9jfiR+3L8Bv2YPBi+CP2dfDun+H9PRMW4htkhL44BhtYwDj/bl/EV+EXxx/aD+Mn7TfigR6tJc3CzSCKGzTMzyMeFUKv8AF6IgAHpWmGxWJxMeZrlib5ngsBgZezT559jrfiN+1D+zv+yrps3hb9hrwxHf65sMU/jDW0E05OME2qMB/KOPp+7brXxf+z3+y3+1l/wUe+J97qmjvcan+8A1fxPrDP8AY7QDHymTGJHA+7bQjOOu1eR+1n7KX/BGDVviDFbfEX9rDztI0fAkXw/C/l3dyvB/0qUY+zoe8afvOuTGa/Y7+3/Bvwn8L2nwu+DmlWul6Vpcfk21vaRiK2tgvZVXhmzkk9ycnmuGvmEIN08Jq+461RUaSr473Y9EfHX7Of7Fv7N//BPrw99o8HRf234uu4vKu/EN5GpvrkEfNFbICRaW5/uJ1/jZzXYeJfGfiDxhLs1ZjHar9y3QnYOmC394/wCeK3NXtLzVrp7/AFFmlmblnfqeP0FeaeKfEHh7wPpja14muRbW4OEXG55G/uInUn6cDuRTy7A39+erPxnizi+viJeype7DsPubOG1ikuJ2SKBELu7sFVFHUnOABXwj8U/j9Lqxn8O+A3MNkcpNdgFZJl6bYx1RPfgn2FUfix8Xtc+Jm6zjBsdKiO6K0U5zjo0xGNze33R29a+Xo7DV9W1+DQvD9vLe312wjighGWc+wHYdzwB7CvpLqlG7PgsHl3tqtoq7MzxGFFo2WwuOP8+tek/DD4F3QjHjL4jCO2ht1NwtrckIiRou4z3bPhY1UDOxiMDl8Divpu0+E/w//Z68AXXxq/aA1W0sI9Fh8+4ubhv9FsAeiIOs1wx4TaCS3Eak/Mf5YP8AgoF/wUw8dftXanc/DD4Yx3Ph/wCHKzbFsxkXmrsGGyW+25IUnBjtFyAcb97YI+YxmayrXp0fh7n9J8EeHKoKOIx2/RH0t+3X/wAFHrbx7Hf/AAa/ZwvWg8O7Wh1PXosxSaivR4bUHBitOzScNKOm1OGxP2Hv+Cb1p45tLH45/tDW/wBn0HKy6ZocgIe/THyzXC8NHb9NkX3pBy2Exum/Yd/YkstGNn8V/j9ZrJeptm07QplDJCR9ya7Xo0gwCkJ+VOr5PA/d/wCGnwp8e/Hm41a+8PRv/Z+hW5utUvTkrCg5CIMENM38KjtycAV8zj81hTj7Chv3P3zLMkv++rfCtkdB8GPg1c/FjxIuh6A1tonh/TVRb7UpQEtrK36LHGmAplIGI4l/RRX78eD/AAd8G9I/Zsv/AAv8EFRtN0s5aUKVkluISrtNKxCl3bg7sYxgDgAD5V+DHwvvbr9mTUvhzpOkvbSRailxYLdR+SZwfLJZncAsx5yxA9BwAK+hv2fNPTwrpniL4Za5r2lahq1xEtw2n2Nws09ujKYWaZQBtBO0DivkpRt+8k9T3qOOlKfs4wtGx/n9ftwxXfwH/wCCg/jm70sCL+x/Fqa9b8YAiuJI79cfhKBX9v37QX7c3gj9kb/gmbeftWeK4Y9TXR7BLfS7MnAvtRlbybG3J/uSMymTGSIlZu1fx5/8Fu/BT6P+2TH4hCAJ4l8NWrsfWW1kmtG/JIo6/Qj9oH4AftTf8FPv+CU3wS+Dv7LaWV/f6JeWuta3Z39+liJUSxeyikR5PlbyZvN3pwQMEA8CvuMZCFaFGrLRHyvDUvZYmrRPwB/Zu+FP7Pfxf1TX/wBrz9u7xTonhzw7farcz22hQyR2X9qXruZbho7O1/0hLGBm2RxQR/vDldwVDu9H+PX/AAVU8FeDvCknwl/YQ0BNAsSpgXW3sorFIVP/AD4WKgfPjO2WcZHUR5wR2v7Jv/BE7R/jR8d1+EPxd+KWn2WomC+neLwtaS3ymXTwDJbtqF4ttArnnHlxTrwa+Rvjl/wT+1bTfC+rfFr9n7TtT1PQfCsRPiC3m/0qWyjQqhuxcLFEsgGcTRog8nG77mSv0SzHBzxChKZ9DGlJRukfcP8AwSY/Z28JXvhG5/aj1vUV1vxPqU93ZIGJdtO+bFwJmf5nurkbXMnTy2ABO5q/ZxY2RFiXgDpX8un7Bn7VU/7LHxMB8Quz+D/EWyDWI0y3k7QfJvo1/ieHJDDq0ZZeoWv6e31SxvoobrTLiO6trhVlimiYPHJG4BRkYcEFSCPavmuK8HUhiLvboelltaDhY5nxHezaSE1e3ba1jLDchu+YmDcfpX83n/BTlv7C/wCCoHxG1+1XbHP4h0/Vlx0/0i1tLo/qa/dr9o/9oH4NfBDw1cRfE7W4bK9mhIhsYh9ovpCRxst0+Yc/xPtX3r+bj4v+MPGP7ZP7R+peL/BmhynVfE0tvHZadGfNlEdnbRW8bOw+Vf3cQeRjhV55wM11cMYWak5SVlY8zOa0VDlR9C6zqX/Ce/tryEHcmpeLolHceXFOo/LbHX9m/wDwSu0k3Hxe8SeKNv8Ax56KY8+huJ48f+Ox1/FN+yBpN94t/ao8NSTnzXgnvb92JzzFBJzn/fZcV/d3/wAEwNDg0vwh4r8Qbfnlmt7bd6iONmx+b18zxrUvWjDsXwRRtSnN9T+Qz/g578YL4k/4KdXGjRMWTQPB2hWTZ7PcS3t6wx24mWv5zpzlRiv1d/4La+PpviT/AMFU/jbrZk8yKx16LRYufurpFjb2ZX8JEevyknUcBeK83Dq0Ej6qq9SvJu4zUEqy4RUOB6VYkb+A1WdtrqtdPQzIpVPmc+lROcbfTFTyNvJx2FUmxvVvYU0ASkCXy/as2bn5Rz3rVyMM3fsfpWVIfmwOOgH507aCuRzB4xtkGCRxiqP70spAHBJ/StA9BFna2ePw4qlztUk/hVxatYdim6yRp+XAFZjgby3TP/1qvTsdi5PORjpVSR2PHDdPwrnnO4FOcLs2n8qpyEEKw4FW35Pljk9D+VV2IX5cZqHKyHcXZ8oUdxms+UMpCn0q1Idxz02jFVpHV8dOOo/CubnJbIMOFLfyrPnGYiPXpVuZjs+T16VnuXB8vrntWNR7AkFx80aBecdfwFVJSPl4xj0qS4ym3jrURYsAxqpWsaJC/IOPWv1W/wCCG4P/AA9p/Z+C9R4zsOPwevymcbMKMcV+rX/BDhyP+CtP7P3/AGOdh/J6y6I2grM//9b+BsKpXcaRiApYjk9qHUqgXoad1TA68Up9DjsTRAuQrjG3pzVhWJ+71qAIX5PAGO1WbcKPlI5FS46ohs1EVGwrc8f/AKqvK5C7FI4GKow8RnsRjGOO1WDjPIHrXbTpvoZc0uhaUjlT0JzViLYoJxntVYH5sn2q3bjJxnnGa3saQiy8jEbeMcjBq5bozgk9qoKBgKeehq7D8xLdvansgL1vh23N6Y5qcqr7QAMjj8KgHyDd6n+dTR7QWOevHp6USbRaTuWII+o960CqLgL0GDVCN278VZQAbVc5zih32Oaa1Psv9jbTUuvi7HqT/wDLjZTyj6ttjH/oVf02fsF3kcF9qTZwTMPxCJj8OtfzX/sWoE8Sa5fH/l2soUP0ebH9K/ez9ibxUsWuz2JdQZJmUfigI+nSv1jh+PLhYn8weMVKVWrPySPxZ/4Kwah/af7d3j6eTPN3Ao+ghXH8v0ruv2AJYm+GmvW7n549VB2j+61umD/46a5X/grPotxpP7bXia/k+5qKWlyuB2aFBVT/AIJ3am9xrHirwouMvb22oKvciGQwuR9BKv4V+f53dV5RP3fgOzyig47cq/I/r7/YjubL4/8A7H1z8KL+WNb7Ri+lAnkxFW+0WMpHpjC+mEIr8Z/+ClHgjWLz9m/XNL1K3MOo+F9Qt7u4hcfMhhcwSj6BJc5HGBkV7X+yZ8f5f2Zfi8msakjyaFqoFpq8SDcwgzlJ0X+J4GJYDuu5e9fsL+1V+zh4G/au+HM+qeG7m2k1DVNPMCTqw+zalZTJtVGccB9hxHJjj7rcAY5Mqx6oNwlszfO8i9rUhiqe8T/O4vFMkE0bD74Kr269K/v/ANE+Jcn7Q/8AwTt8O+N42E02seDNMvn74uLJI/OX6honBr+Er48fBz4gfs8fFrV/g58R7Kax1bRpSm2VSvmw5zHMmOCrJyCpI7V/TF/wR8/a1+D+sfsnaP8As3+P/FWn6Z4k0q/1PTbewvphBJLp94zSxNG0mEf55nXCsT8vTFTmmHco3ij6PBTtufn/AP8ABRPwoNT8CeHvGqqBJp97LaOe+y7j3L9AHh/Wvhj4W3P9qeEp9K2/PbkgBeuG+Za/XL9qTwXdeJPgr4o8KtFuubO3a4iUjkSWLebgfVVIH1r8DtH8Va14ev8A7T4dmZJSM/KMhlHPI9Biv0Dg7Ff7NyS6HxPFeA9pK8D1vWVdZSUJ46jGOlULPE4MTc5GPTqMV22mfFfwV4stgPiHpjQT5A+1234ckdffnNdRp3w80TW38/wDrVtqOeRbu3lzD2wR+HavsFC+r2PjJTcI8skemftwaafEPwb+D3xMiA3SaNNpUzd91pICgP4Ma8Y8L2lhqulW18zMpliVjjpnAzX1R8ZfC2tzfsJ2tpr9s1teeF/EA2hsf6i5VhkEEgjcR09K+OPhlNeXvhqFIRu8lmjx9DkfpWE6Sijz6FRywtl0Z7fpXhjT5OTcyZ7fKK7TTfB2lPIPNuZefQCvO7C5vYPncBQMA5IroI/H/hfR08zVb+GLj+8GP5Cmpp6WPFr06j+FH2h+zB8IvC/ib4sReFbiSbbrFhe2XDAZ8yA7R+YxX5JfA22srP4vx+G9dB8uTz7UgHb88fQfmtfXvg/9sbw18KfFun+M/C8Mmq3enS+aibTHGxAwVZuoBB9K/NzxD46uX8e3XjWyb+zru6vnu4liOTE8rltiAdcbsDiuSvBQ1Z7XD2V4icakJrdaH7H6XL8PfCsovb+O0to1/juWAH/j/Wqmt/tjfDjQZTpnhG2bV5wdu21jCRZHbeQD+QrxH9mv/glv/wAFHv20LmDxB8Mvhfrd7pk+1hrniVv7I0zacfOsl35bSr/1yV/YV/R7+zD/AMGtGgaZBbeNP27viwklpFhpdD8Iqtra4X+GTVLxQWHr5cCn+63SvLxHE+Gw8NWejhPDL2z5qzP5nvG/7VXxj8aaxbeHvA9qLC8vWEUFrpsTXV7Mx4CIFDuzf7i/TpX6Afs8/wDBCr/gqr+1RFb+LvFXhb/hDtKvMsl742vjZSsO3+hBZrtSR0DwoK/sx+Bvw9/4J2/sM6O2hfsgeDNI06/ZfLk1KziN1qEuOCJtSud8zAjsG2+ldrN+0Z4l8UXZ3yfZYc/cQk5+rdT9OlfA5nxpOpL90tD77LOA8NQSVj+cLwd/waweMo2j/wCF0fHDSdPYY82DQdKmvGA7hZLmaFeMf888e1fo/wDBT/g2p/4J4+GoIl8feKfGPi+eP74kvLfTrd/bZawpIAf+uua/TdPFFzdQB0fAOCTnioNV+KGm+DNMbxB4o1CHS7CP709w4RfwJxk+gH4V4FTiLFS2kfTU8hwsfslr4Uf8EhP+CYnwVlh1LwF8IdAuLyHlbrV1k1edSOhzfPPg/TFffFvrnw5+EXhfdfTWHhvRLRcDCxWlvEPQKAF47ACvxC+Kf/BTOw0zT5rD4QwpeSxD5tUvj5NtGB3WM4Jx2LbR9RX4MftEf8FHrzxVrstxeapc+NdVjO1ZJmMen256YjQYBx2CAA+tdeX4PF4uWr0OHM8xweBjzOx/VB8f/wDgqJ4L8M6Zc2/wdjjukiU79a1L91bJ7wwna0h9M7R7MK/nT/aE/b2+IXxL8QSz6Tfz6jdH5f7SvR8qe1rb8JGvodo+nevgPwN4m+Lv7S3jOy8K6Za33ijXbtsWmn2MRfCjGdkSfLGq93fAUD5jiv6J/wBkb/gilbRSW3j39s67SQpiVfDFhNmJenF7dpgv7xwkJ/00YcV9vhcuwmBjz1NZH4vnvFeOzKTpYdcsO5+af7JX7LXx+/a/8TtP4RtZLi08wC/1u/3LawnjI8zH72QD/llHn3wOa/p6/Zo/Yd+BX7I+nw60qrrPiQJtfV7uNRLyOVt4xkQr7LlvVjXqz/E/4e/DPQ7fwB8JdPtorbTkEENvZosNpbovG1QgC4HoorhLDXda8RawL/V5WlkPA7BR6AdK58dmGJxC5fhifJ0K+XYGaUH7Sr+CPafGGu6l4gsDaWmYbZuoXqw9z2HtXz/ceFfJZgAT3Ar6z0TQ7a40MTzYyBnPbH0r4n+PXj2/0wS6F4dJtgcq84++eOi/3R71yZR/E5InF4h0uXDRxeIfojx34sfE/QvAEMunWUa32rKP9SDhIT/ekYf+gjn6V+VvxI8R+IvE2sSax4guGuLgjAb+FR/dRRwqj2r6N8UFQZHmPbLE/qSe9bHwq/ZM8XfGueHxJ4lMmi+G3IYTEYubxfS2Rh8qnp5rDA/hVq+zljaWGh7x+B5ZlWLzTEqGHgfKHwx+G/jz4ya+PDHgG0MxTH2m5lytvaof4pXA44+6gyzdhX1Z8cfGH7LX/BLz4RL4/wDi7qXn6vqIZbWGIK2raxMn/LK0h3fuYAeHckRR/wDLRy2FPif7dv8AwVj/AGev+Camg3H7Ov7OGnWPiX4i2+Y/7PRi+n6PI4/12pTo26e66H7OG8w/8tWjXCn+T9dP/aW/4KE/GXU/iT471e513Vbt1Gqa7qP+otYxjbBEiAIiovEVtCAqjsBzXzNSvUxT56j5YH9QcIcBYXK4JuPPV/I6P9s79u741/t0eM49W8b40zw/ZS/8SXw1ayk2lnvwod2ODPcuOHncDH3UCJha+2P2Wv2D9L+DN3B8R/iGsWqeLdoeFRh7bTQRyI+0k3rL26JjqfyZ+LPw5k+FXxH8R/DZJ3uf7FungimcBGdMK0bkLwCyMDgdK/ue/wCCan7Muj/tH+BPDfxv8bIsvh2OzspRCcH7ZO8KOUIPIiXIJ/vdB3o4iqRoUIex0ifo3D1F1a8vaLVHxz+zF8IdO+OXxDuvC9zeyQw6fp0+qyRQANNdJb7cwRsfkjd8j5j0HOK/VT9kz9oVbvU5fg58L/C9l4Tgu/D19c6TGZDczte24DJ52QsT5+ZmHLnHJK4qz8Mv2WvBv7MPxi0vxd4w8c6Rp1xLe3Vtpmj/ALuKS6S+LJFCfNcO7YZeEjI3ADNcj4P+KX7E/wCzr+0fp/wx8I+HtUv/ABf/AG5/ZVxqtzu8rTbi9PlsEeV1XZhwmIouV/iNfGcsL+6rn0KxNfRVGorY8u/ZO+MX7QH7SPjbxh4C+J2s6jrVh4k8Kaja+YIfKs7G9TCr5flRxRxO25lHOTgCp/8AgnX+zZ+0J8EPi7b+O/iXpUPhrS9Q0a4sXtby6i+3TyFo5Y2W3UlyFMfO7GF7Vvf8N4fF7wz+2PonwS1k6Zo3hOz8WSaFPYWVpHGJ4pSYYHdpCTnc6OfLCrmvifwD8Nfj2n7dVv4w0/R9a1qDwr4yuYbzUrvzTFHZLcPE+2eciPaIGY7VZiRwBSnHRp6aGNPEJSjy62dj4y/4OCvBa6f4x8BeMkXHkX2r6YxxyAxhuY/5vivrv/ggX8XRP8J7Lw277306fUtM2k/whxdxjn2kPSsH/g4T8OxX/wAA18W2oBGl+I9OuQ3+zdW89u2PqwWvgz/ggr8RXsPG+veGmcAW+rWF0o9RdRvA5H12D86+iaVTKfQ8mlD2Wb37n6reGdG/Zd/Zu/bTgt59a1vXfGt14hltoobSBbTS9F/tfcoWdzg3BEcoHytt5HAxXjFn+0n8etc/bLtf2flsrXT/AAlo/iG903UNC0WwXyGtjvi+03jkMSOQ7sSkbcgg5xX3R8Xv2KfB3xM/aX1D45+L/EE9vYP9gni03TsJO13ZKq+ZNO2VRMxrgIu48ncOKb+0h+09+zr+zTa6r42+I+q6Z4cm1qU3FwIVX7Zfy4xny4x59w2OAcYHqBXx1P3mvZq7PuXHkT9o1FH8mv8AwVS/4J13f7OHiG7+Ofwesv8AigtUuG+1WcI/5AtxI+Am1ckWMrf6lj9w/u2/gz+avh39sH9pvwh8Nbb4OeC/Fd1pWh2XmC3W2SNbqOOQ7vJjuSvmpECSVVSMZOOOK/YX9tj/AIK8eJvi14d1X4cfA/R10Lw5qkElndX+pxpNd3VvIuxkjtjuhgVlJHPmP3G01+cv7EP7KGlftU/FmfwRd3UunaZplmL27e3UebInmLGI1ZsiPcTyxBwOgr9Xy3Ey+rL66tj4/G5hD21sMeQfBD4F/E/9o3xp/YXgm0m1PUblg95eTs7pAD1kuJyGLH0XlnPCgmv3k8E/s4+B/wBgf9njxn4vtQt94lh0e7e61GZVEhlMRWKNcZ8qMyMmIgev3jkYr69sb74V/sqeAW+EX7Othb2Mtvlbi8hXPkvjBIc5aWfHBkYnaOPYfAv7fHjC50P9kXS/CJkY3niy9ghckksYYWN1KSe+WWMH61x1sxniJxjTVonJVlGMZc71Pjf/AIJa+EH1j4x6x4omGRo2jpbhiM/Pdyr/AOyQtX9v37Ix0/4b/s8w63qrCGG5mn1GdjgbYEzkn2EaZr+Vj/glp8LLvSPgjqnj2SP5/E+rukHHJgswLZPw83ze3av28/4Kg/Gdv2aP+CYPxEv9HmaC7t/C7aJZFOG+2att06PHupuCwx/dr8/4lqe0xdl0PuuGKKhhEf58Xxe+JN18Zvif4l+Luoljc+LdY1HXJC3rqV1JcgfgJAPwryduTj0q0DEmUtxiKMBEHoqjaP0FVHyZCw71cFZJHoMjckvx9KqMu1iRUsoVnwKqb3MfPFdCVkCQ5Qck+oquAGOOmKnXcRu4FV8bUJNC2sJkbNhiP0qpL1HerjGPbuOCBWYGcse47Vd/dIktUNIHm7mOOOwqrKBHJsX60+SZVc7l7YA/lVWdgo/dnGBzUxVkbJa6FOZWJLZzg9O1Zj74gdxPPT6cVozKI/3cZ29OOgqrMu7G857n06VgCsUpcCbeeARTXwWz27U5lLZGfpULEDbjoayrRvaxLGkLuIJqnKibiTjip5Txvx3xVGX54NycEk1hKArFaVFZNpGB2qgQY3Djooq84YIo9KgmAxn0xyKzlDQcWROVeVVPPHaoplCOFUYwaZECJQelRzZ87OPwpyfumsVqBMaJnvX6s/8ABDcBv+Ctn7PqP0HjXT+OnZ6/KR84Ar9XP+CHGD/wVt/Z+9P+E0sf5PWK2Vjamf/X/gWOFXOeanQZjGOOOar98GrAPyjPbitaeqRxy7Ch8YXtV+DO4kcdPaqKIvmgH9TV5F8s7u1JabmbsWypCgH1qYfwkfpVdck/N0H9PpVlG+QoB16V3LyEmW0Qo5j9AOKtwMQvy4GeKqc5DDo2BxVpGRMKfpRJ3G5NbF+NyrDgHBx+dX4F2qAPxqhF3z0x0+laMe4jdnr6UgRbcqV+X72f51O7kcJj5gKrYYAMvt09KsxY2/N1yCPxquXQvn7Flseevl4GFANTiPayN26VS4Vg57en4VfLruAzlf8AGiW6JkrWPtH9j+6aDVPFEKHpp1vIB3wtyo/9mr9MvgZ47vPCniWe8tPvwGO6Qdj5Rw3t901+Uf7IF15nxkfwuxwdb0y7tF/66IqzoP8AyHX3X4N1tdH8Q2eoTZVFbZMDx8rDYw/D0r9L4dq8+GS7H4Zx7gObESUlujU/4K96Xb6/4v8ABfxk0gBrLW9LNrvH/PS3IcZ9/LkXj2/L8/v2U/iZa/Bz46aB4/1EE6dDN9n1Ff71hdDybkcf3UbePdRX6Z/G7SLj4h/CPVvgdqY8y609zrXhxiMl3jybi1X/AGihYqO5H0r8YjG1i6sflGBx7dMflXz3EuFcantF1PqvDLFr6isN/L+R/TT8SfC0nh/UTaxt5kRXzIJk5WWBuUdccEEV7F+zR+1/4v8AgfKPCWpBtT8MvJk2hb95aMT8z2pzxnq0Z+UnkYPNfGH/AAT6+OnhX9on4Z2/7LnxAu0s/FWhQH/hHruU5a6s0BPkdfmltxxs6vFgjlMHt/Evg7W/AXiWTw94oha3uUAKf3JV/heNhwy+mP06V8g4K2p+lqVj9f8A46fB79k7/goh8PIbTxpapq32JW+x31uRa6tprtySjcsq5xmNleJj2Pb8Dfjh/wAES/2h/hoZ9W+Bd/a/EPRkyUtn2WOpxKOMGJyIJf8AtnIM9oxxX2F8PfEF9pWox6hpc7wTRkbZY2KsMdMYx+Vfo18P/j54huIktde23WMfvT8jjt9DW9DMp0LW2HPDQmj+SHWvHX7UH7OVy3hvxb/b3hYxZT7Fq8EnkN2ICXSeWVPT5cjFfJun+LrvQdZg1rSvLeW1fcgOCvTlSufukHH0r/QYutQ0Lx5oL6Xq1tDqVrMMPbzqk0ZB7FJFI/TFfK3ir/gnF+xZ8RLqS+8SfCvRnmcZaS0tzZkn/t0aIZr6PD8W0krONvQ8fEZTd2P429S+IHh3xKgvG8NpYXb/AHnspykZ6c+U6sB+BFeb6hqt3Bc+farIvPy/MAV/EYr+0jSf+CPP/BOi4lH2j4aaijHjFvqeoIPw/fNXpun/APBFj/gm1eyKbf4Q65e7eNranqjA/wDfMor01xvT5OWx58cgiumh/F5p/wAefiRd+Dbr4fXmq3M2lXoUTW8rq4bYQy4ycjBUYx6VxK+P73w3Zva6RqElssjbmSMrkt04r/Qb+FP/AARk/YZ0W+ifw7+zVDeTfwyan9uuVH1FzcbPzFfo58O/+CeHhXwFZr/wrf4Q+DfBYjGVlisLGKVT67o45JP1/Gsa/HaUOWMS6XC1LotD/Mo+HHwP/av/AGgJoYvhd4D8VeKRPgI9vaXRgP1l8sRKP+B4Ffqj8A/+CAn/AAUK+Jrw3PjfTdA+HdnLy0mt3wuLgL/172fn8+zMlf32Rfs++KLOPZr+uxZ6eXZ27MoHoDIVX8Qtcpr/AIITw9GRaPPI+Nu52Cj6hUAFfMVeNsS/g0PVo5Bh49D+dn4Kf8G2X7LHhOCLVv2nfiRrXjGSIBpbPSo4dGsTjsZGM8zLx1V0NfqP8K/hl/wSm/YZs47/AOAnw20W31q1+5eW1n/aep7hxzqF6ZGT6q+K6n4lQXt15huWaTbx8+cfka+FvHG2ISRAEKvbgD9K8PFZ3iqzvOR6VHA04fCj374zf8FQ/i5rDvZ/DfS7fRkHAub1jeXA/wB2PiFOn9018XP8bPir8UtZTUviNrt7q8mcj7TKTGvskS4jUfQCvI/Eio1wWxgA9Pp+VVNE1ax0ybzickdh/jXnq7OnY/Q/wLqMrxxqWOMYAHb8K9O1P4l+D/AVut/4q1CK2X+FR80h9lRef0r81dd+OZ8I+HpNa1XU7Xw/p8WVa6uZUhQY7b26n0A59K/Jv48/8FKvh1odzNB8MbSfxbfZI+2TF7ayDdiCR5sv4Kg9DXpYPJK9d2hE4sVmFGivfZ/RR4x/b0v0sXtvhjYRwiJTv1DUCPlQDqIshV/4Gfwr8Pf2lP8AgoNpt/rMsianL431iI7QS5FjA3oGHycdMRL+Nfjtr/x/+Ov7Q+uW+jeKr+5vY7qQJbaPp8bCBmP3US3iy0rdMbtzV+4/7H3/AAQY/aY+OsVn4q/aAmHwq8NSbXEVygn1qdD2jssgW+fWcqy/88yK+2y/hilRjzV3qfnfEPGrp+7T0R+Y998Zfi38cNatvD2sT3F/JeTCOz0qwjdg7tgKkdvFl5W9M5Nfur+x3/wQS+P/AMYBaeOf2p70/Dfw7JiRdMTZLrdyhwdvlnMVoD0/ebpB3iFfuL+zp+zF+xH/AME6NIEfwe0OKHXniMc2rXeLzW7rjndKceSjf3I1jjHpXdeMv2kvGni9WtdHP9l2bjBKtuncH+8/Rfov519FCNWUVChGyPwHiPxJwNBtzlzSPRvg94E/ZW/YL8If8K8+BWgw6fNIo88xHz9Ru3QYDXd02W+gJwv8CgVmeK/iv40+IR23sv2axY8W0BIBHbzG6t0+ntXzfaDYyueSxySepPue9dT/AMJJpOg2o1HWJ1t1bhe7ufRV6n+VdNHI1H3pas/Dc48TMZi37KD5Y9ke3+HoS2y3gGemP8MV67beJNH0ABAwnuQf9WD90+9fDE/xjutR3Wegg2lvj1zKw9z2+grU0TxeiJ5jv2zn+fWssVglfyOnI88cPhV2fp74d+IgufDUquwDqD7DpXw/8RX1PxV4j/srQbaS9vbhsJDGOTj1xwqj1OAPavTfhH4W8ZeM9Na+nD2GlTfduJBgyL0/doeT7N0rwD9sr/god+yn/wAE2/Csuj6j/wAT3xjPGJYNAspFN/Ox+7JeTcraQ+7jOP8AVxtXjwqRpz5aCuz9sjkuJzfDwWLfLBHrXhz4D/DL4P8AhS6+NP7SurWFpZaIhurmS+lRNNsUU8GVnIE0mcbf4d3CqxxX813/AAU1/wCC/Hin4mW2qfBj9hSW58OeH23wXfi6QGDU76P7rCwjbBsoD2lOJ2H3RD0r8pP2vf2//wBqn/gol8Qra1+Id1JLYpNnRvCulBxp9p6FYus0wB+a4mywHTanyj3X9nX9ijSPCNxB41+MAh1LWEIeDThiW1tGHRpO08q8Y42D/a4NRXw8KC9ti3d9EfqPDnD1KjBYbAQsurPhT9nb9jrxH8XLyDxh8R3n0nw/I/mr2vdQJOSV35McbnrK/wA7dVH8Q/oD+C3wzt1t9J+FPwm0Q/MfKsNOsI8k9/fPq7ufdj3r1H4FfssfEr4/+JPJ8IWhjsUkC3epzgiCE8Ejjl39I0z74HNf0D/snfBL4R/AbQfsnw/8m9vZSYb/AFVmSS4nkQ4eMlMiJB/zyXAXvk818LmOcVa0tNEfrmU5PSw+j+I/hb/4K5/s1+K/2cP2srew8X+T9q8TeHrDVXEHzJHKu+0kjLdHZfIG5hxzxniv6jv+Dc74oN4v/YqtvDFxN5kuhyyWZGfu/Zp3Vfp+5eL8K/MH/g5o8K41z4WfEtIseRLq3h+ZwAMKTDeQA+2DLitb/g2j+LyaOnxD+G104UQzxXsYY4+W5h2t/wCPW4/OvsMUvrOVRa3R8nhZKhmsk9Ez9Of2u/2LPjN45/bI1r4hfCHQoUgurvS9bi12/njhtIpoUj8yJW+acsHi3FY0I5HTNet/E39jL4W+O/j/AKl8d/E2uaqr3dxa3i6dZukMSXNokaiQzYaRgWjUkDbjnmub/aj/AOCvP7GfwCu7jQvGHjGDUdVgOG03R86hchumGEB8uM+0jpivwl+NP/BxnDI01r8IvhxLKAx2XGs3ohBHY+RAsh/8iV83RwWOqxXJGyPZr/2dTblOV32P6kE074YW/ivUfiRaeH9Mi17U5RPdah9nR7mSQKFD+awJUgBR8mOlM13xxLdKDLMXHbcen5fWv4qD/wAF8f2utSu3W10fwzZx5/1Xl3EhH/AmmH8h7V6Zaf8ABd74zTeFLy21Hwfpba9lRa3cc8y2SL/E0sGTISMDaFlUetaLhHFStcj/AFrwlPSMbH7Bf8FlbRPGv7FvjSSIiU2en2t706GzvYXJ49ELfhX8yv8AwTi/aS8Cfsx/FDXfGfxAu2tbF9NgZBGjPLNPb3CMqRog5YqWwPlHqa5j9oD9s/8Aa3/aT0u6sPHninUL3R3GJ9N0uL7Pp4jP8MscCjcmB/y1ZuB7V49+yz8DNQ/aR+Mul/CTS9Sh0Z79Xke8ljaZY4ogC2yJSCz44UblGepAr7rAZP8AV8K6dbY+HxebPEYlVqSP08/ak/4LkfHb4hy3Oi/ASzTwPo7HA1K62Tai4PHyrzDAfT77D+9XzN8Gf2Hv2u/2xdUX4k6vb3dtY6iVeTxH4laUyXAP8VvCwNzcD0KKsXbzBX9IvwI/4JKfspfswfZfFup6afEfiC3ww1fXhHc3AI/itrQA2tqP7pCPKuP9ZX1x4s+INjpUTQ6Su1n5aRjukYnuznP5du1fKVeIMPhlyYWJ9lh+HK+ItLFS+R+M/hH/AIJ2fAv9mHwXrnjTWIm8U+J7LSNQnTUtTRG8oxWsrBre1G6GHG0YJ3SDH36/KD/gkfeT6T4h8daojGNhpNjEcdfnlkJGR/uV/QF8dfEz6n8NvHMiyYMfhfWH+mbOUDn8cV+AP/BM61ksfD3jy+RfmcabArfRLg4rqyzG1K2HnUqM4M2wNPD14U6aPunxNrMdrbspIXdnjjgk4/rXwL/wUX8cyar8S/D/AMMtPYyL4W0iPdGvP+mXgRtuB38tYuPevqX40/FX4Y/s+6LF4t8eEalq0wzpejKf9fIpHLKOViVvvyN8vZQWxXxR+wt4R139rn9uXw9d+LD9sJ1CXxPrDY+QQ2P74JjoEM3lQqPQgV6+X+5TdZ9EeFPCSdX2fc/p3/ZI+A0fw2+Hngf4YyqA/h7Trc3XGAbhE8yf852avy6/4OTvjh/Z3wn+Hn7PNrKVm8R6zNrd6i8f6LpERSMHp8rXNypA6Zi9q/oS+H9tFZXF1qcoy+0nPp3/AFOD9K/hg/4LbfG2T40f8FBvFGn2c3m6b4Gt7bwva4OV822BnviOcZ+1TPGf+uYr82U3VrOZ+vRpezoqCPyk8oLH6EcY6VV+ZBzx/KpjJkkgVTlLZC16sdjnhGyIpDtXHrxVT5lUKepqWVsEIaacGTHp2q79CgZF8pR6VBLHlVjFWZMBwKrM22X5ucUrAVp0A2g8dqogukRGR/nirsx8zCrgisto2Q4PfH+FKb6CTGzMWAGKq/Nt/d/KTyfp/kVJOWWFE7/0qu+CmNvC5HTj6VMlY2pblKbcw3oTzzj2/wAiqT7mdtvQVauQqOfL+px6VWOApx3/AJVD2CfYrk7R8/8AkVBJgbSOgqZ2CD/CqZyJOTxnpUvYzGTA4IX1yB+FZ0y7lVV4welW7gESeX3PNVJY9z/Pz+lc7qOxmlZlOWcrhF61AGd1CnueKskIHO7oPSqwUBQc9+awh2NUiGMkv75FJM26XeafCyq258d8Co2xI+T9fSqvoWtxpUK4Ptiv1b/4IZFh/wAFb/2fgOn/AAmVjj/vl6/KVt5bmv1c/wCCGOW/4K4/s/gf9DlZfoslYx2NabP/0P4F8Z69KdnOFFRNkdBwRTyVxmqoy0OVotRMS+3HH+cVfLKjeWD161nIx/izyBV4QpIQ6nAx/KtZvQwZaUADcBj0qeJjJLgHAqBmyojwKsIUDAH26VvTegU12JgCcAfMd3Aq6Mcc/TiqO9zGFVauwvJsy2D/AJFW2E2jQj6ZX2z/AIVdiG1cx/dyDVGPgYP+RWhCyA7enApFF7JI29R6VZjDDGT8wODiqkSknGasQyNv+Xj1rS90XBXdiwHVjuU+350BwYxxzkcdKI5gJCMcYz+PSnKw2Bccnjn8MVVrlPseh/CrxhJ4A+KGh+N4/u6ZewXEuO8QYLIB9UJFfsd8YvCEXhjxRLfWZU2OpqLuB06HzPvgfjyPYivw/hh2vuf/AFZ649/p6V+53wC1WH9o39l+y0KZ1/t7wu32HnG7dEo8jP8AsywgL6bl9q+t4TxXK3Bn5b4gYVrlrrbZne/DS3034qeEP+Ee1GY2+pabhoZkOJEKf6uVT7cKwHYfSvy+/aO+EXiDwJ4vuH1C1EQmcyfuxiM56tH/ALB7AdOmBivs7Q7zWvBGsDVLXdbXdm+xlfsV4ZHHp2x/9avqfU734c/tEeDJPDHiWFEvNpbYMCWJ8ffhPce3519lmGXRr0bH5jlWcVstxSrQ1g/wP56LHxFrXhrWrXXvDt1LY6jYTJNbXMDFJYJozlHjbsykcV/S7+x1/wAFC/gn+2D4fsPgT+1t9l0TxmxWKz1RyLez1GQ/KHWc4FndscZRsRSH7vJ2V+Gfx3/ZY8ffCq8m1myibVNFB/4+YBkoP+mqjlT7/dNfKEQmLkbcq/BUjKlfcfT2r8txmXTpO0kf0Nlec0MXSU6Uj+1Hxh+xL8TfA0sl/wCC1fXLGPpEAFvUXtmMDEnsU/IV554Ym1PTL82OoRSQzRHEkMiGJ1PurAEH8PavyY/Yk/4K4ftKfsm21j4R1BofHfg+2UAaJrc0ga2jH8NjfLumgx/CjiSIdkFf0z/A/wD4Kw/8En/2tNPh0H4z38fgHXJtqfZPGVuq2+88bYdYhzAFB+6zywHH8Ir5ytCa0aPchZWaPKPCXiqNFjyxUjoDX2P8PPFTCQIJCeOnT0r7R8Gf8E8/2Y/ivpa+KvhTqs76dNjyrvQtRg1GzI/2HHmrj6Sele0aP/wTE8O6cwm07xhcxgdFnslP5lXWvOSdzZI8h8CeIHkMTLJ1xj2r7c8GazI0SL5zduhridE/YavfDcnmDxbA6L0zalf/AGoa9KtfhXp/hJQtz4ihl2DnZFj+tJtiS6WPoPwpfQzMr7s47Z7V68jWzQAnbtwK+JZfiFp/hVNtiftbL6/KP5dK808TftRfEezhkbQrK2t8fdkaMvj3+YgcfSiKleyKufeGt6HDd5fghuMD/wDVXzp8TNN8NeG9NfUfFGoWumQAY8y6lSJR+ZH6V+L/AO0h/wAFHE8B2syfFX4w6R4aAB/0YajbW02PaGA+ee3AFfz8/HH/AILL/svaXqFx/YGo6t43vRnMltayiOQ/9fF6YvzVW9q66GT1pv3YkfWacXqz+mz4qfFn4K20c1ro2onVpucG1U+Xn08xgBj6ZFfnH468VQ6j5jwJHbxgk5LDge54AGPwr+YLx/8A8Fkvjj4omksvhX4fsfDVuflWa6dr+5A7fLiOEe2VYV8ZeMvjT+0p+0JeLpni3X9Y8RSzvhLKEt5RJ/hS2twsf0+Wvrsu4KrTV56Hi47iOlRR/Qr8bf2w/wBnL4ZSPHrfiOLUb1cj7Jp3+ly5HZvLPlr/AMCYV+X/AMVP+Ck3xJ8SWb2Xwb0eHREydt7d4uLjHtH/AKmP8d9bP7NX/BGf9ub452EGpah4dj8F6NLg/bPED/ZDs/2bYBpzx0/dge+K/f8A/Zv/AOCDn7Lnwot4Ne+PerXPj29hGWjlP9n6UmPVVbzHA4+9KAf7or7DB8L0aW6ufkHE/i/gsLdOqr9kfyeeAPAf7TX7Xvj+PTtLtNb8e65KQEREkufLB442/u4VHsFUV/Qh+yx/wbl/FfxfFb+JP2s/EMPgqwfDNpWmFL3UpB/daT/UQ+nHmY/u1+/uhfF39m/9nXw+vgf4K6VZ2tpBwtpocCW8Ckf35QAG47/MfxrzjX/2nPH/AI1ja1hmXS7Vvl8u1PzsuBjdL978sV9BDDOEFGnofgudeNNeu26MbI7f4Ffsz/sT/wDBPy1/s/4JeGrTTdX8srJqUwF7rc4xyGuGyYQw6qvlx/7NegeIP2hPFfiCEw6OTpcLjlkO+d8+r9F+iivjebUnB808bupPf6561rWfiG2sbdp7x1iiXq7NtUfU1rTy1fFJH5BmvF2YYm95norXwa5aWQku/LMTkt7ljzWvHqllbWrXE8qQwp1Z22qPxPr6V8p+M/j5o+nRGDwzGL+X/no2VhXHp3b9BXzdqHxG1zXr77Trd00pT7gPCLjsqDgDjr1rs51GNkeHQyStWfPPQ+/tb+Nltaobbwym89PtMq/KP9xO/wBT+VeMX3i/ULu7N5qE8k0r9Hflj/QCvE/D+t3mvanbaLpEMt3e3hCQW9uhlmkY/wAKIgJP4Cv0g+EH7CvirxLJDq/xnnfSbYkH+x7Ng97IAOk0wykA45Vdz47pivHzDN6NFas+04e8PsZjZ8lCGnc8O+GNh49+KHiGPw54AsJdSu1/1oX5YYF/vTTcJGv1OT/CCeK/WLwX8Fvg7+zj4Cn+MH7RGv6ekGkx+dc3186w6bZ46BRJtMrk/dyMscBUzX5F/thf8FsP2Ov2AtGuvgj+zdpln458XWJMZ0rSJdmk2E/TdqGopu86Vf4o4fMlPR3iNfy2fFT9sn9sv/gpF8U4H+Jmp3PiW8hkL6fo9mPs+laanfybcHy4hjgzSlpWx8zmvnKtWvivefuxP6Q4T8MMLlv7yrHnn+B/Rr+3L/wX2k1qDU/h/wDsaxyadYbWh/4Si8j2XMo6FrO1cYgU/wAMso39wiHFfz56D8Gfin+0frk3jLXrma1sdQmM13rGoFpZp5G5LKHO6Zzz8xIX36CvnT49eCvF3wd8UyfD/wAYyQvdpawXBe2YvCUnTcAGKrnZgqeMZBxX7vf8E+/ht41/ai+EHhOx8KBS9nZC3vryTIgtFtZGi3OQMFiF+WMcn9a6cdWpYPDqdFH3GUZTPE4jlq6W6H50eFpYPgTqVxpvw8sobVrSUxXdzdgSXN0YyRhnx8qH+4mFHp3r9NvjH4Y+JPgjw74I1v8AtC30rRPHPh+PVraeGPN0HYAyRjf90KGQgY3YbPHSvrD4nfDz9hH9iz4jGb4k+GdW+IfjfULRdUhS4hSSx2EmMsqOy28eXQkhllZcD1r6g+JH7c9xpn7LPgv9o/4Z+HNLd9W1D+zWTWI/tC6VxLG4jaIx/MWg2/JtGCOK+MxePdaUZtXPvcPgVShKCdin41s/jb8av+CYPw1h+Dp1ttVt7uPT9WsNLT7JcX9tC81qzSqmwtGGWOVj8quWLNwK+mP+CZXwl+NXwI+D2reBPi/oUHh7frDX+mwRzxSv5NzGnmeasbuEPmKTgkk5Jr5Q0T9t7xP8Xv8AgnP8ZfHfjHxxY6T4q8JeZHBqdi8dh5cUqQzW8cTI3DvtkiTGXbjvX8gXxK/4KN/tEaTc+JtL+EPjLWtJsPE8CWup35upTe3UMbbtqzSM0kK84yrKzLwTjK1lhcoqYiLhsjStjoUpRmtz+g//AIOMP2o/2ZvGHgKH4A+HvElvq/j2w1zT9Taysf362IhhmguFupl/dxOyyriLO8nqoxX8rXgvxn8VGuLrwD8KbrVvO8QRpBd2GlPKHvIojlUlSE5aNSc4b5fWvqv9lX/gnj8Vfji9r4m+IAuPDGg3YWWHcmdQvVbBBihcfu0b/nrKMnOQjDp+2eh/Bb4J/sn+GP8AhHtFsE00yIN9tbDffXRHRrmcnc3cfMdo/hXHFffZPl9RU1hsPG58hmuKpc/1jESsfkL8JP8Agnz8U/EsEcnjy6h8ORtg/ZYFW6u8ejbSIYyT/tMR6V9an/gnr+z94GslvfG1v9pbp52t3/lKf+2cbQx49sGvc9d+LPjnUN9l4WK6DZHolt/rtv8AtTHn/vnbXy38QdI0PTrCbxR431BIYuhubx+S3+85yx9AOa+5wnAdepG9edl2R89DijDKXLRhcdf/AAg/YI09Htb648L2zL8hMckwI+jxt/7NXBav+w38HfiJZyal+z54st1niXcIUuUv7bPo6jNxEPfL4/umvhj4lfGvwZHO1r4SsZdQQnHnsPJjb/dUgt+gr5+j+JGs2+oLrWlw/wBn3cJDRT28rRyoRwCrLgg1Nbg1U/4NQ+jwzlXXvw0PqbTdV+N37KPxEn07Vbd9OvJbWW3uLcuzWmpWM6NGw3IQksbBjtI5Rh2YYr0f/gnVrP8Awi37YXg91IAlF1AM9ybaRgPzStD4c/tDaf8AtPeF4/2dP2j5449SuXLeG/FMoCvb6iwwkN7t4EcxARpeM5/eAkK48O+A+pal8L/2nvDD+JLdrO60jXo7K8hf5WicsbaVD/u5IrxcdhKioTp1VrY4PqXsMRGUdj+674oeP5ZwX8zO5Qcg8c4r4c8ZeOSSwSTPOCK2PHnjcXejWd0TgyW0TYHclRxivy+/aQ/aq+GnwUjLfETU/s95Iu+HSrTE2pT9MfusgQIezylV9M9K/AoYGrVqcsEfs1XGwp005M+ivi34oX/hS3xHulPEfhTUgdvbMDCv5/fgl+0lqfwO+GGt+D/AGlPqXivxHqFubNim+GFUi8tcRr800pZjtjGB3Y4+Wrnxd/av+PP7SXhrVLfw5plzoPgTTPLa+tbHfKgV3VIjqV4FXcWcqFi+RC2MITzX2B+wL8LfBPhr4YTfHfxBEh1eee6iiu5vu2llbjbI0a8bdxDb367QACBkH9Ly/ArB4R+01ufm2aYj61ilydD87P2gfhb4n8BWOn+Kvj3q82p/EPxYxuXtWlDCys4uMzEcFycJHHHiOMKwGSOP38/4ILfs5z6T8JvFf7Sms25SfxTc/wBj6YWXBGnac265dc9pbn5P+3ev5y/HmsfEL9s39qq30jwFC9zqfjPVoNF0GA/wQs4it93ZVVcyy9MfO3ABr/QO8JfDbwb+y5+zx4c+CXgoAWWh6fBo1m+ADKsKAzTsBxumbdI/+05rz+IMa6WFVLZs9jIMsvX9q+h4d8evj34e/Zp+B3iv43+Ifmt/Dmnz6j5fTzZUXbbQfWacxxj/AHhX+cp4r1vV/EevXniPxJM1zqWozy3t7M3/AC0ubmRpZn/4E7E1/T3/AMF6f2ko4fCnhf8AZh0C4xcavKPEGsJGcbbS0JjsYmxjiWcPLtP/ADwU9xX8t9+2W+Y8mvj8FG0T7HEz6FUttTK1U6Zap5PkQAVTd+OK9BLoZR0K5YHluAKdEADu7UkvMYVeppkpKgFeTWvLbYBcrncfyqLAxv8AxpzH90B0Y1DcfcAHf24qUBRijBfAbiqsrEbw3IU4GKvIFUExkHbWc+OcAA/e/Xipcrgo2RXkTfgnoP0FV5T5xyCMDj24qS5EipgemSPUVSabYmQvfFRPU2hoyOb92fk4z14/Ss+RCvI4z1q7I+0VSkOWDfwqai9iars7lZpCFbdjgY/lVdujY7H+tSTlQ+F6HFRZJODzjpjtUN6GRVlG6QP2P/6qo7mZixzxVyRtqlugrMmYhAQMc1zSbaQ0iGRT1xnOKYMAcg0u8h8EdsdKe4XywvQjt/KhPY0Y0xrsPTIqBflHfkYqR1O3BFNJIAGeCKi9hwkM/wBodT1r9YP+CFbZ/wCCuv7Pw6D/AITKy/8AQHr8n2BK5PpX6vf8ELG/424/s/Bv+hzsh/47JWEDeFj/0f4Es5G5e1T7AWBPf9KhRcDZ3qVAABnmpi+Vo5pFuPYF2H+Lrj2qwjERfT8sVQTJ+X0qXzd3yHvx7Vu3fYw5TSLovTmr6oCgb1ANZsTBk9anhJJwRgfTH8qqk5XuZpW0NEDGF9aswKTuQcleKz4zuGWJIwAOKvRHb86dDg/yrplEc1oXo13M6t/D/QVdjypGeOxqif8AWmQjirkbYA6dPyoKhsjQjbv044qcZC5x0Iz9KpQtnO7rnmrSnD5Uex4/SrWxcS3gjJHp0qwvbIyOKrNlMHHPSpyowpUYApQ3Jk7SNUIQBj9PpX11+xt8cU+DPxdtrjWn26LqpSz1LPREJ/dT/wDbJjzj+AmvkNR8mD04q5buQwI6dCM4yD1FdWGrujUUkcGaYCOKoulPqf04fGj4QW3jCy/4SPw5s/tFEB2jG25Qfd56b8Dg9CPwr8zdWutV0nU2+z+Za3dtJ2yrxsO3bBFe0/sHftSw+LNEg+Anja4/4mlpFs0aaRsG7gXP+ikn/lrCP9WP40GByvP018TvhDonxBzdk/Y79QAlyg6gfwyDjI9+o+nFfq+BzNV6Wh/OOMwlTLK7o4le70PDPhv+0UkezR/iNH5o+6byMbuMY/exjg+5H5V2Xiz9if4D/HCD/hKfA9ymkXcnzG5sAHhYnn95Bxj3xtr5b8X/AA78SeCrv7HrEBj/ALkq8xv6bWGPy6+1TeDvE3iXwnqA1DQLua0mGMNEdufqOhFdEsJGekkS6c4/vsDU5fyOY+If/BPT47+ECZ/D1rF4hso+RJYt+9x7xNhs/TNfF3jXwX448Ju2m+I9NurGRRgxTxPGfxDDH9K/cXwX+2B4u8PxJF4ssodSjxzKjeRL+JHyn8hX0Npf7VfwM8aQGw8XxvChGGjvrUTxf+O7uPwrhr8P4afSzOzDeIWbYX3a1PmXkfzHfD34h/FL4QayPEXwn13VfCt8p4udEvLjT5s+72skZzX6U/D7/guB/wAFa/hkI7Xw98dvFM0UaAImqG01Q4HA5v7edz9Sa/Wa1+Hn7CXxFcy3um+F5WfjC7bR/TsY627T9gj9g3xA5kg0K1O48fZdTbH4DzWFeb/qhRvuet/xHCEP4tKS+R+f9p/wchf8Fh0iSC4+KNtcjoTceH9IZvzS2UVg6v8A8HCP/BW3WlZJfiXbxZPWDw/pIOPxtWr9dPD3/BMb9ha4IeTQp8HoDqb4x+Br2HTP+CdX/BPPQlE974btJOgxdanKR+XnKD2rpjwjhFq0ebifpCYaOkYS+4/mm8af8Fhf+CpvjwPDrPxn8RwJIMbbCO00/wDI2tvER+Br5e8R/FP9qn45Srb+O/FHivxW8hx5d9qN7eBs9gjyFfyFf2gaV8BP+CcPw/CSjw94KtWTobh4bl1x04kd67+3/ac/Y1+F8Ig8K3ulwCPomj6d0x2DJEo9vvV1UMgwcHseDi/H+vNWw+Hkz+Nb4a/8E8/2vfihLGfB/wAPNU2yYAlktWt4/X/WShVxX6F/DH/g31/ao8WzR3fxO1fR/Cdu3LrJKbq4A/65xZT/AMfFfvbr3/BSr4cQDy/DekalqZ/hNw8drH+hdv0rxfXv+CiPxd1oeX4Vs9P0FCMB40+0zAf70vy/kle1Gjh46RifIY7xS4ixH8GmoLz/AK/Q5P4F/wDBAb9lLwAkOt/FS/1XxtcQ4LrIw0+x49drb8DH/PUcV+k/g27/AGL/ANlew/sj4X2GhaFNGuPL0K2W5u2wOj3Azz/vSV+Qnin4v/Ez4gz+b431291NTztmmby/wiGEHtgVmWury26hVPpgDGBT5H00PiMfXzXFu+NxDfktF/XyP1h8Vfts6pdDb4J0lLbuLi/fz5ceqxLiNT+Yr5u8TfFTxj8Q7kSeLtSuNQI5VJG2xr/uxLhB+VfKNpr8pwD09MY4rRTx1pdguZmyfROTSVK254v9kW2R9B292wYlnIHYGurh8UWGmRrNfSi3iAHzOeD7CvkTUPirfzx40mEW/GNx+ZsfToK8nvPFFzdTma9meVwernJz/KtHJRiaU8glP4j768R/HGwgs/I0CDz2PHmS/Ko+gHJ/HFeDal481vXH83Wboyj+FeiDtwo4rybQtTvPEt5Ho2hwzXt3JgJDBGZHOPQKD/KvpjwX+yj461y6jvvH10mg2h/5docTXrD0wPki9OSSP7teTj85o0o6s+myHgLEYiXLQpnn0GpfbPLtIQ888zbIkRd7sT0VUAJJ9hX1X8Kv2LPiV42vY9V+Jkp8L6e2CLcASahKvtEflh+shyP7lafiv9qf9hz/AIJ36AY/F+oQ23iFojt0+zC6j4gucjgN8w+zoR13mCP0z0r+e/8AbS/4LpftSfG8XPhD4Dr/AMKt8Lygxs9hL52s3Cnj95fbV8nI6rbKh7b2r5Srm2KxP8GNkfunD/hBQoWnjHd9j+mj4qfts/sEf8EttIl0PWrpf+Eokj/5A+nbL/xBdE/dFxJlfsqEdfNaGPH3UfpX84P7bf8AwWr/AGs/2z4rv4c+EHf4f+BLz9ydC0WR2vL1Dxsvr5VWWbcPvQxLFCehRutfkr8Nv2eviZ8R7xPEOsq+nW14/myXd6S9xOTySFb52Lf3n61+pHgT9ni08HeGrK9+F9g91cM3k3N5Im6Vmx03HaEGOoXAUY71yweHoa1PekfrWFyqNKn7KhHlifJnw4/ZC16e2ttc+LM58OaWVDpZQrvupF7bgAVhzjHOWHoK/ZL9mDwj4T0jwvb+GPhho40/zZ/J+ywoz3MsnRXY43yM3bJOP0ro/hR+yh40+I3w71vWvEviK3sLjw/cLM6SSRzR29sykzyXHl5ZQir8oAbO0jPp+rv7BVt+zD8M/FV14O+EniiXxX4mv7MXd3fy2zpF5VuVDLblowqDLchSWPcnAFeDm+ZTqwaXQ+gwOEhSmtD8Df8AgrZ8APHHwyvfAfxA8Y2J0+XVLa60p4CQZEaydJo/MAztOyc4U/3a/TX/AIN1Pi9Fd/Anx78IpJFMmk6zHfpH38u8gxn6Bom/OvQ/+C/XguHxj+ygfHFvzL4b8R6deHPLeVewy2cnPpvaL9K/HD/gg18XB4F/a98Q+BbyXyrfxLoDuCehms5VZf8AxyV69WnJ4jKfQ8V0fYZlfuf0F/8ABTGH4DQQ+FPiP8bf7dZ7b7Zplouh+WDJuX7QVnd/uBdpKlfUivjqz/4KPfsB/Av9ky70fxT4bdLGw1OT7B4O1Fk1O71K6O2dZ13llVC5+aRxsjPA3HC15/8A8Fu/24vg38P/AIX2vwKsb1NS+In9pW2qwaZAFZLGNUdPNvn6Rh0k/dxjDtwcBea/mG/Z3/Z0/aL/AG9PjE/hj4d2r6lfttk1LVbvcllptt0ElxIBhEHSOFQXfG1FPbjybJfaUVKp0O3MMZ7Oq2tj6r+PP7XH7Qn/AAUK+I+m+CtD0WO006W6x4f8GeG7dY7OByMB/LiVPPm2f6y5l+6M42JwP2e/Y0/4JE6Z8MfsvxF+MsVtrvjJdsscDbZdN0oj03fLcXC/89SCikfuwcBz+hH7CX/BO/4OfsZeETZ+G1Op65eoqat4iuYwLq7I58qEZP2e2/uwqe2XZm5H6P6pYWlvoE823y7a3iLkY9BwT71+nZPkMqtoyXLA/C+M/EfD4O8KD5p/kfnV4t1jTvhwJbHwifNvpQwm1GQZyT1ESn6fer4e8b6ZNqF619c75ZZzuy3LsT6nvX0V8YvE+m2dze+ItanjstOs0MrSytsjiiXux4H0/QdBX4R/tTftpar8Rre48EfCR5dP0Nt0dxejMd1er6L3hhPoPnYddo+Wv2WhgMPhKaVJH5/ksMxzapzVHodh8eP2rvCXwvuZfDXg9I9b12HKS/N/olq3/TR0P7xx/cQ8dyOlfl1418deNviXq41rxpeyXtx0TeAIox6RxgBEHsBWamlynG3hR0HStq20h+AcnGMjpXnrFNysz9xyzJ8PhIJJanHy2fmAbkx0HtVU6V3fFeqxaVCSdqdAAQKeukhVJ2YHFY1LvY9aOYWOCtNBSWPEq71dcYxgenSvRPip4pn8RazpPja6fbrM1lFHfuPvPeWJ8pLhvVpoUhZz3k3mtO30oxoOuB6DmvPPiTbNYXFjcMdqsp/8dNeXm+HjOjeSOLE4rn0R+lfiP9vD9p/9o9NL+C/7M3h65sdSktUhklsF+1arNhRvZX2+XaRK3/LTAZVxmRcV6l8IP+CQOkeDJE+KX7eniLZNdSecdAsLgzXNy55P2m8U75Tn7y2/y883Havef+CYvxTHw9/Y6t/+ENsbW31bUNS1D7TftGhlPly7YsjHzsqHapfcFH3RXofjTXtU1zUpNY1m6mu7qcgyTzsXc+xY+3AHbtX8551m3spyo0I2P0HKssVSnGpVdzwn/goT468C+Bv2GLT4c/CfQbfwx4f1TxNbWttY2yLHm3sopbhncJgFi4TJYs3Ayxr4l/aH+Jcnwh/Yv8G/A/R5RHq/irTY5boJw0VjIfOnJA5/fO/lD1Acdq1f+CpPiuzs/DXwi+Hd7O0ULpqGsXW3BKpPLFCj7eM/Ij7enSvjfwX4Q+LP/BRL9rnQvhX8MrbdrPjG8h0vSoWBMVhp1uuBJKRnbDa2yNNMfZj1Iz9Lk0E8Kp1notTw8VR/2t+zXkfuj/wbi/sP3HjDxhrv7cfjK0/4l+gCXw74aDrxJfTR4v7pOmRbwMtupHG6aTulfuN+038WfDmm6tqet6pepaaD4btpjNcsf3aRW6mS5mJ9AFJ+gr7NvPAXw2/YG/ZD8OfAf4UKI7fRNPXR9JJAEszqN11fSY/5aySM80h/56SYHA4/j0/4LTftVL4Z+G1j+zP4Vuf+Jl4vxdavtPzRaTbycIcc/wClzqF944pAeGr85zfFyxWIbWx91gaCoUkj8Gv2l/j/AK/+0t8dvEvxt18PEddu99pA/wDy72ESiKzg9P3cKruxj5ix7188SZY7TxtppYO7MRzn0pJmHGe/ftXRGOyOeU7y1KdwQHwvIqAuMYxS87d7EbeAKYzYBYDt6Vuos0TGld028dhjFQvlpBtPFTldqbugFQkfJvHFaJjEcAhWUcCs+R4920dF44q+7cZbpjj+QrKkVWbcOCSOgpLTcmSGSn5Nvr6VReRvMPrjGPSr7FMBV4/GqpO1jvxz2qLFopzfIpK/Q1TyFRVwD3OfT2qe5fEeUGAeKqMrsN3YdP0qFsXPyIixCYOGqpJhvnXtyalmyoKD+IY6YqjIXX6cD8KkhsimdBJluB/nFVjIOH/vVI7JKN2OCcfpURH7tUHUelRoiUR3BPldAM/0rNlKkjbVy6A3LGMt3H0qk20j5Rx71z83YqIzcC42DFJI+wcDk+tNUH76/TjtTWLSdfX8KypyaVgtrYLl8lQRVaUkEFO1PYndgde1MxknjoKnmujWC2JMHG1q/Vf/AIIZYH/BXD9n/wBvGdj/AOgvX5RPnGPTrX6u/wDBDFgn/BXD9n/d/wBDlZfT7r0tjaG5/9L+BbkcGjrSNnbxTgTngUuZHL6D4wNwHrViTMcn7vgcflVYEqRipw5wemK1p7aGbLNuQp8vPuKuxfMPnH0BrNtlGfMPGelaAGVJ7Ditab5TKoX8ZTgAHFKrts3bcYqGN5Wk8pT05qRXkX6k9q3Q9zSjf5dr4wavLu4JGM9Ky0+UZHUfpVtB8i7Bj5aq9yVU1sbMbZwFJOKtRttb5Dz7celZcbFFzx1wPpV9MREDrntRE3s7F9W/dbPX5j3wfQVZibPUdOMdqppcbSYkyT27CrPnLgE9GptdiZJFuMT7vLbp+VXoxhcY9P8A9VZcROeTV2MsQSxzRJXRElpoXbS9vLW5S+spXhngdZIpIyUaN05V0YYIZTyCOmK/c/8AZM/bO8OfGe2tPht8YrqHSvGfEVpqEmEtdVxwBKeFhuj3HCSHlcN8p/CmP5oy2elMdFkhMbDjjIPtXZgMfOhK8Tw86yKhjqXs66P6rdf8LSoX0XxJaA+Z8pSRd0bY4OOMcfp7V4r4g/Zx0G7DXHhyVrBsfcYF4ce38S/rXwr+yP8A8FGfE/w2t7bwB8e7V/F/hcbYxcsd2pWkQG0BdxAuEQdFYrIoGFfHy1+73gfw98Kfj14THj79nTxPbatZcBoN2TCx/glUjzYG7bZU+hIwa+9y/ienJJTPwLO+BcfgpN4N3ifkZ4n+D/jbw8GlubMzwJwZbf8AeJx9Pu/iBXmn9n3MbFGXHt3+mOK/YTxR4J8U+EZ9viLTprT/AKbDmI9uHXK/hkV5pqXhrQNcy2pWUF0SOrxgn/voAGvfhjYVNYnyss8r0XyYmnY/L4mVByNoOB0z+VaFg7K+44A7DGK+9bn4F+BdSdnhtGhboohkOPybNLF+zF4dkJMFzdJ25CNj9BXRBxb1HLibC294+RbPWbi0TBfAIwOSK6K01eaZVXg5P1r3fVv2arW2T9zqMv4xL/Rqbp/wDsIBl9SmOOn7tQP5mtm6dzllm2Dkro82tNUES5wEI9Bz/KtI6tK+0Bic+lewj4PeH7UYknuHOMH5lX+S1FH4O8L2EhVLbzMcZkZm/TgVcqtNWscn16g/hR5xYak4kwW/D8q9a0VLyaFcRs2cc44/wrW03StPicGzgjjz02oBx9a69EijiGTjHXt/9aiGIha5xYrEpq0UZlvBcxR/vcJgcDvVldQdU2R8gcVm396u028BLseAqjP6Cr2meDfHOrtmy0+SNcfen/dL+R5/KuKvmdOGrYsLlFev8ECrNqVwzhSenb/9VQ/bfIHmTfKPX1r6A8J/s8XmpmOXWr8lj/yytE7f77f0WpfG/wAVv2Qf2XIzL8QfEGk6fqEQz5DN9v1An0FvEJJFP/AFHuK8OvxPTXu01dn3OU+GONr61Fyo888J+A/HXjYKfD2myPCf+W8o8qED13PjIHouele1eGv2VNP88XnjvU2ugg3vBZ4ihVf9uV+SvfIC8V+Znxi/4LV6ZayyaZ+z/wCFJL9xwuo68/kxj3WzgYufbdMn+7X5ZfF79oz9rj9rec6L4u17VNatZ2+XSNMQwWHsPs9uAjfWXcfevJrYnG4mN/hR+k5T4dZfhbOq+Zn9H3j3/gpX+xT+yRZzeDfCF1F4g1eH5W0vwyFm+cdBdaiW8hcd/nkYf3K/I39o/wD4K/ftW/GyOXw98PZ1+HeiT5QW+jM0moyg8Ykv2AkBPfyFhB6V8f8Aw4/YY+KWuSwXPiwDRLYY/cRAST49OP3ac+5Ir9Ivhb+yR4Z8F2O7SrHE+MfaJV3zN2+8fu59BgVwQ9hSV5rmZ+hUcIoQ5aCUUfkAvw7+JcXhG/8Airq+mXC6VHdwwXV5cE+a093uMe4MfMYvsbLHvX6D/wDBPH4U+CPin/wk17qWn29zrmhvazW80/z+XbTK6nah+UEOg+bGRkdK/T3wL+yhYeP/AIEfF34X61d28cniHw1JPpnnusZXUtNcXdp8zkYy6BPTDEV+X/8AwST+O/gD4H/tHNqvxWvYNP8AD3iHQ7nT7ia6x5McyFLiAyE4CgtGUB9Wr0qmInXwklTVrHNyKFZc5+hfij9jP4kzx3HxBsZt2kOyrJ5rfMpdsDZHHksD69Pwr7i/Zk/ZYSX4QeN/Ces2V3PqVzHA2lyXYktbfzkw2xN+MnKKrEjBU54rrvHf/BVP9jnwzbJDb+PdOYJGFSOzt7i4AVedv7qJga+RfFP/AAXD/Z60+Vm0WHXNccNgmKyEKntkG4kjx/3yK+IeDxcl8J7vtKKe5+uX7Jv7O+u/By91qfx4mmx6Z4g0o2N1Y2sjzSu2f4yqqm3aXGMkfN7Vm/Aj9lXw98AvHln49TxZdX9zZLPFDbx28dvAYZ1KbZDuZmABB4wCQOOK/ETWP+C82qGBovBPgDKjjdqWohB6DKQRH/0P8a+SvH3/AAWo/bA8QPJJ4U/sDRFb7v2e1e5dfT5p5GGf+A12UuHcbUOapmGGhZdj+qT/AIKD6Rb/ABf/AGNviV4XtwrySeGLq5iXk4n03F9Hj3zDX8IPwx+MfxC+Cnj+z+KHwsvBYa1b21xDbzlVfy1uYmhZgD8u5Q+UyOCAe1e6/Er9vX9tb9ou0h+HHibxjqupwasy2a6PpESwC9klKhYBBZosk5kOAE+bPTBr+j7/AIJc/wDBugVTT/j9/wAFJbQLwtxp/wAP1k6AAFH1qVCMY4P2KJv+uz8NHX02V0FgKLo1dW+h4uZYmFWaqrRI/Eb9gL/gkz+0X/wUR8VSfF/xrc3nh34fTXbPqPiu/UyXWqTZzLHpyzc3UrHh7hv3MPcs4EZ/s7+EXwH/AGev2OfhdafB34NaLBpthagSraId088uObq+n6yzP3ZucfKoVQAPUPjj+0R4Z0GKPwF8G47aKDToVs0ltI0jsrSKL5VhtYkAjwgGF2jy1H3Qe3x9pfiKW4cvdSs0kh3u7EkszdyT61+l8M8LTrQWIxCsuiPwDj/xAk5vCYRn0LZeImvL/wA2d+eygYVVHYewrzn9qf8AaD8A/Bj4ZC/8XXwtYJ8s6p880xGCsMMeQXLHrjgD7xAr5d+NX7T/AIW+C1ozXBF/rDJuhsEbGB2eZ1+4ntjcew7j+dL4/wDx+8cfHfx7deJ/Gt7Jd3A/cwjhYoYxwI4UHCIPbk9SSea/QVgopp9D824Z4Mq4uv7ev8JT/aw/aY8a/tC655MxOnaBbv5ltpiPvXcOBJO3HmS4/wCAr0UDv8jWekXE8O8D5T1z/n8q+u/gt+zL8TP2gNW+xeC7P/RLdgLvUJ8pa2w64d8Hc+OkagsfTHI/VTw7+zX+zv8Ask+FP+E++JOp2glteH1fVti/Pj7lrb/MFYj7qqry/hXNisQk9z9drcS4bAQWFw0by7I/E/wh+zr8W/GiC50HQ5xbHGJ58W0WPVWl25H+7mvcdO/Yb+Kkke6e70qNjj5DPIx/MREV6h8cP+CrPwp8PalJa/CHwzceJNhwL/UpPsUDY7rEoeVlPuYz/sivlOP/AILA/Fs3u7/hDfDjW+c+UDebsD/a8/8ADp+FfNzzmEZFqGfYmPtIRUV2PR9a/ZN+L/hi3lvbrTBe2kQy8ti4nUY65UAPj/gOK8nbwysZXcOuP0/lX6D/ALLf/BTP4J/FHWbfw78T7P8A4QrUbpgkNy832jT3duAHmwslv2GXDIP4mFfav7TP7I2neNtHuvH/AILtkg122jM8sUIAS9jAycBflMgXlXH+sH1Fe3gMbCpE+br8RY7BV1RzCNuz6H4Tf2EsTZPTuOlfPP7RKf2fZ6Su3aWMoHvytfelz4bMLZVewr8/P2wbh7DXNB0voTFNJt9PnAz/AOOn8q5c892lZH3GRY329VI/V79gbUZIf2WdMjk/j1DUHHH8PnY/pXa/HL9pP4V/BS0K+NJjeaku2SPRrUg3MwP3RK33beM/3n5P8CseK/Nf9mn4hftM/Fj4eaV+zz+zfpn9nppqyHUtb3bfL8+V5WLXDDZbgBsAIHmbHyV9QfEb4ffBT/gnr8Nv+EvvpY/GPxb1wMNKu7xd8VnLjEt9FA5OFiz8s0paSSUAAqocD8ArZPTnjHzvfoftFPGyhQUIK1j8rv2qP2i/G37RPxJ/4S7x3ZwaR/Z9qmm2unwhwlnawlmEbGT52fcxLM2Mk4woGB/a7/wbQ/8ABOyP9nz4E3f7dnxqtUs/FPxDsM6OLkbW0vwwP3pnbd92TUComPGRbpHz87Cv5uv+CMv/AATJ1j/gpJ+1aNZ+JcE0nwu8Dzxan4ru5M41CeQ+Zb6WrnkyXbKWuCPuW4c5DMmf7fv+Cgv7Q1n4Q0aL9nbwS6QPcRxvrH2cBEgtwAYLJFXAUMoDMo6RhVxgkDh4lzFUY/VqR0ZNg+Z+2kfDn7dP7Xnhm7HiL42eKLhrPwl4ctZGgX+JbSH7u1e81w5G1e7uq1/AL8dPjH4u/aB+K+t/F7xodl/rVx5vkhiVtrdRst7VD/cgiAT3ILdTX6pf8FZf2tD8QvGUX7Nfgq48zSfDUwuNZlRvluNTUfu7Y44KWinLD/ns2D/qhX4sXQbeSeCMZr5PB0re8z2sTW+yiHAQAgYxVaRsyZYZUetTTyFAqH8KrT7lxnvXpQ3OdRV7laQBnUjgDpTuuAh4/wDrVXIKgqMj6U/BTPJB610FDZ02kduKgJyNp6k81Ixdd0jnIpgbep9PyrN36FFaTeFwOentgVVYSI4K9uamlJDEqMVXldtox0OBx6Vm59Cad7kLsGJk2gD2qlLF5Qznacjj09qtBGDnnn1qtPIY1y+T6UObNpLUzp+VCnrnnIxVJw7sI+i+3+elWWODmTLZ9PTtiqokk256AGhyJcrEL5j/AHZzVOdWOF+hH0q68isMjHoBVJjkbj0Bx7VClZGfM72RFuI4xgVXZXAO44x0qWWTBGO3FVmyzNgAY5FYu7EUpnby8YA3HrUEmIYuR+f+eKnn3CRUUdarSt+8EeOhya500axSIclBkLgipAdyb6jlLZwoxj+lIz7U2DoakLEQ5A3dqiO4tvzirGwiPJ/Sq+xh0GanmvsaRY4kIlfqx/wQ05/4K2fs/j/qcrD/ANBevyfb7201+r//AAQ23L/wVu/Z+Cjj/hM7D+T0zaB//9P+BJsgf4Uqk7RnmkG4r7VIg7VMonOKOuDShsDpUfapR1HHNUmzMtQklhxgflV9wT8kbY5wazYmIOOvH8qtQuGYg9RTu9jKSNEK+QOhzipwrDGCTioVPzHHAwKsbdyg4HP8q7KOxMWh0bKmQOdw/wA9qvxsx6k/LVKOPIygrSiglU4UbQBj861RmpxTLcbqE4GSKswsQNzjO7ge1VxE0ZCMNrVYiUKVV/r6fhVPyN/aJl/GG3cAf5FWNqsvkhRjINVpNqx4bIJwQB6cY5FWYVLKQTn9KEMlVWUbTnB6AVdRiBhuv6f5xVY8dO/YU5RGSN3OKXMZTnbQ04o0OAMAjt9KeGDH+lVE3Oxx196fGN77e/8AhW1kzTc1YVdduDgf5+lei+AviT4/+GfiWPxt8NtavNA1a3GEvLGRopSP7rEHDoe6uCp9K80WTamRk9sAVMlwrfKeccHPas5J6JGTpq+x+7PwI/4Lc/FHwtZxaF+0X4Zt/GFn92TUdOMdlfbfWW3YG1m467fJz61+ofwy/bO/4JXftDTRQ6t4itvBup3JC+Tq8cuiShjxjzsPYt7fvCDX8dnmDGG57DPbirMZlj2urdsY7Vvh8RUg/dZ4+YZBg8VpWpo/0Ifh1/wT3+Hfxhsv7c+CPjy31WxyCrxNbanCP+21nJ/7LX0JZf8ABJj4nIgW0vtLuzgdHlgc/VXj/riv85HwX4n8Q+AdUTxB4Nv7nRr0EMtzp80lpMrDoRJCyniv1I+En/BZ/wD4KT/CdrfTfD3xh8Sy28e1Al/dDUVwP+vxJT09+K9vDZniHJQUj84znwtyya5lG3of2B+Kf+CTPxmlQLaWtuxUclZ0x+GQK+ePEP8AwTB+Puhl4xa2cYUZ+e6QZ/IGvyR0H/g4u/4KaafZLbP4r0+9dB9+60q0Yk/8BRK8u8ff8HIf/BVSYSWcXiTQIVONv/EhtX/9CyK9uvRzGEebQ+QwfhzlkqnIpNH6eeJf2EvjXpLE3txpMAGDzcu5/wDHY68tn/Y98YWt0f7W1q1Rl6iCGSQ/+PFK/Ebxt/wXC/4Kc+NnZL74hW9rk8/ZNE0yLnpnm3Y1826v+3j+3h8RblbfVfij4kmJ58uxdLY88fdtYo8CvOw9fG1XbmR9th/DbK6S11P6e9N/Ze0vTrTz9RvrubZ3VUiT88NivPvGHiT9kn4UxNL468T6FZNHjK3upRPJkdR5Kyb/AMNn4V/LPrusfF3x5qMOk+NtW1vVrq4ZVjTVL2dtxc4H/HxIFUE8ZOBX0Npv/BNf9qTUI1+06Jp3h9Gwc315GWwe+y3ErdK7quBqQhevVse1g+F8tg7U6Nz9R/Hv/BTz9j3wSGtPB9xda+wz8mk6e0cfHHMtx5C49xmvirxx/wAFfvH18Xg+FXguz05P4bjVbl7t/Y+VCIUB+rN+VfNHx+/YH+JXwF+GUfxJ1LVrXWoY7lLe+js4JEW0WT5Yptz8uhfEZO1cMy+vH2b+zT+xZ+z/APEv9m/RPjn4d06fVr6NnsNfhu5zKLPUYeSPKTYohkj2Sxkg/K2DnBrgq08NGl7W90fR4fBwg+SlBI+G/GP7YX7WPxtT+x/Eni/UpILg7f7N0ofZIGz/AAmK0Clx/vk/lXFaF+zZ8ZPFBRLHR0sftHCtfzJbF29MMd+T7iv2Uh8AaV4PsfsGh2EOnogxsgiWIY99oFcyqwaPrNtqskH2hLWZJXibo6qQSvr8w44rCOfwirUoJHS8vm/iPwv8PeC/E2t+Nrb4f2lsyazdXv8AZwt52EO253+X5bs+0Kdw28196eHv2LP2xdMtPsXh+2bT4/8AnnBq8UA3fRJAM8V9Ef8ABVr9nO18DfFzw7+1T8OFaPw18TLWK6E8Qx5GtW0aF+nRpohHOOeXWX0r9APhH8RB8bvg9o/xU0aRba+1S3e0vtgB+y6pbjZP8uO7YkUdNjLXqYvN6kaKqU1ocdLAwlPlmfj/AHf7Dv7d12/yyykf7XiFQPpxMePatDSf+Cc/7aupOI7t7MLxn7Rr+7+Rav0j8C69+0U3iOTQPGd3EYryCS2jupBbD7LdpnypNkfJV8fdI6EcVU+F/jn9oVPEt1onjS5I+2W0kMN26QBbS9jGYmVIxl1Yccj0rwJZtO90kdksLG1j4x0//gj9+1Z4mVPtt34cty5H+v1OWTqePuQNXx58f/2e/iJ+yb8W9X+B/wAUFt31bSUgmEloxktZ4bmFJoZYWZVJVlbHIHIIxxX7u/BD4k/tJ6N8QNIi+Kl20unTu1reQTSWsagEbRMFTDZ3lcLjJHrnjnP+C1nwsTxr8JfAH7VmmoG1DQJD4R1wqMf6PIWuNOlbH91vOiJ9GQV72T5zOVdU6iVmebjcvj7Nyj0PBvhr/wAEvfhr8RPhfonxJ1X4g301rrdhBepHp9jDFs85Axj3yPJyhyhO0ciu70v/AIJqfsh6DdIur/21rbrw32q/8pWb/dt0iP614z+xx+1z4G8EfswXGgfEnXINN/4RW9lggjkbdPNbXJM0aQxD55CHLrhVOOMkCvhn9on9uX4u/GrVR8P/AISQ3ej6bqMgtYYrMNJqmoGQhViAi3Mu/tFDljnG4jisMXHFOpKLdoo3wsaXIrLU/Qn4mfGP/gnV+yTLP4Y+Hfw50Xxf4zg+VbOYNeW9q/HN5czNMAV4/cxfvD0Jj618vfs9/ss/tnf8Fa/jm+h/BHwzb3skDLHe3sNsml+HtCtz8wEzxJ5UYUZKxKJLiXGQrHJr9av+CWH/AAa7/Fn4wLpfxh/4KFSXHgDwtIUnh8JWzBdcvU4IF7LyunxtjmMBrnkg+S2DX9UfxP8A20/2OP8AgnD8NYP2YP2TfDOmNf6DGYYdA0gCKw098Ab764XcWmzy4y87nmQrndRhcZU/gYNc0u5yY/6vSj7XENJI+XP2F/8AglJ+x9/wSD8DN8Z/Hup23iP4hrF5V74v1CJVFu0i4a00a0+doFccbl3XEo6sE+QeefHX9t3xN8ZLybwx4USTR/DLEqYi2Lm7T1nYH5UP/PJTj+8W6D4M+Lnx++Kv7QXiz/hNvitqjX93yLeNR5draxn/AJZ28IO2NO2eXb+JmNeT+IPiF4c8BaO/iLxFeLa2iHAbq7HsiL1Zj2Ar9V4V4MVK1bF6yPwfirimtjanscLpE+vv7YDw+TuXgZGeAFA/IDFfDPxl/bUtfDs0/hj4YzLNdplJdR4McRHVYB0dv9vG0ds18g/Fz9qfX/iKsvh/Q/M03RuQYQf3s49ZmHQf9M149c18o6VpviLxZ4ktvDvhezuNS1LUZVgtLS1jMkszt0REUc/yHsOn6nzqlDXY8DA8L04v22KPS/H3jvUdahmu72d5mly8sshyxY9WYnqa+u/2Pv8Agm14x+L89p8UPjatxoXheciW2sv9Xf6jG33WGRm3t24wxHmOD8igEPX6N/saf8E3PB3wb0dfjd+1W9jc6ppiterp9xJEdN0sRjJluZHIjmljxksT5EX+2cGvyf8A+Cn3/BbW48XXd/8ABD9jm9msdH3PFqHild0VzeZG147LOGhh9ZjiV/4Qi8N8XnPEUIvTY0o43F5jV+o5TH3esui9D7Y/bJ/4KAfAb9h3Qv8AhSHwX0+x1TxRp8Zgi0m0Oyw0rPQ3UkZy0uTzECZCc+Y6ng/y6/FP43fGP9pT4gLrvxF1O41vVLuRYbWE/LHH5jALDBEMRxLngKoH5810/wAAf2cfG/xvlg8Ra476ToMzBjdyAma5H/TBG65x/rW49N3SvPfiP4ch+DPx61bwlpzOU8Na55cBkOX8uGUNGSRwTtxyBj2r4KefqvKUYPVI/XuHeAsPltNTlrJ9WbXxM/Z0+Mnw38LJ4r8Y6MYLLIWSSOWOfySSFUTBGYoCTgE8ZwM9qv8A7Px0D4l3dx8OPGlnDclYN9rN5KCZEUgMN4AJ28Ec8jjpX7mfGbTdHvvhj4tt9SVFsJNHvnk3cDaLd2U/gQMe4GK/EL9iPw3ea98c4REDtt9OuZJfoQqD9SBXkZJjqmLvzrY+mzyjDD0nKL6FLXPhM/hvUr3T7FfKubORo2jH3HC/3fTI5GOK/oa/4I5/tP6v8SfBupfs8+NZ3l1LwnAt7o8kpJkOnF9kluc9RbTMhQddkm3gIK/J347aTDpfxWv4YTn93as3sxgXP6Yr2b/gmbqc3hD/AIKCeDvsjbLbXUvbGZOzC4s5uMe0iI31FfomEvGKPyniqhDHZdPnWqV18j7p/aZ+Glp4N+K+tafpyBbSWQXcKKOFS4USYHsrEqK/nO/bN157/wCMup6dZgkaRBFp8S9cy7d7gfR3I/Cv6xf2549O8OeLZfE+qbYrWy0dbmckfwQ+Y5zj1A/wr+R7wTrXhLWfj7pnj74t3GzRbfU217UwBvkmSBvtAtolP3nmcLEo6fNk/KDV8U1n7BWOfwng6kfaT6I/oNXxv4A/YR/Zj0VPE0aBdNs4bW3sIAsUmpaoYwZACOpZyzSSnPlp77RX49/CT4WftJ/8FPf2tbL4feEUGpeK/FU26WZwVstM0+H780hGRFZWkfQdWOFXLuM+ZfEHx/8AHn/goR+0rY2XhrS5bzU9Wl+xaDodu2YrO3J3HLnCrgfvLm4bA6k4UKB/dD/wTS/ZR+DP/BMD9n28uLmeHUfFWrpDN4m1yJfnupUH7uxss4ZbWMnEScGRsyyY+UL+F18fHBQlN/Gz+gaWHdeSXRH3/wDD7wL8Bv8Agk3+xXo3wd+EkUc7adG6WrzKq3GsaxKoNzqV2F7FsMw5EcaxwrwFr+Vr/gof+21qHwP8I3Op2t99r8feLnlNg7kM8JY4n1GVf7sROIgRhpNqj5VfH3B+3l+2rY6BpWpfHf4vT7La1UWmlaVC43SMeYbO3z/E2MyPjAG524GK/i0+NPxa8Z/HH4jan8T/AIhziTUtScYSP/VW8C8RW0IPSKJeB3JyxyzGvh0pVp88z6GVqceWJws9zJPO89w7TSSFi8jnc7uxyzMTyWY8k9z71nyOyYTtjp6VHu2ICenbFRsUYKCePSvTpx8jz1FXuRKP4yeKiLGRG39BzQzFmESgbaieUy8AcLxjp0reCsbtolBV1LEDHT8aqvy28cccVIXATCD0zUL7c7jkZOKVhkfBxv5x0quz/PsGMDrVhmVV3ngdKz5Mt83TJ4ocrIXK2SM8ap3JPQVRLIBvxnjAHvVpiUxt49Mfh/8AqqgQ5JHbOR2rKIKnbYj+0MpGwDDH0qrdkSJhT37VaZxjDAD2ArNkkVmwgwBwaTsbSlZalJ/Mh+cnGRjiqrN5pwOFqxKGdvnHyn+dQfujnHHf9KXKYOHUryIz5zjjBqoz4TLew/Gnzb8gbsnr+FVyXdFzt4oqQ0sNoSSUfMpHP41Ud93GP/rVNtaUjZ2x0OOOKglLlNo6E1jOVlYBqMyg7yOO3YYqo7iT96RwR9Kb8yemDUbygrt//VXM2irDH+Ziy1G/zY9KeGxggdKZlieaU5IuI5pCq7WqvuyMninSDcQV7UybHFZxSWxajYb/ABZr9Xf+CHRI/wCCtn7P5/6nOwx+T1+UnU4r9Wv+CHjbf+Ct/wCz6V/6HTT/AP2ajm1saRXQ/9T+BKFuuakJCnmoF4pzpgZoOdpEmdr59KcCd+ajIPDHoanUDqadyJaE6YRhnirMaRLPyNufSqijnce1WioZAelCRk2aiKDjPQ8CrCKsjAjkAYFQRI3KEcVr2luXKrjn0rppuxwzklqWLe3/AOWZ9R09P6VqiCRdrg5GcH6Vq2OnsxDMBzxiurs9FLtjGCOtdEYnn1cXynJJatLxxkY7Z/lUy2YB/ecjPQDHH4V6Yvhf5AUXpVKfSBnHTbxgf59K39hZHLDMUcH9lj+VgcdBjpwe1QPF5LdeOldNNYNHkuCMHA4xWRdRBPkPft/KsWmj18LiubQoZVH3p0BwB+FSRSKAQ3rUaKkZ2joe/T04qXaGYrECCPm59KTsem4dSdJccqAe1W12OqtyCOazVd8biAoPbpVu3YCIY78fTtWkTNXvY0441jUeVx3PvUsaxgZxjOOpqlGrxxhHOfTPp+FSo/JJ59sVY/IsPHHHIViPHfpUkbPHhs8Y/OoAVUKBzxVsYdeO1UBrxzvs4HSrBncSIM/MPbjP+FY8Muw5Y96uKy3cQ7YpRqOElNdDnrq6s9j6ftrN7bSdN8QxEyadqgbyJj2miwJoG9HjJHHdGVhwayNfgtdWhEb8P2/CnfA34keHfD1zP4D+JMJu/CmvFEulDBZbadD+6u7Z2yEmTpuPysp2v8vTrfix8K/FHwouLfVppBq3hu/Ypp+tW6kQysvWKdf+WFwnR4mPUfKWXmv2PLM1p4iglI+AzDKnCrzwPmfVtNaxuPKdc+vuOxFer/BX4o+K/gt48svH3gxk+1WYw8MozDcREYkgmHdJB6cqeVwQKpKlpq9l5NyvI+42ORXMajo93pWG4ePj5gP846V4ea5DUpv2lHY9bL8cpJQnuj+gef4d/A79vb4KHx54KAsb+2PkXMbbTc6VdEZMMw43wN/A33XXphgQvwZ4U+P/AO17+x94yT4RXEKeIrK2YR2+i6nG1xbyxE4U2MylJowxOAiNgHjy6+Kfgx+0T8Rf2aviHB8SfhvcKswAhurKYk2t/a5y1vcqOqHqrD5o2wy81/QZYWfwC/4KNfAv/hMPBcrWV7YkCaFsNf6HfMudj4wXgbHyOuFkXkbWHy/JUsV7J+zq6x/I9mtRuuekcZ8Nf+ClP7HfxU07VPhb+1D4U1jwb9vgk07VIFQ6lZ+VKCjofLWO7hK9RmBihAOcjNfIX7E/7Rnw2/Yp/ao1z4ear4gt/FPwl8STjS77VIFYxm3yTYaoIiqMslvv23CbVIVpB/Ctfevwf+IHwn8eaxF+yP8A8FOfCem3msWIS20Xxfep5ctxGfkgjuNQjMc0fGBHciQKxGyYK/Lcf+2N/wAEXtO8K+FdS8cfsp6hqN5c6ehmfwxqZSaaaEDcfsF0gQyPtBKxOpMg+65OFPqYN4bWhNWUjlVebSnHdH6HfF79lC4SX+0PAfkalp0xWW3CSrvaNwGRoZP9XNGRjYVbkV8deKfgD480xpI9Q0C+hMY3FhA0ibe3KZ496/C39l7W/wBsrX/Fknw0/Zk8canouqQ27z22jnV2tIJ0gGXjgguT9mLxjLNEQDtBIBwRX3Yv7T//AAWq+Dm1PEWkXWtR23zGSXSLO/yBxgyaftYrxXj4jhqdKVoy0PTjndNrVH6zfDn4TWv7YX7KHjH9g7xQPK8QWkB1vwhNdIYzFeQsXjUF+Qqyt5b/APTKd8fdr8bf+CbPxJ1DwP8AGfUf2a/Hcb2MfiuV7aOC4G02uvWIZUjYHGGmCtAf9tYxX0p4X/4Lf/ts+A3tn+Ivw20qaW2IkJmsdTsHUjgjLSOBuHBxjg1+Wn7U37SNt+0L+0Nqn7SXhPQYvBOqazPBqNxbWNyZUj1WLaXvIWZIyhldRKykHEm45wePeynKasqM6M9uh5mKx1NTU4H7WftIfB/wjB4ltfHOvXlxpEmp4iZre388farccPkEYJUcAcceteNfFbw58O9U1aw+OL6zcwPqwH/HtAs0ovrIKJJGHmBUY43hRxzx7W73/gsr8C9R8JWc3xH+Hl9qWvSQRvqEBWzbT5btF2vJHJKSyq7ZYZj+UHaBxmvgf9oP/gpz8SPilojeHvh/4e0j4f6M2CptEW5vQeMETOiRxsfWKFT714dHIcRzWkrI7KmLg9UfTv7QfiT4OeEdQj+MPibxIlifEMKTmxC+ZemVAqtsiDEhjjrsCjld3p8t/tMf8FU/iN8ZPhBqPwH8NaVaaX4X1WO2j1G4uwJrq4+zPHJE6D/V2xDopyNzf7XWo/2U/wDgjp+37+3NqkHjvw34bk8PeHNRYM/izxc8lnBKnHzwRurXV1kA4MMWw9Nwr+sn9lD/AIImf8Exf+Cbnhi3/aC/a+1qx8d65pRWQ614tWK30W1mGMCy0ksySSZxs843EpYDYqmuyn7LDtKPvSQcjkrt2R/MV/wTm/4Io/tzf8FHZrHxV4C0EeEPAMrASeMfEMckFo0fGfsFuQJ71sAhTEBDu4aVK/t//Zp/4J0f8EvP+CGnw3h+Lni++t77xvLE0T+LNdRJ9Yu3KgPBpVpGCbdGzjy7ZC2MCWRgM18T/tOf8HEsMcU/w/8A2HtF3gDyV8U61AYo1UDANjprYJAx8j3GxR/zwIr8FvGfxS+I3xk8aT/EX4ua7feI9evB+9vdQlMspXsiD7sUY6LFGqoo+6or6DBcOZhmUlLEe5A+ezTiHD4OPLRV5H68/tkf8Fm/jN8eZbrwR8CY5/APg+UmOScSf8Ti9jPHzyoSLVGHVISX7GXHy1+YXhfXI8COLjuMZ+p+uT3r5x8WeMPDXg62+3azdCHd92JeZH9gvXp3OAK+RfHfx48TeKEfStLY6bpx+UxxN+8kXp+8fjj/AGVx75r9OyvJ6GCiqdGJ+Z4unisxnepsfpz46/ab8M+Do5NN0gJqmppkFA37mFhx87L94j+6v0JFfC/jT4i+J/iBqo1XxDdNcT4xH2RF/uxoPlUf5NfOmi3V9qV9BplgjyyzOsUMUSl3kZjgIiLlmY9gBX7z/sc/8EofE/jBrLxt+035ujaY2149BhYLf3C9hdSDi1QnrGuZiP8Anma+jp41RRwYyOEyyN57nwv+y5+zF8af2qfGH/CL/C+wH2a3dUvtUucpYWSnBzLIB8z45WJAZG7ADkf0MWfwz/Y2/wCCTHwcuPiz8SdZT+0pUME2s3MaNqWoS4BNrp9qG3Ih4/dRnC9Z5MDI+dP2rP8Agql+zH/wTt8LH4JfAXS9P1zxVpiGC30PTz5em6Zkcm8niOS+eXiQmd+fMeMnn+RX9pj9pv41/tZ/EG4+Kfxv1uXWdUnXZDvIS3tYQcrDbQLhIIVzwiKO5OSSa+UzTPJz92LPDwXD+NzufNiP3dHt1Z9p/tv/APBUr9oD9vjxcPhl4UgudE8Ey3ATTvDdkxllvHQ/JLesuDPL3C4EMX8K5BY1/gt+wvY+HZ7fxd8aI49Q1XhotLGHtrc8f64jImdePlH7sf7Xb44+E37Rtx8EbD7H8F/B9pca7dxiO61W/wDNvbuT1SKKERLFD0wgJzgby3GP0E+En7Bv/Bbb9viK31Hwh4X1rR/Dt/t232omPw3p5jbow3iO4mTHeOOSvyPOcfVqPkcrI/fuH8kwuCpKlhoWSPt/w1rPwI+Gt0Ne/aA8Y6b4X02Ab/Knk33k2zHyQ2kO+ds9tseO2cV+Gv7ZfxL+G3xl/ai8c/FP4Q/aB4a1zUftGmtdQC2mMYhiQloct5eWUkDOcY9xX9DHwa/4NdfAngrUINR/br+PumaBfTFTLpXh+NHuXPHH2q+PmE+4sz+lfj5/wWV/ZF+C/wCw7+2rqXwA/Z+kvZPCkPh/Rr+1m1Cf7TcSPd2xeWR5CqfekUkKEVVHAAHFc/Cs6CruMXd2PZzOnNwTa0PDfjP+2H8bPjT4ci8O6lHDomgXsao1tZROq3gh258yeQs0ihsFkQhM4yK+8v8Agmf8Db8eCNd+L9/Ht/tSZdOtCwxmGD5pnH+yXKrn1Q+lfAfg22+L/wC3p8fvDHw30C333ktraaPp9uuTBY2NpEPNmbsEGJJ5iB1Jx/CK/py/aY8JeDv2Nf2WLP4c+DpfKmNv/YukAgLJLgf6Xdtt6HazO3bzJFA9v1PJcJShC0VY/FvEDiH2bhg4v3pfkfg58VNch8T/ABE1vXoOYZ7tvJP/AEyj/dx/+OqK+k/+Cb3h+bXf24/At2Fyulfbr+Vj/DHBaShT+Lso/EV8iXUex2aMegx7V+v/APwS2+HkHgrQvFn7THiuRLG3khbS7O4m+VI7S3/f31wScYQMiLnoNj17WGjrY8LPcX7LASjHdqy+ehk/8Fs/jJZ+HNJk8CafKRqPiIQWOBwUtLULJcHj+9IyRj1G4dq/mb8PeFPEPj3xNZeEPB1lLqeralOttZ2sI3SSyORhV9B/eY4CgEnABI+h/wBs/wDaWvv2ov2itd+JsHmnTGkFno8Bzu+yRMRF8o/jmYtIw/vOQOK/dj9hX9kjwj+zL4Ut/GetQC+8cavbr9tunUE2ayAE2Vt/cRekrjmRhj7gC18dxfxNGjT0+R+keHnCksNg4U5b9T2P9gf9kXwR+xJ4TfWNaaC+8ZapEv8Aa+pqoIjUfN9itOAfJU4z3mcbm4CqPpT4+ftRaD4T8JX3xF+Jl/8A2X4c0SLcqn5my3yoETOZbmU/KqDknjhQTXmXxj+KPhD4VeDb/wCJXxO1GPTtI05Q0kjc4LfcjijHMsrnhEXLMfQAkfysftbftb+Nf2rPGKapqCNpnhvS3b+ydJ3hhEDwbicg4e5kH3iPlRfkTjJb8GlOeJqc8z9cShSjyoZ+1j+1V40/ao+JT+L/ABGjWOl2e6HSNMD70s7dsZJIwGnlwDM49lXCKor5Rkkj35YZ9KQOxIK/pUShi3P0rvhFRVonO3zallg21R1+Wq0i7TiPHuf6UxpG+6mKYSEXHGfT0renGxNOGmorsSNq8VER5MfqCeBTy3y4PQVXKfPzRY0GlsRF+2KjJOwNzg4pZE3uQpGF4IpjNgAKRx+lJT7DS0I2Ctw3NQKIcA4+7+XFDeZ82Tn0/wAioA+0lscEVm0VGTQMVVmROOOapSB85H3RnipG3Bi5wR2x6dqz55ihAYgDqMfyo9BoS5kK85rJlfDZz8rVZuJEPzSHPYVULhnx1A4otpYKjuE2VcK3pVJ/K37RxQXyxxzj1qJIw+1zjAobtoShrFGbEXbH0xVZ90cZ29N36VMSHA7bfSoGc5I6D24pOQit8oO8dOB+VQyklwE4x6VNv2p7ccVGo2D5sZPNc1SV9CbEflBhtJ468CqM0IzxjFXhtiQk/wCfpVWSXdnHbisZKw0ViUAx2NIeOlNb5lG3jFRNuztasXG5sokhA6gVFMf4alxtXjiomUU+UtAemBX6s/8ABDcq3/BW/wDZ99vGen/+z1+Ux6Zr9V/+CGp2/wDBWz9n9+w8ZWJ/R6LG1j//1f4DicDcKfz1PpTGHyEflUsZ3J+lBh0HxBWG04yKcDuFQrw+KlR1BIpNESRIqgDir0DlW2dc9PSqJG0+WKtwLtYMO3FWkZPub+ngF8tyO+a7XTLcs6vswG/rXK6fGHcRt3xj8q9Z8OWol2Sfw8Cu+nHoj5/HVuVHVaBoXmso29fbgV7Lo3hIMgaRecfNUvgzSlbYGHbg1+l/ww+Gnwc0f4Jaj418RTpq/jHU99npejpuMenW6ECXUbojjfjKwx5I/jI4Ar3cJg29bH5/mmccrsZXh39keDUP+Cfni39op1je60zxjpWmQeotjaymfn033EH/AHzX526l4UKOUiXO0nJ9x9K/sV+E/wCy34g1f/glk/w0trMR3Ou6LceIZIuNz3kt2LqBR0/5d4Yhx+VfgzefCr4c+JPhzc2c8sOg+KtHjku7ZpiRBqtqzDNvnH7u5h5KZwJE+X7wXPdHBXWiMMXnNGnyKMuh+RusaM0ZbzB/n2ry6+gaOQtx1x7fSvrXxvoogkMQTaa+bNYt4opSz9Dx/hxXl4ihyn0+TZjzI4N0RFwR06/WsqQFHBIABrcvXCgJtPy1gq2cqfug/lXmJH3OFqtx1Jw0ZHTG4g9Pwq7CpUhexrPUZUI3HpjtVld2MKcDNLmNJT1saTeZtAHI9O2KepKNuHPGDiqEcmOW5NX45ed7fL7DitkiiyGUquelPKkZ2nj0qp5sK53g/N046VOXKcH+KhIRcDhj8vWpIyIsFRjGKqLmEndyKn2sygr609OpMo3VjS85VQkjcCNpBr7I/Z9/aL1zwfbTeCdegi1vR7qMRXWl3gDwXduvAUq+U8yMcLlc4xgjaCPitZD06Vct72SKUTQuY3Qgqw6qw6EV6uR5l9WqWqfCedicLzLQ/Vi//Zb+HXxc0Sbxz+yxqyRlF3XXh3U32vbMf4Y5WLOq9l83dGe0/wDDXxr448L+MvhxqJ0Tx5plxpV3j/V3KFVbtlHA2uvuhI96k+G/xF1E6hHq2iXkmma9ZcrLA2x2/wBuMg45/iTp+Fffeg/tnwapog8H/HzQLfX9PbAkuEijcn3ktZB5TH1KbDntX7Jh5VFS9rh/ej2PnJ4aPNZ6H5I6raafelnt8xSHkkfdNej/AAH+NvxF/Zn+I9r8TvhPqP2bUYV8u5gkBNte25OWt7lMjfE3GOjKcMpBAr9Prb9mz9g349/vvh7rn/COX0v3ba1uvIYN/wBel8G9v9WQvpV+6/4I5ane/vfC/j5UiYZUXunHB4/vwzEfiF+lfE5nQw9SX7yFj1KHPBe4z7Tsv2of2Fv20fg3HF8VNZsfAuuoGDWmoSbJ7OdsBjb3DL5dxavx8pwSOGVWUNXB/BH/AIKOy/sZ6nbfCzxf4l0/4jfD63kEdo1heLLd2EQOfMsHJ37B1+yzHaP+WbrgV8qf8OWv2jWTbpvi3wxcAY273u4jjtwbcj9apS/8EVf2m3jKXHizwpAV6nzruQ8ewtxXn4XB4WMeWUjKvhqk5qotDlP+CinxN/Y81v42aZ+0z+w74xni8R3V2t7qVnFYXNk1vfx4ePUbd5Y1iDuf+PiIMVL/ADDIdhXv+sf8Fqvh7d+AdNln+Fct54wNqq6rM+oR22mG6Xh5LeNIpZPLf72w7SuducAGua8N/wDBDD4jam6x+JviZpNsONws9NuJzj2MkkIr6b8Hf8EI/gZpii+8f+M/EetiPBdLWG20yIjHTcVuHx06MMV1VJ4eyja9i/qje5+c/i3/AIK7ftN+J4HsPCFvo/hG1b5QtpA1zLj3kvZJV/FYlr5u0Dwl+1J+2R4wFz4U0bXviDrBURGe3t3lRFH8LSqogiUZ7lQK/ot8MfAP/gkb+yXeJe+K7DwpFf23Ktrt8dZuwV7/AGZ5Jfm/3bcdOK9H8Z/8Frv2YPh5pQ8O/BvQdR8SpbDbDFbW66Ppy46YMuHC+y23SuvDVsR8OFpBLCUo/Ez8u/gz/wAECv2k/HNxBqv7QniHTfh7YNtZ7S1I1XVCvoQjLbRemTM2P7tfvf8AAb9kH/gk9/wTE0Kz+IPj610v+3rcB4dc8XSJqeqSMv8AFaWQXYjdMG2ttw6bu9fgV+0D/wAFhP2vfiokmmeCbu08Baa3Aj0VPNusehvbgMwPvEkftX5vf8JJr2u6rN4m8U3lxqeo3J3S3V3K89w5/wBqWQljXfR4QxmJnfEysZTzGnTX7tH9WH7WH/BwNc3Kz6J+yL4cYu/yDxF4iUrgH+K305W9vlM0gHrF2r+e74mfG/4xfH/xofH/AMcPEt/4o1YH5Jr2TckKHqkEShYoEHZI0Ue1fPr+JLKFN9y/QYBJ/AcVy138RvKHl6Wu1h/G/wDRa+yy7hfDYNJxieNiMTiK+j2PqiHxFpujIl/qFwkER4+Y9foP6Cs7XfjteyWwtvC6eUP+fhwNxH+ynRfqa+OLrXLrU5vtt7I0jgAb2PT+g49K+pfgJ+zJ8a/jvJFceDtOMGmOwV9Uvibe0Uf7LEbpTjtErfhX00OW+h4mKwlCivaVmea61rV7rHm315I0zn70jncfxPpX09+zL+wv8eP2lriHWNJtRoHhpnAfW9QRkhI9LWLiS5PHGwbM8F1r9Z/gz+w3+zP+ztof/CyfjTe2uu3OnASyX+tbINMtmHTyrVm2sf7vnF2J+6gr5j/ar/4LNWGiNceEv2TrBb25VfL/ALf1CMrBH2za2jY3gcbWlCoP+eRGDXmY3Fxj7zZ87WznE4l+wy6Hz6H6D+DPhp+xd/wTG8Cj4n+OtUit9TZGjGs6iEl1S8YDDRWFtHzGG6FYRx/y1kA5r8ef2w/+C1/xi+PFpc/Dv4FLN4F8JSBopZI5P+Jpexng+dMpxArDGY4eT0Z3Ffl5cab+0b+2J4/uPGniK8vPEN7O2y51bUZGEEIHRA5G0BR92KJeBwABX6FfAf8AZP8Ah18Kpoda1cL4g1uMhlubhAIITj/ljD0BHZmy3ptr89znjSnR92J9HkHhpBy+s4x88/PZeh+ZXjv4bfEHwjpWi+JPF2lT6dZeII5JtPknG0zJEVDNt+8OWUjcASCCOK/Qz9in4C/D34reB49bj0WPUNVt7qS1unu8zorptdSsZwiqY2XseRX15+298NI/iV+xhdeN7GJn1LwNq1tqbyY+b7Dff6JP+AkaBuP7pr57/wCCUPxS0rQ9d8cfC7WG2HUrO21iy/vGW0kMM6D6xTKf+AV8ricxlicG60dGff08JTp1VTex+v3wO8H+Cf2fL2LxXo+i6dqWrW+Gt3uocW9u69CkCbUYqem7I9q9m+Kf7Y/7TPxCWSz1zxrqCWrD/j005xZQgHsVtgmR9Sa8Om1JdRfy7CDeF9T0HvjgYrwT4m/tJfA34W20n/CY+J7C2mQf8elmftV0x9PKg3sP+BbR7ivzmpRrVnofSfuqaO2l8Q23hiS48c+JLsWNtp6NdXd9cE/uIY+XkdjyRj8T0HJAr8Ov+ChP7Uo/b3/aim+LPhHTLiG0+waboGlo6k3N3DYReTHO8YztkuGZmEXJQELkkVx37V37Yvib9o+5h+HngWyuNN8MJOpFsTm61GcEeW1wqZAVT/q4F3YPzMSduP6X/wDgjX/wSZ0v4AadZ/tbftXQRQeKoYjd6TpV3tWPRotuTd3ZfCrdBeUVuLZfmb97gR/pfB2SvD/vJrU/NvELjnC5bhueT16Lueh/8Ev/ANgfw9+wB8DNR+NXx3MWneMdXsftGs3M+CNG05MOLMHrvOFafHLSbIlzty35V/tg/tJal+038WLzxjFG1ppFsPsmk2jHmG0U5UsBx5kpzJJ7nHRRX1d/wU0/blm+P3iB/hN8LJ2h8DabNvadQUbVLhD8srKeRbx/8sUPLH943JUL+W/hjRNX12/h0nToJLie5lWGGGNSzySOcKiqM5JPAFfoOCdnZH85ZRQr16ss1x79+Wy/lXY674P/AAU8R/HD4g6d8PvDQ2z3zZlmK/Lb2ycyzt2xGvQdzgDkivdP+Csv7Unhr4G/DSx/YJ+B7m38q0hj1t4m+aCzXDxWZI/5aznE0/ttX+NgPrrxz448If8ABLD9mttcvPs998WvGUXl2dqdkv2cJxlsf8u1q3LnpPPhRlEJH8zngP4V/Ej9rT42Po63E1ze6rPJf6xqk3zmGJ2zPcyE9WYthF43OQB7VnOZKhRbR+j8I5NLMMTHEVV7kdvXufSX/BNj9nub4ofFBPjB4nhH9heGJ1NsrD5bjUQAUxnqtuMOe2/YPWv6EPi78c/hh+z14Bk+IHxIvvIth+7t4I8PdXk+MiG3jyCzHueFQcsQK/Pv4rftHfA39hbwFYfCzwnbrqOr6farHYaJE4DKp5E19Kv+qVyd7ZHmSE/KuPmH4c/Fv46fET48eLZPHXxOvze37p5cSgbILWHORDbxg4jjU/Ut1YscmvwfM8TPFVeaWx/Q+GUaMLI9H/av/av+IX7VXjBNd8VH7DpOnsRpejwuWgs1IwWJ482dwMPKQP7qBUAWvk4Yd8Dg4q2HXJQj8arFo1feR+FZqk4K0UYyqN7kqhVRmf0FQMxkwIuKiYSyfeOelBfbyBz0pRT3LgmLJIIiFjXJI7dPxqP5FAmbqR6YpzOEG9uo9Kqlstl/uiteXQ1H9Ru3celVH8p/u5+lWS4l+aLp6VSaSOIfMfbrSewInZfJjCjqef0qmxZjtCZXvgU8TBgE6tj0xUEjlWAUnjjJ/wA/SsLGjJCcrtHTqcdKz7iTCER4546091ZV3cc8e1UndSMYxgDGPbvQipbIZNK4cIoGe9Z08hA+ZcYPft9KtNMp+6evGc4/Ks+V855yM9OO30qlboTyiSOjZGBwAtUXlIUKew61MTx9cYqqy7hgdvShRJZH959q/jTJW/55Aj+VOwwYu+DnpUE7FiFJArMkhZyqqo6tVaQ/cROvHT0FTb4phnHTiqy7ckoMY49qHZbgMcyNgr+NMwGbZzwKd8qReYe/b2NRu6hv5VyysIinZw4UdCKrZxT2kYtk1DJyQRWUmmXGPQYCc4poO5s+lSSbVANIhTtSNSJ2O0Cm59aHk5xjpQORk0ikgP3a/VX/AIIbgf8AD2v4A8dPF9l+gevyocdx0r9W/wDghudn/BW74Bf9jhZf+gyUGqkf/9b+A5z8tNjdk+XFGQWHSkYfMBSRj5FlOeTQ2KUfd+WmpyMHmk5WILGckEcVpxADbnnpWYuxvrV2BuPm6j+VXA55rQ67SgSwwoxnA/wr2/whHBI6o+Rn8s/hXg+lzusmP4RXsfhi7aEoMgDsa9PDTs0fM5rDQ/T/APZl0r9nO5v4G+M19qtttPS0iTyMcYyw3Sfktf0Kfs0+G/8AgnNPJDF4an0q7u967I9WnuN7njgxSqqkfQe1fyk+DdUMMKzK2MYr7e8CfEf4c6p8M5NC1S3j0rxToMpuLK/iBI1O0ldRLZ3AzgTQ/wCsglABZN0bdEI+wy7GxifhPFfDFTGX5Kjj6H99ngjUwPAd/cWtlA1nbNaxh1PzpyfLSHAwFxjaAMD6V+S/7Wehf8E7dOvL2++LB0i01qUs0kdozfaEc/MQy2jt8+T3Arsf2Gv2lIp/+Cd2q/EnxHqOb3wbbXsU0jH7zafEzWoJ/vESwgfSv5kdf+J/gGw8Dal4p8YL/wAJD4k1Rp7ezsZGZYLMty+oXTAqZZMkrBDnbkGSTgKp9eeLgrtHwdHgDGc1N1qrVl0MH9qa9/YlkW5T4Pf8JA90MiMjYLXPVd3njzMf0r8jtfK+Y6nHHP8ASvXfFWtbYjubcMd68G1zUSzZfHGMfSvk8bW5tT9+4Zy10IKF7+py14+5FbgDArn92VBXnbjP+FadxMcZl7+nQViyOIpvMxyf614UWfpuB00LfmDomcdT/wDWqTdnEiY96qxcnYuTUpDQ96aSOuqktSyJCp+X8ulW4p23bMZz/KqDcMRJyOoxVkM6D6jHFXGRVJqRqhBwVqbKn5TWVFN2JPHBqZWZQOeK3sFjVQtjY54qQHbyvK1VV1YbQPwqRGxwelZDJ+WGei08AEYOKiDYbBPBpzttAI5B9KYmjRtbi4S4W5tXZJYsMjL1UjoRXufhzx9p+tQppPiYi3uTgJOvEUn+9j7rfpXgMLkNkcDGMVYjkBBC8e3avfyPiLEYGXu6x7Hn4vAwmj6su/CsgG4IJo+ucZHsfp+ld74O+JPxS+HoLeCPEmqaSAMBbS7mhX/vhW2/pXyr4W+IOteFtsFufOtVx+4l+7/wE9V/CvoPSviP4F8Tp5GqlbC4bos3C/hKBj88V+4ZLn+W46K57X7HzWJo1qT8j6KsP24v2udBgENr471EgDgXCW1wfzliY/rTrz/goX+2e0Qhi8bSoF6YsLD+fkV4lP4Qt763FxpdwGUjg8Oh+hWso+A9faYGFEnyP4SM/kcYr1XkuDlJOMEYLHSXU9fu/wBuv9snUU8qf4jazGG7WvkWv6wxIR+deM+Mvih8UviBEf8AhO/Eusayp5xfX9xMvP8Ass+39BUkvgLxTGvOnT4x0VN38qrw+CvEjEBtNufp5D//ABNdsMlowekAeYabnlY05bV/MiQR5/ugD8Ksi4JH7w4K8Yr1xPhr41udqwaNenPT9ywH64rU074DfE7VJMQaLJGO5nkjjA+oLZ/Stp0FT0SOd5nSW7PG1uWJII47D1qu9zcR5SMgZ/u+npX2n4R/Y28b6qVfXNRsNNQ9Qm64cA+w2L+tfRGl/sa/B7w3arqnju/n1NV5YzyraW34iPB/N8VFWyjc86rxDQi7JXPyq0+3udbu1sbKJ7i6kO1IoUMkhPYKqgmvrX4e/sK/HTx6YdQ120j8MWLkHz9S/wBeR/sWyZfP+/sHvX2LB+01+yZ+zrCdM8ISWbTAbfs2hwrNIf8AfnHy9/4pPwr5X+Lv/BSv4oeJY5dN+FlhB4ctzkC4kIubvHTuPKQ/8BOPWvOr5lTjDU4p4/G158tCHKj7W8F/sn/szfs+6anjL4l3ttqc1vydQ1t4ktlYf88rXd5ZPoG8xs9K4j4wf8FWfB3gyFtH+A+n/wBt3SrsTUL1Wt7KP08qEbZHA7f6sexFfl58OvgP+1X+2D4jbWdB03UvEjM22XVb92S0h9muJf3YwP4I8t6Cv0F0f/gjtqcWlpJ4+8VTSX+MyR6VEnkR+3mTZZ8eu1fpXw+Z8a0qXurQ7KHBvtX7TEy5vyPzR+Lv7R/xd+PusjWfijrdxqzx58iFjstoAcfLDAmI0HuFye+TX1l+yn+z78B/FnhqH4ifFDxJp17JvKNpl1cpZw27jOBP5rRvKeA3GI+cfN0H1x4e/wCCRXw9/tCO0vfEOuPyAf8Aj3Q+mf8AVY4r8zv2jf2YfiJ+yl8TYPB/xd0hrixdvtNlcRMUt9SslYZMM4BKN0V1+/E3UYxn5epnMMfHkpysz6jD4L6tblhofrrrPxG/Zh8G6VDp11438OWUFum2KC0uY5VQD+FYrbfgegArwTWP24/2R/CO54dVv9aZD832CwkCn6PcmAD8K+8f2U/2If8Agnn+0N8JrL4pfC/wz/bFs/7m6i1C9uZZ7K5Ay9vcxLKEV1/hO3ZIuGX5Tx9e+G/+CefwN0W9hh8F/DzQ4Zf+WZSwhkY/i6sf1r4LEfV4T5ZJtn1VOpVcLxWh+G2o/wDBSZ/iF4E8QfCP4OfDi91q38U6dcaTN9pked/LuF2hkt7SNv3iE7k/eEBgPSvzG8B+KfiD8L/Hltq3gu8bQ9ftnksBNOigwNN+4lSVJEYLjJDAr8uOmRX9e/xU+PP7J37FzPD8YfGlpY6rb/c8M+HY1vNTJX7qNBAypb+mbiSED3xX8sH7WPxf8HftJ/tGeJ/jF8OPDD+F7HxJcrMumecLqQzlFWWdnREXzbhwZXRF2q7EAnrX2fDCVROm6dos8DM3yWnKR2Hx90P4qeC75/D/AO0h8U5tW1r7raDp00t06H/pupMNvAD6Mu7HRMV4R8MfhL49+MHi60+H/wAL9HuNY1S9O2G1tk3ORnqxXARVH3nOFA5OBX2b8A/+CZ/xe+Keo23iX4p+Z4U0a4IkZZF36hcZx0ib/V7v70mCOu1q/oR+FXiD9mD9hf4ff8If8MtGjfV3A81IiHvLhx0N5dfwgf3Og/hQV9ZgMvp0k42PyvirxEpYdezw3vz8jzb9g/8A4Jn/AAl/YjsU/aJ/aSvLLUPFlgn2gSSlWsdI9od3+uuOmJccHiIZAc8V+2Z/wUT8S/HwP8Nfh40ul+DY2xIpJSfUShyrT8/LEDysXc8vk4A8U/aI+NnxF+Ol4t14oudtpbszW1jBkW8OfQfxN23tk/QYr5s8E/DDxh8RdbXTfDFsZAGCyTNkQxe7tj8lUFj2FdFS0H5H4/Sw08bX+vZhLml0XRehzs2i6h4h1C3stKhlu7q8cRwwRLvkkduFVFGSSegr7n07xP8ACb/gmp4Dg+LfxdSHWviZqcL/ANiaHE4PkD7jEsp+RO0txjnBjgz8zjwP4iftZfBX9hyxuvDPwvFt41+Jxja3uLyTBstNLDBUlGILDvBGxJPErjHl1+EfxJ+JPjn4reMr74hfEjVZtX1jUHDXFzcHLtgYVVAwqooACIoCqoAAAFeNmPEEaLSgfqHD/CFbG2dVWh+f/APf/GHjX42ftofG7UvHHjG/jutTvf317fXbi30/TLKPAUu5+S3toV+WNOrHCqGc4PtPij9qvwR8AvhtL8Dv2Oy/mXB36v4zuIvLur+dRjdZQvzDEqkiFpBlVOVRWJc/AUnifWLnQI/DslwwsIXEgtkASEzdpXVceZJg4DvkheBgcVyk85z8xzmvhc3zeeI917H7nleWww8FGCsRXD3F7cy32pSvPcXDmSWaZi8kjt953dslmbuTUQYZ8sfnRgnBfv8AlTBgkrH2rxUurPR5NR8myMBRgGqjqQMnp7CpCQgy1M3ehFVzsrlHFiAdopnAG48Dp+NMIwfl6mmbSsfz8c96kZG2V+V+R79qiZmZhHtG3v2z2p8srEKg7VD5ojAQ4yfWtYwuNLQYwEa5jOKr7lUGRxnPTPGKWR2xnHB9Kqt867hzj8K5pyKQ5THGx3jPpj9OlQPIcEtkg9MU5uFx2IwKrvI20spwOM8/hUiK8pJGwnPb8BVMtgcklc4H+TT5Sjn5OSB0Hp6VRnuPlUY6ce+TVqJqmP3qAFk4KkYxx0qjJn+Lkg/pSySZw3vjiq7yeWSGxk8YoIbFdnAzxVf5nO4df6U6U7QDzVcyFuvQcYpOWhDYTEKB1qlLvz8meOtIzOEYkA5GOO1NZj949/T0qNiZPsI+VUfQGmMGVvm69TSGUqg3cjtim52EsR16Z4/KuerfYFfqNkI6EVSZxuJ9f0qw+5VBc4HTjrUEigDJFc8mykMZ9gqrjd8+MVKzZ+T0pS7LFtxWc3bRGy02Iyc/e7Uzco7U9QMbhUROw49aUXqaLyDOScdqOAM0AbeDSegPSrGmRn26V+rv/BDYn/h7Z8Acf9DjZfyevyjfnla/Vv8A4Iajd/wVu+ACevjGx/k9JFI//9f+AeMAGpSGJAxSOuPmHapOgHtSdiHYVH52nmlX5TtpqjD4Ap5XJwOKiSM7aEynbyKmRzkMp4FVwRilQHOEp0dzNxOos58Hj8a9A0i9bcpGMDH0/wA8V5np4nuZlt4Qd7YVQOTn0r7S0n9hr9rmRIp1+H/iDY6hlP8AZ8/QgYx8nT0r0cOpS+E+czjEUKP8aSXroYWleIEhg+Y46f8A6q9L0XxPFuUk9f8AIqe3/Yn/AGuIgA3gPXscf8w+f/4iu10v9jL9rS2i8yTwFr2OP+XCYf8AslerS9pH7J8Li8bgWv4sfvR9/fDj9rZfCn7DPxB+C8dyiXGva/pW2MPtYwMhec46Hm1jDfUCvzw8SeNfPyobOQcfjWnN+yF+1rDKJF8B66AP+nGfp6fdph/Y/wD2r7kbf+EE14f9uE//AMRXf7ao9EjieJwOjdVaeaPnnxDqvmK5dupry2+uwxMpPU8AV9aax+xB+1u0ZmHgTXv/AAAm6f8AfNcQ37Fn7Whyi+ANfcjsLCf/AOIryq1Go+h9Hl+a4FbVI/ej5iuLoudvHPTFUkKbiFz7Yputadqnh3V59E1eF7a7tnMc0Ui7HR14ZCD0IIxiqtu+Bluc9Ae1ciR9zhlFpSWxpW7NGfmPX8OKuqRj64rNUO5PljGzg/SpA5ckdMHgHoa0SR12ujTBIYDP04q0jYHQelZ7SeYvzcY6GpUd26Dpwc0uVEtJbGkzY4HFSwyptCOOaop+7UBzwelT44xj3q0xtGgvXCnkelWEYkbhyB1rNR0Vtwxg8Cp8nh1ODx+VNIm5oI5A2kDrUifuuvIP6VRBypx1qWNir4PanawzS2qwyKNycbuo71VTKfc4BxVhWVuoxVxnbQNC35zY2nJp6ykAjswxiqwYxnbjPtQz5wRxilB8rvHQzlC+5r6Zq+saHN52kXc1o2cjymKg+ny9K9X0P46/ETSiElmgvV44niwf++k214gGc+w/lTthC5jPWvZwXEmNofBM4qmXUpbxPs7Sf2rNUhjT7foMbse8FwU4+jKf513Fn+2HocRzc6FeKw/uzR4/kK+CbfBjbcAKsHySodP1r6NeJOYRVjyp5DQb1R9/y/traQi4t/D93JngB7mNcfkDXM3v7cXiuNcaL4etYunNxO8n6KF6V8NfMsm4YPSpGb5v3ePSs6viNjZ7mUeF8M+h9V6v+2V8ftViEdjqkWkx9vsNuqn/AL7few+oxXzx4p8ZeMfGs5ufGGq3eqSZ4NzM0oGfRSdo/AYrEtziTcdrAdVbgcf57V7R4Qi+BetbLDxo+o6FP0+1WhW7t/qYyBIo78bqmlxZXryUZysZYjLqGGXNCBwuk+Dr+7jV7e4stoH3ftcEbD/gLMv5VPqnh3ULAbLlVJPTypI5B/44xFfUdr+yBa+N9PbVPhH4usfEEQ5EagLIP96MnzB/3x1rg7n9kb4z6HKYp7aHA75Zen1UV9LhsQ2tXoeLUzvC9XY9H+H3/BQD9tT4TafDpXhXxvfS2MGAlpqMMF7CFTgIBPGzKuOysK+itC/4LNftL2Y2eNvDHhrXCDkusdxZSEen7qV0B/4BXw1P+z38U+j28I/3p0H6Gstv2dfiMxPm/ZY88H9+D/6ADWOLyKhVV+QulxNQirc6P198Ef8ABbm1tHjfxD8Kjkn5vsWrjGPYS238zXQftFf8FevgD+0n8Er/AOCvxE+CN5qNhdHzLWebW4YprG7UYjuraRbNykqdOOHTKOCpwPyJ0f8AZm8Uu4FzewpjrsWR/wAuFFe9eEP2ORq90n9qzahd/wCxbwiIf99Nv/pXPh+FcPCSla1jnxHHeHpRs5Hhn7Mn7V3xz/Y38dt8Qvgfqq2F1cRfZ7y2uYluLG8hH3UubdiFk2E7kYbWQ/dI5Fe3/Fr9vv8A4KH/ALWkEvhvUfGWtXNjdDa+leHIV021ZT1WRbBI2kXH/PV296+1/h7+xl8PtIEdxf8Ah6EyKR+8v289v++Wyv8A46OlfamgfD7R/D+lrZWCqkcY+WOFREg+gUCvWqZXQcudpXPh8w8X4UVyUFc/DP4P/wDBPT4o+Litz40ni8PWbnc8aYuLts/7K4RSfVmyPSv2V/Z3/Z9/Zz/Zvgi1LT7GObVUGBe3QFzeHH93+GLIOPkVfc11GqQTWUXlRNtQfw5rjP3MbvKzpGq9WZsAe5PYVdN06dtdj89zji/HZkuVOy7I9e+JXxk8T6tZyaT4PB0uBwQ7g5ncH/a/gz7c+9fJNppGrXmp/YrSKS5mlJO1BubJ6kn+tZnxB/at/Z4+GkH2fxBrf9r3y/8ALlpO2d8/7Tqdi/i4r88vir/wUS+JmvxyaH8J7SLwdZPn97CfNvX7DMpGyP8A4Au4dmrizDPsNS1idHDfBOPxHuxhZd2fqj4of4MfBTR01/8AaI12KyZ1LQaTanzbufHYRp8xHv8AKn+2K/Lb9pD/AIKDeOviBpknw8+Dln/whfhPDRGO3b/TLqNuollTCxIw6xxYJz87PX596l4h1jW7+bV9avJru8nbMs8ztJK7erO3J/lWLLgkc/8AfOK+LzDiOrW92OiP3Lhrw3w+El7TEPmf4DYncnewAC8fSppHDHGffmqi5U56ZqcSRqQznORxXzc5Sk7s/SYUYJWiiUytL8q/KKh2hThOp4qBizH0z0pDuQZUjis2bEjtgYPpjFQMHAxHjmhskZpDJhcJSAYR0MmPpTf3bnCD8aYwy2+XgVHkZ8tBwKdgHh1jOOvaoXUtg/5//VT3SOPEjnaD2qq0nyjbwO1FgEYxoRkknGKrNk4ySfp0pzw7iHH3QKqTSSJ8mcDsBjmlzdEVFdx2GJ+b/wCt2qH90XwAAak34AHbpULuQTxgCs+XUbQx94C+ZgDtj0/Cs2SXfmMdB37HFOklVxsPA6f/AFqpTSsFUgHbjHSqSErCSOFzt4PuePw96oK7fe/vDj2p/wAxO3g96pEMwBi4ph0LIxyx4471Rl2v+8x8wwRj+VJJK3/ARxVe5kkSI+X9aCSSSbHysapSsVBCnbuxg05ZI3y7DGBjBqvOu4fKBgelZqxMY2JcNuEY6nk8dMU14zIm3sPp0qMyOCFUZJ6emKrb5R1zz7dKzknfQGiV1KygLjpx6VBJ83y5zzU+zC7MjIqMjbEQwrG9xoqzsWPFPJVYPc1XzsOG70SEEfIOlYtmiQzbk1HJuxinOzIeRTeNvzHmua+pqhRgIAahxt4NKwL/ADCnAAdK0jGxSQYA6VDIegqRnwNwqHIPJpopC4Ir9Y/+CFyb/wDgrl+z+o4/4rGy/wDQXr8myc9a/WX/AIIVjP8AwV0+AH/Y4Wf/AKBJTsXY/9D+A1t3IFIAwpyAjrSkqB81Sl3MvIicnzKmD4IzUewHnpQpKtszTaKkWMqDilIXO5elQkYGTUkZJGfwpRVkZWO28BPv8WacABxcRf8AoYr+zn46fEX4h6H45+zaRrd7aW/9n2DLHFO6oCbaMnCg456n3r+MPwCGHjHTe+biLA/4EK/su/aGtifG8RRcj+zNPz/4Cx19fwqvjP528bn/ALRh4vs/0PCo/jb8Xhckf8JFqeAe1w/+Nbr/ABw+Lnl8+JNT9v8ASX/xrhrPQ2muDx+ldDLoJReR0FfY8h+LVI0trIhvvjZ8XZDg+ItT45/4+X/xq5pvxr+Lilc6/qWP+vl/8ayv7CY84Ax60+30SRJ8YFLla2E/ZctrHb3Xxm+KstmV/wCEi1LJHH+kP/jVf4J/E/4o6n8bfD2l6nruoS2s1/CrxvcSFXXcMqRnkH0qpF4amki5TINdH8L/AAxJp3xl8MXeNu3UIT+tYV4aaGdCpSimkkfzG/tZvu/aT8cMuNv9sXnP/bVq8CRmRV2Hjj+le2ftT7pP2kfG/I/5C94OfaVq8Oj2RqsdfnsleTP7byONsHSX91fkaKNJt54HpVsKpHz8Djk1moCrZboQMAVbXYQP5fSqWh68UasRcgFdoFXgSygA8ng1jQEAYBx3z7VeCq+FH59v8KQ7K2heiYbNrdQam3MACtUIZTKq56Ljr/8AWq0023gDGPlPrS12IhsSr8vJG70FWVY9OPz7VT37fl6+mOwqMFnbaOg9f1q+domyNiPbgqR6Zq0H3kAdKyNzAHd/F6Yq9HIMeuKroMvAy49KnGWGDwSOKz1kx1PFXIyMAjtzTj5k36FkMyMQ1I3zAslVDOqsVY5OakVm/hwKVyrFwPgcnjFRrtEnmIfzpFY7cP3/AP1V2fw/+FnxN+LOq3GhfCzw7qfiW9toRcS2+lWkl3JHCWCb3SIEqm4hcnAyQKd0tWBzcD5iCv046VKwQZx6dv0/SvpOD9i/9rtbcO3wr8XD/uD3Q/8AadV5v2NP2vZ4maL4VeLvl6n+x7o4/KOpWJphyHzOkk6dcY/pV4MrDsRWUgkgIS6XZIpKsMYwQcEY9QRU4dTyP07VUdBGqxCk56VZgnKDKcZrKHmv86tkHjGKUTzpgMMf59KpSJlBPQ1l1O6s51vLNnimjxiRGKEHPUFcV9HfD79sP9obwA6xab4hlvLdcfudQUXKEDjGX+cfgwr5d+0GTGQcev0qRdrD61008VWj8LPHxmS4SqrVIn6m+Hv+CnHjSKFF8ZeFNOvz/E1rK9uT/wABcSD+Vez6T/wUj+Dt5GDrvhHUbVv4vJ+zzqPpnZxX4lA9ckZ7dKnXdGMg9a9WnneJVtT5bEeHeW1HpGx+7P8Aw8V/ZqUfJaarbEAZH2GMgf8AfL1PF/wUf/Z2X5g+qgen2Lkf+P1+DF3C5zu5x17VRgiVepxVTz/E9zzf+IVZbJWuz93dV/4KV/BG3VRY2es3J7f6NHH+ZaWuG1f/AIKgaXHAw8OeFZ5CRw11dRxD2+SNH/nX4wsgHJ/n+FKjcYAH4YxWM8+xD6mtHwpymO6uffXjP/goh8c/EMMkehQ6boqHIBghM8gH+9MSv47a+MfGfxY+J3xCmJ8a6/e6gh5EcszeUPpGu1APotc6ORtJzvHArMaPa4Y4A6/lXnVsdWqK0pH1+XcL4DC6UaSQkDPAuccNxgDFXi0uAB26Vnh3AAQcrU6GbJzWMZW1PfhTjHRICiJ078U9CQCABg/4VXVArZ/lT1IAPpWcpj5UgYkEimZjjPTIp8h3deRUJQxoFPT/ACKn1GNG13+TOB/KjaI+lRvJlQoAGKhHlk5BxigESu4Iximgx7QR/wDWr1PwD8B/jf8AFnSp9d+GPg7W/EVjazfZprnS9PmuYo5goYxs8alQ+1gduehHau0b9j/9qxPv/DHxYP8AuD3X/wARWTqxRXKfOXzudpoZ9nydCBXsvi39nH9obwJ4duvFvjTwF4j0bSrFQ1xe3ul3MFtCrMEBklaMKgLEKMkc4FeFhirYYgnpWkJp7CsSSOTye1UHkIY7fWrBZj8pqoZPMcgkfLxQ9hx3Hbt3yY9vao24+9le3GKHdkZpGAGRUU80xjLADjnn0xU3uhsiaTYyoGJz3Pp6VUnYfdfOR9KSQupDDGFHaoJ5syBeu4DpURZEZPYilkDVWZmPelk+Tlunaq0mQenWrfYZDJJ8oVRz3qs5Bb5eAx/KrEkmDhRgHjj+VVZUwViHX2ouA4yRqCQBx1qkrMHODkE4r6P8GfslftNfELw5a+NfAvw98S61pN6pa3vbHS7me2mUMUJjkRCrAMpXg9RitW8/Ym/a9tEy3wr8W5Pro93x/wCQ65pYqCCz7HydPK/mbGOaaix54BOf/wBVeqeP/wBnr9oH4WaOvir4leCNe8P6a0q263eo6fcWsHmuCVQSSIq7iFOFzzg+leUyyMke3oeDUxqXdkU420HF/LxTHlaJML36VGzlm347cUgyw3v0pzZImMKJMHnuarl5mOM8VPPJwIweB1qEjC781yN22GhJsbQOKh5C0EZPNMLfwms3K5qo6CbmZhupk3b0pw2ry1NY7+lONi+thjHP3RSsflpyA4xTH+7j0qjWyK7Ak08DCindqTPHNJobQcZ5r9Yv+CFXP/BXb4AY/wChutP/AECSvyZbIPFfrL/wQrx/w9z+AH/Y32n/AKBJQgSP/9H+BDGKikTK5pyc5JpzcDOKlMxSAdM0z/aPFLyH21IVA4Bz06VVi29BUfI5NNBKc1E24HA5B9KsqB3qHKxnY19B1Q6JrNrrAXf9nkWTb0ztIOK/e3Uf+C4mka2IpvEHws0q5uI4YoDK085ZliQIuSGUfdGOgr+fs5ZcdKpSJsfYTXXhMdUo/wAN2Pnc74SwGZuLxkL8ux/XT+xz+1b8Cf227+88D6Fov/CJ+MIYXntLVZDJbXaoNzxrv5V8DivoOfwyqZTbzyPx9K/nE/4JFahcWP7fvw5Ns5QPqsUTY7q4KsPxBxX9YviLw8qeIdQSNeFupscdtxxX3+RYyden7+6P5G8VcjoZPmao4b4JK9ux81/8I1lduzj8qYvh1YTvdRgV78fDkm04jxn/AGazLvw40Me7bjPGe1e5KOmh+arM+lzwT9ov9oP4I/sUeFNIv/iNp7eIvE2sRC4t9KV/KjhgP3HlZRu+bso7V+e13/wWy8J6ZdJqWhfCrSkubZw0MhuJ9ysvII56188/8FttWnl/a8m0uSQmO10zT40Gfur9mTgV+OLQiVQR37dq+BzLN6yquENEj+neAvDTLa+XUsXio80pK52fxG8cSfFD4k658QZoRavq97NdmFfmVPNcvsBPJAziuWRyvzjpxx09KrRRmKT5ew6VMT84LcDpXkU276n7vRSglTp6JInhnk3YkHyg4FaImcE47ngVkoCUXPXPHbFX4WxwT1rdytodCdtDUZWC/ez+XApVlkUjAz6CqYEg59+R/jUi+ZkhqcSma4QtgoRj/PrUoJBBJOePwrOiQpkLwp7+1XVVm2leCBQhXRaLeWM7iATQvUbe/wDn+VRyh5E2rgZ4qCFNqh2PI61Vl1D2fU1o08weWOvXHsKmVsHdjAPGBWdH+9YEHaVwPStBASd56/SovYnmsWEEcYP86sbioAb8KpASE7Y+/ao3Zioj7/4VcamxDSb0NWOVC2CBjpUw3DBQAisuCGRCZBjaelW2Eoxggf1pp2KNCNlfKjrX7Uf8EVpdRg+Ifxjm0q5e2mTwAGSSFjHIpGp2+CrLgjHtX4qRruHA5x/hX7jf8EOLVLv4m/GCMD/mQlXA99ShrixbfIzSnvY/U268ZfEmKIKniPVQMA/8fs3/AMVXp37PHibx7ffGXSrTVdd1C5t2S4LQzXUrxtthYjKlsHB5HoazpfCiscMvH9K9B+DegjSPidYX/l7Qkdz0HrCwrwYyO1H8S3ieRJPEupyp1N9dfh+/esBNu8hCOTVzVpi2vaiH5H266H5TvVMpEx3sBwOMV9TQleCucDVmXI0K52ttFDBmb903JxUIDj5Rzx9KkX5drDk1ck0FhEMgYc8d6eUjI3Z2nP8AnFNE4XkYx0pjyoQN+Mj04oWmxA7yoxlh1AqVXdSASDjrTMb/AJkHaomG1CxoaY0WGEhyxORxwOKrqHDAjH41IiM2cfT86rzQsBuboOlF2OyLKMZB8/T8qAkQPP6cVXgHYHoBwKtP8oBYA+taT3RKHrIkce5Nuaqvcq7DaOlQSDbkLj8PSpkCocv+QqJFib3HKrhW4o+Y/e4p0k7Bf3f1qDLlsHj0xUgWMKeWOD+VRbyMADdx2qHKJ/ric/5xil3BB+779qaEyYvIfuAD2pJCF4kwcVAwZsbj7ColcxKA/JNKwIHkdxtAxgfyqjPzGA4q7IZnAc8emKglURAsT2JpvQJLSx/R1/wSi8S6/on7AHi6Xw9qFzp84+IOPMtZWhYqdPhyuUI4PHHTgV9qwePvik4G/wAT6sfrdyf418Qf8EkrA6l+w74ttTgg+PC2B6CwgH9a/Rq08HqU+5xXzGJfvM747I8E/a08R+LL7/gmr8eJPEmqXeogWmjJH9qmaXZuv4923d0zgZx6V/ItJM32iUAZUucV/Xn+29Zf2X/wTP8AjjGq7N1vov6ahHX8gaSPvkz/AHz0r0ctn7rRz10WBL1HcdhUTvnAI+7jj3FLIrZDdOc01m8vLEc+tdtzm5+hBcMysUbjPpxUGN42sTjIpZieDIfpUDFlbamNtXHYFoiORuTFGR8v8qgwyPuU7d3FI67TlMcVXfCZbOTnGB6Vdy0wlZUAIOBxuArOklZDtjGQfWrLEE7WG0VA+Ihvk4qZMAlcHDHnPT602KFnkjIJCs1Q5Mh4Oef0q5aY81GbnkYrNy90zlKx/aH+xxq3irSv+CZnwDfw3ql3p3mWGsCQWszwh9uoSbd2wrnGTjPTNdlqnjT4oHj/AISTVsqO95L/APFVR/Yo0w6h/wAEy/gPGvWOx1jA+t+9el3HhRtxYDk8V8zV0kerBaH53f8ABVDUfEOr/wDBMW8k8SX9zqMi+PNM2PcyvKyr9km+UFySByTjpzX8mRBK5x746cV/YB/wVh0b7H/wTJu+x/4TnTG/DyJRX8f9wSMDGOeK9PCO0Tmr9EKGJbk8D/8AVUUnKAAjBp6oEjwQeaok8gDpXQ2YJEsceV3H7tMfONi9qGdigXgU0ZVea55s0SHH5Rk1XJDSbgOO1L8zE59KZhl9qiMdDXlHysvTtUSYxxRyWwaf8qjp0q1GwIhk+Vjio169aewXvTWwFwKo1Q8jHSm5PWkGc/NSEkttHFAyMmv1o/4IU8/8Fc/2f1H/AEN9n/6DJX5Lda/WX/ghcwX/AIK5/s/f9jjZfyek9gP/0v4CIy24YqXHduD2qqjc4qeLLDPbNJktaBJnfnNKgzUnlq53saiXeH2g0xdCRdpXOali24w3aolCoCM0wblbK1lJdCWkW1C5GRVaQhvm74qYHeNuOcVCXZGzUoUT9GP+CTzCL9vT4cSd11i3/nX9oGreHmm1u9k7NcSHj3av4tP+CVsnlfty/D2X01aH+tf3hx+GftEr3BTl5GP5mv0ThH+E2fxL9JjF+yzWl/h/U8KXwzlN3XvWVqHhbMLZG7j0/wAK+no/C6qB8hx9Ko6h4UD27kIeFr63m7H8z0841P4vf+C37mD9tzUY+gFhp+P/AAHSvyTjlC4Kkke1frr/AMF01aD9ubUo8cCxseP+2C1+PFvIwHHPavyjMnavM/0y8PFzZDhZf3F+R0bIp/e8YHHFRzSAKMjj8hTYVYsp6DHSvor9mr9ln4y/te/FS0+DvwP0s6nqk6+bNI7eXbWluuN9xcyniONc/VvuqC2BXO5tH1cItvQ+alml80LCvXg4rbsraSaXyI8Fz91V5b8AOa/s3/Zp/wCCDX7K3wTtLfVfjx5vxS8SxqDLHIz2miwuOqRwRlZZwPWV8H+4vSv2K+Hfwr8CfCjT49K+FfhDQPDFtEuETTNLtbfaO3zBAT9Tz61ySxvRHpKhof5tP/CMeIo1Ex0+6KAZJNtMFwPfZWQEEUvkltrE/db5T9MGv9P+S88bXMO2S6cg9vLjx+WyvD/iJ8HPh38RrOW1+JvhHQ/EEUnBGoaTaTnB/wBoxhh+BoWO7k/Vkf5vhG1vm6EYUVY2yocdOw+mP/rV/Zb8bv8Agiv+x38XGlu/h/pt18OdVfOyfRHaa0BPQyWFyzDaPSKWL2r+WX9rH9nDxL+yf8Y774M+J9UsdYuLaCG6jurBm8t4JxmIujhXikKDJjOcZHJBBrtoYiMtEYzoSitD5ocuR+4+UjqP0qEvExKP8pBq1LiQB1J3Vnm0v7+7gstPhkmuZ5EhihiVnkkkY4VERRlmJ4AA9K2lUtuFKb7GtbTNIvlY3Fvz/AYq+yPb/PMyxr2LELX71fsRf8EIPin8UYbXxx+1TeXXg/S5Aso0OyCHVGQjj7VM4aOzz/zz2vKO6oa/pR+CX/BP/wDY5/Z0s4YvhR8M9FS8hH/IR1GH+0r1j6+ddb3B/wB3aPQCuCpjVsjR0OZH+exBYajeR79Pt5Z8jIMUTuMevyqRWDdqbSX/AE0iAk4/egxk/g4r/T1EmtWkP2XTkitYk+6sFtCigdBgBeK47xH4dsvFVm1n4u0rTtXhcYaO+0+2nUj0IdD+VZfX+xSwkeh/mjCWRQG6o33SD/h7VahnZiO9f3CftHf8Elf2Lvj5aXF5beDo/BmtSKSmpeFgtiwfsWs/+PWQdMgop9GFfywfti/8E9vjd+xV4lFz4kH9teFLibyLTXbeMxp5h+7FdwncbaUjpklH/gducddLH8+gVKNlofG6FGiGzg/4V+8P/BAe0W9+NfxVtMA+b4KjTH/cQjP9K/BaTfGpBG09v8/0r+gf/g3aT7V+0n8RLNlwZPCUK49vt8YpYn4Gc+G+M/fgeCndslcfhWh4c8NNp+vxXrx/LEkvT3QivqKbwmQxCpx+VYWq6DBp1nJez/u1ROWPAA4/SvDi7HprY/zcdeDf8JHqccY+7qN50Hb7RJVhYYA6wGRFkOMLn5j/AMBHNf0VfsR/8ETrTxbcy/F79slriO3vrye6s/C1rJ5DtBJK7xyX9wh3rvGCIIirBcb3H3R/Rp8J/gL8FPgZpcek/BjwPofhmKNQAbKwhWU46bpiplY+7Oxr1VjklZGDo3Z/nZ3Oia1aw+dLZ3CR4HztbyqmP94rism1/wBJTzLRlkVeCUIbH5dK/wBMC81bxHdL5c8sjxnqjJGV/LbivkL41fsH/spftF2sx+KngLS572UfLqFlCun3qfS4s/KY/wDAgw9Qacc1exjLCH+f8Xij+Uc9M/X6VH5kbNjaBj0r9fP+CkX/AASi8bfsjWlx8XPhXPc+I/AcZJuWmVDfaSGYKnneWAs9vn/luiqVPDqv3j+OtrOT99c5I5/yK9KjVU1dGfLy6GpGqDHoaqPHjhTjJ/CpRJHH8jjvx/ntUE8AkTzEz04/wq5Sa0AdauHJUsRt/DitG4sd0G9cgdeelfV37Fn7Cnx1/bT8Xf2Z8PbUWGhWkwhv9cu1b7NA/B8uJF+a4mx/yzThf42UV/Wd+zx/wRg/Y4+Bum2+oeLfD/8AwsHXo1Be88RESwK+MHy7CIrbqOOFfzGH96uKpjVHQ0hTbP4arKcXV19ntG81v7sXzn8kz2ravre8s7USXcckIxx5iOgx9Sor/SH8N+BdC+HtuNN8B6LpmhWkeNkWm6fb2qAewRBxXQahPq+pwm21JhcIeqzQxOPphlxXK8zfQuOGR/mc2Ei3k4Fs6yDuVIIreciPhu3XjHtX9+/xd/YG/ZH/AGgIZm+K3w50a5vHGFvrK3XTL1T2IuLPyWP0bcPav53/ANvT/git4/8AgZo178T/ANmu6uvF2gWqPPcaRdKn9q2kCjloGjCpeIo/hVVlA/hfqOijmCb10CVBn4MSXCEgRrxVcM0mOcYrJi1B7gjyfmz3xwP061rocpjjnrXdGRgKWTeAxxxyPp+FItxGj+Wo68VWusoCF7dK93/Za/Zn+M37XHxMi+GXwX0j7ZeALLd3UzeVZWEGceddTYIReyqMu54RSeKU5qO4rX2PGEjuHT90OR9Mf5/lWbYRy3twbOzJuJP7sQMjfkgJr+079mT/AIIlfsvfBrTLbV/jDan4leIowrPLqIMOkRSY5FvYKR5qjs1wz5/ur0H6l+HvBmkeALWLR/AWkWOh2cIAjg020gtIlA7KsSAYrzKuY22OhYfQ/wA4W50nWdMRX1C1nt0x96eCSNcfV1UVzeo3JFtvgIYEZ3LyMeua/wBMeY61qdm9rqTtPFIMFJljkQj0KupBHtivzM/ae/4JX/snftMQ3F5qfhaLwrr8w+XXPDsUdnMpHO6a3jUW8w6ffi3Y6MtTHMn1KdDsfnT/AMEQtJXWv2QvFNsEyP8AhNJm+m2ythxX7MR+BgkGSvUelfPX/BMn9ibxr+xv4I8afBbxdeW+rxS6/wD2tpl9AhjS4spraKEMYzkxSB4iHj3NjjBxiv06bwoyr80YFedUd3c2irKx+L//AAUy0JtG/wCCbHxmG3HmW+kfpqEVfxYRnbO5H94nAr+8H/gr94aOnf8ABNH4sMQF82HTMf8AAb6E4r+DufbBdv6Zr0MuVkc9dbGgfvjeRgjjJxWXczMnAIz2+YDH4V/UB/wQn/Z1+Bfxo+BnxK1/4peDNE8Uahp+v2cFtNqtlFdtDE1orNGhcEqpY5wO9fsrefsH/smySnZ8KfB4x0/4k1v/AIVVTG20SBYZWP8APrUs8e99ueOcioS21fmr+5v9sf8AZG/Zj+H/AOxx8SPF+nfDTwvZ3lh4f1I2txbaVbxSwyizmdJEcDKsrqpBGCMcV/CuZWYKuey/oK6MNW5zKpGxZAzuVe/f2rPmZx8qD5sjipnSRk+fgCsi7k/cSSIR/q22/wDfP/1q6XKyFBdC+kcspCN0+o4NVdUheJQ569ulf6Fn7OH7F37KPiX4A+AtduPhh4TlnvfDmmXE8sukW0kkkzW0e9mYrkszcknqea9U1j9hL9lJ03R/CzwgMdP+JLa//E15s8d2On2J/m0pLIzdQCuBgYrYspEWaPP3dwxX78/8HAXwT+FnwV8afCyw+GPhjSfDQvbHVHul0qyhs0lKPbFN4iVd20Phc5xmv58IrgxOFYACtoVeaFzkrU7SR/ev/wAE9NFGpf8ABMr4HrgHbp2pHjqN17JX0t/wg4bkpnd2P/6q88/4JRaSmuf8Ex/g4EHNvp92Pwe7mxj/AL5r77i8E/dJGcV4k4Xep6cdj8Jf+C1mi/2L/wAE0J4nG0t4y0p/zjuB/Q1/FOx3ZU8gHFf3T/8ABf8A0eTSf+CdATbhX8VaU31wtyP61/CkzEynoMmu2m9LI5q6GziVx/KqHmKOGPStmUFYun5fyr7S/Yi/4J5/tA/t4+MX0b4VWK2mi2DKup67e7ksbLPIUsATLMV5SGPLHqdq8jZTIoK58NxxvI3yLkVfsdE1XVZfI0u3kun7CFDIfyQE1/ex+yx/wQ9/Yl/Z6062vvGeh/8ACyfEkKgvfa+MWu7H/LHT4z5QX0Evmt71+svhPw1ofw90uLRvh/oum6DZwjakWm2FvbIvsFRFFczqnR7NH+Wde+D/ABVpkXmahpt1AvrJBIgx/wACUCuc8lzwOcdhX+rFe614hukNvqEwmRhjbJDEVx6YK9PavkP42/sJfsj/ALR0Lw/Fz4caDf3Ug/4/Le0XT7se4uLPypPzJHtTjiV1Goo/zW9rLgEYqJulf07ft3f8G/fif4daRffE79kO5vNf0+1VppvD17se+jjUZJs50Crc7QDiIosuB8vmHiv5kL+1urO5ktblGjkjYqyMCrKRwQR2I9K2i77EpFPau7ingD6VFyOtKeFPrVhzMjbjGKjHrS565oUZBoNBdm3Gf0r9Xv8AghgQP+CuX7P+f+hxsP8A2evygPpX6u/8ENW2f8Fcf2fz/wBTlYf+zUAf/9P+AHnOKlU/LgVG33jSoBnrQBdPGF64qA4U/JxUqsASaRmAHT6UE3RDuYKGNTxyEgbue30qPbuI9KlQEcAdKWgNoVS6n0okkDYC9v8AIoOcYXtUXJ5I6UrIUUfoH/wS6lMf7b3gJ15I1OIj8jX+ip4c8OebpcDMOsan9BX+dV/wS7QH9tnwJj/oJxY/I1/pXeF7mwXQLRWX5hDGD+VfecMO1GR/AH0uqzhmVDl/lPPD4ajU7QvI6cU2fw0vlMoUZA9OOleoveaerD5elLLc6ebZ2b09vSvp1UP5Cji56H+f3/wXptPs37dOqMw/5cbL/wBErX4sQPzjpX7if8F9tr/tyarsHC2ViM/9sFr8OiRkbeCuK/Lsxs68z/XTwtk3w7hL/wAi/I6aB+Tu6dQB+nT6V/or/wDBHr9gXSP2VP2SdKlubJV8UeLYodU1udl/em4kTekGf+edqjeWq9DJvbvX+eh8ErGz8Q/Gfwh4b1Lb9mv9b063l3dNktzGjZ9tp/Kv9iX4U+BI9Q+HGi30CcT2gfpjlmJIGOOPavNxErKyP0WlTsj5THw/i8391H93jpUGv6b4S8H24vPFN7BpyEbv3p+baOCdo5x74xX33p3w0ElyPMi3HqFxycDgfjX+aF/wXe+NX7Svir9tjxF8M/ifd32n+HbIQS6bp+XitbhXjBaYoMB9sm6IZz5YTYMENnjhS6I0bsf2wr+0H+y0bw6XH440M3Knb5ZvrUNk9BtMob8MZrs/L8H6/Gs2jX8Fwr4CFT94nptPQ/8AAc1/lEavmNSsaKMY7V6f8Hv2n/2ifgDqiap8F/GOq+HXBy0VrcuIHPpJbsTDIPZkIrZ4ZijJM/04PivJ4X+Enw81v4jeMZvsel6NZXF5dzdClvBE0srD3EaNgeuBX+aP8bvjb4g/aE+MviT4y+Kv+PrxHqEl75fUQxE4ggXttiiCxr7KK/T/AOLf/Ba39pT9ob9iPWf2UfihY2zanrMttFLrdr+68ywRxLPG8PRZJTHEuYyqbN42fNmvxeRDE4CLg8cfT/61deEpcurRjUmmrI622G5gzj5QOfp36V/bV/wRL/4I92nwp8Fad+1p8eNM3eNNZgFxpVtMn/IGs5kyoCnpezRkM743QqQgw2+v52/+CK37J0X7Y/7enhLwHrtp9t0TQWGvajCwBjlFs6JawPkcpLcvEHHeMNX+qrb/AAttNI0mLSLJSyW6hd2OWb+Jj7seeKzxlXoh0IdT89R8OlhVIIItkSdEA4H+e9a1v8PHmPk7ScjgAdq+2bnwFbWaNc3m2GJFLO7cKiLyWPoAPyr+KX/gs9/wXq8U/B/x1f8A7NH7JTQLqNthb7UHUSLbKwBTKdHndSGETZjiUrvV3JWPgp07uyNz+lq48OaDbzNb3N5ACpwV3biPqFziqTeD9LuSY9OninYdkYFvy6/pX+Xn43/a1/aq+K+ptrXxA+IXiDUZn5w+oTQxrnskMTJFGB2CqAO1eo/Bv/go/wDtv/s56lbat4B8e6pc2kDh203VZ5NQspMfwmOdiyf70TIw7MK6ng3uYLEQvY/0ql8Dqw+ePvXD/Ez9nbwp8VfBmpeCPGmmwalYapbtbTQXUe6KeJhzFKP7p7Eco2GXkV8e/wDBIn/gqN8Pf+Cgfwvll8UeVo3ivRNsWp2bvu8piCYyrHmSGUK3lSEZyDHIdwVn4L/gp7/wWt+BX7Gdje/DXwFnxD45Efy6bbMEaHcBh7uYhltFxyE2tMeyICGrnVN3sb3P48P+Cjf7HeofsR/tD3Xw1tzLL4e1KM3+iST8yra7zG9tMe81rIpjY/xpskwA4A/Sr/g2uaS//bD8W2C8GbwzEp/C+j4r8Sf2l/2yfjh+2j8Q/wDhYnxivUYW4kWxsbZSltZpKVMgjDM0js5Ub5JGZmIGTgAD9z/+DXS2jvv2/NZ02Q587QIlA6f8van+lelNNUfeOWCXPof2fy+CHJOxOOelZN78Moby0a2u4BIhA+QjIz2471+gL/DdGYusXt0xV+z+GkT/ACeUPevJ5Trsfm3/AMKmZHC7Oc5AUYz6niryeBdOtBsvp4YnPG13VT+RxX4//wDBcP8A4LIf8MXvF8D/ANn5La/8YahC0mXJEdvb5KfapthVtrOpWGJWXzNrOxCBVf8Ai18V/wDBQn9uz4g6s+ueIPihr8budwisZxZQJn+7FbiNB+Va08LKWqJckj/TZi+HcLr51uA8bdGTBU/iMimH4dFY9iR45zwK/hB/4J9/8Fr/ANqH9m74o6VpPxp8Ry+JvB99PHDey6ll5rVGO3zWZeZI16uGy4UZRgRg/wCjh8J49H+LXw8sPiF4dAa1vo87QQ2xx99Mrw2D0YcEYI4IqJ0+R6ijJSWh8VeJfg5Y+KNFutB1G2S4iuY2iZJVDoysNpR0YbWRlO1lPBHHev8APV/4KZfsaf8ADFH7Ump/DzQ4Wj8Pasv9q6IpyRFbyOySWu49fs0qlFJOTF5bHk1/qd2/w7Es4Aj4z6YzX8jH/B1l8BbHQfAngD4tRwiO4tdV+ys+OTFqNvKHX/v5aRH8a6cFU5ZIU4XR/EpdAA9Rng/Wv0F/4Jw/sOeK/wBvb482/wAMdM8+00DTkW812/iXJhticJBCSMC4uWGyL+6AzkYQivzm1CQfNIMbV5P0H+Ff6SP/AAbwfsK2XwK/Ye0jx5qlkY9e8YBNZ1CVh8zTXUavDH24trYxx46BzJ6mvRxVbljoc9KFz6i+C/7Kfw//AGefh5pvwy+GmlQ6XpmlwLBDFAuBEndATycnlmOWdiWYkmvXrbwM0iiEJ6cAdf8A61fcuo/DlmLFEz+HX6V/OJ/wXH/4KhW3/BPjwGvw4+GJiufHWufubaNjhUbapkeTaQwjhVkL4xvZ0QEDeR4dm3Y6tEj9AviHrnws+HVlLe+NNesdNjhO1zLKoSMjs7/dQ/UivHvB/wAef2ZPHmr/ANj+EvHGiajcDC+Xa3kE7Z7fLE7kfiK/zUvjL8Z/jP8AtI66/i/4x+ILvX72Qkr9pk/cxA87IIFxHEg7Kige1eQaTouo6Vdrf2ZFvPAwZJIyUdGHQqwwRjtiu+OXS0MXiIrQ/wBZhfCFvJZpfWbJNBJ92SMhkb6EZ/8ArVUv/AkF/bGKdNwODjp+I6YI7Y6dq/jS/wCCNv8AwWN+KXwr+LOkfs3ftFatJr/h3xDOlpYX97IXnhnb5Ut5ZWJ3LJwsUjncj7VJKEhf77dB8HWmu6Rba3o5FxZ3cSzwSgcMjjI/Q1x1acoOxvFpo/go/wCC4f8AwTNh+CuuyftcfCixFvo2rXIXxDawpsjimnYLHqKqo2r5shEVwqgASlHA/eHH85wkEbBV4I496/1tv2of2WPDfxx/Zw8VfDjxjZfaLC8064jnTGWMEkZWcL6Ns+ZMch1U9q/yavjL4G1f4M/FfxH8JvEZ33/hjU7rSpnAwHa2laIOPZ1AcexFergK942ZyV4W1R6P8Cvgb4+/aQ+K+gfBT4ZwefrHiO7W3iLA+XCgG+W4kwOI4IlaRvZcDnFf6Iv7G3/BP34ZfsW/Baw+F3w+sh5ihZ7+9lRVub67K4a6uCP+Wjfwp92JcIvQk/in/wAGp37H1l4/8TeMv2r/ABJbCb+zsaNphYZAih2S3LAf9NJWhT1xEw6E1/a/e/DiSQFymWznpXLi6zbsb0oWR8DweBZHfaFJPcY7Cpb/AOG0cVqbyQbEGMs3Cj6k19IfFrVvCXwK8BX/AMSfHTJBY6chY+YVjV3ALBd7YVFABLMeFUFjwK/z1f8Ago3/AMF8v2kv2j/G2o+FP2cNYl8JeELOV4be+slCXl4AceZGXBNvCcfJtAlZfmdudi8kIOWiNG7H9r50DRgcrd2+F4zvG3P16Vv2nw8WYCdUyG+6w5B79R14r/LFP7Tv7Vq65/wkf/Cx/FP27dvE41i8357dJe1fvR/wTO/4L4fH/wCBnjPTvAv7Vmo/8JV4UvZkjk1a7H+mWQbgNOY+J4RxvYr5qAbgzAFDrPCuKuR7RbH9vMHgJY+fK6DP51A/gd2Yh48Kfbjmvrf4bReF/i18PdM+JHg11uNP1OIOhQhwrfxJleDjsRwRgjgiutHw3BbJXj6VzNdC0fzOf8F19E/4R/8A4Jk+PjtwZ2slPsBe29f569+3zSEHAJJ9uK/0kf8Ag5M0RfDP/BMfxMu3HnSWoz06Xtr2r/Nivy0qu6dFP8q9XB2UUcuJ6H9if/Bs1Y/258Dfijp47+I7UgD2sEP6ECv6fIPhm0oUGPj6V/OZ/wAGlmif8JF4L+Jmnld2Naik6f8AUPX0Ff2hQfDFRhWj6D0rz679/Q6kfz7f8FVfCf8AYf8AwT5+KMyoV/4kWo549LKav817H3Wx1wR9O1f6o3/BcTwc2hf8E1viPdou0yaRqSen/LjMf6V/lcsRH9/nAGMV34KOhy4p+6Pkkcrg+nGOwrCvUAikxzlHP/jtaDzfNt6Hj0FV7sI0Mu3nEb/X7pruqP3TkoN8yP8AUe/YR8Mf2x+yZ8Ob3bkDw1pqce1vGf5EfSvsYfDsSR4eLPGK5X/gll4RbWP2DPhrrLJuB0WzTP8Au2sNfozbeBVZMGPGfavnZb2R68j/ADwP+DpLRDo3xe+FFk42lNP1XH/kkK/lVuJSu3Izgj+df2Bf8HdumNov7Qfwut1+UDTtX4+sloen0wK/jseR5jj3FenRsoWOOSvUP9In/ghzpn/CR/8ABNL4axkbhBYSD6f6XcZ//VX65weA/mCqn6dq/On/AINtfDp8T/8ABNDwjKEJ+zRSRn/wKuDX7/x/DgbgGjxz6fSvOe7Os/kc/wCDlzTU0D/gntaW23aZfEult6driv4A4GG/5ume1f6Hn/B2XpEmhfsPaJargKdf01iOna7Ff52cFwA/XAHJH0rrpL3dDKpC5+jf/BO39hTxt+39+0bpfwU8MF7PTEH2zWdQVNwtLFSFYoMYM0pIjhU9XIJ+VWx/pB/A39lT4cfs5/C7Svgx8JtIi0jRNEi8mC3jGcHqzu/WWZ25kkb5mY/Svhr/AINm/wBhix+EH7DyfG3WrLHiDx5Kt/LIwG4Qsn+ixg/3Y7dg4/253Hav6LLj4cBT5hj698ZrnrSbYU6XKrI+BbTwN5c5iSPJzxgfhXEePfFXwg+GVkbv4i+ILDRo4yVY3EqrtI6hiflX3BIx7V8N/wDBdH/gpTB/wTi+D6aB8PDDL468QL5Vkj5/dh1JLHaQQFX53IwcFVBUyBl/zg/i/wDH/wCL/wC0H4ul8b/GfxBeeINRkbIe6kJSMZ+5FGMRxIOyRqqjsKKVK5qf6b3hn9pj9kT4hat/ZXgn4haFqV2W2CG2vbeVs/7kTs36Yr6g0nwTDqEK3OnMs0R+7JGQyfTI9K/yNQZ1mW4tf3TIQVZOCCOhBFf0lf8ABFr/AILQfGD4A/GPQ/gN+0Dq8viDwZr1xHZW9xqMpeWzlf5Io3lc5aBzhAXyYTtIPlhkNSoW2EpI/uuj8DI0TWs0W5GwCG9vT3HbFfx0/wDBwt/wS60/wr537avwbsVtw7BvElrAmFkRiqC/2jgSoxCz4GHVll4IfP8Ae5onhDTPFGiWXijw+fNs9QhWeE4x8rdj6EdCOxFeH/tM/s2aJ8Wvgl4j8DeIbNby1vLKbzIWGQ6eWVlj+jxll/H2qIy5WOx/jQSgo+xe1ROSOGr6D/aq+CV9+zp+0N4w+CV+xc+GNWuLBZGGPMijf9zJ/wADiKP+NfPTnJwDmu8SG45wKBjrS9OlKq+nagYMNuMV+q//AAQ5P/G2z9n8Y/5nLT/5tX5UYJx9K/Vv/ghxhf8Agrf8AO4/4TKw/m1JjR//1P4AmA7Ug9qSlHvQBJ5jD5RVgLnk4wKqL8p+lWUwFKjFFiZIXdj5R2pyybGGKcyKqbqg9xWcVqRpYndspwKrHKthutG7jANOctvJ9sVoVFWP0Q/4JXxGb9uPwBEOp1WH+tf6F9h4neztRas+BH8np92v89z/AIJP7n/bv+Haj/oLwZ/Ov7l77xG0OoXULMflkcfrX3vCi/dM/hL6UuE9tmtFf3f1Poo+KnDE7varC+K/3TDfk4r5dfxQoBLMcVJD4p2qVDdR+lfW8iSP5e/sbyP5Mv8Agva279trVCv/AD52B/8AIC1+GU/GGXjIr9u/+C8E7y/tp6i4HP2Gw/8ARC1+HTu/Q8ivyTMo/vpWP9SvCmFsgwq/ur8i9per6h4f1u01/THMdzYzRzwuO0kTBlP4ECv9in/gk9+1t8P/ANrP9jnwx8RfDs0MjTWizyRowLReYSZIyOzQz+ZEw/2QehFf45flNLgDnPQV+yv/AASr/wCCrvxh/wCCa/jfydOWXWfBOoTCW/0oSbJIXI2tPalsoHZQA8bjy5ABnDBWHBKOlz9EdSK0Z/riRa5pME+5VAGeDnvXyN+1Z+w9+xL+2NpL2/x+8HafrErZYSzQxyEOerruU7HOBlk2sfWvzZ/ZQ/4LA/sh/tfaVb3Xw38XWaarKqiTS7txa3yN6G0mYOef+eJlX0avufUPitbMcLcbfrlPxG4CuSU7FH4g/Hj/AINcf+Cdfjyee8+Hj33heR/uCwu5kC/RZzcx/kgr8d/jn/waV/FvQ1m1H9nj4hWusCIbks9ZgCZx2+0W25unpbflX9m3/CwNyhfMznBGD2xV238amJ93mcY/KlCrJEuJ/lg/tRfsF/tU/sWa6vh/9ofwhc6LDI5jt7+LFxp07D+GK6izHu7+WxWQd0FfE+rRpG+IuP59q/11vi9pHwt+PXgPUvhp8ZNHttZ0XVITb3MFzEsqOh6K6n7wB5HQr1UqwBH+bJ/wWE/4J9XX/BPr9pQeE/DLy3ngjxNG9/oFxJ85iRGCzWTv/G1uWXa/V4njY/MWA9HD4rm0Zzzw9ndH9FP/AAZ6fCzRJPEfxC+NWpIplS8gsomI5VbK2MuAfd7pT9VFf38Ra9oEpDbVOfav4Iv+DT7xbHo37Nnj994VofEksZA6/vbO0Zc/UI1f1uwfFFUUN5hA9K4Ks9TqS0Lv/BTD436T8EP2LfGvxCssMLWxnd1A+9FBBJcypx/z0SIx8djX+ND4w13XPGvirUPG/imd7rVNWupb27nc5aSedzJIxPuxr/VU/wCCrWoah8Uf+CenxR8MaS5a4Tw9qk8ajqSLCcYr/KckJkjSVCNpAP4V04GKvqZVr2L8L4wRjgAde1aUvlTRYb7p7Vz0BkM37rgfp0rehz0lGcHr7166tY5bHqfwm+L/AMWPgRrlz4t+DPiO/wDC+pXdo1lNc6fKYZXt5CCYyR0GQCCOVIBUgivOr2e81OeW91GV55rhzJLJIxZ3kblmZmJJZjySaqyu8UYd+hFLbSiTDbvvcfSpUVcUr7E0SCzjGwZH8q/pM/4NZNRWD/gpS+R8n9kjd9FMzflkCv5sZg6nYx4I49K/og/4NkZpbH9v7VdTHSy0HzT7ZaRP/Z65MZpHQ2w61P8AT/h8S+H5FztUZrkPi74x0vQfhV4g1PTdsVwtm6RsMZDy4iUj3BYGvjCD4nzhQPN4+tc38SviHcav8PNUsI5RmWNO/wDddT/SvKhW6HXc/wAsT9vn4s6p8dP20fiV8SNSkeQXXiG7tLUMT+7srCQ2lrGPQJDCor5XiYI/l4xz09B+Vb3j2+lvfiBr17I2Wm1O+ck8ZLXDnNcn9qXqFwOhr2aMfdVkcNWXvFrU9k0Bgj53cN+Vf6oX/BvH8UT46/4Jp+CLzxJKJ54tJslZ2+8xgjazJ57kWy1/lbXU0b7I+B8w5r/R7/4N/tcn8M/8E0fAFwZQBd6c4x/1zvboVy422hphT+pix1vw1FmRY8Z/Kv5Rf+Dt2Sx1T9hnSdVsFXFjrelnn+HdPKn8mr9zE+JjcBZq/nO/4ObPEja//wAE6XnaTcyeI9HQfjM5/pXJTmrqyOmSP4RvhN4OX4mfFTwv8PJT/wAh7V7DTDxnC3dxHCePo1f7MP7NLeGPhx8CfC/hqGJFVLFJWTHAM2ZMfhux9BX+P/8AsLIqfthfCeW52rGPGOiAl+gH22IA/TOK/wBVfTPiCLPQdNs1lx5VpCuPogH4V04yp0MqOx+jDeNfDyqXES5GSB79hX8Qv/BRT/ggR+1T/wAFAf2m9R/aI8U+OIdGiuYvItNPa1W5+zp5jyud5uUBLyOx4UYGB0UV/TVD8UFVgrP/AIVmav8AGjwt5ZBvl3L8rABjg9xwMcV58Kj3Rsfx6aF/waefHTcsc/xJgwB/0DIv/kyuxl/4NMPjQvJ+JUfPOBpcX4f8vlf1hab8bvDiTK5vBjr91vp6V0uo/Hvw5HE0f2zBI4+V/wD4mur65Oxn7GPY/jY1D/g0y+OP2oTWHxOWORWDxyDTolKuvIYbbzgqRkYIr+4/9jzR/Ffwv+Aeh/D/AOMLx3euaXH5M1ygAE/A3y7QW2+ZJvYJk7c4zXzJb/G/QXlLfbflB/uPwfyrqofjfoEQXFz2wPkbr7cVzyqyluaJWP0Pm8SeGJYHspYkKSqyMO21xtI+nNf5LX/BdX4aR/C3/gpB4shtECRa1ZafqRCjALCM2ch49XtST6mv9HrVvj9oyTbFuGwMH7j/APxNfwD/APBxhJYav+3zpd9ZctdeE4nPUZU6jfFTg88g8cVtg2+YyrfCf2Lf8GxPgPSfhf8A8E1fD15dBBJrCpdPxgn7SXuyf/I4H4V/R+mu6DIPupz16dq/mt/4I0+LP7G/4Jy/DN4pF2z6LYuMcdLWJcfgVxX6oQ/FCTaD5mSvvWE27mrPwc/4O0P2gtV8C/sc2fw18LTPB/wlN3badIYjj93dtLJOO3WG1aI/7MrCv852yCKPKPOzgf0r+6T/AIOpLLVfFv7NfgHx1buWtrHxRb2lx7brO5MRP1LECv4WVPlysP4QfwFengErHPiLbGu3lvIH69jST+XDCXxuHoP60Rt8uQMds1FduRGI48fN8v8An+Vd/KjjcVsf6Uf/AAau/tH6j8T/ANg9fBfi6f7S/ha4l09TISWC2r7Ix+Fu8C8f3fXNf1ENq+gLgqF6fjiv4kf+DWK01LwT+xx4x8ZXRKW+qeJbyK33dxHHao2PbKEfhX9Pb/FAA4EhAFfP1NJHpx2Pyg/4OlpLC+/4Jf8AimewHEP2ZyB6/wBoWYr/AC+TKzIUfuTX+kd/wcR+K28Sf8EufiBh8mCOzz34fUbX/Cv82iIl92PvKa68NPQ5MWtLn94f/Bm+lpBonxQu7vGyPVYf/TegP86/unPiPw4v8K8fSv4MP+DTnWYvDvwl+LGos21hq9tH/wB92cX/AMQa/rSuvicvIMv09K4a29zrjsfKX/BfW5s9d/4Jj/Ez+zAP3OjanIeOgGnziv8AJAeQRr8/HFf6p3/BV3xNJ4r/AOCdPxf0yFt7r4Y1aRV+ljNmv8puS5LncvoMCvQwclsYYiGiLBk2Y3DqPp+VTCUbJO37p/w+U1W34j3ddvb8Kro8reahGdyEKv8AvDFd9VWiZQWqP9k7/gj7d6do3/BOn4Z29+BuGl2p5/69Ya/TODxBoe/f8oGR2Ffj/wDsgXbfC79lzwL4GmbZJY6LaK65xtYQomPyUV9Dr8Tm8zHmeg6187KWp2s/iW/4PI5kH7SPwvmi/wBXLYaxtx04eyH6V/GDCSZVyOhHFf2C/wDB3nrB1n4x/Bm8Vsh9M1s+3/HxbD+lfx9WrYuI/wAM4+tehB+6Ry2P9WP/AINcTZaR/wAEv/Dkl7t/eBiPUH7Tc/pX9Hg1zQQQ/wAvHbAr+XD/AIN9/Eh8J/8ABLP4eoXAN5byPn2W6uFr9lZ/ie+wZkwR05rjluaH8+X/AAeEm21D9iDSdRtNuyLXtKXjt/x+V/m+eC/Dlx4x8X6V4Rs+JdUvILNMf3p5FjH/AKFX+hj/AMHSevf8JJ/wTfTUGOTH4p0aL6fJeGv4Ff2ary2079orwFqF3gQ2/iLSpHz02rdxE/pW9DSIj/Z4/Yi0nwz8I/2Y/CfgOziRIrOyXCqMBRyFH4KFA9hX1JN4q0EqA6KBkflX5teFPHq6Z4dsbJJABDBGnHH3VxXQH4oZ+XzP1rlA/ng/4Kw/8EIPj3/wUz/aivPjpqXjxdA0y2iNrp2m/ZI7hUTeWaXcbqL5pPlGNvyoir/CK/MWH/g0H+LRmC/8LRixwR/xLoh/7emv7G9S+N+jWtw8T3PzJwQFY4/EDFVIPjlojyBvPY88YR/04qo1JJWA/kwsP+DQH4ouoaT4or0HA0yA/wDt5Tbv/g0C+Kdp/pNp8Vgsi8j/AIlkXBHfIvR0r+xS1+NuixwqjTuC3T92/wDhVHVPjroItmX7S2QOmxv8K09vIXKj2j9jnSfEfwh/Z+0T4afFSZb7V9HQQy3WAvnkIu+XaGfb5km99uTjOM19SQa/4auVMcsa7JMg/wC6wwentX5cL8ddHQ7VumGR/cb/AAreg+O2lQWu/wC0txz9x8Y/KudO7uM/zl/+Djn4Y2vw4/4KXeIZrQAJremafe8AcmNXsyfxFsDX4KV/Rj/wcz+IbLxT+3tpeq2EgkWTwxA3o3/H5dYypwRnqOOlfzng4OBXox2Ehw+Wjr+X0pOuM047doqhgcA8V+q//BDcD/h7b8AP+xxsP/Zq/KbAOMV+rv8AwQ5+T/grZ8ASeg8Y2P8A7PQB/9X+AHAB20vbFJ1Oaco5446UAJ04p6vtXHemYGdopuMUBYuKwUYbp6Uw7Qfl6VGgUjntT+pAoSJSGGPH4UgOeKkIO3P4VGMKcHpQOJ+k3/BJkf8AGeXw644Orwfzr+wvxJ4l8jxFqEO77lzIMD2av4/f+CRqqf29vhyH5A1aD+df1IeONd8jxnrEUTdLybH/AH3xX3fC7tSZ/G/0gML7XN6a/u/qerDxQrLnftPej/hJcqWZzwPX+VeBL4jlI+YhahfxIxVlyPu/SvrFUXKfhaynyPwb/wCC51+k/wC2pfrnj+z9P/D/AEda/Fzyy569BX69/wDBbli/7al2x/i0vTjx/wBeyV+REMQYc1+T5i7YiZ/oJ4c01DI8Mv7qLlsjb1VeTXpem+D/ABVqHhu68Yafpt1c6VYPFFd3kcLtBBJPnyllkA2o0mxtgbG7acdK4ezt1J3FTtX0r/QA/wCCYvwH0b9iz9hDw94F8Xaba3GtfEe3/wCEi8TWl9BHLHLFeJttLK4jddrJHb7cqw+V3fivNnVsj672UZ6s/gTlu3sW+0wsY5F5QrlSD2wRjkV9M/Cv/gpD+3R8EEFn8Nfihr9japt2Wsl01zbgL0AhuPMjA/4DX9QX7Uv/AARZ/Yf+PmoXXiz4I6tefB/WLol2sUh/tLQyx/uR7lnt19lcoo6IOlfkn4q/4N2/2zLS6c/DnxJ4N8WW2fke31X7JKfrFcxpj8+KXPFm1OnynXfAP/g4x/bR8F3sUHxf0zRvHFkmN5eH+zrsgdds1sRHnv8ANCRX9dH7HX7bnw//AGz/AIBWXx3+GyzWtq1w1hfWVzt8+yvYgGeFivDrtZWRx95SOnQfx9+A/wDg3r/biublE8b3Phbw1b7sPcXesRzbQO4jtw7t7ACv6Sv2Qv2fvAH7CX7Otj+z14D1dvEN095Lqus6x5Zgjur6ZETbDETlYoo41Rc8nGT1wFLltoWr3P1An8fEDLOccfjX4F/8HFXhzT/H/wDwT/0H4jTgNfeFPF1lHFKQN3k3sF1FIo9mMcXH+wK/S6fxmRxv69q/GH/gvx8V7bw/+wh4L+F8sw+3+NPFpv44Tw32PSLeUPJj0Mt3GPw9qxpN8xTPHf8Ag2J+N9toHib4q/Ay7lVJ9SsbPxFYxk/eNg7W90F9T5c0bfRTxX9ca/EFim5JOv8AhX+Zb+xJ+0n4i/Y//aM8JfH/AMPxNcvod0PtdoDtF3p8ymG7tz/10hZlHo2D2r/QRtPH/hXxF4W0j4ifDm/TVfCviWzTUtHvo+VmtZRkAjnbJGQUkQ8qykHpVV42ZnTmnofV2oeN9M1W0udD8QBbiwvo/IuEflTG/DAjuMZB9q/zZv29f2S/F/7Fn7T/AIh+COuwSf2dFcNd6DdMvyXmlTtutpEYcFlX5JAPuupHpX930njoyyMY3wT/AC9K8S/aC+C/7P37YXgGL4WftJaK2rWFmxk07ULVxBqemSN1a1m5+U4GY3BRsDK0qFblZo0mrH8AlsueBxjgjpXSwHoqgHpkV/Sb4v8A+DfDwpdX7z/B344WMNj/AAW/iPTJIblAegMlu7I5AGMhF+leofAn/ghZ+zh8O9ei8RftJ/ESb4gpasG/sPQbRtPs5iP4bi8kdpTH6iNY2I6MK9KWNhynG6Mrn5tf8E8v+CTXiz9u/wCHXiv4pa7r7+CvDmlgWOjag9r9oW/1YkFoxGSha1hQYmkjYlWZQA3zCvk79pj/AIJ8/tQ/sbai8fxp8PumjmTyrbXdPzd6Rc9gVukUCJj/AM85ljf/AGa/uT03xP4e0HwzYeCvA2nWug6Fo8C22naZYIIra0gTokaDj6nqTknkmp7X4gw21pcaTqCRXFldx+Vc2s6LLbzR91lhkBR1PcEYri+uST0N1SVrH+cndSSxS+S457DoDX9C/wDwbaSG3/a78e368GDweXJ9P9KUV5n/AMFxf2b/ANkD4B6h4L8V/BXSx4W8Y+NJLi+vfD9jJ/xLo9Mi+SO8Fu4LWz3E2ViRHEZRGIjHGe7/AODcx47X4+fFTUVOPJ8DF/pi9iFdFWrzUyadPlkf2Ry+P2twA0mOgq9B4wl1hTpobd5qNx67Rn+lfENz45b7of8AOuz+FfjMX3jix0+RifMWYfXETf4V5SVjc/znvGC58X6u3Qm/uyD9Z3rlmkcPs6+9a/iufd4p1Igjm9uhn/ts9cz8ychuP0r6Kk3ZHBUfvWNPEks0Ss23BH4V/oRf8Ef9dfw7/wAEzvhPFv8A9bptywx/1+T/AONf57dr+8uYhjILCv7xP+CdGtHQ/wDgmf8ABIlsGXR7r9L2UVxY/ZGuHR+uT/EEjjeQK/Fz/gvprL+Iv+CbGpyg7li8U6EM/wDbSavsabx6c7lfpX59f8FhtQOu/wDBKvxTdOcmPxh4eA59WlP9a86k/fR1H8bfg/xPqXgbWtM8a6S2270a8t9Qtu37y1lSVP1UV/pp+E/jZofxJ8GaL8RfCkwl0vxFYW2q2bA8GC8jWZR/wHftPuK/y+LpZjGWH3V7V/WV/wAELP2v7f4qfAu4/ZL8TXYPij4fLNeaJGzfPe6HK5llijyeXspWJ2jnynGOENejjad0mjmpS1sf0p/8Jo2C+/iv5sv+C/fwb+J50jw7+2P8INV1SzsbJV0XxPDp93cQrCC2bS8dYmC7SSYXfGM+WK/Zi88arEPLDe+KIPFmmXtneaLr1tb6lp2oQta3lldxrNb3MEgw8M0bgqyMDgjFedSdnqdDWh/nxy/Gr42Qfd8Za8P+4pd4x/38rBk+PXxzkkKHxtr+M4H/ABNbv/47X9SH7Tf/AAQ7/Zu+JWpXHir9mfxk3w4nuDvOg6vA99paMe1tdIfOij9FkEmOxAAFfAcf/Bvr+0wdQKn4jeAxbL1mF7P0/wCuflZ/CvR9vSRkoyR+Q+k/Gr42Nk/8Jnr7HgjGqXf/AMd/wr0+38aftR3vge7+JFlrPi2bw7p11FZXWqJe35soLmcFooZJw/lrI4UlV3A8cV/Qd+z9/wAEHv2fvBd5Brn7SfxFuPGzQ4c6L4btjYWshH8M19MWkKcciJUbHRhX7i2Fl8GtF+FLfs9af4S0yD4cvaSadL4agj2WL2k3+sUj7zSsfm89iZd4DbtwrOpXgkuVAoPqz/PO1r44fG5pgo8Z+INox/zFLz+sn9K4t/EXiLxFqQ1fxTf3Wp3JAQy3c0k8mwdF3yMx2j0r9Kf+Cm//AATo8QfsUfEC38S+C5JtZ+GHieVzoWqOMvbyABjpt5t6XEK9GOBMg3jowH5eopTjoB1ruo8r95GEk9j+/f8A4In/ABstfFv/AATb8FWMEymbw1dXuhXAU/da3neSIEe8EsZFfq9B47KoMyH0r+Mj/g38/aatfDHxX8TfsjeJLpba18fqmo6E0rYT+27NG/0cds3UHyr6vEqjlq/pzv8AxhPZloJWKsh2sncY4rycRTtM6oO6J/2/vgjb/tr/ALI/jD9ne2eNNY1K1S60SSTgLq1i3nWoJ/hWQgxMegVq/wA33WdB8ReE/El94U8V2M2n6tps72t7aXCFJYLiI7ZI3UgYKsMfyr/RZk8eknfHIfwOPp+VfHf7VH7B37H/AO3DqA8YfGCyvPDfjHy1jPijQDGLidEGFF9bSKYrgqBjf8smABvxxTwuI5RVIXP4a5LlUGevQZrX8HeHfEfj/wAa6X4I8H2E2qapq93FaWVpAhaW4nmYLHGgA5LNgeg78Cv6U2/4N/fg8dVMo+Psw04n7h8On7SV/wDAkJn3r9I/2Vf2Iv2RP2EblvFPwQsrzxD4zljaF/FeveW11Ejja6WVvGFitg68FgDIR8pcrxXZUxytZGMKDW5+h37E3wksf2LP2UvB37OUUsb3+hWm/VZIz8kmpXLtPdFT3VZZGVT3UCvpeT4kgkHzf0/CvhV/iLJJh5pCT6k8/U05PH0mNrSda8xz5tTqPGP+C0niI+I/+CXvxXjDbvIg0s/+VCCv8+2KPY/zevav7rv+Cm2uf23/AMEwPjXk7ikGjDH+9qMNfwryuN2NvfjvXbhOxx4z4T+vj/g2c+IUOkeAfjN4Y3ATW9zo1+Fz/BIkkBP4FRX9MyfESSXlZD1x/n+Vfwhf8EI/2gLb4X/tvn4U67ci30/4n6PNoEbOdqDUF/f2HOcDfLGYl95AK/r4tPFlzbE290DHJExR0PZl4IP0rmr07SOmk/dR9QeNJdF+Jfg3Vvhn4qO7TPEVnPpt1ntDdQtA5/APX+Xp+0D8D/Hn7NHxu8SfAj4kWzWuseF7+SxlUrgSKh/dTJ6xzR7ZIyOqMCK/0Zrvx3tUOr8Yxjpken0r42/a3/ZQ/ZG/bw06yt/2j9IvLTxBp0IttP8AFGiPHFqcNup+SCdZFaK5hT+ESLuXPyFeadCryFNdD+CS2kWeMgcnpX6Bf8Ex/wBjXX/2zP2w/DPgIWz/APCNaPcRa34lutp8q20uzcSOHboGuCBBEvUs3HQ1+73gz/ggP+wxp+uJf678XfFt/pyNk2dvplrbTuo/h89jKq5x1EdfsL8MfBf7PP7KfwwPwd/ZY8Kr4W0CV1mvZnfz7/UZ0G1Z725b5pGAyFXhEHCqo4rprYzmVkRCnY/RBPiWrxKIP3aKMKq8BV7AfQVDL8RPnLM/U18R2XjsEAO/OKml8biMfvJOD0rzmjQ/n4/4OoL7+0vF/wACbw/8tdG1p/zuoB/Sv5P4QwkVz6jj26V/UT/wcr3razJ+z5elsq+g6zj8L2Kv5fvKbcFXg8V2wl7uhLkf6Qv/AARv8SDR/wDglh8HWVgPPstQJ7fcv5lr9GG8f44L4xX4l/8ABMTxU2j/APBMD4HwhsbrHWB1x01ObivtIePZG4Z+2PpXHKVnYo+Hf+DiXXDrf/BL+6mz9zxpoyn8ILqv4JNHnu7HUodRsDtmtXWWM+jIdy/qK/uP/wCC4WqLrH/BKnUJHIOPHejL/wCStya/hyhxBN06GurDv3Sbn+ph8BfjfZ/F34AeBfi/pEoa18UaFaaiu3+GR0xMn1SQMpHqK9Hbx0Ac+Z1r+Yb/AIILftm23jj4L6r+xF4ivETxF4Ylm1vwrHI2Gu7CXMl/ZR88yQP/AKQidSjvjhK/aM+O3PG/7xzXLUhyso/HX/g4S/Z4+LviLwxov7a3wN1LU4otBgXSPFlpp9xMnlwB82WoeXGwGwbmhmbHy/u88ZI/knT4z/GRsD/hK9ZIGP8Al/uf/jlf6O2lfEiOB5IJhFcQTRtBLBOokgmikG14ZY2+V43BwVPGK/Gr9qD/AIIa/sd/HHWbjxt+zz4ok+Emq3B8yXSLm3a/0TzD1+zyRkTWyf7J3qOiqoGK2o1FazA/k6T46/GGPaf+Er1jAH/P/c//AByqV78dvjLKCi+LNaGf+ohc/wDxyv3Qm/4Nz/2gDeskHxV8Avaj/lsLu4ViB/0zMIP4V9X/AAG/4N/v2ZPAmqQ65+1B8TLnxt5BDnRPC9sbKCXH8Mt/MWYJ6+WiNjowrXniZ8h/NnoOo/tceIvh9qvxc0O+8VXfhbQbm2s9R1aK4vGs7We7z5EUsytsRpNp2gnn8qxLj45fGeCDb/wlmtHj/oI3X/xyv9HLwI3wE8EfC4fs++E/BOlWXw5ktZtOuPC8cYFlcWlyMTRzE5eSWTAY3DsZN6q27IFfxWf8FaP+CYOtfsN+O4/iD8KmuNf+D/iadv7F1RxulsJyNzaXqG37lxD0RzgTxjevIYKU6kWU4n5B694n13xPd/2n4ivJ7+527PNuJXlfA6Dc5JwOw7Vz1BUqdppwU4zWxVg9qXgdelJ257UuEJwKAEGMV+rn/BDfB/4K2/AH/scbD/2avyk9MV+rn/BDTA/4K3fs/lv+hysOP++qT2HFH//W/gBON1GaTrTgBQAcUDk0vtRjB4+lADkIPFLuANMGKccUAWPkbn19qjkhcYwpx24rrPA9hban4q0+xulDxyzRqw9QWAIr+wT4vfBz9jv4aeIF8KWPwf0C5WGys5RK5mVmMsCOSQr46ntXo4HLpV/hex8Dxfx1SyedOnOm5c3a3Q/Ev/gi/wDCfxN4n/bC0H4gRwPHpHhVm1S+u2GIoooFJGW6ctgAV+5PifxWmpa9e6khG24nkkHsGbIrze0+KVpovhp/h58NdD07whoE7B5rTSovL89h082Q5d8ehPHpWDcai7fMO2K+2yvCexpctz+Z+NM5lm2O+tyjyq1kvI9ETxAM4JH0qjd+ICkTMMHC5HvivNnvZQ3H+fwqGa/k27s8Yx+FepzaaHy8cCj4D/4LY/DHxJefGTw/8ctMt3n0LxJotn5VwikoJbeJY5EJ/vKR0r8WrXTJ2jDBD054/lX9cvhv4tXVn4Yl+HfivTbHxJ4dlff/AGdqkPnQq5/ijzyh+hr2X4TfD39kPxx420nwje/B7w9EmpXMcDunnHaHPJCl8V8jjck56jnFn7Dw/wCK39nYGGDrUr8ul1bY/lv/AGGvDfwY1/8Aa4+Hmi/tE6vb6H4JbWrV9Yu7vIhW3iPmGOUqDtWUqIi/RA244Ar+7T486r4tvNem8fMiXGi6oxksL+xkS4sXt/ux+VNCWjKgDscenFfwKftgaVpXhP8AaT8Z+HPDlulpZ2msXkcMMY2pGizMqqoHAAAwPSuu/Zm/4KEftb/siSfZ/gj4yvLDS2bdNo9ztvNLm9fMs5w0XPdlCt718dXoWlY/ovK8T7ajGta11c/s7i8Xyqm5H49jW3o/ip3ffJg/UV+C/wAP/wDgvH4A8RLHbftLfB61e5wPM1PwffPprt6k2dwJYc/R1H0r7W8Hf8FXf+CXmuWwl1DVPHWgSMuTDPp1td4/4FCeR2rn5H2PRP0+TxqY8DhSO+BXF6x40AnMmcDvzxXxRqH/AAVN/wCCVWmIJo/E/jXU2Az5UGkRwkn0zKQK+S/i1/wXW/Zl8Hs8f7Ovwfute1Af6q+8ZX48hCOjfYrT7/0MqU3DsB+ythruj2Hha/8Aix8UtUh8L+BtDTzdU1u9+SCNB/yyhB5mmf7scaAszHAFfx6/8FK/20b79un9pKT4gaZbyab4S0O2TSfDWmyEbrfTYCSskgHHnXDlppccAsEHyqK8t/az/bw/ad/ba1+31T46eIWu9P09idO0ezjW00qxz/z72kWEBxwZG3SEfeY18rGGYxLJnk/5Fb0qdjnrVEtDUjhZG2Idv49vSv2S/wCCZP8AwVQP7I8cvwA+PiXOsfCfV7kzZt/nvNBu5eHvbFScOj8faLfgPjemHHzfjLE23aX429fes7UoBsJPVjwBx/npXTUgpROPDS5ZWP7/ACXVNP1nwhZ/FH4ZaraeKvBup82Wt6W/nWrj+5JgboJl6PFKFZD1FVdM8SNN+9zn0r+Ib9mj9sL9pP8AY98Tv4j+AXii60MXGPtlmMTWN4o/hurSUNDKMDHzLkD7pFfur8Kv+C7fw11ywt4f2lfg/bm9YDzdS8HXr2DMe7GyuBJHnvhXA9K894drY9S6P2/m8XzpFvJODXPP40nkJTd8x4/KvgVv+Cs//BMLVrZXuNQ8d6M2OYpNPtrjaf8AeR8Vx2uf8Fdv+CZvhW2N1o+neO/GFx2i8m10+E+m5zJuA+gqJUpBc/Tqz8UXGEjDbZHIVFUZLE9gB1P0rj/2kv2jvhh+xN8P4/ix+0cd+o3MRl8P+D1fZqOsSjhGlUfNa2QbHmTOAcfKgLcV+H/xM/4L3/EZNOuNF/ZI+H+i/DXzVMY1WcnWdYAIxlJrhFgiPp+7bHY1+H/xJ+JPxD+L/jC9+IXxN1i813W9RffdX19M09xK3+07EnA7DgAcAYraGGbMpVoo6j9oz9oT4nftV/GvWvjt8YLz7XretzB2CDbDbwxgJBbW6dI4IIwEiQdAPWv3H/4N9buLT/iV8Yrs8+X4Bkx/4HQ1/O6sTKQrgHP8q/TH/gmr+3b4I/Ya8c+L/EHxA8K3nizTvFfh86I9tY3kdlJHm4Sbf5jpJxhCMAZ713VaPuWRlTqPm12P6oJPFwdGfpj869E+AvieW8+MujWWc7zP7f8ALB6/EyL/AILYfsaeXz8FPERA/wCpmi/pbitHwx/wXZ/ZM8A+Krfxf4Y+C2vx31puMTSeIoZU+dSjZQwY6MR7V5vsX2Oq6P5u/EEhbxVqyn/n+us4/wCu71m+VsYBelVb2+Op6nc6rt8sXVxLMV6481y2M+2cVJt3DeOMcYHtXtU5Wijz6kveNeFoo5oiOuR+Qr+0z9k3xmmi/wDBNv4B2+doOhXh9/8Aj+l/xr+Jt5SrK7dumK/df4Af8Fif2fvhX+zF4A+APxO+F2sa3feBrCWyF9aaxFaxzCWd5iwjMLMB8wHJPSufGwclodGHR+4afEIySjB/IV4l/wAFONYbUf8AgkZ4ynI5HjTw4P8A0bXwBp//AAWp/Yvkny3wW8Rt348RQ9Pxt68z/bX/AOCtHwO/aX/Y81P9lv4RfDbVvCrarrenatNe6hqkN7GPsO/5NqxI3zBgBg4GOnpwUaDU0bSkkj8Nrg+YowOM4NdP8L/id49+BXxI0f4xfCzU5dH8Q+HrpLvT7yA4aKVPUdGRhlXUjDKSpGK4pSjSZXtxinSFdmCuK9mSueW5Wkf2m/si/t4/Cj/goRokS+HXtvDHxViizqvhR5BHFeuPvXWiu5/eq+Nz2ufNjPTcuDX0peX9/pMrWGpRvb3C8OkilGGPYjiv4GrEXumX0Ws6bO9vcWzrLFLE5SSN15DIykMrDHBBBFfsZ8E/+C3n7U/wy0i38K/HOz074taLbqFVfEIePUkQcAJqUOJT7GZZTXnVcG1qj0IVVsz+jm98cTRjaHOD61mjxxIJN27rj0r8tfCX/BZH/gn54xjWbx34K8a+Dblhl1026tNVtl9dpk8mTHplK9St/wDgpz/wSu8oXM3iXx4cc+WNHg3cds+Ztrj9jI1uj79X4gXSS8N/kflXb+CtQ8T+P9aTw34Ws59Sv5iFWCBSzc4644VfUngV+Ovj3/gsj/wT58HQmb4c+AfGfja6X7i6ve22k2hPbd5HnSbfbaK/Nn9oP/gtZ+1n8ctDuvhj8NhY/CrwheAxTab4WRoZ7hDwVub9ybiQEcMFMat3WqjQlcTfY/Wj/gr3+3f8Nfh/8F9Z/YT8CXGn+MvE2vPEPFF2oS7sNDW3cOlvaPyr6huA3zJxCuUBLMcfypSPHIwEOQBjg+wqwGZhlsqD1Ofz/Oqb28Y5Ir2KFPkVmckp8zN/SNf1Xw3qlp4g0O5lsL2wmjubW4gYpLDPEweORGGNrKwBUjoRX9iv7FX/AAUb8Hf8FBfCdn4Q8VXNvo3xw0+ERXmnuVht/Eixrj7XYFsKLwgZmtupOWjyOB/GZkbMfLjpmsSaTUNKv4dW0uV4Lm3kWSGWJikiOnKMjLgqVIyCMEVOLpKSsVSqWep/ey+t39pfPYXqvBPA2ySKRdroR1BU8ito+JZoYxFnGRx2r+bX9nT/AILgfHXwhp1p4Q/an8P2Hxa0m1URx31/I9jrsUY4AGowhvOx2+0RyHj72K/RrQf+CwH/AATX8T2iy+ItL8e+FJzwYljs9RhU+iyK6MR6fKK8n2DXQ6VNH6SL4ou2yVfOO1WU1fUNUnTSdMikuru4bZHBCpkkdj0CqvNfmzq3/BW3/gmR4di87Srbx94ol6rB5FrYRsfRpHkyo46hTXwl+0Z/wW/+LHi/w7e/D79lLwxafCbRr6Iwz39nM19rs8Z42tqDqggDDr5CK3+3Thh5SdhTqxjuf0FXOs+Erfwz4pit9XS+8ReD9W07S9VtbV1kt7Ke+hmm+zSSDh7iJIlMoQ7ULbTlgQOATx8zcI2M4xiv5u/2Gv8Ago/8PP2SPhJ4t+EvxS8Fah4uh8T69a659otNRWydHtbeSAK5eOUuSZGYkEZJ5r69tv8AgtZ+yYjhj8GNeYA/9DFGP/bWlUwsk9Bxkmro/TL9uLW21L/gmV8cE4OINDx/4MY/8K/i6u8RfKwya/eb9p3/AIK7/BL40fsseMf2d/hj8MdT8OXHjJbNXv7zWY7xIxZ3KTr+68hCc7SvDDrk9MV+CN187fJ2x7dq68PT5VqcuIlfRFWx1fVvDuvWXiTQLiWz1HT547m1uITteGaFg6Oh7MjAEHsQK/u9/Yz/AGxfC3/BQ34Hp8R/DLw2/wAUdCtUXxl4dj4llaMbf7WsY+skE+MyqoJifIPG0n+D3ClS5A+Xua7j4efFr4ifBjxvp3xH+FGs3mg69pMgmtNQsJWhnhcd1ZccHowPDDgjFXUo3Q6VRrQ/vAv/ABQ6Zw+QDg+ox7VzD+Jd8gyxPoa/Dv4X/wDBfB9fgh079sP4bWXim8UBJPEHh+b+yNRl/wBueDDW0r46kCP6V9haJ/wVn/4Jfapai51I/EDSJCoJgazs7jHsHVhnpXBKizsuforZeIriKRQmf5V1d1rsCeFdT8d+KdTtdA8M6DCbjVdbv28uysol/vN1klY/LHDGDI7YVRk1+P8A8Qf+C0v7DPgmAv8ACP4e+JvG18g/dHxDeQ6bZBuxeO28yRx/s4GfWvxM/ba/4KOftG/tuyWml/ES+t9L8L6W2/TfDmjR/ZNKtCf4xEDmWXHHmylmHIGBxTjQZLkj+xDxF448JC08NeIvAk882keI9CsNZtJLlQkzxXqeYjPGPuFkwSnO3pk4qunjPzovvdfyr8KfAv8AwWp/Zq0z4YeCvB/j/wCEut6nqvhPw3pnh9rm212O2glGnQLCHWMWzbQ23PJJGcV6dpf/AAXB/Y6VPm+COvN9fEqf/I1T7JjMv/g4Xl+2eE/2dLxgDnQdb/8AS5K/meyo2uf1r9a/+Cov/BRLwF+3dZfDvS/h14NuvB1h4Dsr6yWG7v0v2mF5Mk2d6xRFdu0jnOcjB4r8isHAWtoOysZS3P7a/wBhbxL/AGR/wTO+A+0gbrPXB+WpyV9EWnjR5J8I/wBBX8/n7MX/AAV8+AnwY/Za8D/s7/E34Y6t4gvfBkV7El/Z6ylnHKLy6kuf9V9nYjaGC8senbpXvWlf8FtP2OkuN0nwZ8Q/+FHH/W3FYzoO90bH23/wV31ZtX/4JR6qzHOzx7o4x/26XFfxf3P7qY9jX76ft6/8FZfgd+0/+yHcfs0fCr4fap4Xe616y1uS8v8AVIr5c2scsZj2rEjDcHHfA29OeP5/WcvIT19K6KcbKwjtfAvxM8c/CnxzpHxI+G+qXGi69oVzHeWF9atslgniOUZD7dx0I4II4r+zf9ij/goR8Mv+Chfh230mKSz8LfGaGPGoeHXZYLTXHUfNd6OzkATP96SzJ3Kc+VuXp/El5RPNWtOu7nSb6LULGR4p4GDxuhKujLyrKy4IIPQjpVTppkqyR/oMyapfaXdNpurRSW11C22SGZTG6MOxVhkflVefxfJHmNWI/Hj+VfzR/s+f8Fzf2k/h9olp4I/aB03Tfi5oloojibX/ADItWhjUYCxapARMwA4HnCXH0r7/APDX/BZf/gnl4piE/jfwh448HzYGUsLqz1SAHjO0yiB8emVrm9i9i0fqcnjKbzMeZ1GP88VWk8WXM0n7xjX59J/wVO/4JWIokbxD4+6fc/si0z9M+diuC8Wf8Fnv+CePhGJ5PA3gbxr41nUZVdSvLTSbdj2BMPnyY+iVHsmB+uXhPXtZ8Q6lHoGhW8t9fSkLHBApd2/AdB7ngV+ff/BVr/goJ8Mf2Z/gL4t/Y/sp7Dxp8RPG9qNO1jTTsvNN8P2uQ2646xvqQ6wovzW7fOxBCqfx2/aL/wCC5n7VHxT8O3fw9+A1jpvwd8NXimKeHw0H/tGeNhgrPqcv7/BHB8nyQe4Ir8V7i4lupXuLhi8jnczMckk9SSepNbU6FtQsRSFGkJQYHYU3ikAzTwMV0gIR+lKOtJSjANACcCv1d/4IZAH/AIK4fs/Kf+hysP8A2avyixnpX6tf8ENzj/grf+z8f+pysP8A2akwR//X/gB4zzRxmjqaUAUALj9KaPanDnikA7dKADpTQO1LRjFAHefDb/kedKBHBuYhz/vrX9kn7ScK3PxPdSM407Tv/SWOv40vAN9a6b4v02+vnEcMNxE7MegCsCfyAr+vjxV+1t+wB8R/ES+KLv4mtZO1rawmJdOncAwRLEeSB1256e1fT8P14wvzOx/P3jPga9StQnRpuSSey9DwvUIRp8gZRwccdKsiZ5oAwFafib45/wDBPt3ynxXk/wDBZLWfYfHP/gn+qfP8WJgBwMaXLX0yxtKL3R+RRyvGOCfsZf8AgLI3yvzYPHpVFmI+Qr06VvP8bf8Agn0V5+LEw6f8wuWoG+Nv/BPrr/wteYY/6hctL6/Rt8SGssxn/PmX/gLM20/4+B8oH1NfUv7Ngkb43eFlxgHUIf5181QfHH/gn2JA3/C2Zv8AwVzV7L8M/wBq3/gnv4B8Z6Z40b4pSXJ0y4Sfyjpkw37McZHTj2P0rOeOotfEjkx2T42UbKhL/wABZ/Mr+3Qnl/tW+O1P/Qavf/RzV8lh1Wvov9rTxv4e+Iv7Rfi/xn4Tn+06dqOqXU9tKAV3xSSsytg8jI7HpXzqoAG0ivzvEfGz+zMgpyjgaUZLXlX5C+WjDIGKkSNFPFRbeOOBUoB2DPFc+qPWaZKd44BqJolbBxTjncMcU/K0Q2M27Eg+RdyitW0kGMn+GsVyQAKs29x/A/FaQfcxnC6NQzJtIPHpVWdZHYY7UjjevynBpHkZFz1re+hnCNtiZIUkQNxzj2qaWNCVBGCPSoICJUzH2/SrA3AfN0qZPQUm7kMiRSY3DAGBR/Z0LgsFBWpJPIcYAx0xTQ+3pQNT6FiCPyhxgYHT2qz5mRxUCXGcIcKM4/CpG8rG1OK0i7aIzejuOEvzhmHAFTRhXPzc+lUim1uGOG6VZgdoMr2roU0auorF5BBkbtuM9OPSopbOE4cgc+3YdKhknj/jGD/jQGEp2ofx+lS4oz5eo5GIUBhgYqwJdpyBS7Cqbz0Pp61W3+S+/Gd3Aq0tDZFljGkZ3d8ZrHNqk2Gxx0HFX2foHz9PaocxeYFVtuOpxUpCSZetLGGIDYo6elWXCBwoGPUDijeYIhySMf5/Ss+eZt6s3PSlyJGDve7NW2Zox5mOAeKaZ2eUttPPamW8jldxAx0/EUSCYfMcDjPNVcpyjzEqzH+BcY6D/wCvVLUJvPAjOSPT/wDXVgTNGd3HQVUnnbzCWwO9W2rWNOZaFRbO3yCAgP0zWuttFGuCBj2WoIw+/wDDv0rRLHZwg/HpislUj2M5TSMe6sEEYLANVKC1W3fPX07VrXkof5QMADtVPdg7Rjgfp7VO3QIVGjVDGWLKDpjr/hTZULqDJwQPTtVK2dC3luTVlkgx354//VWnMTKcip5qodgOMimFsn2zUUyqpyBwMYojZ+jY59hipnBXNXBPUtw2Sn73Oen5YqpNaImW28dx07VdjcrHjcMjv7e1NkZWwWPPt0xUyVjmTaMlYI4hkLk/StSCXyvlHTH9KgwVc7sc8elQkhOrU4yijoTUiS9xOu4KD26dqyEsYvM3Bc+2KvNPIMqcAVA53sGHtWcqnkOOmiLvyKM4Ax7VVlmTdhTnIxUTKR64NRnBAzWMpNvYi2oLknnvSuxBJNICxGTxUE+PLwOrVSlbcuxSuId8m/HTFKkJCnHAPp0qIyt3qRG3rsPGKyqM6W3YttbkoMnJb+lUSBtCH0rQ81CmF+9gVjncr7cVLa6EUyx5UZHApIcRyZAGKRulVsEHiogaxjdWLUknduAahDED5qase75venFYgeKbSL5bIdsU9Rk1EVRTimGRuaYx3de1WOzRIXZxs61Hgde1IeDxSgc80CXZEgO3p+FNb2pGPaog+Bmg0SH7sYH+cVG33qQMKXK4560DSA8Dmm5Y0Eg+1Jj0oGL04/Ck68UYFKMZoAUAUgAxScU8HmgAC9qbjPSl4NLxQA3gGv1X/wCCHILf8FbvgAo6/wDCY2H/ALNX5UYJIr9XP+CGg/424fs/D/qcbD/2agaP/9D+AHo2KUUbTnFL9OKAAABvakxk8UduKXpxQAgwDSe1Lx2oAxQBKpXpVlLuWM/Kx6VSA4p+0jHFAnFPclkuHkOWY1H58g6MRXq/wQ+BnxN/aJ+Idp8KfhHp39q67fJLJDbeZHDuSCMyyHfKyINqKTye3FfaL/8ABID/AIKExkqfAfT/AKiOn/8AyRScu4uVbH5s+bKf4zUnmuRjca++vEv/AASz/b68H6ZNq+r/AA01O4t4F3MdPe3v3AHfyrSWWTH0Wvgm8sbzS7mSyvomimhYo6OpVlZTgqQeQR0x2oTDlXYh3Pjg1OtzMnfiqwxjFGT0FOxLh5Dmbcc4o3cDjpSY7UlArlkhT06Uu35c9KgO4LtPanq6hQOlS0DHoCgOKeuc470wEk0EswyvHtU2JJ943YxzTzt9Pyr9hv2F/wDgk/qP7aHwIvfjZaeNYfD6WV7d2X2OSxNwWNrFHIWDiaMfMHxjbxivx7uwIJ2hweDjt/SnHyM3HsMO4Hj9KlVxIwDGo2Ixk0bWwD0p6kdDUTFunyDP/wBap4Jt+QBhRWTvKx4f8KRLhgdorbm0MnSuX9Swi7o/l6VFAjGDczY71+tX7E3/AASO+NH7ZngKH4pXmpx+FPDNzK8NlM9u11dXpjJR3hgDRqIlcFN7yDLAhVOCQv8AwUC/4JZ+Iv2Afh/4f8c6t4ti16z8RX0thb2zWTWlwDDF5rSf6yWNkAwDhsgkcVmqkW7GiptQPyZLbTxinjEhPbuKzJbj96R6YxU1ozSTbS1bproT7LqbaREvtz0/KpRL5aeYyinR5kwAMf1qDUy0WWHUf0olA43rKwx7iKST5h2pFwjgLg1zwu/NbHQ9K14IiOe2ODS9odLhyqx0SxiSIAjkcflUFwHjOOnPbgVv+HtF1rWmNto8Etwy8kQoWI/ACodW0u/0y5e1voGt5UxuSRdpH1H/ANat6Ssrs44YqKnyXMEgsBtHNQrMyHefyqUl4/kKj8KoSzRhiWFN1TtjNM0BcsDktxxjFSPhmDRj06/59qygCwG0Af1r7V/Y1/Zgj/al+IV14Bk1M6SLaye781YvO3FHRdu0suM7s5zxjpW1Jc7UYo4szzKlhKLrVtIo+PFlSImMk+2OPb0q+hllBBH0/KvY/wBp/wCCMP7Pfxau/htFqB1FbeKCbzniER/fRh9u3c3TOOv5V4lEMQ5U+nX/AD7Un7rtJbDwuMp1qca9PZ7BMSr7sfLt6fTiqQkfOdhz0/KrUkkmwe1UI533bUHLGspVNTqVQ04D5f7wE9e/0q19oKrv7f41Dgwx7n4yP1rMknbtxRGa7GSlHqaEqecBIF/Cs+YYySMYParkXmKgTnpmke32den0/wAKp1EjR1exTXjlgFA/z2q7bjK4BPc8VhzTpn94c9uPT9Ks2twjShARisfbPoXO/KbV3GgjBVevrWWLmOLhjjPpX1D+zz+zl49/aQ8Xr4L8ERpvWIy3E82RFBCuAWfA9wAAOT0r7n+I3/BJ678H+EbzxAfGEPm2Vu88hmtnSALGu4ksGZlXA67K3pYStOHtEtD5bF8W4HD4hYWtU959D8d4LtDKIm6npWx5DMA0ftyRivoj9k/9kPx1+034nu7bR5l0/StM2/a7+QFlUtnaiKv3nYKSBwMDkivuv4+/8E19N+C3ws1H4jx+Llmi06JZJIprRkLlyERVKu4BYkYziqp4Cq6ftLaCzHivBUMSsG5+++h+P16JAxjJzXPTTlDt6HrXSaku1zt7dfpX60f8E2/+CXXgz9tj4UeIfi1438VXmkQ6Vqn9kwWWmxxPL5ggSYzzNLkBCHARAo3bW+YYxXBKaSPqcHTTVz8eLR97YPPP0rUZAvyp24/KvS/2g/g/L+zt8ffFnwPn1BNWbwzqUtgLyNdglEZGGKZbY2OGXJ2sCM8V5jI7IpI6VElzCrq0kkZ0kuHx0x6VIAuKy1uy8+wdz+VaEsynv09K0jZIuSa0EZ9mCaoTSOxA7CpHx/F+FQGsnV7FRQwx4YbhninBmH3aXLudw6UzcRlajmbNNS0zKqhgORVSeZGbgfSqck7E47VJbKHLDrRyLc0VOyuPyT0oHFAwh2mmnGCKpDXkSh6rufm4GajyMkU8e1Fi2rEeakBULyKftUcEYpHUrgYx9KZUthHZQOOlVmz+FPbpgVG3XigIoflc5pAfypAj0YP3aCrDhtzxTfl6AUqhvSm/d5FACds0YOK+gP2XfgZeftLfHzwv8CNPv00u48TXgs47qSMypESjMGKArkfLjGRX0L+39+wdrH7B/inw74T1rxBD4gfxBYy3qvDbtbiMRSmLaQzNknGeMY6UCPz6+lOAGaQDcacQcc0DF4HX6UYWkwR0oxzzQAD3pvFKORRxQAcDpX6u/wDBDIbv+Cuf7PwPT/hMbD/2avyh6nFfq/8A8EMzs/4K3/s/sf4fGNj/AOzUnsNH/9H+AM/e4puc8UpHNKFHrQA0ccUUdaXrQAADpRjtR14pQoxQAvbFIcYpdopNoAzQB+yf/BBbSxrf/BSrwdp7jd5lhrXGPTTLg/0r9bP+CwX7e/7R37Cv7Qmh/C/4U2+kf2fqWhpqMn9oWZnl843VxCdrCRMLtiXAx1zX5o/8G4unnUv+Csvw+seMPZ62D/4Kbs/0r92/+Dgf/gkR+3P+2L+014M+JP7K/ggeKNFsfCyWV3PHfWVr5d19uupvL8u6nic/u5EOVBXnrmosriPyc/Y7/wCC6fxV1T40aL4M/aN0LSLjQNau4LKW/wBLhktbmy89hGs20ySRyRoSC6bVO3OGzgV9Ff8ABx5+xb4W8EeGvC/7Weiaemn61far/YGtyRLtF7vhea1nfGAZYxBJGz9XUpn7orE/YB/4NkP24dd/aE8N+Kv2vNOsfAngvRb+C+vka/tr2/vVt5BJ9lt4rR5VQybdjSSMoRSSAxAFfZP/AAdo/tS/DOHQfA/7EnhC7hu/EVvqJ8Ua/DCQfsCCB4LG3kx0klE0suzqqBCRhxUuCvdAmfydfsn/ALEX7RX7afi+bwf8BNDbUDZoJL6+nYQWNkjfdaedhtUtg7UXLtg7VOK/X6+/4NqP2tIfCh1ex8Z+Gp9QC5FqRepGx/uif7P+pQCv6hP2e/2Lvjh+xD/wRR0L/hivwKfF/wAWdf0Kw1n7PEsOZNY1tI5Hu5vOdEdLCBwqIxwfKVcfM2f5vPD/AOxl/wAHQXg34mJ8YrDQfiFcaus3nuLrVre4tpecmOS0e7Nu0R6GPy9oHAxxS5pdBn4A/tE/s0/G39lX4l3Pwm+O+hTaHrVuokVHw8U8LcLNBKmUliOMbkJAIIOCCB9s/sZ/8EgP2wf20vDdp8Q/A2m2ui+Fr1nW21bVZTFFceWxjf7PFGsk0gV1KFtgTcCN2RX9Vf8AwXh/ZO8Q/Gr/AIJNaF+1d8UvCbeE/iH4GTStV1HT5Qpmsf7SaOz1KxLKWzGs0kci8niMHua/nj/4J4fFb/gr38SPgZqP7Hn/AAT3sNevtFXUTqFxfaND5c9gZkG+3GpylY7OGUgSFQ6OzZIbBYG76CsfTni7/g2B/ay0rwy2paB4z8PXt8EyttPFeWqu2PurMYnUexYKPcV/PR8ePgF8Wv2Z/ifqXwc+NuiT6D4h0pgJ7afH3WGUkjdcpJG45R0JUjoa/sB/Ys/ZG/4ONP2aP2kPCPjf4iaL4i1zwfcalaxeItP1bxHZX9tNpssgW5ZoZr6UiSOItJG8ah1ZBjjgwf8AB2t8CvC3h3wz8JPjRFAsWsm/1TQZJQoDS2axxXMKse4jcybfTzDUxb2FY/lI/ZR/Y6/aA/bR+Ih+GvwB0RtTureMTXl1Kwhs7KAnHm3M5+VATwq8u54RWPFfuVZ/8GwP7WM3g59YsfHfhqfUxHu+x+XeiItj7ouDD+piAr91f+CbPw0+Hv8AwTl/4IQv+2JdaXHfand+G7nx3qQYbTe3Vw7Q6XbO4+YRBDBH/s73I5Y1/HF4o/4K6/8ABR7xZ8T3+K03xe8R6fqDTGaK30+8e1sIBnKwxWcZFuIlHyhWRsj72eTUtsVkf1c/8EkP2O/jp+zX+yR4v+F/xu0KbRtb0zxHq4eBtrI8TWNqY5opFykkTjO10JB6cEED+WT9iz/gl38aP+Cg2ieIvEfwa17Q7KXwxdwW9/Z6jJcLOq3Ks0MwEMEq+UxjdckggqeOlf6AP/BIj9suf/goX/wThT40fEyGBPFmk/2noutG2QRxTXVpBvW4VBwnnRSRuyD5VfdtwMCv4mf+CCn7XEP7Lv8AwUj0LQfE9ytt4Y+I5bwvqfmHEaS3MgNhOfQxXaxrnskj9qcXYatofi/8Svh34q+EfxG174VeObY2ms+G7+4029hIxsntpDE4HHTK8HuK+yv2DP8Agn18cf2/fFGueGfg89nZx+HrSK5vLzUfNW3Xz38uKIGKOQ+Y+HYDH3Ub0r9kP+DqH9jK3+Bf7X3h/wDai8J2vl6L8UtNxetGPkXWdMCQzZI4BltzA/8AtMHNfrJ/wTP8I+Hf+CTv/BCvXf21vH9vHH4n8VWcniuKKYANLcXYFp4ftDnkq26OYjssz+lU27E8qP4h/wBpn4F67+zN8c/EXwH8T6jY6pqnhi5+x3s+nM724uEUGSNWkRGzGxKP8owykds11f7In7H/AMX/ANt74tn4K/BH7CddFhcaiF1CY28Rht9gcBwr/N84wMV8/eLvEmueM/FeoeLvE1095qWp3Et1dTyHLSzzsXkdj6sxJNdt8GPjt8Z/2c/GJ+I3wH8T6h4S177NLa/b9MmME/kS4Lx7152ttGR7VaRirX0P9CXxb+wh8aj/AMEx4P2V/gxf2mgeME8Nabov2zzpIYI2j8n+0AssKtJ+8US4YJk7/ev4v/8AgoT+xl+0d+wjrfhn4Y/H/wAQw61/a1jNqthDZ3VzcW9unmGCQ7Z0jCOxj52ryuMn0/uJ/bR+N/xd+Gf/AAb/AMP7RvgTxRe6X47/AOES8J3h1u3l2Xv2i8ksBcS+YOd0okcP65Nfyb/8ErdI+Ln/AAV7/wCCnXw68Efti+KdQ8dab4XtrrVbhdWl88tY6cDci0HH+qluCgdehVmrNK2pu3pY8P8A2Tf+CGH7aH7Vfhay+JEsNl4M8PapGJrKbWDKbq5hb7ssdpCjyCNv4Wk8vIwVyuDXuvxg/wCDcv8Abk+F+hz+Ivh7eaP46eBCzafZNNa3zADJEUdzGkch/wBlZNx6AE8V+sX/AAch/wDBSj42/szfFjSf2Lf2X9YuPBmdJh1jxDqenHyL2Q3jOLazhmXDQxrHH5jmPaW3qudqYP5v/wDBFP8A4K6/tQeF/wBr/wAHfs+fHnxbqXjXwT471CLRnj1q4e7nsLm6Oy2uLaeUtIoEpUSIW2FSTgECmpO10Flax/Plreka54R1G50HxLZzWOoWErwXFrcRtFLDJFw6OjAMrKRgqQCDX69fGb/ghr+298OvhD4e+K9v/Y/iCLxNc6XaWNhpU08l276sm+DKyQRxqqrzKxcKnXOBmv0u/wCDrH9kvwT8Kfjr4B/aS8KRLbXHxCsL2y1YIqqJbzSfKCXDY6u8Eyo5HXygepNf06/tDftHeEv2Jv8Agkcn7UOqafFrM+keFdAi06wmysVzf6haW9vbxOy4ZYt0haUphjGrKCM1XtLmMKEUz/Pz/au/4JG/tBfsc/s3wftG/FjWdGe2n1W30oadZPPLOJLiOSTf5jRJEVXyiDtY89OK/MvTI3uQsKdWwB+OPb8K+1/2sv8AgpP+2V+2bpcnhL48eL/7Q0E3qX8Wk21pbWlnDNErJF5awxq+I1dlXc7cHv1r4s0xjbFSSBt5/L2rSKFiPh0P6pv+CNX7FXj/AMM+GJvj1q9zZPpfivTP9FiR285fKuMbZAygAHy26MeMV5/+33/wSu/aD+J3xu8S/GDwdNpn9ktCk4+0XQSXZbWyhyQFx/AcevFbX/BBf41/Fj4geMdc+Emta9dT6BoeiqLCzkk/c2++6j+4vQfeb8zXzN/wVn/a/wD2i/h1+2D4z+FvhHxrq2m6EsVvAtlb3cscAjntIjIgjU7QH3HIxg96+8qxwyyyMpRP5TwtPOpcZVqVOpH4U9tOXT8T8wPgH+yt8XP2nfGc/g74U2H2qWzQSXdxI3l29tHu2h5ZDgKM8Duewr9Hbb/ghX8bnsmlvfF+ixzjqka3MiD/AIH5Q/lXw3+xn8c/2j/hR8R7hv2aLOTVNc120ksXsY7drsSqw3K3krnLRMA6EggEcjGQf0G0r9mP/gtf4w8Qr4yv7zXre5dxIFm1eKAjvjyfPUKAB93aB2xXzuBoUnC/I36H6rxJmWPoVeWGJhSSXXdn55/tJ/sC/H39k54NQ+IVjHd6PdP5cOo2TGS2Lj+EtgFGx0DKM44zivuL/giTpf8Aaf7S2q2rjpotxu47eZCK/o1+K3wb8Y+Ov+CZXiLS/wBoaySLxRF4VnvNQjPlsVvbINIkoKEruYxqx28ckV+BP/BCKzhuP2ufENmQMjw/dbeO4lhFeu8njhsZS5dmfnT8QamccOY721ualeN1s7dUfF3/AAVc0uSy/bO1fT1GNtlp46etqlX/AID/APBMj4/fHj4cD4j6fJZeH9Nkz9mfVDLEJ0UfNKmyNwI1xjc2B17A4/os+If/AASki+On7dOp/H74uqreD7S3sPstoHG6/mgt0RlfB+SFGX5zwW6DjJH5zf8ABaT9uzxN4N1S6/Yx+FVlNoVhbwxx6rciP7OZ4yqtHbWyjhbYLgkjHmcD7g+Z5hlfsnOvXVlfQ34V8Qp4+GEyfJ2nNRTm+kVZfifgH4s+HWo6P8ULn4VeENQt/FlxDci0iudIEksFzLwMW+9Edxu+UHZhsZXIwa/XP4Of8ENf2o/HOlRa14tu9N8ONIATa3DyS3Cem9YEdV+hbI9K7n/ggJ+z3ovxF+Kfiz4xa9HHPceFoba2sfMXISe+Lgyj3SONgP8Ae9QK+7P27fhr/wAFTfij8XL7S/g9pGq6X4P0yUxabFp90lusyLx57gSqWaTG7noMAdK5MFlkXR+sVFe+yR7HF/HmKjmf9i4KrGm4K8pS/JI/GL9sT/gl3+0h+y34cl8bX0EOuaFbkCe907c4g7DzY3VZEH+0V2+9flQk0hAWQ4IPTFf3NfsLeFf2v3+Heu/Cz9tbR7ie1SFUsrnU5I53uIJdyTWsh3sZFwcru+6Mj0A/j3/bF+Eml/Ar9qHxp8KNHYtZaPqk8Ntnr5O7MeffYRmufNctjSjGtDRPoe54bcaVcbXrZbi2pTp680dmjw2zklm+VTknHavvj9lj/gnx+0H+1fG+peANNWHSIW8ubUb0+Taq+M7d2Muw9EUkcZ4r5K+EHhF/G/j7RfB0WFk1S8gtQSOhmkVBX9uv7efxY0z/AIJr/sT6Z4f+B1nFa36umi6TKVU+TtQvNdYxhpWxnJH3n3dsUspy+NZSqVfhiR4jca4nA1aGX5fFOrVdl2SXU/n48Yf8EH/2hdN017nQ/EOi3l2FyIN08e4/3Vd4tnPvtFfj98V/gX8U/gD4/f4d/FXSJ9H1OAjMcw+V1PR0YfK6Hsykg19f+CP+ClX7WngH4mw+NR4z1DVAZw81pfzvPbToSNySROSuCOOMEdiK/of/AOCqXws+H/7TH/BODTv2p9KtRb6ro9pYa1ZOQDIlvftGk1sX7qpkDexTjGTWjwdGtTlOho49Dmp8U5xlGKoYbN3GcKz5U0rWZe/4Jd/sEeJvgj8N9U13xde2F3ceJo7K5hNoznZB5TPsYuiYP7wcDIyPYV8lftc/8ExP2rvGPjzxJ8R08X6ZHp2s33lLCbm7UiG5k2wxMog27VXaCM4x0zX1R/wQD+MHxP8AjZ8OPG9v8R9eutXGh3OmW1kLyQyCGMxTDameg+RBjpwK/Eb9uH9tf9rDwX+0h41+H+kfEPXE0zTNdvIIIReS+WqwXDCPC7sAKFG0AcY4r2MRVoQwNNtaH5lkmW5zW4pxdKFSPNG266dLH7q/sa/sL+Kv2bfgW/g3XriyudVa5ubyaS3LtE0hULFksqsQmwZ+XjPFfhP+2R+yR+038CPAGofEz4o+L7XVdNv9RjSe1t7m6cySzb3V2V4kQhdh7/Sv6P8A/glJ488d/Gn/AIJ5zfET4havc6vrEN1qsf2u7kaSbbDGrIN7ZPyk5HYV/Gx8aP2qf2hfjBZXPg74l+LtS1jS/tPmi1upi8e+PKo2D3UEgelZ5vUoxwtNRW60Pd8NMPmWIzvGe3lF8kkpaeu3Y8JkPmy7UO4t3x29K/V7/glz+yT+3V+0d/wmWofsY/EE+BP7MNnaaptvL22a5FysrRELaRSbvLEbcnDLkbetfkXbuQw5yPT0r+5z/gz68NWGt+G/jfc3TBWi1Dw/t45H7q9r4epJcp/TlHR2P42Jfgb4/wBR/ajn/Zy1K+guPE0/id/Dkt5O8jQvfNd/ZWmkkKmQo0vzFiu7HOM8V+rfj7/ggZ+3d4T8U+HfA2gxaR4ku/ETXIMmnzTi3sYrMRmWe8muIIVjj/eKExuZ2+VVJ4r571qCG1/4LZXtuzBUj+Nbrk+g8QY/lX9pn/BxV+3J8Tv2Gf2bvD1r8A7tNK8TePdUm0+LVURTJY21pGJppYcgr5xMiIjEHYCxX5gpEcztZGjpxbuz+a28/wCDX/8AbKh8PNrGleLvDdzqCpuFq4vIY2bGQi3BhKgnsXVV9xX4D/G/4IfFL9nX4nar8HfjPo02g+ItFk8q7s5wMqSAysrLlHjdSGR1JVlIIJFftb/wSV/4Kv8A7ZvgL9unwF4f+JPxB1rxd4V8Za7aaLrGm61ey3sTRahMtuJ4vOZzFNC0iyKyYzja2Qa/R7/g7y+DPhfwj8Qvg78WtJt0TVNWttX0i6mRQPMhsJIJbcNjrs+0SAexx0Aw4Sa0ZTinqj+NfczrlvpX0H+zR+y98a/2ufiba/CH4EaM2r6xPG075YRQW9umA89xM2EiiUkDJ5JIVQWIFfPa9MV/aV/waMah8F9T1T4t+Ctbmt08Zyy6PfQQybRNPpVuJ0lMQOCyxTupkC9NyE8AEN6IUUux8h+Cv+DXL9q/WPDy6hq3jXRoLkJlo7ayvZ4lPp5zJF+YSvyl/wCCgH/BKf8AaV/4J42On+I/i7Lpd/oOs3TWVlfWFxhnnRN7IbadY51woyWCFBx82SBX9If/AAUi/wCCW3/Bezxb+0n4q+L/AMGfF2p+NPDVzfT3ejDRPEX9mvaWbOTDbpYSXFssZgTEeIt+4rnOWr+Zr/goT8Uv+Ch+vax4b+Cv/BQoeIIdY8EQXCabD4jtmhvDFdMheRpXVWuh+7VVmLP8qhQ5AxWa3KcUeLfsjfsM/tIftveK5/C/wI0T7XDp+37fqVy3kWFmH+7505BG5sHbGgaRsHapAOP2f/4hkf2wIvCra1pHi7w9dXwXItjHfRxscdBMYD+ZQCv6TPhv+xj+0P8AsL/8EddE8J/sI+CT4s+LF/pGn3bRwrBvGq6wiTXmoyGdkjk+xo3lwqx/5ZxLgjdX8/Xwv/Y3/wCDnj4dfE5PjJonhz4hTa2k/nu13rEF1DOc5KTW8t40EkTdDGU244AHFKTb2LP57f2kv2Xfjf8AsmfEu4+E3x70KXQtagQSojkPFPC3CzW80eY5YjjAZCcEEHBBAufs2/sl/Hv9rnx4vw5+Anh+fXNQCebO4xFb2sOcebcTviOJOw3HLHhQTxX90H/BwP8Asu6n8cv+CT3hj9rH4q+FD4P+I3gt9Jv9Q02bYZrFtWaO01CwZ0LBo1uGjkTk/cHcmvWf2Ifhx8Mf+CTn/BB3/hsWHR4NR8R6h4dh8W3Ql4+2apqrrDpkMjr83lQrNDHgY2r5jLhmzVKWhPKkfzg6f/wbD/tkXPhldX1Pxd4ftr0xhjbLFfSxg/3TKLcH8RGRX43/ALXX7DX7R37EXjSDwZ8e9F+yJfbjYahbN51jeCPAfyZgB86ZG+JwsiZG5BkZ9s8b/wDBXL/goz4t+LU/xZm+LviSz1PzzKiWd7JbWUXORHFZRkWyxDoEMbDH3s9/Wf24f+Cyv7Sv/BQH4OeG/gX8TNJ0WwtdOaC41K5s7ZWuNT1GDcqXO5wfsg2HBittoJJydm1FI36jPmT9jX/gnh+09+3P4iutM+Bmiedp+msiahq1432fT7MuMqskxB3SMORFGruRztxzX7E+Iv8Ag2E/astfCp1XTvG/h2e/Vc/Zzb3yRE+gl8pmx7mIV/SH+0J/Yf8AwQ7/AOCKOman8KbC1k8U6Tp2l6fbSTopjm8Ra0vmXV9Ov/LUxFZnVW42xRxn5Riv4bvDX/BXX/go74e+Jq/FC1+MHiWfUzMJWjurx57KTnPlvZSE2pi7eWIwoHAxStLoOx82/tP/ALIvx9/Y7+IH/Ctfj1oUmkX0imS2nVhLaXcQwPMtp0ykgGRuAO5OAyqeK+nv2Ff+CVfx8/4KCeE9d8Y/B/UtJsLbQL6GwnGpNOpMk0RlBXyYZRtAHOcH0Ff2K/tg/D3wJ/wVV/4IQH9rrVNMt7DxLa+F5/F0EcS8WWraK8kd+kJPzeVOIZkwT910zkoDXzf/AMGkuh2Wu/s3/FI3O0ufF2nR4YZ4ayIHHp2pqegz8ZvgH/wblftp/Fnw+PEvjm/0fwTbS7jax35mnup4gxCT+RCh8qOTGUErJJtIJjGRXy9+2/8A8EWf2uf2KvC03xN12Ky8U+FLfb9q1LRzL/ogZgitcwTRxyRoWOA6hkHQsMgV73/wUq/4LIftk+Pv2uPGeg/CPx3q3g3wj4Z1m70zSbDRbl7NXjs5TALid4irzSzFN53kquQqgKAK/qw/4IZfH7xN/wAFSP8Agnnr2hftPPHr+r6Tqlz4S1S6nRN2pWN3axujzhQB5vlzNG5AAbYHPzc0ndE2P813yJfNEIBLHgADn8BX7tfs1f8ABvN+2/8AHnwjaeOfGItPAtnfRpNBbaikst95Ugyjy28YAg3DokrpJ6oBXqn/AAQX/Yc8F/HT/grPN4X8f2yanofwsj1PXWt5gGSa5024W0shIvRgk8kcxU8Hy8EYOK/RX/g4v/4Kv/tC/Az9opP2Kf2X/EN34NstE062vdd1LTJDDfXV3foJ0hFwPnjjSIozmMq0juQTtVVqnLsNM+av2YP+CG37YH7Hn7efwo+JWoJZ+KvCVlrsP27UdL3o9mrxyIr3NtKqusZJA8yMyIP4ivFebf8ABzX4Xm8MfGv4URTIyNL4bu2weOl9IK9a/wCCAP8AwV+/aq1P9uvwf+y7+0V4sv8Axz4S8eTSafA+szG6utOvfJke3lguJN0vluyCKWJ2KYYMAGUGvXf+DxfTNHsf2ifgy2lKFD+Fb7eB0yNQfGKlN3Bn41fsJ/8ABE/9rn9t7wdB8UdFhsvCnhG+z9j1LWWkVr0KSpa1t4kaSRNylfMOxCRwxwcfdHxL/wCDXT9rnwxpR1Dwb4y8P6xdhQVtZYrqyL5/hVykij6ttHvX9SPxx+DvxF/av/4JR+HNP/4Jf+MLTw5c63ouitpN1b3TWYOnW0KJPp6XMAZrWYbfLfjIKMjFQxNfyfa3+yf/AMHE/wCwtrTfE3R18aTw6afPmk0vVP8AhILVlT5j5tmk91vT13w4x6VPNJuyGfz9/GD4V+M/gb8Ttc+D/wARII7XXfDl5JYX8Mcsc6Rzwna6iSIsjYP904rzbdXQ+LNS1zXPEt/r3iWWSfUb64luLqWXO95pGLSM2f4ixJPvXPcdBWy2Eh2QKQDmlHNIKYw+7X6u/wDBDVc/8Fbv2fx/1ONh/wCzV+UQAJxxX6t/8ENwR/wVt+ABH/Q42P8A7NQNH//S/gCPB20ntR1NKOOlACYxxRj0o6inCgBFHOKByaSncDpxQAnT2pvvTqCBjigD9ov+Df8A8Vv4I/4KeeCvEseAbex1rr76ZcL/AFr9yv8AgsN/wW1/bO/Zi/aB8PeB/wBn/VtPsNJvtBS9nW5skuHac3dzEWDMRhfLjQBenFfyOfstftHeMf2UPjFp/wAa/AdraXupabFcRRw3ocwstzC0L7hG6Nwr8Ybr7cV0/wC1x+1z8QP2xPHdj8Q/iHY2NhdWFiLCOPT1kWMxiWSbJ8x5Du3SN0IGMcVLiB/ar/wR0/4LX/ED9tTQ/EHwO/aF1GC18e6dFLdWtxpyLYnUNKddswi8s5jubQnO5CCY2DDHlsT/AB+/8FK/2aPiV+y9+1t4l8D/ABB1K819NQmbU9M1y9kM02p2NyxMVxLIxJabgxz5PEqMOmK+Vfgj8ZvHnwA+Kuh/GL4Z3Zsdb8P3KXVrJjK5Xhkdf4o5EJR1/iQkV9hftnf8FHPiZ+3B4d0vQvin4b0Gzl0O4e4sLzTo7lLiFJgBLDulnkBjkKqSpHDKCCOcpRsI/tL+BH7ZXxs/bT/4I/6Ba/sm+Pm8G/EfSNFsdKW6RoyINX0VI4pLW5EiyCOK8hjyHKfKJVfkKa/nO1D9s3/g5R8O+Mm8CXWt+Pl1HzPL/d6bby25PTK3Mds1uyf7YkKY74r8c/2Xv2xvj/8AseeK5vFXwN1ttP8Atqql9YzIJ7K8VM7Vngb5W25+Vl2uv8LCv1bT/g4I+PzaWsN34G8NyXm3mYPfLHu9TF5x/IPUqFhmZ/wUX/ac/wCCzPw58B2nwU/bA+KWo+IPCXj7TY/tdtF9lezeSJ45ZrGWSGFP3tu6xM207T8pUsK/pL+BXxR+IX7NH/BDTwsf2ArCK48XyeEbfWYRawrNNcapdyqdRuvJwftFzBmXZGyt/qlTa20LX8NX7Un7Y/x2/a/8VweKPjLqi3EdkGWxsLaMQWdmr43CGIE8ttG52LOwABYgDH0T+xz/AMFUP2mf2OPDB+HvhC4tNb8MCV54tJ1VHeG3kk5draSN45Id55ZQ2wnnbnmtLAfpZ+yj+2z/AMF1P2iP2k/DvglPiD42i04anavrlzeW/wBntLOySVGuDM8kCouI9wSIYZjhEBJxX3D/AMHQPxPk+IXwK+GVoG3Jb+J9TK+g/wBFjH4V+UXxc/4L8/tafETwrN4a8JaVpHhdrldkl5btc3FyisMMITNIUiJHG4IXXPykHBr46/bS/wCCkPxa/bf8L6H4T+IOi6TpVtoN3LeQHTRPuLyxrGVbzpZBtAXjAHvmgk/r1/4J8fE7wR/wUE/4Igx/slXmppZ3kPhmfwLfknP2G7tHMumzyR9fLZFgk4+9tcD7pr+P7x7/AMEvv28fAnxCk+Gtz8Mdcvb5ZjBHPY2zXNlNzhXjuowYPLPBDFxgfex28i/ZU/bF+OX7G3jdvHfwQ1c6fNcoIb21lXzbO8hByI7iE8OFPKnhlP3Stfrjqf8AwcP/ALQF1oL2Nv4H0BL8rjz/AD70wg+vkGTP4eZUqLJep/S5/wAEovhBq3/BPv8AYBk+Dni+6ifxJqh1TWdZWBw8UN1cWxTyEdflbyYoo1Lj5WfdtJXBr/OlOqXlhrA1SwkaG4glE0UiHDI6nKspHQggEH2r9Y/CH/BbX9sfw5pevWWu/wBj+IJvEF3PcyzX8MwaFJoFgFvAsEsUccMaIPLXbkEkkkkmvgz4cfsqftA/GP4dav8AFj4YeF73XNG0K4itrySzjMsiySKWwkS5kkCjl/LU7ARuwCKpIbP7zbm5+GX/AAXM/wCCWPgGH4s3S2+pLdWF/f3Sj95a6xpMgg1NV9PtduZsegmjbB21+TP/AAcw/tvRav4e+Hn7CfgBkstK0yOPxFqtpb/LHEqo1rpVrt4wIohLJs9HjPYV7J/wRt+GnxS/ZK/ZD8Ua1+0NJJ4b0nXLv+3IrC9BjlsLK1titxdzK2DEZ1QYRgG2xAkfMK/kt/au+PGtftNftFeLvjprZO7xBqMk1vG3/LG0TEdrCPQRQIifhWa1YnseDMe/61Hk7Tn0/pTSxU5HakDLuIbgEYrUzsj+7v8Aby+Lt3ff8G/EHgosrIPCPg6PjsElseP0/wA4r+bn/giB+1noH7G//BR/wR8UPGFyllompi60DULqQ7Ugh1OIwJK57JHN5bOeygmvO/iv/wAFR/jv8Xf2WYf2Sdf0nRLXw9FY6fYi5t47hbsxacYjF8zTNHlvKXd8mOuAK/NEM64OOM1KWmpbP7U/+Dh//gnx8aP2pvitov7Zv7OukT+KpV0eDRfEOk2P7+9heyZ/s93FCuXmikifY3lBihjBxtbI/Ln/AIJLf8Exv2jpf2v/AAd8ffjV4U1Dwd4L8B6lFrM0+sQNaSXdzaHzLa2t4Zgskm6VV3uF2IgPOcA+Cfssf8Ft/wBsL9mzwnZ/D+9nsfGeh6bEIbOHW1lNxbRKMLFFdwSRy7FHCrJvCjhcCvUvjd/wcB/tefEzw7Lo/gTTdG8HSyqYzfWvn3l4gI6xNdO0cZ9GEZI7EGi2lkDa3PpX/g5s/bMtPj38cPBHwE0i4E//AAr+yu7rUNrBhFeaqYysBwcb44IUZh28zB5Ffqx/wVx+LsniL/ghbY+E2k3CO38FdP8AYjiFfwj6zrOs+JdUute8RXUt9fX0rz3FxO5klllkOXd3bJZmPJJr9Ivjt/wVT+Ov7QP7M0H7LXi/RtEttDhTTk+02kdwt0w0xVEWS8zR/NtG7CD2xUqD6C5rn5oNF5igntSKXUjH0pYphFyecdKXzGcbl/GrcTnaP3S/4IU/E+x8B/HHxbaXzqHvdDIjBOM7Z4t2PXAOcegrF/4Kt/s0/tAfFn9snXfiF8PPDF/rem65HaSWs9jA0qHbbxxspK5CsGUjacH2xivyB+GXxM8ZfCHxnZ+O/At2bLUbJsxSAAghhhlZTwVZchgRgiv0qb/grz8Y10j7DH4e0kXRAJk3XWwsOf8AV+bgc5yM4/SvfoZhSlhPqtXS2p+X4/hbG0M9/tjApPmjytM+7f8AghRH4Z8D2PxB1LXLdYPE1vd2dg5kUCWC3Im8xB0KhpEw+P7grwj9o79q3/gphqP7Q+qeGNEudf0aJb2SKxsNKjljg8oNiPyzEv70FcfPlt3XNflz8N/2q/ir8M/ivqXxf8KTx2l9q80kl7Aif6NMJn8xo2izjZu+6ByOxFffUn/BYP4wx6ULWLQtO88rw3mXHlc9vK8zp143YrTC5lS9kqLdrdjzMy4PxSzWpj1SjU50lZ/Z9D+ifTPH3xQ07/gm74h0H4230974nTwvqy37Ty+bIJGjlKo7gnLIhUEdulfg5/wRP8WR+F/2udY1GVgE/sS7z9BJFXzfqv8AwVP+PniH4Zan8MNUtdMng1a3u7e4ujHIJtl3uD7dsgjXYrYQBMAAcV8ofs6ftLeK/wBmrx9P4/8ACdtbXtxPayWjR3Qcx7JCrE/IynPyjHOPau/G59SnWpzj9k8XIvDLEUMuxuFqJJ1m9Fsf0zf8FA/+CyPxJ/Z9+O+j/DD4d2EB03TltrrUzIPmvIp1VjAvURJs/iUbs81H+3R8IPhR/wAFMP2c9K+OfwjeOTxXYWvn6XLlQ91Bn97p02OksbZMfYPlR8rgj+XL9oD45+Jf2iPiTP8AEvxZBBbXVxDDC0dtuEYEKBARvYnPHrXs/wCzD+278W/2YtHv/D/hU219p1+6zfZb3zGSKVePMj8t0KsRw3OCAOOBjOrxAqlSUa2sH+BthfCKOW4bD4jKkoV6e/8Ae7pn6jf8EQfj3Y/Av4seK/gz4rP2K68RLBJarN8mbuwMgMHOMMySPgeqhRycV9Bft2fFn/gpH4A+KV/4l+CvijW9W8IahKZbP+zszG1B5MEkaqzJ5f3Vb7rLgg5yB/PR8Vfj34h+K3xRuvi09rbaNqlyyTTHTg8amZcZmG52IkYgFiDyeetfXPgP/gqr8d/Dtith4vt7TxCYQALmcyQ3DAf3niYK/wBWQk9zXHQzZez9g20ltY7c18Pq08x/tanTjKUklKMv0PrWL4j/APBYrxD8PLz4k2XiDW7e2t1LC2uJUhu5UQZZordwJHAA7Dn+EGvxD+IfxD8efFjx9qHxG+I9/Jqmtak/mXd1Lje7hQoJwAOgA6V+gfxO/wCCp/xx+IXhm78I6Bb2vh+C9QxzT2plkujGwwyLLIxCAjglFU9s4r81Z3VX83HU9a5MbVjO3LK9j7nhPKamGUnXoxg3tyroeh/DTxXf+BvGOleLrLHm6ddRXMfpuidXH8q/r6/bj+x/8FEf2NtPm+E9xFdapHNFrelxmRQJ90Zjntck4WVM4wf4k29xX8YAupcbV4C88V9O/Ab9sj42fs8O9j4Jv1m0qR/Mk066XzLZmxjcBkMjEcZQqSOK3y/HxpQdOWzPK4y4Lnjq1HHYZpVaTuu3oem/Dz/gn/8AtL/EHx9D4Vk8K3+kokoFxdahA9vbwID8zO7qBwOQByegBNfup/wUx+OHhb4F/wDBP61/Zo0W7Dzanb2OjWUZOJGtrAo8s5XPCkxqp7bn46V+Xp/4LEfGeTSjaWvh/SI7kDiVzcuqt6qhlx+ByPavzL+M/wAYviJ8dPF8vjj4l6nJqN9LhNz4CRoPupGi4VEHZVAFa/2jQo0pRo7vQ8v/AFYzHM8dQrZolGFJ3SXVn9GH/Bvt8QI/BXw9+IcshA8/U9MH5Rz1+Gn7eeppq37Wnj+/jORJr+ot+dw5q9+zH+2p8Rf2WNA1fQfBmn6feQavNDcStdrKWVoVdFC+XIgAIc9Qe3SvnL4i+N9U+J/jbU/HmsJHHdatdTXkqRZ2K0zl2Vck4AJ45PFceIx6lho0F0PZybhKrh8+xOZS+GaVvkj+vv8A4I6/EGz0H/gmpfabctyb3WcD6wJiv429dbfq90fWR/5195/A7/goV8Wf2fPg03wY8J6fps+nyyXEvm3KzGUm6UK33JUXAC8ccV+fdxM087zSdWOePejH49VKVOC+yieDuE6uAzDG4qptVldDSghGB3r+yX/g1X+Kknw78KfF1Y2EYutU0EcnrtivP8a/jZ3k8ivvb9jD/gol8Zv2GtN13TfhTp2lXyeIZ7a4nOpRzuUe1WRUCeVLHgEO2evbGK8dq6sfpFNHf+ILtrv/AILAalrMZHPxfkm/8rm6v3z/AODo/wAezeMPhj8Jtz5+ya3q64HbMFv/AIdq/lBX47+K2+Psn7RU0Ft/bMuvf8JE8O1hb/aftP2opt3bhHv4xuzt796+pP22v+Cknxi/bs0XRdD+KOmaRp0Og3U95AdMSdWZ50VGDebLIMAKMYx707FJng37Gt5NYftbfDC8h+XyfFejOPbbewmv6aP+Dpb4nH4jeEfgwWbe1rqPiFSfqLLj0r+TT4c+ONT+Gvj3RPiDoqRS3mhX9tqECS58tpLaRZUV9pB2kqAcEHHevrr9tL/goH8Wf24LTQLL4laZpWmx+Hprq4gGmiYFmuxEHD+dLJwPKGMY6nOabWwQVj4OYcY6V+gv7Bn7Iv7Znx51bWvjB+xy09nrfgDyJ0urS/8A7OvDPPu2RWUu6MGbYjsV3r8oxySqt+fLZCgnv0r7y/Y3/wCCjn7Sv7EC3OmfB/ULaTRb+bz7rSdRt1ntJZSoQuMFJY3KqFzHIuQBnNTJ9ioaH7M/Db/gpl/wcX/BzxtZ+FtU0zxX4raORUk07xD4cNxHMOARJdpbxTAEf8tBcDHXdX6G/wDBwX8XfD3xt/4JwWGt/FzSbWw8W6Zq+lSaUvmLLNZ3t0jf2haQzDmSLy1k3bflby0bsK/H7Uv+DiL9oTUbA203gXw4bgj7/nX/AJYb/rn52fw31+RX7VX7aPx//bI8TWuvfGjVElttP3Cx02zjEFlab8bvLiBOWbaAZHZnIABbAACSva5pdH96vwt/a0+Ov7dH/BJLQvEX7Hvj9vBfxMg0mxtkuYXjG3WNIjjgu7G581XWOO6VCyMygKJIn+6DX84tz+3J/wAHLnhvxs/w/fXfH8epiTyto0q3aHIOMi4W1NuU/wBsPsx3xX5D/slftsftBfsZeJJ9f+B2t/Y4L/Yt/p9wnn2F4E+750DdSufldSrrzhhX6Yaj/wAHBP7QFxbtHP4G8Ovd9PNWW+EWfXyvOzj231KTTBMZ/wAFJ/2mf+CzPgzwDY/BP9tz4maj4j8HeM7WC4mhj+yvYSXMDJM9nLLBBHma2kVGYBtp+VlLLzX9Ev7EXxd8If8ABTb/AIIhSfsjXesRWOp2Hh6LwldO5/48NR0uRZtLuJkHPkyCGFiwHI3gcqa/iD/an/bN+P37YXie38Q/GfVVngsAwsdPtU8mytQ+N3lRAn5mwAXcs5AAJwABi/s0/tW/Hf8AZI8d/wDCxPgPr02iX7p5VwqhZLe6hBz5VxBIDHKmegZeOq4PNU0DPePHv/BLn9vrwh8VJvhfP8LNfutQacxRS2dq09jLzgOl7GDbGI9d/mAAfexXrv7av/BJz4w/sOfBzw/8bfFHinRdVjvGgtNSsreTZcWOpSqzfZ4QxK3aIEO6WI8EH5AmGP1bB/wcMftHSaOLXWvBvhy5vNvM0Ul/BGW9WhWcj8AwH4V+S37VX7ZPx4/bD8VweJfjLqqzw2AZbDT7VPIsbNXxv8mIE/M20bnYs7YALYAwo36gj+5z9pLxbZf8Fof+CRFlo/w61K2TXNYsdL1O0jmkVUi8Q6MvlXNjO2cRb90sas2AN8ch+U5r+MHwv/wTG/by174ip8OIvhVr8Go+aIme5tGhs4+cb3u3AthGOu8SbSOhNedfsk/t1/tG/sX69c6j8E9ZENhqLI1/pV4nn6fdFBhWkhyMOoOBJGUcDjdjiv1kk/4OLP2jRoptLXwT4bS8I4mMl80at6+V5wOPbfTV16BY/eL9rn4q+FP+Can/AAQ/P7LMmqQ3eqy+GZPCVt5TYF7qers738sKnDGKETzuGwMKEBwWAr5F/wCDXj4it4H+BXxEgRgguPF+lnP/AG7EV/KZ+0/+1z8c/wBrzxv/AMJ38ctZbUrqFPKtII1ENpaQnny7aFPlRc8k8sx5Yk817z+xd/wUo+N37DXhXWPCPwr0vRtRtdavYNQlOpxTuyywIY1CeTNENuDyCCfSi2gkj5O/aEk3/Hfxq7ck69qR/wDJqSv7Jf8Ag1h+KUngP9mT4g6eHCCfxtp5Ge5NtEP5V/E14v8AEd74x8T6j4v1MItzqt1NdyiMYUSTuZGCg9ACeOelff8A+xR/wU3+Nf7DPgrVPBXwu0jRtRt9U1OHVpH1JLh2WaBAiqvkzRDbgDOQT6EU5RurBGJ+jv8AwR1/bD8N/sqf8FcNfufF91HY6b46n1nw7JczMI4obi5vBPaM7EgKrXECRZJwPMyeBX1n/wAHB/8AwT7+MHx8+PUf7Zn7PGj3PicanYW1h4g0uzXzL62urFPJjnS3HzyRSRKikRqSjodwwQa/kx8TeJ77xT4rv/Fl8FW41G5lupAnCh5nLsF7gZPFfrV8C/8Agtl+1p8JfCVr4I8XCw8aWVhGsVtPq3nLepGg2qhuYXUyhVwB5quwAxuotbYpH1l/wRL/AOCefx+8I/tgeF/2pfjdoN34P0DwRM9/aRalGbe7vr1YmSFIrd9sgjjLeY8jAL8oUZJ49p/4OlfiQnxQ+O3wmurWTzjD4au0G3/av5MYHXtX55+Pf+C3v7Vvi7xZousaLZaRpGmaTeQ30mnW4ndb1oeVjupnk80xbsEpGYwSBnOK+NP2tP23/ip+1/4v0Hxv46tLHSbvw7bNbWn9mCZBhpjPvYySSNvDnggjoO/NLld7iaP0L+Efwv8A+C4H/BO/wfpXi79nGbxNYaF4jtIdTlsNCb+07eFp1DeXe6YVlEVwFID7oPbeSCF/ob/4I9/8FM/+Covxe+JWpeDf26vCEyeErWweeLxFf6U2j3Fvdx7fKhA2xRziUFgQkYZMZJxxX83Pwt/4Lp/tZ+DNCh0Tx7Z6T4we2UKt7frPDevjvJLbyIrn1Yx7j1JJq/8AEr/gvD+1f4r0Z9L8C6XonhiZxt+1wpNd3Ce8f2l2hUjtmM+1S4gjjP8AgvQvwyl/4KW+N9W+GcUFsmpw6ffahDbKFRdQntka4YgdHk+WST/bc55r8bRxXReLfFXiPxx4lvvF3i+9m1LVNSne5u7q4cvLNNIdzu7HkkmudxWiVlYYoAoxSdacMA0wAYXpX6t/8ENQD/wVw/Z/H/U42H/s1flHX6t/8ENMD/grh+z9/wBjlYf+zUmho//T/gB74FJxSn0oFAB0OKXjGBTetOAoABxxRRkmgA0AJgCk4paXA6UAFJmgelKBQAc0As3egYxRgZoAdnim5JpvWlAFADu3NN9hRilA7UAKuRSgseKbzSjg4oAdk45NIvLECmdeaUcdKAJwVBJFfpp+yB/wVR+O37HXw+k+FHhTSdI1vQDcSXkcV9FJFNDNMAHKz20kTEHA4k347YHFfmIORSkAUCsfqT+1X/wVj/aW/al8DTfDC/Sx8NeHb3ab200oS77wKQQk80zu5jyoOxdqnA3A4r8vSRTEbbxml+lJKwuUnVgeKPl/Cq4YcCjIpkKBYxx1oBbfjrTA6npTTy2RxQOxYMmOtODjbmqYPanqe2KCHGxbJI4NM3ciq+4qeOMVIWdznjAoCMOxY2gjFRrtxTN56dMU4EDjFRqJRsOdm6gZp5ORUYcZwKfketOKTJJd549qckuGwSPxqDIpOG4pxp2IUSyJ16E00umCR9KgCjOKRYcU/ZIpRRYR8MGX/ClViQCx/AVCI/al2sT0odugmi2m0dvzpi4B5FV9tNK4HSoTQuUliB3Zx0qdZAw2cCqO0AdKAirxittC3E0ElWIEPgg1WkkBbgflUGzn+lSLHxwM0vQSVh4kA5IJpvnyn7opSHUZbimYqXFEpA7NgHHTtS03NN6+1RyyLW1h/Jx6Ug64pBxwKM4GccVdgsHC4NBLepqNtxXJ4xTPMI4NHQpImd2XjpmmeY2OD+FQcN1/ClAQHjmlc05CySFFRNxyKYHFLuAp3EotBnIxiglyKckqdccUxnUrgCpsO3kJz1Pej2qLc3Q00kk9aoXIafmbUz2/pWW+Wct1p3O0560z0PrQaJWJN/SoySevSnhlHbimYAAoGGSOBSE5NGRS4ANACYxR9KOMUoFAC5bt9KTc35UgxTsAUAA3dKZmlyDQOuDQAUE5pOO1KOKAD2FGTQKcOKADnoKbmilAGaAEG3vRSfSnAdqAAelFGAaXtj0oAMhTkCv1Y/4Ibgf8PcP2fv8AscrD+bV+U3Wv1b/4IbAD/grf+z9u/wChysP/AGahDR//1P4A+N3PFN60p64pB7UAA4OKT6UvalGKADGOKb9KXOaUAUANHWlpKdigBo4p30ptOAFABj1pPYUUoGaAEGM4pOKXrShaAEGKMDoKMCnDsKAADsabjtS9aTgUALx0pOtHalAoABgUdaTk8UoA6UAKPSk9qOtLj/CgBBjpSUDJ4FLigA+lJ1NLQKAFH8qXcymm4HalwRxQA4tTRk02nDjpQAuccUfNTBT+QcUAAz0oAfFAbilBI4oACDSDdTck9Kdk5xQADP5UYYim9ad2xQAozigBqaKeD2oAKTLjvTcmlGTxQAokPTNO3nOBmohzS0BYkyxFNw54NNyelOHpQAvzU35qTcTRk9KAHZ7UZOKYMnmnDOaAHj0NN2n1po5p2aAFIIpuQRSDkUAUAKWHamEk0UoHrQA4cUwcml4Ipy4z+lACr6Zxioz1pTyaXHPpQAgx0pOKMZoA9qADr1p3GMetIRjg9acPmOaAG47YptO6nilAyaAGDg4opetLgUAAx2pvajjpTgB2oAAKTA6UU76UANAGaT6UdacBQA2l4pMU4AUAIBzRR1p3HT8KAEHBpPailAxQAg4pB7U7kmlCDvxQAgAzRjPSk7UoAoAOn4V+rH/BDjj/AIK3/s/Z6f8ACZ6f/M1+U+M1+rX/AAQ3H/G279n5vTxlYfzagaP/1f4Ajw1JxSkZNJ3oEhQMdaMc8UdeKB1xQMbgiilJzTlUUAMHWil9hSgUAIOOtLgZx2pBzSgAfyoAQCkpx5NAxmgA5HFJ7UdaXAoAQDmlwOgpc0ADOTQAgApMZHFL1oAFACCjtiloAAoAABRgZ20uc0DHWgAAFN9hS5zSgDPFADRRk0ucnNAoAAKQU7jFAGePSgBMc0delLyelJx9KAAelJkmncngcUg6UAHPT0pfvUZoAHagAAFJwBS98cUNgmgBv06UdfpS46D2p6qCPSgCMZBxR2pRz+VPUJnGKAD5MUz6elKQevHNJ+FACD0pecY9KOMcUoA6HtQAnJ4NJml+90oA/SgBwAPWjaOlNxk/LS46j0oATpSZNOznikwPpQAZOcfhSCjrTgBjpQAuBuwKCB1pWJ3Y70nQUAJ9Kb9KdxikwOlACDOf0pKdjPPrQMflQAAEnFAGRS5OcUYoAQAUntS+mKABnnigAG7IWkFL1o6CgBSSRQOmBQCDke1KowfSgBowDSH2px56UgAFACdOKO2KPanbaAG4IPIo/lTs55oAFABhRwab7Cl4oAH0oAQZHSjNFKB6UANxil9hR6U4Af0oAQDBwaMf3aTrS4FACcj+VJ9KUYNGBQAcg4oopwA+lACAUvymlPPApuMcUAGQORX6uf8ABDVd3/BXD9n4f9TlYf8As1flF1r9X/8AghkP+NuP7Pw/6nKw/wDZqT2Gj//W/gCY/NScZ44oPJpQCOlAkGMU36U7HIAowM0DGiilzSgelAAAc4FGPTtSYJ6U/aQc9KAEHHy4o+lHNGOcdKAG9+lJ9KdnNAxxQAmMcUvNHU4pwQg8UAKo7UlHzmjBz6dqAG4wcUmKXjjFHfigBBmlAz0oAJOBT9hFACYIpSMDj/CjDUKuD6CgBn+yaTFO9zScdqAFX7uKXb3FN9MVIFJ6UANUYHNLt5wO3NJhsA0mD17UAKMbgKD93P4UcDn2poPr2oAFHIAoA3cCk78U4D9KABRzyKPpxS4bORTgrYxQA3IOePypCBtyKVie5pdyZGOnegCPA4pQMgY+lJ0pw5XA/CgBSpH0oXvj/CnDcVC9KRs53DigBS3yBfWmNzyKdkn5R2pnU8UAIAemKMYpxbkEcUKAaAFIK47UL932oCt09BTtrYwOgoAYp2kcUhOTmnEHP+e1NwO3agBcEDmme1P3EnNOVVJx3oAaBx9KMAfdp2Dnin+WS3FADPm3AkfSkYL0FKS3T1/pTP8A9VAC4GP0pMDoKc3XPamjg/LQAYOeOgopwBJ4pxQrQA0deR7UE9xil2EYPrSY9KAG03A7U70oAFACAUv0o69KdtPSgBcY+XpTQTgClIZaccjBPUUARgYNJj0pRRgCgBBwcUAZ6UdeFp4Uj2xQAgGB0pee3SkwxpwUge9ADcnPNM+lL1pRigBMYOKBzxR1pwXnigBApzTgM9KTDHilCnGMUAN5HFJ9KMmnACgBmO1L9KXIox6UAA9DRj07Uu05pwBHtQAnt0pvJNOxzTcD8qAFyFNfq5/wQyG7/grn+z92/wCKysP5tX5Q1+rn/BDUlf8Agrh+z9j/AKHKw/8AZqT2A//X/gCPDc0nHSlbrQAO1ABx0pKUdgKXqc0ANA5xR24pKfigBQApxSAHnHpSY705QM0ANHp0oPpSnGKTigBPuml20HninEAYIFAAuaXJPAoA6Z4zTtgztGaAGc5pMbhxSngdqBjvQA3GD0oxS8k8UoXPtigARcn6U4YJxkUvBAH501Rn2oAPmBxTSST6VJwfmz07Um1duBQAztyKUKtJuOKMDvxQAoH8OKXI6DpSqQMAelKFJG0DGKAE+9x34FMxkYBpfu8ZpSgA4oADjp/kUzGcBad/Wm0AKDgbQKWkH96n7F+lABk03nGBTsc03A6igBBlmwaRueRxSqxVgaOPp2oAbxgCnZB5FKMHj2pQFY+lADicj07fSlI4Cj9KTHGSeaQIcH0FAEYoI4qRcDB/Omn5uTQAnX5m70mO1HNKB+FAEnKDI9cUn8J9TQvHBOKTGOOlACAnG2m4yeKkI4AHcU0DPB7cUAGBjBHShVBBbsMUbsnHtS8B/pxQApHA46UDDE4OOKdtxhiaRVDcdMUARjJwPwFJxjFPGetNHBwOlAAOcKf5UBQeBSAnG0dKcF4z26UACsyfd705W7df5UKq7cigLhs0AKzZ+XpTCvUjntSkA03PBz9KAEFJj0pc5oGOKAFHH8qcQAOMU3gnAp6oCMUAByQM/Sm5BPFKSD1NN4PJoAb3oxnpR1pwx3oAbg1IBSYBAxTwvNADckGmkg9KcelNxxQA3HOKPpSnnpSigBAMc/hS470U4KCOKAEyeMUmSehpcA9OtAwOPwoAb3puKXPrSj/61ACAU5RTSe9PwD0oABkdKOc8GjHpS7R2oAYOuKMdhSdaUCgBcAdK/V3/AIIZhP8Ah7h+z8G/6HLT/wCbV+UNfq5/wQ24/wCCt/7Pp9PGWn/zNJ7DR//Q/gCb71N+lOP3qOh4+lAlsJ0NH0opQBQMQClo4xxT+DQAwY4BoB7dqXcuRgUvAXgUAMHBxRijr0oxigAwc04HPFIBmpFZQ2SKAI8joe1Ozzt7U8FWHzUw7WPy8YoAGIJximilBA6U0igCQ47U3sAKBgj6VIu0KT6cUAICD8uKQFD2pobmnfJ1HWgBuAM/lScmnKckdqbwGx2oAUY/CglSPpxQO1AAz0oAMkkH8KerKoGKXiP60mR0xQFhvU4poGelPBCcj9KTbz8p6UAGMD6dqAAQTTQB+dKOKAFBHQigEYwKUFc0uRnkUAM3e1J14FOYqx9Kbxj6UAHOeaMZ4FHX8qUYBzQApAHApARTlPG0U8AIBxQBHuGcDil3ZGF4xSjbn2pnf0FAC4GMDrTR7fpR1PHGaVVzxQAgp4KjpQDxTgq7uelADAdowaafmPFPUqwI6cUfKSO1ADSc/wCe1OALn5eTTQKF6/T0oAOBnPWlIXoPSlQFuaD2xQApJ24alH3eO9G7nIAGaQbeMUAMbI+UdKXB4FDL6GkwRyKAFxnpStkAKe1MB5GKkDKcEj2oAaG2ijcN2RT/AJVPSk+QHIHSgCMnnil2ED0pd2B8vem855oANoo+lKSSKXH4YoAaDg07PFL8tKu30x2oAYeuPTim89qUkHmjGAKAEwR1pcelOHK8dhQoycfhQAA4xnpRlSKXcAaOD90e1ADcnpSEc4HanH1Wk680AAU7c032FHfAqRMdWoAQZ9KQkHpTw2Rx2FHyccYoAZ/FTfpUhZSOBjimGgBMH+lH0oHtT9vGe1ADQOcAUZ9KdncRinYAPSgBgOOlN6804lelAAoAbgZxS9aQ04elAB938K/Vj/ghvj/h7f8As+5/6HPT/wD0I1+U5Ffqx/wQ7Xb/AMFbf2f/APsc9O/maT2Gj//R/gDbG/2pVUNQy85/SkwQMUCWwnQ0AZ4FGOOaMCgYAfrS8456UpfsOPpQeQB2FADR6UDkAdKAcc/lS554oACADgfTikIG3OaOSKABjigAHyikPtTwc4pRjfnpjigBvQAEU0rjj0pc0p5IP4UAID2oIH8NHHbik74oAX5h8vpS9aNzfTNKV6D9KAFALNt6CmEinhyBkYpn0oAd/Dj0pMZ4FJnOBRQAv3TgdKBz8o70me9PHoO1ACc8KBRjCc00UUAOG0DbTcg4FIccbfSl+X8qADjp+VA9VpQeOKUDPFADenFB56UdTS49PpQAnSkPPSilAoAOnSkApy9PpSr93C0AIBjjHPanYLD2xQh6HPP+FBHy57UAN5PH8qT29KUHJ4oAHVaAAdsUi8dKMdh3pQDux+FACgAdaRhjijJ79elHNAAOABRgdKTOeKD97igAYEHGKMjoKbTwuRkdqAFVQeP0puSRipByM8c0mMnAPtQAh7ACm9Dx2pB1peBQAY4/SjPORRnijFACj/61GO460AgbakIBPA4FAA+D/wDWqHtxUrEEfLxTVxjBoBDMYbFO4xjNMp+NzZoAPYUY4zSDpmn49PpQAwDFIfalJB6Ucf0oAbjtS9aOtHXgUALjjFLtwAQfam9qkONoWgB2zB4HtUXJHHSnNknJ64puKAFPynFMp2SaOB/KgBMDOKdncNq/4U3tT1wPbtQAeimkwcU4kHikye/0oAZSUvX60EAUAGO1ODEDApo6/LTtoGc9uKADnHT2oK8UYyMCpHwVz6UAR4GePSm44pM0uOKAHAZGB1pc4UCox6VKVTdgdPyoADj7w/Kv1X/4IboW/wCCuX7Po7nxnp+P++jX5TFTnFfq9/wQyz/w9z/Z9Hp4zsP5tSewH//S/gCPD0FieDSEfNijHPFAAeWo9qUe1AoAXAHFIen0o470oA70AM6cUUUuOKAAelGCelFKKAF5BAH0oxkYFJQaADpxikzR1owKADmj6Umc0o/+tQAuO1BXjijr0pQMDj6UAJ04pOvSigYFAAODSUuaXH+FACAc4p3cgUnU8U4Y+nagBntSZ4wKXrS4/SgBBxSE5petKBQAnfFOx/dpoPpSgCgAwVOKTg+1KTmkx6cUAFHWgUoxxQAue3rSEUntThQAnTApOegpTzRigBPaj2opRigBOaXGelJ1pw46cUAA/Kk69KOT+NAAoAO2MUmRR9KXbigBAfajjHFHsKcBQAAYpc5PHWm454oAFAClj06UzOaXrxS4/wAKAE68UHJoPPFKBg0ALgj+VHQYFJmndfw4oAbkjikzQeaKAEpfpSZ7U4Y6UAA/+tS9sUlKB60AN/8A1UZ54oJzQBQAd6SilGKAAelGMdKM5NO47UAN6GkNL1pcUAHQ0n0o60UAGCODR9KM07jGaAExg/pSH2opeKAE6UmaXr0oFAAOtLzSdadigA6Cmmg+9L34oAQUZpKcAM0ANFOHNJS4oAcTjrX6uf8ABDIZ/wCCuf7Pv/Y5af8AzNflD7V+rf8AwQ1bZ/wVx/Z9J7eMrD+bUnsB/9P+AE4zRwTSsBuxRgZwKAE6Gk+lL1pQKADGP5Un0pT04oAoAb2ooPtT8CgBoHaj6UvJ6UACgA4zim0uc0uKAEwQcUn0petOCigBmKXGTR14p1ACDI6ig8dKTrS9aAEAwcUmOwpTSgCgBuMHFKPaj2oGPSgBcdBSe1ByaXAH8qAEHWkpRzShRQA0UtBpRx7dqADBDYpOvFLnNGMUAJ0OKPpSdTTgFxQA0cUU44xxSj+XFADQDnFHUUtKPSgBuMGk+lOxmgDtQAg4pPal69KdgUANxzijGelGc0o7CgBMYOKSnUYH07UAN9qXqeKOD1pR19O1ABjtS444pAaXA6dKAE9ulJ9KWjj+lADcc4pe1HFLgUAJjBoxmj6U7/8AVQAYFNx6UdaXFACdOKT6UvWlAGaAG+1L3oPJpQP8KAE70Gijr0oAbTvpR1pcAcUANxjilAJ6UHGeKdjHIoAaPlPNLx2pOtLjnHTtQAmMcUnsKXilAH0oAQCkp33qUD0oAaMA4pfpSe1LxQAnSgegop2B0oAZil7cUU4AflQA0Cj6UdelOAoAbyOKSjjFOxQA3milPtS4oAQL2pcf3aTrS4HSgAHy8iv1Y/4Ic7j/AMFbv2flTj/is9P/AJmvymHWv1a/4Icf8pbv2fz6eMrD+bUnsB//1P4Am+9TeDTmGWpcdhQJCAYNJ9KWjoKBiY5xSUlP46UAN6UuO/ak608AUANHBp38qMGlxQA32pvHalzmgYzigBMdqXGeBR1pQOlAAAc4pfp0pfvHmgKPwoAbyOKbTs5oGOlADcY4o+lKeacNuelADcYOKdzSYzinBc/hQA0570n0pSaKAG8g0UZpwHpQAmMcUfSl5bgU4DHWgAOc4pnWlzRigBuKMUuc0oAoATbil746UdRShelADQDmlPt6UcmgelADaPpS9adigBmMcU76UmeOKeE5xQA3npRyTgU4qT1pMY60AN+lH0ozSgUAJjB5o+lGc0oFAB93jFKRzjpS+5pO9ADcYNJil6mlGKAG4wcGlx6UZ9KeF4/SgBozml7YHSl5PINAFADaTrR7UuAKAG0uPSjPpTsf4UAIBg80v0pe/HSlAP07UAR96OtH0oGOlACY5xR9KXrSgCgAAOfSjk8Ckz6U/AHB4xQAnPT8Kb+lLnijHp9KAGgUY7ClzSgUAIODSj2pfpSkAY/KgBuCOB9Kb9KcRxQMUANwelGKXrSjGcdKAG4PSlxnpS4zxT9vagBvQ0080pyelHegBuMUUdadjnFACAc4o+lJTsYoATvS+wpxApMYoAToeO1fq3/wQ0G7/grj+z8v/U5af/M1+Uh9BX6t/wDBDZgn/BW/9n4noPGVh/NqT2A//9X+AM/exTetOb71GB24oEthvp+VHbApeDQOtAxMYpO1LmgelAAF7U7rR8p5NP2p9KAGAAGg46CggdqMDtQAzGDRTjk9aABQADg80vGcCl9jTgiYx3oAbwDikPtTgF6etLtGOP0oAjx2xTacTuOTQMdKAD2owD0oqQKuKAG5xxSewpcLShcHH4UAMx2pPpRRQAAYNLwelLnJ96dtWgBuMUvHRaX5e1G1R0oAbim47ClzmgcGgBMYOKPpR16VIqj+lADFAzg8Uuc9KeVWjCZoAZ7U36U44I4pMUAJjHBpRikzmnhe3pQAg4wKdkdqQBTTtij27UANHXFN68UpHpSAUAJznFGB2pdxzSgDFABigAZ49KXauMU7agoAYR6Un0peONtHegBuOaOKUkmlAoAaBTs5p2AevpQETOKAEGOlIaMLS4A4/CgBmMHApKXrSgUAJjtTuOlAFO2pnFACcZ6UhGOlLhfXFLgUAR7SKPpS5NGKAGjrincdqUfMadtWgBOKQ4HSl4I4pcJ2+lAEY4OO9B56UUvXpQA32p2PSk61KEWgBoAxSZyMU7C0bEFADDwcUn0pfpQBz+lACYwcUcGlyfzp2F/KgBqgA4p3B/KghSaXCY+lADMY4pMY6U5uMdqTjOBxQAgFB/KjvTgKAEAAODS/LRhcU8KtAEajnFGOwpcDFAUUAHANfqz/AMEN8H/grf8As/A/9Dlp/wDM1+UnU1+rP/BDouv/AAVu/Z+29f8AhM9P/maT2A//1v4A2+9ScYpW700HAyKBLYXGDigc8UHpTewoGKBzig0rU3NADuB2pc+lSt9wH2pp6fhQBHyOKOvApzfdzUYoAXnNLx2pSTtz60L0NABnJ6Uucn5eOKcegPrS9CKAIx6UmN3SpG5GahBIoAXFGKU9AaaKAHrwdvSl7U5emaBwePSgBhHrSd6mYDZmoD1oAKPpQegNHbNACgc07Pb0oHQe9HQ8UAIO4xSYz0qQ8rmmZwQB6UANHXFA9BSdqOgyKAHAYOKd9KXqMn0NGelACZ9KbUxAwKi7fhQAgz0pKD0BptAD8c9KXgtxS9B+FCdKAF449Kb1qXtmos/yoAO+Kb1p7+tR5oAUDnFO4PTtSdADQeDx2oAUcHp7UcHintwuaa3A4oATuB+FNxnpUnWoelADsGl47UH71IeMY9KAHD5TilPP5U/NM7D6UAN9qDzSvxSHt9KAEAp3bimGlBOKAHjpz2oHPFPH3c0nQjFADB9707Un0qVgNuagzjpQAuMHFHtTu2aT+IUAKDigc8AVI/3hTexoAbwDSc9qmYcA1XyaAFApPpSnoDSDrQA7ocfhT85pG7U/AoAZ04x7UnX6VI/Cg1H0Xj6UAJgg4/CkwccUrUygB+KcCOopV5GTQv3aAG8A9Pak6r6VOegNR/xY9qAGc5xSdelOboDUdADhwcU7joBSfw5pf4sUAKMjkD2pDjNKPu7vejODQAn3TjpSYzSHpSDrQA/OOlfqt/wQ5H/G279n4Dj/AIrPT/8A0I1+U/bNfq3/AMEOeP8Agrb+z/7eM9P/APQjSewH/9k="
    st.markdown(f"""
    <style>
    html, body, .stApp {{ background-color: #000000 !important; }}
    header, .stSidebar, section[data-testid="stSidebar"], footer {{ display: none !important; }}
    .block-container {{ padding: 0 !important; margin: 0 !important; max-width: 100% !important; }}
    #MainMenu {{ display: none !important; }}
    </style>
    <div style="
        position: fixed; top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: #000000;
        display: flex; align-items: center; justify-content: center;
    ">
        <img src="data:image/jpeg;base64,{_logo_b64}"
             style="max-width: 80vw; max-height: 85vh; object-fit: contain;"
             alt="iSchedule" />
    </div>
    """, unsafe_allow_html=True)
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
    st.caption("טען נתוני FIDS מקובץ Excel/CSV או מלינק ישיר")

    fids_tab1, fids_tab2 = st.tabs(["📁 העלאת קובץ", "🔗 טעינה מלינק"])

    def apply_fids(fids_df):
        fids_df.columns = fids_df.columns.astype(str).str.strip()
        fc = next((c for c in fids_df.columns if "טיסה" in c or c.lower() in {"flight","flightno","flight no","flight_no"}), None)
        if not fc:
            st.error("לא נמצאה עמודת טיסה. ודא שיש עמודה בשם 'טיסה' או 'Flight'.")
            return
        fids_df["_fk"] = fids_df[fc].astype(str).str.upper().str.replace(r"\s+","",regex=True)
        base = st.session_state.get("saved_flight_edits", flights_editor_df.copy())
        base["_fk"] = base["טיסה"].astype(str).str.upper().str.replace(r"\s+","",regex=True)
        COL_MAP = {
            "גייט":    ["גייט","gate","Gate","GATE"],
            "רישוי":   ["רישוי","reg","Reg","registration","Registration","REG","tail","Tail"],
            "נוסעים":  ["נוסעים","pax","Pax","PAX","passengers","Passengers","seats","Seats"],
        }
        filled = 0
        for target_col, aliases in COL_MAP.items():
            src = next((a for a in aliases if a in fids_df.columns), None)
            if not src or target_col not in base.columns:
                continue
            for _, fr in fids_df.iterrows():
                val = clean_text(fr.get(src,""))
                if not val: continue
                mask = base["_fk"] == str(fr["_fk"])
                if mask.any():
                    base.loc[mask, target_col] = val
                    filled += 1
        base = base.drop(columns=["_fk"])
        st.session_state["saved_flight_edits"] = base
        st.success(f"✅ נטענו נתונים עבור {filled} שדות. הטבלה עודכנה.")

    with fids_tab1:
        fids_file = st.file_uploader("קובץ Excel / CSV", type=["xlsx","csv"], key="fids_uploader")
        if fids_file:
            try:
                fids_df = pd.read_csv(fids_file, dtype=str) if fids_file.name.endswith(".csv") else pd.read_excel(fids_file, dtype=str)
                apply_fids(fids_df)
            except Exception as exc:
                st.error("שגיאה בקריאת הקובץ.")
                st.exception(exc)

    with fids_tab2:
        fids_url = st.text_input("הדבק כאן את הלינק לקובץ FIDS (Excel/CSV/JSON):", key="fids_url")
        if st.button("📥 טען מהלינק", key="fids_fetch"):
            if not fids_url.strip():
                st.warning("יש להזין לינק.")
            else:
                try:
                    import requests as _req
                    resp = _req.get(fids_url.strip(), timeout=15,
                                    headers={"User-Agent": "Mozilla/5.0"})
                    resp.raise_for_status()
                    ct = resp.headers.get("Content-Type","")
                    from io import BytesIO as _BIO, StringIO as _SIO
                    if "json" in ct or fids_url.endswith(".json"):
                        import json as _json
                        data = _json.loads(resp.text)
                        if isinstance(data, list):
                            fids_df = pd.DataFrame(data, dtype=str)
                        elif isinstance(data, dict):
                            key = next(iter(data))
                            fids_df = pd.DataFrame(data[key], dtype=str)
                        else:
                            st.error("פורמט JSON לא מזוהה.")
                            fids_df = None
                    elif "csv" in ct or fids_url.endswith(".csv"):
                        fids_df = pd.read_csv(_SIO(resp.text), dtype=str)
                    else:
                        fids_df = pd.read_excel(_BIO(resp.content), dtype=str)
                    if fids_df is not None:
                        apply_fids(fids_df)
                except Exception as exc:
                    st.error(f"שגיאה בטעינה מהלינק: {exc}")
                    st.info("אם הלינק דורש התחברות, השתמש בייצוא לקובץ והעלאה ידנית.")

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

        # Debug: show status of TSA supervisors
        with st.expander("🔍 מידע debug — מפקחי TSA", expanded=False):
            tsa_col = next((c for c in employees_df.columns if "מפקח" in c and "TSA" in c), None)
            if tsa_col:
                tsa_emps = employees_df[employees_df[tsa_col].astype(str).str.strip() == "כן"]
                for _, e in tsa_emps.iterrows():
                    ss = clean_text(e.get("תחילת משמרת",""))
                    se = clean_text(e.get("סוף משמרת",""))
                    bl = clean_text(e.get("חסימות",""))
                    av = clean_text(e.get("זמינות",""))
                    sick = e.get("חולה", False)
                    in_shift = is_within_shift(e, datetime.strptime("18:00","%H:%M"), datetime.strptime("20:00","%H:%M")) if ss else False
                    st.write(f"**{e['שם']}** | משמרת: `{ss}-{se}` | חסימות: `{bl or 'אין'}` | זמינות: `{av or 'אין'}` | חולה: {sick} | in_shift(18-20): {in_shift}")
            st.markdown("---")
            st.write("**name_key test:**")
            st.write(f"name_key('שיילו בר') = `{name_key('שיילו בר')}`")
            st.write(f"name_key('שילו בר') = `{name_key('שילו בר')}`")
            # Check shift map
            sm = build_shift_map_from_excel(daily_file)
            daily_file.seek(0)
            k1 = name_key('שיילו בר')
            k2 = name_key('שילו בר')
            st.write(f"shift_map[שיילו בר] = `{sm.get(k1, 'NOT FOUND')}`")
            st.write(f"shift_map[שילו בר] = `{sm.get(k2, 'NOT FOUND')}`")

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

                # Workers sorted alphabetically
                all_workers = sorted(
                    [w for w in timed_g["עובד"].unique() if "❌" not in str(w)],
                    key=lambda x: x
                )

                # Build data per worker
                workers_data = []
                for worker in all_workers:
                    tasks = timed_g[timed_g["עובד"] == worker]
                    tlist = []
                    for idx, task in tasks.iterrows():
                        role = normalize_role_label(str(task.get("תפקיד בסיס", "")))
                        tlist.append({
                            "idx":    int(idx),
                            "flight": str(task.get("טיסה", "")).replace("LY","").strip(),
                            "role":   role,
                            "start":  str(task.get("התחלה", "")),
                            "end":    str(task.get("סיום", "")),
                            "color":  ROLE_COLORS_G.get(role, "#9fb7d7"),
                        })
                    workers_data.append({"name": worker, "tasks": tlist})

                gdata    = _json.dumps(workers_data,  ensure_ascii=False)
                rcolors  = _json.dumps(ROLE_COLORS_G, ensure_ascii=False)

                gantt_page = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>גאנט עובדים — סידורומט</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:Arial,sans-serif;background:#f4f7fb;padding:10px;
     -webkit-user-select:none;user-select:none;}}
h2{{direction:rtl;color:#071b3a;font-size:18px;margin-bottom:8px;}}
#legend{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px;direction:rtl;}}
.li{{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:800;color:#071b3a;}}
.ld{{width:13px;height:13px;border-radius:3px;display:inline-block;}}
#gantt{{overflow-x:auto;-webkit-overflow-scrolling:touch;
        border:1px solid #d9e2ef;border-radius:14px;background:#fff;}}
#inner{{position:relative;}}
.hour-line{{position:absolute;top:0;bottom:0;border-left:1px solid #e8eef7;pointer-events:none;}}
.hour-label{{position:absolute;top:5px;font-size:11px;color:#8a9ab5;pointer-events:none;}}
.wrow{{display:flex;align-items:stretch;border-bottom:1px solid #eef2f8;position:relative;min-height:44px;}}
.wrow:nth-child(even){{background:#f8fbff;}}
.wrow:nth-child(odd){{background:#fff;}}
.wlabel{{width:120px;min-width:120px;display:flex;align-items:center;justify-content:flex-end;
          padding:4px 8px 4px 4px;border-right:2px solid #e0e8f4;
          z-index:2;background:inherit;position:sticky;left:0;
          font-size:12px;font-weight:900;color:#071b3a;text-align:right;direction:rtl;}}
.timeline{{position:relative;flex:1;}}
.task{{position:absolute;height:28px;border-radius:7px;display:flex;align-items:center;
       justify-content:center;font-size:10px;font-weight:800;color:white;
       white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 5px;
       box-shadow:0 2px 5px rgba(0,0,0,0.15);}}
.task.missing{{background:#ffcccc!important;color:#9b0000;}}
#info{{direction:rtl;font-size:12px;font-weight:800;padding:8px 12px;border-radius:8px;
       margin-top:8px;display:none;}}
.ok{{background:#d4edda;color:#155724;}}
</style>
</head>
<body>
<h2>📅 גאנט עובדים</h2>
<div id="legend"></div>
<div id="gantt"><div id="inner"></div></div>
<div id="info"></div>

<script>
const WORKERS  = {gdata};
const COLORS   = {rcolors};
const DAY_MIN  = {g_min};
const DAY_MAX  = {g_max};
const HOURS    = DAY_MAX - DAY_MIN;
const HPX      = 90;
const LW       = 120;
const HDR      = 26;

function h2px(s){{
  const [h,m]=(s||"0:0").split(":").map(Number);
  return(h+m/60-DAY_MIN)*HPX;
}}

const inner = document.getElementById("inner");
inner.style.cssText=`position:relative;width:${{LW+HOURS*HPX+20}}px;padding-top:${{HDR}}px;`;

// Hour lines + labels
for(let h=0;h<=HOURS;h++){{
  const x=LW+h*HPX;
  const ln=document.createElement("div");
  ln.className="hour-line"; ln.style.left=x+"px";
  inner.appendChild(ln);
  const lb=document.createElement("div");
  lb.className="hour-label"; lb.style.left=(x+3)+"px";
  lb.textContent=String(DAY_MIN+h).padStart(2,"0")+":00";
  inner.appendChild(lb);
}}

// Worker rows
WORKERS.forEach((w,wi)=>{{
  const row=document.createElement("div");
  row.className="wrow"; row.dataset.wi=wi;

  const lbl=document.createElement("div");
  lbl.className="wlabel"; lbl.textContent=w.name;
  row.appendChild(lbl);

  const tl=document.createElement("div");
  tl.className="timeline"; tl.style.position="relative"; tl.style.height="44px";

  w.tasks.forEach(t=>{{
    const x1=h2px(t.start);
    const x2=h2px(t.end);
    const bw=Math.max(x2-x1,6);
    const d=document.createElement("div");
    d.className="task"+(t.worker&&t.worker.includes&&t.worker.includes("❌")?" missing":"");
    d.style.cssText=`left:${{x1.toFixed(1)}}px;width:${{bw.toFixed(1)}}px;top:7px;background:${{t.color}};`;
    d.textContent=t.flight;
    d.title=`${{w.name}} | ${{t.role}} | ${{t.start}}–${{t.end}} | טיסה ${{t.flight}}`;
    tl.appendChild(d);
  }});

  row.appendChild(tl);
  inner.appendChild(row);
}});

// Legend
const lDiv=document.getElementById("legend");
[["ראש צוות","#8e24aa"],["דיילת","#5b9bd5"],["מתאם תורים","#f0a000"],
 ["מפקח TSA","#d32f2f"],["שומר TSA","#2e7d32"],["טרייני ר״צ","#f9a825"]].forEach(([r,c])=>{{
  const d=document.createElement("div"); d.className="li";
  d.innerHTML=`<span class="ld" style="background:${{c}}"></span><span>${{r}}</span>`;
  lDiv.appendChild(d);
}});
</script>
</body></html>"""

                # Download button
                import base64 as _b64
                st.download_button(
                    "⬇️ הורד גאנט כקובץ HTML",
                    data=gantt_page.encode("utf-8"),
                    file_name="gantt_workers.html",
                    mime="text/html",
                    use_container_width=True,
                )
                st.caption(f"מציג {len(all_workers)} עובדים | גלול ימינה לשעות מאוחרות יותר")

                _components.html(
                    gantt_page,
                    height=max(500, len(all_workers) * 48 + 120),
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
                        name     = r["שם"]
                        role     = r["תפקיד"]
                        btn_key  = re.sub(r"[^a-zA-Zא-ת0-9]", "_", name)
                        role_color = "#8e24aa" if role == "ראש צוות" else "#5b9bd5"

                        break_info = st.session_state["break_log"].get(name, {})
                        on_break   = bool(break_info.get("ts")) and not break_info.get("end_ts")
                        break_done = bool(break_info.get("ts")) and bool(break_info.get("end_ts"))

                        # Break duration from shift length
                        emp_row_m = live_employees[live_employees["שם"] == name]
                        if not emp_row_m.empty:
                            bl = break_label_for_employee(emp_row_m.iloc[0])
                            break_duration = 65 if bl == "הפסקה ורענון" else 45 if bl == "הפסקה" else 20
                        else:
                            break_duration = 45

                        # Worker card
                        if on_break:
                            card_bg, card_border = "#fef3c7", role_color
                            card_label = f'☕ בהפסקה'
                        elif break_done:
                            card_bg, card_border = "#d1fae5", role_color
                            card_label = f'✅ הפסקה הסתיימה'
                        else:
                            card_bg, card_border = "#fff", role_color
                            card_label = ""

                        st.markdown(
                            f'<div style="direction:rtl;background:{card_bg};border:1px solid #e0e8f4;'
                            f'border-right:4px solid {card_border};border-radius:8px;'
                            f'padding:6px 12px;margin-bottom:2px;font-size:13px;">'
                            f'<strong style="color:#071b3a;">{safe_html(name)}</strong>'
                            f'&nbsp;<span style="color:{role_color};font-weight:800;">({safe_html(role)})</span>'
                            + (f'&nbsp;&nbsp;<span style="color:#92400e;">{card_label}</span>' if card_label else '') +
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        # Buttons row
                        col_start, col_end, col_reset = st.columns([2, 2, 1])
                        with col_start:
                            if not on_break and not break_done:
                                if st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}", use_container_width=True):
                                    import time as _time
                                    st.session_state["break_log"][name] = {"ts": int(_time.time()), "end_ts": None, "end": None, "start": ""}
                                    st.rerun()
                            else:
                                st.button("▶ התחל הפסקה", key=f"brk_start_{btn_key}", disabled=True, use_container_width=True)

                        with col_end:
                            if on_break:
                                if st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}", use_container_width=True):
                                    import time as _time2
                                    st.session_state["break_log"][name]["end_ts"] = int(_time2.time())
                                    st.session_state["break_log"][name]["end"] = "done"
                                    st.rerun()
                            else:
                                st.button("⏹ סיים הפסקה", key=f"brk_end_{btn_key}", disabled=True, use_container_width=True)

                        with col_reset:
                            if break_info:
                                if st.button("↺", key=f"brk_reset_{btn_key}", help="אפס הפסקה"):
                                    st.session_state["break_log"].pop(name, None)
                                    st.rerun()

                        # Timer — self-contained iframe with Unix timestamps
                        if on_break or break_done:
                            import streamlit.components.v1 as _comp_brk
                            s_ts    = int(break_info.get("ts") or 0)
                            e_ts    = int(break_info.get("end_ts") or 0)
                            done_js = "true" if break_done else "false"
                            _comp_brk.html(f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;font-family:Arial,sans-serif;direction:rtl;">
<div id="b" style="padding:6px 12px;border-radius:8px;font-size:13px;font-weight:800;
     border:1px solid #fbbf24;background:#fff8e1;color:#92400e;"><span id="m">...</span></div>
<script>
(function(){{
  var sTs={s_ts}, eTs={e_ts}, dur={break_duration}*60, done={done_js};
  function fmt(ts){{var d=new Date(ts*1000);return String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');}}
  var b=document.getElementById('b'), m=document.getElementById('m');
  if(done){{
    b.style.background='#d1fae5'; b.style.borderColor='#10b981'; b.style.color='#065f46';
    m.textContent='✅ הפסקה: '+fmt(sTs)+' – '+fmt(eTs)+' ('+Math.round((eTs-sTs)/60)+' דק׳)';
    return;
  }}
  function tick(){{
    var now=Math.floor(Date.now()/1000), rem=dur-(now-sTs);
    if(rem<=0){{b.style.background='#ffe4e4';b.style.borderColor='#ef4444';b.style.color='#991b1b';m.textContent='⚠️ זמן ההפסקה הסתיים — חזרה לעבודה!';return;}}
    var mn=Math.floor(rem/60), sc=rem%60;
    m.textContent='☕ בהפסקה מ-'+fmt(sTs)+' | נותרו '+mn+':'+String(sc).padStart(2,'0')+' מתוך {break_duration} דק׳';
  }}
  tick(); setInterval(tick,1000);
}})();
</script></body></html>""", height=44)
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
