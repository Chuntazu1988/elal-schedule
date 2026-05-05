import io
import re
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter


st.set_page_config(page_title="מערכת שיבוץ טיסות", page_icon="✈️", layout="wide")

st.markdown("""
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 900;
    color: #003B7A;
}
.sub-title {
    color: #5f6f89;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)
</style>
""", unsafe_allow_html=True)
}
.main-title {
    font-size: 36px;
    font-weight: 900;
    color: #003B7A;
    margin-bottom: 0;
}
.sub-title {
    color: #5f6f89;
    font-size: 16px;
    margin-top: 0;
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">✈️ מערכת שיבוץ טיסות</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">סידור יומי + עובדים → השלמת נתונים → שיבוץ חכם → הורדת אקסל</p>', unsafe_allow_html=True)


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


def normalize_yes_no(value):
    text = str(value).strip().upper()
    return "כן" if text in {"Y", "YES", "כן", "TRUE", "1", "V", "✓", "✔"} else "לא"


def parse_times(value):
    text = str(value).strip()
    match = re.search(r"(\d{2}:\d{2})\s*\((\d{2}:\d{2})\)", text)
    if not match:
        return "", ""
    return match.group(1), match.group(2)


def load_daily_schedule(uploaded_file):
    raw = pd.read_excel(uploaded_file, sheet_name="דוח שיבוץ טיסות - המראות")
    raw.columns = raw.columns.astype(str).str.strip()

    flights = []

    for _, row in raw.iterrows():
        flight = row.get("Unnamed: 8")
        time_text = row.get("Unnamed: 7")
        destination = row.get("Unnamed: 6")
        aircraft = row.get("Unnamed: 5")

        if pd.isna(flight):
            continue

        flight_text = str(flight).strip()
        if not flight_text.startswith("LY"):
            continue

        departure, boarding = parse_times(time_text)

        flights.append({
            "טיסה": flight_text,
            "יעד": "" if pd.isna(destination) else str(destination).strip().upper(),
            "המראה": departure,
            "בורדינג": boarding,
            "גייט": "",
            "סוג מטוס": "" if pd.isna(aircraft) else str(aircraft).strip(),
            "רישוי": "",
            "נוסעים": "",
            "טרייני רצ": "לא",
            "סוג הכשרה": "",
        })

    return pd.DataFrame(flights)


def normalize_employees(employees_df):
    employees_df = employees_df.copy()
    employees_df.columns = employees_df.columns.astype(str).str.strip()

    aliases = {
        "מפקח tsa": "מפקח TSA",
        "שומר tsa": "שומר TSA",
        "טרייני ר״צ": "טרייני רצ",
        'טרייני ר"צ': "טרייני רצ",
        "ראש צוות חונך": "חונך רצים",
        "ראש צוות מסמיך": "מסמיך רצים",
    }

    for old, new in aliases.items():
        if old in employees_df.columns and new not in employees_df.columns:
            employees_df[new] = employees_df[old]

    for col in ROLE_COLUMNS:
        if col not in employees_df.columns:
            employees_df[col] = "לא"
        employees_df[col] = employees_df[col].apply(normalize_yes_no)

    for col in ["תחילת משמרת", "סוף משמרת"]:
        if col not in employees_df.columns:
            employees_df[col] = ""

    return employees_df


def to_datetime_time(value):
    return datetime.strptime(str(value).strip(), "%H:%M")


def time_to_minutes(value):
    h, m = str(value).strip().split(":")
    return int(h) * 60 + int(m)


def safe_time_text(value):
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def get_body_type(flight):
    reg = str(flight.get("רישוי", "")).upper().strip()
    aircraft = str(flight.get("סוג מטוס", "")).upper().strip()

    if reg.startswith(NARROW_REG_PREFIXES):
        return "צר גוף"
    if reg.startswith(WIDE_REG_PREFIXES):
        return "רחב גוף"
    if aircraft.startswith(("737", "738", "739", "E")):
        return "צר גוף"

    return "רחב גוף"


def is_remote_gate(gate):
    return str(gate).upper().strip() in REMOTE_GATES


def get_pax(flight):
    value = flight.get("נוסעים", 0)
    if pd.isna(value) or str(value).strip() == "":
        return 0
    try:
        return int(float(value))
    except Exception:
        return 0


def get_requirements(flight):
    dest = str(flight["יעד"]).upper().strip()
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

    if str(flight.get("טרייני רצ", "")).strip() == "כן":
        req["טרייני רצ"] = 1

    return req


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


def is_within_shift(emp, start, end):
    shift_start = str(emp.get("תחילת משמרת", "")).strip()
    shift_end = str(emp.get("סוף משמרת", "")).strip()

    if shift_start in {"", "nan", "לא"} or shift_end in {"", "nan", "לא"}:
        return True

    task_start = start.hour * 60 + start.minute
    task_end = end.hour * 60 + end.minute

    s = time_to_minutes(shift_start)
    e = time_to_minutes(shift_end)

    if e < s:
        if task_start < s:
            task_start += 24 * 60
            task_end += 24 * 60
        e += 24 * 60

    return task_start >= s and task_end <= e


def shift_length(emp):
    s_text = str(emp.get("תחילת משמרת", "")).strip()
    e_text = str(emp.get("סוף משמרת", "")).strip()

    if s_text in {"", "nan", "לא"} or e_text in {"", "nan", "לא"}:
        return 0

    s = time_to_minutes(s_text)
    e = time_to_minutes(e_text)

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


def assigned_minutes(assignments, emp_name):
    total = 0

    for task in assignments:
        if task["עובד"] != emp_name:
            continue

        if not task["התחלה"] or not task["סיום"]:
            continue

        total += int(
            (to_datetime_time(task["סיום"]) - to_datetime_time(task["התחלה"])).total_seconds() / 60
        )

    return total


def has_room_for_break(assignments, emp, emp_name, start, end):
    length = shift_length(emp)

    if length == 0:
        return True

    current = assigned_minutes(assignments, emp_name)
    new = int((end - start).total_seconds() / 60)

    return current + new + required_break(emp) <= length


def is_available(assignments, emp_name, start, end):
    buffer = timedelta(minutes=5)

    for task in assignments:
        if task["עובד"] != emp_name:
            continue

        if not task["התחלה"] or not task["סיום"]:
            continue

        existing_start = to_datetime_time(task["התחלה"])
        existing_end = to_datetime_time(task["סיום"])

        if not (start >= existing_end + buffer or end <= existing_start - buffer):
            return False

    return True


def count_team_lead_tasks(assignments, emp_name):
    return sum(
        1 for task in assignments
        if task["עובד"] == emp_name and str(task["תפקיד"]).startswith("ראש צוות")
    )


def sort_candidates(candidates, assignments, role):
    candidates = candidates.copy()

    if role == "ראש צוות":
        candidates["_score"] = candidates["שם"].apply(
            lambda name: count_team_lead_tasks(assignments, name)
        )
        return candidates.sort_values("_score")

    if role == "דייל":
        candidates["_score"] = candidates.apply(
            lambda row: 0 if str(row.get("ראש צוות", "")).strip() == "כן" else 1,
            axis=1
        )
        return candidates.sort_values("_score")

    return candidates


def has_required_mentor(assignments_for_flight, employees_df, training_type):
    required_col = "מסמיך רצים" if training_type == "הסמכה" else "חונך רצים"

    for task in assignments_for_flight:
        if str(task["תפקיד"]).startswith("ראש צוות") and "❌" not in str(task["עובד"]):
            emp = employees_df[employees_df["שם"] == task["עובד"]]

            if not emp.empty and str(emp.iloc[0].get(required_col, "")).strip() == "כן":
                return True

    return False


def build_schedule(flights_df, employees_df):
    assignments = []
    role_order = ["ראש צוות", "טרייני רצ", "דייל", "מתאם תורים", "מפקח TSA", "שומר TSA"]

    flights_df = flights_df[flights_df["המראה"].astype(str).str.strip() != ""].copy()

    for _, flight in flights_df.iterrows():
        req = get_requirements(flight)
        used_on_flight = set()
        assignments_for_flight = []

        trainee_needed = req.get("טרייני רצ", 0) > 0
        training_type = str(flight.get("סוג הכשרה", "חניכה")).strip()

        for role in role_order:
            amount = req.get(role, 0)

            for i in range(amount):
                start = role_start_time(flight, role)
                end = role_end_time(flight)

                if role not in employees_df.columns:
                    employees_df[role] = "לא"

                candidates = employees_df[
                    (employees_df[role].astype(str).str.strip() == "כן") &
                    (~employees_df["שם"].isin(used_on_flight))
                ]

                if role == "ראש צוות" and trainee_needed:
                    mentor_col = "מסמיך רצים" if training_type == "הסמכה" else "חונך רצים"
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
                    used_on_flight.add(worker)
                else:
                    worker = f"❌ חסר {role}"

                task = {
                    "טיסה": flight["טיסה"],
                    "יעד": flight["יעד"],
                    "תפקיד": role if amount == 1 else f"{role} {i+1}",
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
                "עובד": "❌ אין חונך/מסמיך מתאים בטיסה",
                "התחלה": "",
                "סיום": "",
            })

    return pd.DataFrame(assignments)


