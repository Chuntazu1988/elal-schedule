# =========================
# CONSTANTS & RULE SETTINGS
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

# Early morning shift: starts 02:00-02:59, ends 08:00-09:30
EARLY_MORNING_START_MAX = 3 * 60       # 03:00
EARLY_MORNING_END_MIN   = 8 * 60       # 08:00
EARLY_MORNING_END_MAX   = 9 * 60 + 30  # 09:30

# Night shift: starts before midnight (21:00-23:59), ends 06:00-08:30
NIGHT_START_MIN = 21 * 60       # 21:00
NIGHT_END_MIN   = 6  * 60       # 06:00
NIGHT_END_MAX   = 8  * 60 + 30  # 08:30

# Late shift: ends by 01:30 — preferred for flights up to 01:30
LATE_SHIFT_END_MAX = 1 * 60 + 30  # 01:30

MAX_CONTINUOUS_WORK_MINUTES = 4 * 60  # 4 hours max without break
NIGHT_BREAK_WINDOW_START = 0 * 60    # 00:00
NIGHT_BREAK_WINDOW_END   = 2 * 60    # 02:00
