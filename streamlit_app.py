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
  <b>מקרא צבעים:</b>
  <span class="legend-item"><span class="legend-dot dot-teamlead"></span>ראש צוות</span>
  <span class="legend-item"><span class="legend-dot dot-agent"></span>דיילת</span>
  <span class="legend-item"><span class="legend-dot dot-queue"></span>מתאם תורים</span>
  <span class="legend-item"><span class="legend-dot dot-inspector"></span>מפקח TSA</span>
  <span class="legend-item"><span class="legend-dot dot-guard"></span>שומר TSA</span>
  <span class="legend-item"><span class="legend-dot dot-trainee"></span>טרייני רצ</span>
  <span class="legend-item"><span class="legend-dot dot-missing"></span>חוסר שיבוץ</span>
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
        return "טרייני רצ"
    return role


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
    minutes = required_break(emp_row)
    if minutes >= 65:
        return "הפסקה ורענון"
    if minutes >= 45:
        return "הפסקה"
    return ""


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

    for col in ["תחילת משמרת", "סוף משמרת"]:
        if col not in df.columns:
            df[col] = ""
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
        req["דייל"] = 5 if dest in USA_TSA_DESTS else 3

    if dest in TWO_TEAM_LEADS_DESTS:
        req["ראש צוות"] = 2

    if dest in QUEUE_DESTS:
        req["מתאם תורים"] = 1

    if dest in USA_TSA_DESTS:
        req["מפקח TSA"] = 1
        req["שומר TSA"] = 1

    # טרייני רצ לא נקבע מטבלת הטיסות.
    # הוא יתווסף אוטומטית במנוע השיבוץ לפי טבלת העובדים, אם יש טרייני זמין.
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


def required_break(emp):
    length = shift_length(emp)
    if length > 9 * 60 + 30:
        return 65
    if length > 6 * 60:
        return 45
    return 0


def is_within_shift(emp, task_start, task_end):
    shift_start = clean_text(emp.get("תחילת משמרת", ""))
    shift_end = clean_text(emp.get("סוף משמרת", ""))

    if not is_time_text(shift_start) or not is_time_text(shift_end):
        return True

    task_start_min = task_start.hour * 60 + task_start.minute
    task_end_min = task_end.hour * 60 + task_end.minute

    s = time_to_minutes(shift_start)
    e = time_to_minutes(shift_end)

    if e < s:
        if task_start_min < s:
            task_start_min += 24 * 60
            task_end_min += 24 * 60
        e += 24 * 60

    return task_start_min >= s and task_end_min <= e


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
        return True

    current = assigned_minutes(assignments, emp_name)
    new = minutes_between(start, end)
    return current + new + required_break(emp) <= length


def is_available(assignments, emp_name, start, end):
    buffer = timedelta(minutes=5)

    for task in assignments:
        if task["עובד"] != emp_name:
            continue
        if clean_text(task.get("התחלה", "")) == "" or clean_text(task.get("סיום", "")) == "":
            continue

        existing_start = to_datetime_time(task["התחלה"])
        existing_end = to_datetime_time(task["סיום"])

        if not (start >= existing_end + buffer or end <= existing_start - buffer):
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