def get_employee_shift(employees_df, emp_name):
    emp = employees_df[employees_df["שם"] == emp_name]

    if emp.empty:
        return ""

    emp = emp.iloc[0]
    s = str(emp.get("תחילת משמרת", "")).strip()
    e = str(emp.get("סוף משמרת", "")).strip()

    if s and e and s != "nan" and e != "nan":
        return f"{s}-{e}"

    return ""


def build_next_task_labels(result_df, employees_df):
    df = result_df.copy()
    timed_df = df[df["התחלה"].astype(str).str.strip() != ""].copy()
    timed_df["_start_dt"] = pd.to_datetime(timed_df["התחלה"], format="%H:%M", errors="coerce")

    break_used = {}
    labels = {}

    for idx, row in timed_df.sort_values("_start_dt").iterrows():
        emp = str(row["עובד"]).strip()

        if "❌" in emp:
            labels[idx] = emp
            continue

        emp_row = employees_df[employees_df["שם"] == emp]
        needs_break = not emp_row.empty and required_break(emp_row.iloc[0]) > 0

        future = timed_df[
            (timed_df["עובד"].astype(str) == emp) &
            (timed_df["_start_dt"] > row["_start_dt"])
        ].sort_values("_start_dt")

        if needs_break and not break_used.get(emp, False):
            break_used[emp] = True

            if future.empty:
                next_text = "הפסקה וחזרה"
            else:
                next_text = f'הפסקה וטיסה {future.iloc[0]["טיסה"]}'
        else:
            if future.empty:
                next_text = "סוף משמרת"
            else:
                next_text = f'טיסה {future.iloc[0]["טיסה"]}'

        shift = get_employee_shift(employees_df, emp)
        labels[idx] = f"{emp} ({shift}) - {next_text}" if shift else f"{emp} - {next_text}"

    df["טקסט עובד"] = df.index.map(labels).fillna(df["עובד"].astype(str))

    return df


