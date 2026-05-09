"""CSS styles for iSchedule application."""

CSS = """
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

.ops-title {
    font-size: 34px;
    font-weight: 900;
    margin: 0;
    position: relative;
    z-index: 2;
}

.ops-subtitle {
    color: #d8e8ff;
    font-size: 18px;
    font-weight: 800;
    margin-top: 8px;
    position: relative;
    z-index: 2;
}

.flight-card {
    direction: rtl;
    text-align: right;
    border: 1px solid #cfd9e8;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 3px 12px rgba(0,0,0,.07);
    overflow: hidden;
    margin-bottom: 14px;
}

.flight-head {
    background:
      radial-gradient(circle at 12% 10%, rgba(255,255,255,.14), transparent 24%),
      linear-gradient(90deg, #06172f 0%, #092b58 48%, #071b3a 100%);
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

.flight-name::before {
    content: "LY ";
    color: #ffd166;
    font-size: 12px;
    margin-left: 5px;
    letter-spacing: 1px;
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
    display: inline-block;
    max-width: 100%;
}

.panel-title {
    direction: rtl;
    text-align: right;
    color: #0b3d78;
    font-size: 16px;
    font-weight: 900;
    margin: 8px 0 8px 0;
    background: #eef5ff;
    border: 1px solid #d9e8fb;
    border-radius: 10px;
    padding: 8px 10px;
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
    font-weight: 750;
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
    width: 13px;
    height: 13px;
    border-radius: 50%;
    display: inline-block;
    border: 1px solid rgba(0,0,0,.18);
}

.legend-color-name { color: #475467; font-weight: 900; }
.legend-role-name  { color: #071b3a; font-weight: 900; }

.dot-teamlead  { background: #8e24aa; }
.dot-agent     { background: #9fb7d7; }
.dot-queue     { background: #f0a000; }
.dot-inspector { background: #d32f2f; }
.dot-guard     { background: #2e7d32; }
.dot-trainee   { background: #ffd54f; }
.dot-missing   { background: #9b0000; }

body { background: #f4f7fb; }

/* Swap row styles */
.swap-row-wrap { position: relative; margin-bottom: 7px; }
.swap-row-wrap .assignment-line {
    margin-bottom: 0;
    cursor: default;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
}

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

@media (max-width: 850px) {
    .ops-title      { font-size: 25px; }
    .ops-subtitle   { font-size: 15px; }
    .flight-name    { font-size: 18px; }
    .ops-top-strip  { grid-template-columns: repeat(2, 1fr); }
    .legend-grid    { grid-template-columns: 1fr; }
    .legend-item    { grid-template-columns: 16px 70px 1fr; }
}
</style>
"""

HERO_HTML = """
<div class="ops-hero">
  <div class="ops-title">iSchedule 👩🏼‍🔧</div>
  <div class="ops-subtitle">סידור עבודה? קטן עלי!</div>
</div>
"""

LEGEND_HTML = """
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
"""

TOP_STRIP_HTML = """
<div class="ops-top-strip">
  <div class="ops-mini-card">🛫 המראות<span>סידור לפי טיסה</span></div>
  <div class="ops-mini-card">🧳 דלפקים<span>Check-in continuity</span></div>
  <div class="ops-mini-card">🚪 שערים<span>Boarding gates</span></div>
  <div class="ops-mini-card">🛡️ TSA<span>יעדים מיוחדים</span></div>
</div>
"""