def sort_candidates(candidates, assignments, role):
    candidates = candidates.copy()

    if candidates.empty:
        return candidates

    candidates["_area_penalty"] = candidates.apply(
        lambda row: area_switch_penalty(assignments, row, role),
        axis=1,
    )
    candidates["_task_count"] = candidates["שם"].apply(lambda name: count_all_tasks(assignments, name))

    if role == "ראש צוות":
        candidates["_role_count"] = candidates["שם"].apply(lambda name: count_team_lead_tasks(assignments, name))
        return candidates.sort_values(["_area_penalty", "_role_count", "_task_count"])

    if role == "דייל":
        # Prefer team-lead-qualified employees as flight agents only when appropriate,
        # but still avoid area switching and balance workload.
        candidates["_role_fit"] = candidates.apply(
            lambda row: 0 if str(row.get("ראש צוות", "")).strip() == "כן" else 1,
            axis=1,
        )
        return candidates.sort_values(["_area_penalty", "_role_fit", "_task_count"])

    return candidates.sort_values(["_area_penalty", "_task_count"])

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
        # אם יש עובדים שמסומנים כטרייני רצ בטבלת העובדים,
        # המערכת תנסה לשבץ טרייני רצ לטיסה עם ר״צ חונך/מסמיך.
        if has_trainee_available(employees_df):
            req["טרייני רצ"] = 1

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

                candidates = sort_candidates(candidates, assignments, role)

                selected = None
                for _, emp in candidates.iterrows():
                    name = emp["שם"]

                    if (
                        is_within_shift(emp, start, end)
                        and is_available(assignments, name, start, end)
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

        if trainee_needed and not has_required_mentor(assignments_for_flight, employees_df, training_type):
            assignments.append({
                "טיסה": flight["טיסה"],
                "יעד": flight["יעד"],
                "תפקיד": "בדיקת טרייני",
                "תפקיד בסיס": "בדיקת טרייני",
                "עובד": "❌ אין חונך/מסמיך מתאים בטיסה",
                "התחלה": "",
                "סיום": "",
            })

    return pd.DataFrame(assignments)


# =========================
# OUTPUT TABLES
# =========================

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

    break_used = {}
    HELP_THRESHOLD_MINUTES = 120

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

        next_plain = next_task_plain_text(timed_df, idx, emp)
        task_end_dt = to_datetime_time(row["סיום"])
        gap_to_next = gap_minutes_to_next(timed_df, idx, emp)
        break_minutes = required_break(emp_row)
        break_text = break_label_for_employee(emp_row)
        needs_break_now = bool(break_text) and not break_used.get(emp, False)

        if next_plain:
            if needs_break_now:
                break_used[emp] = True
                if gap_to_next is not None and gap_to_next >= break_minutes:
                    remaining_after_break = gap_to_next - break_minutes
                    if remaining_after_break >= HELP_THRESHOLD_MINUTES:
                        next_text = f"{break_text} עזרה ו{next_plain}"
                    else:
                        next_text = f"{break_text} ו{next_plain}"
                else:
                    next_text = f"{break_text} ו{next_plain}"
            else:
                if gap_to_next is not None and gap_to_next >= HELP_THRESHOLD_MINUTES:
                    next_text = f"עזרה ו{next_plain}"
                else:
                    next_text = next_plain
        else:
            return_text = return_text_by_shift(emp_row, task_end_dt)
            if needs_break_now:
                break_used[emp] = True
                next_text = f"{break_text} ו{return_text}"
            else:
                next_text = return_text

        df.loc[idx, "טקסט עובד"] = f"{emp} - {next_text}{shift_suffix}"
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

        for _, task in tasks.iterrows():
            role = str(task["תפקיד"])
            base_role = normalize_role_label(role)
            worker = str(task.get("עובד", ""))
            shift = employee_shift_text(employees_df, worker)
            text_value = str(task["טקסט עובד"])

            item = {"text": text_value, "role": base_role}

            if "ראש צוות" in role or "מתאם" in role or "מפקח TSA" in role:
                management_lines.append(item)
            elif "דייל" in role or "שומר TSA" in role or "בדיקת טרייני" in role:
                agents_lines.append(item)

        rows.append({
            "מספר טיסה": fnum,
            "יעד": clean_text(flight["יעד"]),
            "זמנים": f"{dep} ({boarding})" if boarding else dep,
            "מטוס/רישוי": f"{aircraft}\n{reg}".strip(),
            "תפקידים דרושים": " | ".join(reqs),
            "ראש צוות / מתאם תורים / מפקח TSA": "\n".join([f"{x['role']}||{x['text']}" for x in management_lines]),
            "דיילים / שומר TSA": "\n".join([f"{x['role']}||{x['text']}" for x in agents_lines]),
        })

    return pd.DataFrame(rows)


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
    if role == "טרייני רצ":
        return "role-trainee"
    if role == "מתאם תורים":
        return "role-queue"
    if role == "דיילת":
        return "role-agent"

    return "role-agent"


def render_line(line, current_role=""):
    st.markdown(
        f'<div class="assignment-line {line_style_by_role(current_role, line)}">{safe_html(line)}</div>',
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

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel-title">👔 ראש צוות / מתאם / TSA</div>', unsafe_allow_html=True)
        if left_text and left_text != "nan":
            for line in left_text.split("\n"):
                if "||" in line:
                    role_part, text_part = line.split("||", 1)
                    render_line(text_part, role_part)
                else:
                    render_line(line)
        else:
            render_line("אין שיבוץ")

    with c2:
        st.markdown('<div class="panel-title">🧍 דיילים / שומר TSA</div>', unsafe_allow_html=True)
        if right_text and right_text != "nan":
            for line in right_text.split("\n"):
                if "||" in line:
                    role_part, text_part = line.split("||", 1)
                    render_line(text_part, role_part)
                else:
                    render_line(line)
        else:
            render_line("אין שיבוץ")


# =========================
# EXPORT
# =========================

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
    employees_df = pd.read_excel(employees_file)
    employees_df = normalize_employees(employees_df)
except Exception as exc:
    st.error("לא הצלחתי לקרוא את הקבצים.")
    st.exception(exc)
    st.stop()

st.markdown(
    '<div class="ops-rtl"><h3>🛫 טיסות מהסידור היומי</h3>'
    '<div class="small-note">השלימי כאן גייט, רישוי, נוסעים וסוג הכשרה. טרייני רצ נקבע מטבלת העובדים בלבד.</div></div>',
    unsafe_allow_html=True,
)

# עמודת טרייני רצ יורדת מטבלת הטיסות.
# טרייני רצ נקבע מטבלת העובדים בלבד.
flights_editor_df = flights_df.drop(columns=["טרייני רצ"], errors="ignore").copy()

edited_flights = st.data_editor(
    flights_editor_df,
    use_container_width=True,
    num_rows="dynamic",
    key="flights_editor",
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("טיסות", len(edited_flights))
m2.metric("עובדים", len(employees_df))
m3.metric("יעדי TSA", edited_flights["יעד"].isin(list(USA_TSA_DESTS)).sum())
m4.metric("עובדי טרייני רצ", (employees_df["טרייני רצ"].astype(str).str.strip() == "כן").sum() if "טרייני רצ" in employees_df.columns else 0)

if st.button("🚀 בנה שיבוץ", use_container_width=True):
    try:
        schedule_df = build_schedule(edited_flights, employees_df)
        labeled_df = build_next_task_labels(schedule_df, employees_df)
        workload_df = build_workload(schedule_df, employees_df)
        continuity_df = build_counter_continuity_rows(labeled_df, employees_df)
        output_df = build_output_table(edited_flights, labeled_df, employees_df)

        missing = schedule_df[schedule_df["עובד"].astype(str).str.contains("❌", na=False)]

        st.success("השיבוץ נבנה בהצלחה.")

        tab_schedule, tab_missing, tab_workload, tab_continuity, tab_raw = st.tabs(
            ["✈️ לוח מבצעים", "❌ חוסרים", "📊 עומס עובדים", "🧭 רצף אזורי", "🧾 פירוט גולמי"]
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
                render_flight_card(row)

        with tab_missing:
            st.subheader("❌ חוסרים")
            if missing.empty:
                st.success("אין חוסרים 🎉")
            else:
                st.warning(f"נמצאו {len(missing)} חוסרים")
                st.dataframe(missing, use_container_width=True)

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
        st.error("הייתה שגיאה בבניית השיבוץ.")
        st.exception(exc)