def build_workload(result_df, employees_df):
    rows = []
    timed = result_df[result_df["התחלה"].astype(str).str.strip() != ""].copy()

    real_workers = sorted([
        worker for worker in timed["עובד"].dropna().unique()
        if "❌" not in str(worker)
    ])

    for emp in real_workers:
        tasks = timed[timed["עובד"] == emp]
        total = 0

        for _, task in tasks.iterrows():
            total += int(
                (to_datetime_time(task["סיום"]) - to_datetime_time(task["התחלה"])).total_seconds() / 60
            )

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


def build_output_table(flights_df, result_labeled):
    rows = []

    for _, flight in flights_df.iterrows():
        fnum = str(flight["טיסה"]).strip()
        dep = safe_time_text(flight.get("המראה", ""))
        boarding = safe_time_text(flight.get("בורדינג", ""))
        aircraft = safe_time_text(flight.get("סוג מטוס", ""))
        reg = safe_time_text(flight.get("רישוי", ""))

        tasks = result_labeled[result_labeled["טיסה"].astype(str).str.strip() == fnum]

        column_e = []
        column_f = []

        for _, task in tasks.iterrows():
            role = str(task["תפקיד"])
            text = f'{role}: {task["טקסט עובד"]}'

            if "ראש צוות" in role or "מתאם" in role or "מפקח TSA" in role:
                column_e.append(text)
            elif "דייל" in role or "שומר TSA" in role or "בדיקת טרייני" in role:
                column_f.append(text)

        rows.append({
            "מספר טיסה": fnum,
            "יעד": str(flight["יעד"]).strip(),
            "זמנים": f"{dep} ({boarding})" if boarding else dep,
            "מטוס/רישוי": f"{aircraft}\n{reg}".strip(),
            "ראש צוות / מתאם תורים / מפקח TSA": "\n".join(column_e),
            "דיילים / שומר TSA": "\n".join(column_f),
        })

    return pd.DataFrame(rows)


