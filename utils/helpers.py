import re
import html
from datetime import datetime, timedelta

import pandas as pd

from utils.constants import (
    EARLY_MORNING_START_MAX, EARLY_MORNING_END_MIN, EARLY_MORNING_END_MAX,
    NIGHT_START_MIN, NIGHT_END_MIN, NIGHT_END_MAX, LATE_SHIFT_END_MAX,
)


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


# =========================
# TIME UTILITIES
# =========================

def name_key(value) -> str:
    """Normalize name: no spaces, lowercase, double-yod = single-yod."""
    text = re.sub(r"\s+", "", clean_text(value)).lower()
    text = text.replace("יי", "י")
    return text


def name_key_reversed(value) -> str:
    """Return name_key of the reversed word order."""
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
# ROLE HELPERS
# =========================

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
        "דיילת":      ("דייל",         "דיילת"),
        "מתאם תורים": ("מתאם תורים",   "מתאמת תורים"),
        "מפקח TSA":   ("מפקח TSA",     "מפקחת TSA"),
        "שומר TSA":   ("שומר TSA",     "שומרת TSA"),
    }

    if base in gender_map:
        male_form, female_form = gender_map[base]
        return male_form if is_male else female_form

    return base


def role_area(role):
    """Operational area for each task."""
    role = normalize_role_label(role)
    if role in {"ראש צוות", "דיילת", "מתאם תורים", "מפקח TSA", "שומר TSA", "טרייני רצ"}:
        return "שערי יציאה"
    return "דלפקי צ׳ק אין"


def default_area_for_employee(emp_row):
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
    emp_name = emp["שם"]
    target_area = role_area(role)
    history = employee_area_history(assignments, emp_name)

    if not history:
        default_area = default_area_for_employee(emp)
        return 0 if default_area == target_area else 2

    if target_area in history:
        return 0

    return 5


# =========================
# SHIFT HELPERS
# =========================

def classify_shift(emp):
    """Returns one of: 'early_morning', 'night', 'late', 'day', 'unknown'"""
    ss = clean_text(emp.get("תחילת משמרת", ""))
    se = clean_text(emp.get("סוף משמרת",   ""))
    if not is_time_text(ss) or not is_time_text(se):
        return "unknown"

    s = time_to_minutes(ss)
    e = time_to_minutes(se)

    if s < EARLY_MORNING_START_MAX and EARLY_MORNING_END_MIN <= e <= EARLY_MORNING_END_MAX:
        return "early_morning"

    if s >= NIGHT_START_MIN:
        if e < s and NIGHT_END_MIN <= e <= NIGHT_END_MAX:
            return "night"

    if e <= LATE_SHIFT_END_MAX and e < s:
        return "late"
    if e <= LATE_SHIFT_END_MAX and s > 12 * 60:
        return "late"

    return "day"


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


def employee_shift_text(employees_df, emp_name):
    emp = employees_df[employees_df["שם"] == emp_name]
    if emp.empty:
        return ""
    row = emp.iloc[0]
    s = clean_text(row.get("תחילת משמרת", ""))
    e = clean_text(row.get("סוף משמרת", ""))
    if s and e:
        return f"{s}-{e}"
    return ""


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
        return 20
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
    remaining = minutes_until_shift_end(emp_row, task_end_dt)
    if remaining is None:
        return "חזרה"
    if remaining <= 30:
        return "חזרה הביתה"
    return "חזרה לדלפקים"


def break_deadline_before_flight(emp, task_start_minutes):
    """
    For early morning shifts: latest time employee must START break
    so they can: break (45 min) + walk to gate (15 min) + arrive on time.
    Returns HH:MM string, or None if not applicable.
    """
    if classify_shift(emp) != "early_morning":
        return None

    deadline_min = task_start_minutes - 15 - 45
    if deadline_min < 0:
        deadline_min += 1440
    h = (deadline_min // 60) % 24
    m = deadline_min % 60
    return f"{h:02d}:{m:02d}"


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


def continuation_text_for_employee(timed_df, current_idx, emp, employees_df):
    next_plain = next_task_plain_text(timed_df, current_idx, emp)

    if next_plain:
        return next_plain

    row = timed_df.loc[current_idx]
    emp_row = employees_df[employees_df["שם"] == emp]
    if emp_row.empty:
        return "חזרה"

    task_end_dt = to_datetime_time(row["סיום"])
    return return_text_by_shift(emp_row.iloc[0], task_end_dt)