def to_excel_bytes(output_df, workload_df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        output_df.to_excel(writer, index=False, sheet_name="שיבוץ")
        workload_df.to_excel(writer, index=False, sheet_name="עומס")

        wb = writer.book
        ws = wb["שיבוץ"]

        ws.sheet_view.rightToLeft = True
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        header_fill = PatternFill("solid", fgColor="1F4E78")
        header_font = Font(color="FFFFFF", bold=True, size=12)

        purple_fill = PatternFill("solid", fgColor="EADCF8")
        red_fill = PatternFill("solid", fgColor="F4CCCC")
        green_fill = PatternFill("solid", fgColor="D9EAD3")
        blue_fill = PatternFill("solid", fgColor="D9EAF7")

        thin = Side(style="thin", color="B7B7B7")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border

        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                cell.border = border

            col_e = str(row[4].value)
            col_f = str(row[5].value)

            if "❌" in col_e or "מפקח TSA" in col_e:
                row[4].fill = red_fill
            elif "ראש צוות" in col_e:
                row[4].fill = purple_fill

            if "❌" in col_f:
                row[5].fill = red_fill
            elif "שומר TSA" in col_f:
                row[5].fill = green_fill
            elif "דייל" in col_f:
                row[5].fill = blue_fill

        for col, width in {
            "A": 16,
            "B": 10,
            "C": 18,
            "D": 18,
            "E": 60,
            "F": 60,
        }.items():
            ws.column_dimensions[col].width = width

        for row_num in range(1, ws.max_row + 1):
            ws.row_dimensions[row_num].height = 70

        ws2 = wb["עומס"]
        ws2.sheet_view.rightToLeft = True
        ws2.freeze_panes = "A2"
        ws2.auto_filter.ref = ws2.dimensions

        for cell in ws2[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border

        for row in ws2.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                cell.border = border

        for col_idx in range(1, ws2.max_column + 1):
            ws2.column_dimensions[get_column_letter(col_idx)].width = 20

    output.seek(0)

    return output


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

st.subheader("🛫 טיסות שנמצאו מהסידור היומי")
st.caption("השלימי כאן גייט, רישוי ומספר נוסעים. אפשר גם לתקן סוג מטוס/שעה אם צריך.")

edited_flights = st.data_editor(
    flights_df,
    use_container_width=True,
    num_rows="dynamic",
    key="flights_editor",
)

col1, col2, col3 = st.columns(3)
col1.metric("טיסות", len(edited_flights))
col2.metric("עובדים", len(employees_df))
col3.metric("יעדי TSA", edited_flights["יעד"].isin(list(USA_TSA_DESTS)).sum())

if st.button("🚀 בנה שיבוץ", use_container_width=True):
    try:
        schedule_df = build_schedule(edited_flights, employees_df)
        labeled_df = build_next_task_labels(schedule_df, employees_df)
        workload_df = build_workload(schedule_df, employees_df)
        output_df = build_output_table(edited_flights, labeled_df)

        st.success("השיבוץ נבנה בהצלחה!")

        tab1, tab2, tab3 = st.tabs(["✈️ שיבוץ", "❌ חוסרים", "📊 עומס עובדים"])

        with tab1:
            st.markdown("## ✈️ שיבוץ טיסות")

            search = st.text_input("🔎 חיפוש לפי טיסה / יעד / עובד")

            display_df = output_df.copy()

            if search:
                mask = display_df.astype(str).apply(
                    lambda row: row.str.contains(search, case=False, na=False).any(),
                    axis=1
                )
                display_df = display_df[mask]

            for _, row in display_df.iterrows():
                flight = row["מספר טיסה"]
                dest = row["יעד"]
                times = row["זמנים"]
                aircraft = str(row["מטוס/רישוי"]).replace("\n", " / ")

                with st.container(border=True):
                    st.markdown(f"### ✈️ {flight} → {dest}")
                    st.caption(f"🕒 {times} | 🛩️ {aircraft}")

                    card_col1, card_col2 = st.columns(2)

                    with card_col1:
                        st.markdown("#### 👔 ניהול / TSA")
                        left = str(row["ראש צוות / מתאם תורים / מפקח TSA"])

                        if left and left != "nan":
                            for line in left.split("\n"):
                                if "❌" in line:
                                    st.error(line)
                                elif "ראש צוות" in line:
                                    st.markdown(f"🟣 **{line}**")
                                elif "מפקח TSA" in line:
                                    st.markdown(f"🔴 **{line}**")
                                else:
                                    st.markdown(f"🔵 {line}")
                        else:
                            st.warning("אין שיבוץ")

                    with card_col2:
                        st.markdown("#### 🧍 דיילים / שומר TSA")
                        right = str(row["דיילים / שומר TSA"])

                        if right and right != "nan":
                            for line in right.split("\n"):
                                if "❌" in line:
                                    st.error(line)
                                elif "שומר TSA" in line:
                                    st.markdown(f"🟢 **{line}**")
                                else:
                                    st.markdown(f"⚪ {line}")
                        else:
                            st.warning("אין שיבוץ")

        with tab2:
            st.markdown("## ❌ חוסרים")

            missing = schedule_df[schedule_df["עובד"].astype(str).str.contains("❌", na=False)]

            if missing.empty:
                st.success("אין חוסרים 🎉")
            else:
                st.warning(f"נמצאו {len(missing)} חוסרים")
                st.dataframe(missing, use_container_width=True)

        with tab3:
            st.markdown("## 📊 עומס עובדים")
            st.dataframe(workload_df, use_container_width=True)

        excel_data = to_excel_bytes(output_df, workload_df)

        st.download_button(
            "⬇️ הורדת אקסל שיבוץ",
            data=excel_data,
            file_name="SCHEDULE_PROFESSIONAL.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("הייתה שגיאה בבניית השיבוץ.")
        st.exception(exc)