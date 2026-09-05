import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta
from textwrap import shorten

st.set_page_config(page_title="BhuJal · Flood Risk Command", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

#MainMenu, footer, header {visibility:hidden;}
html, body, [class*="css"] {font-family:'Manrope',system-ui,sans-serif;}

.stApp {
  background:
    radial-gradient(1200px 600px at 50% 8%, rgba(34,217,232,.10), transparent 60%),
    radial-gradient(700px 400px at 8% 0%, rgba(34,217,232,.06), transparent 60%),
    #040A12;
}
.block-container {padding-top:.8rem; padding-bottom:2rem; max-width:1780px;}

/* ---------- command bar ---------- */
.cmdbar {
  display:flex; justify-content:space-between; align-items:center;
  font-family:'IBM Plex Mono',monospace; font-size:11px;
  letter-spacing:.2em; text-transform:uppercase; color:#4E7A8C;
  border-top:1px solid #22D9E8; border-bottom:1px solid #10293A;
  padding:10px 4px; margin-bottom:18px;
  background:linear-gradient(180deg, rgba(34,217,232,.07), transparent);
}
.cmdbar b {color:#D6F3F8; font-weight:600; letter-spacing:.12em;}
.dot {display:inline-block;width:6px;height:6px;border-radius:50%;background:#22D9E8;
      margin-right:9px;vertical-align:1px;box-shadow:0 0 8px #22D9E8;
      animation:blink 2.2s ease-in-out infinite;}
@keyframes blink {0%,100%{opacity:1}50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.dot{animation:none}}

/* ---------- bracketed panels ---------- */
.panel {
  position:relative; background:rgba(10,21,32,.85); border:1px solid #12303F;
  padding:14px 16px; margin-bottom:12px;
}
.panel::before, .panel::after {
  content:""; position:absolute; width:11px; height:11px; border:1px solid #22D9E8;
}
.panel::before {top:-1px; left:-1px; border-right:0; border-bottom:0;}
.panel::after  {bottom:-1px; right:-1px; border-left:0; border-top:0;}
.panel .h {
  font-family:'IBM Plex Mono',monospace; font-size:10px; font-weight:600;
  letter-spacing:.2em; text-transform:uppercase; color:#22D9E8; margin-bottom:9px;
}
.panel .b {
  font-family:'IBM Plex Mono',monospace; font-size:12.5px; color:#CFE6EE;
  line-height:1.65; white-space:pre-wrap;
}
.panel .n {font-size:11px; color:#4E7A8C; margin-top:9px; line-height:1.5;}

/* ---------- headings ---------- */
h1 {font-weight:800; letter-spacing:-.03em; font-size:2.35rem; margin:0 0 .15rem; color:#EAF7FA;}
.eyebrow {font-family:'IBM Plex Mono',monospace; font-size:10px; font-weight:600;
          letter-spacing:.22em; text-transform:uppercase; color:#22D9E8; margin:0 0 6px;}
.sec {font-family:'IBM Plex Mono',monospace; font-size:11px; font-weight:600;
      letter-spacing:.2em; text-transform:uppercase; color:#7FA8B8;
      border-bottom:1px solid #12303F; padding-bottom:8px; margin:0 0 12px;}
.lede {color:#6E93A3; font-size:14px; margin:0 0 16px; max-width:52ch;}

/* ---------- native widgets ---------- */
[data-testid="stMetric"] {
  position:relative; background:rgba(10,21,32,.85); border:1px solid #12303F;
  padding:13px 15px; border-radius:0;
}
[data-testid="stMetric"]::before, [data-testid="stMetric"]::after {
  content:""; position:absolute; width:9px; height:9px; border:1px solid #22D9E8;
}
[data-testid="stMetric"]::before {top:-1px; left:-1px; border-right:0; border-bottom:0;}
[data-testid="stMetric"]::after  {bottom:-1px; right:-1px; border-left:0; border-top:0;}
[data-testid="stMetricValue"] {font-family:'IBM Plex Mono',monospace; font-size:1.6rem;
                               color:#EAF7FA; letter-spacing:-.02em;}
[data-testid="stMetricLabel"] {font-family:'IBM Plex Mono',monospace; font-size:.63rem;
                               font-weight:600; letter-spacing:.2em; text-transform:uppercase;
                               color:#4E7A8C;}
[data-testid="stMetricDelta"] {font-family:'IBM Plex Mono',monospace; font-size:.75rem;}

.stButton>button, [data-testid="stFormSubmitButton"]>button {border-radius:0; font-weight:700;}

/* ---------- alert band ---------- */
.band {
  position:relative; font-family:'IBM Plex Mono',monospace; font-size:12px; font-weight:600;
  letter-spacing:.16em; color:var(--c); border:1px solid var(--c);
  background:color-mix(in srgb, var(--c) 14%, transparent);
  padding:11px 14px; margin:10px 0 14px;
  box-shadow:0 0 18px color-mix(in srgb, var(--c) 22%, transparent);
}
</style>
""", unsafe_allow_html=True)

BLR = (12.9716, 77.5946)

# ---------------- DATA LAYER: Open-Meteo / ERA5 ----------------------------
@st.cache_data(ttl=900, show_spinner=False)
def forecast_rain():
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", timeout=6, params={
            "latitude": BLR[0], "longitude": BLR[1], "daily": "precipitation_sum",
            "timezone": "Asia/Kolkata", "forecast_days": 3})
        d = r.json()["daily"]
        vals = [v for v in d["precipitation_sum"] if v is not None]
        return max(vals), d["time"][vals.index(max(vals))]
    except Exception:
        return None, None

@st.cache_data(ttl=3600, show_spinner=False)
def archive_rain(day):
    try:
        r = requests.get("https://archive-api.open-meteo.com/v1/archive", timeout=8, params={
            "latitude": BLR[0], "longitude": BLR[1],
            "start_date": str(day), "end_date": str(day),
            "daily": "precipitation_sum", "timezone": "Asia/Kolkata"})
        v = r.json()["daily"]["precipitation_sum"][0]
        return None if v is None else float(v)
    except Exception:
        return None

# ---------------- WARD PROFILES (synthetic; real Bengaluru localities) -----
WARDS = pd.DataFrame([
 {"ward":"Bommanahalli",        "lat":12.9082,"lon":77.6180,"density":22400,"informal":62,"dependents":31,"ground":78,"drainage":"Poor",    "lake":True},
 {"ward":"Ejipura, Koramangala","lat":12.9352,"lon":77.6245,"density":28900,"informal":54,"dependents":28,"ground":71,"drainage":"Poor",    "lake":False},
 {"ward":"Bellandur",           "lat":12.9260,"lon":77.6762,"density":11200,"informal":33,"dependents":19,"ground":44,"drainage":"Poor",    "lake":True},
 {"ward":"Yemalur",             "lat":12.9424,"lon":77.6712,"density": 8600,"informal":41,"dependents":24,"ground":66,"drainage":"Poor",    "lake":True},
 {"ward":"HSR Layout",          "lat":12.9116,"lon":77.6474,"density":14800,"informal":12,"dependents":16,"ground":29,"drainage":"Moderate","lake":False},
 {"ward":"K R Puram",           "lat":13.0080,"lon":77.6960,"density":19300,"informal":47,"dependents":27,"ground":69,"drainage":"Moderate","lake":True},
 {"ward":"Hebbal Kempapura",    "lat":13.0450,"lon":77.5900,"density":16100,"informal":38,"dependents":22,"ground":58,"drainage":"Moderate","lake":True},
 {"ward":"Mahadevapura",        "lat":12.9920,"lon":77.6970,"density":13400,"informal":29,"dependents":18,"ground":41,"drainage":"Moderate","lake":False},
 {"ward":"Shivajinagar",        "lat":12.9860,"lon":77.6040,"density":31700,"informal":44,"dependents":26,"ground":63,"drainage":"Moderate","lake":False},
 {"ward":"Jayanagar",           "lat":12.9250,"lon":77.5938,"density":15900,"informal": 8,"dependents":21,"ground":24,"drainage":"Good",    "lake":False},
 {"ward":"Yelahanka",           "lat":13.1007,"lon":77.5963,"density": 9200,"informal":19,"dependents":17,"ground":33,"drainage":"Good",    "lake":True},
 {"ward":"Rajajinagar",         "lat":12.9910,"lon":77.5520,"density":18700,"informal":15,"dependents":23,"ground":31,"drainage":"Good",    "lake":False},
])

DRAIN_MM = {"Poor": 32, "Moderate": 58, "Good": 84}
BANDS = [(75,"RED","#FF4D4F","Take action"), (50,"ORANGE","#FF9F45","Be prepared"),
         (25,"YELLOW","#F5D547","Be updated"), (0,"GREEN","#2FE08A","No warning")]

def band_for(s):
    for cut, name, col, mean in BANDS:
        if s >= cut:
            return name, col, mean

def assess(w, rain_mm):
    """Risk = Hazard x Exposure x Vulnerability."""
    cap      = DRAIN_MM[w.drainage] * (0.75 if w.lake else 1.0)
    hazard   = min(max((rain_mm - cap) / 90.0, 0.0), 1.0)
    exposure = min(w.density / 32000.0, 1.0)
    vuln     = min((0.50*w.informal + 0.30*w.dependents + 0.20*w.ground) / 100.0, 1.0)
    score    = 100 * hazard * (0.30 + 0.70 * (0.45*exposure + 0.55*vuln))
    return round(min(score, 100)), round(hazard, 2), round(exposure, 2), round(vuln, 2), round(cap)

def action_for(band, w):
    if band == "RED":
        return f"Evacuate ground-floor homes ({w.ground}% of stock) to ward relief centre now"
    if band == "ORANGE":
        return "Pre-position boats and relief stock; residents move valuables to upper floors"
    if band == "YELLOW":
        return "Alert ward volunteers; clear storm drains; monitor hourly"
    return "Routine monitoring"

# ---------------- COMMAND BAR ---------------------------------------------
st.markdown(
    "<div class='cmdbar'><span><span class='dot'></span><b>BhuJal</b> &nbsp;·&nbsp; "
    "Ward-level flood risk &amp; early warning &nbsp;·&nbsp; Bengaluru Urban</span>"
    "<span>ERA5 rainfall &nbsp;·&nbsp; synthetic ward profiles &nbsp;·&nbsp; BBMP disaster cell</span></div>",
    unsafe_allow_html=True)

st.markdown("<div class='eyebrow'>Climate risk mapping · Early warning</div>", unsafe_allow_html=True)
st.markdown("<h1>Who is at risk, and how much.</h1>", unsafe_allow_html=True)
st.markdown("<p class='lede'>Risk = Hazard × Exposure × Vulnerability. Rainfall the ward will get, "
            "people in the way, and how badly they cope.</p>", unsafe_allow_html=True)

L, C, R = st.columns([1, 2.15, 1.15], gap="medium")

# ---------------- LEFT: INPUT ---------------------------------------------
with L:
    st.markdown("<div class='sec'>01 · Rainfall input</div>", unsafe_allow_html=True)
    mode = st.radio("Source", ["Scenario", "Live forecast", "Verify past event"], index=0,
                    label_visibility="collapsed")
    src = ""
    if mode == "Live forecast":
        mm, day = forecast_rain()
        if mm is None:
            st.warning("Forecast API unreachable — scenario slider.")
            rain = st.slider("Rainfall, 24h (mm)", 0, 160, 85, 5); src = "slider fallback"
        else:
            rain = mm; src = f"Open-Meteo forecast · {day}"
            st.metric("Forecast peak · 3 days", f"{rain:.0f} mm", day, delta_color="off")
    elif mode == "Verify past event":
        d = st.date_input("Replay date", value=date(2022, 9, 5),
                          min_value=date(1990, 1, 1), max_value=date.today() - timedelta(days=6))
        mm = archive_rain(d)
        if mm is None:
            st.warning("Archive unreachable — scenario slider.")
            rain = st.slider("Rainfall, 24h (mm)", 0, 160, 85, 5); src = "slider fallback"
        else:
            rain = mm; src = f"ERA5 reanalysis · {d}"
            st.metric("Recorded rainfall", f"{rain:.0f} mm", str(d), delta_color="off")
    else:
        rain = st.slider("Rainfall, next 24h (mm)", 0, 160, 85, 5)
        src = "scenario"

# ---------------- SCORING --------------------------------------------------
rows = []
for w in WARDS.itertuples():
    sc, h, e, v, cap = assess(w, rain)
    nm, col, mean = band_for(sc)
    rows.append({"Ward": w.ward, "Risk": sc, "Band": nm, "Colour": col, "Meaning": mean,
                 "Hazard": h, "Exposure": e, "Vulnerability": v, "Drain cap": cap,
                 "Informal %": w.informal, "Action": action_for(nm, w),
                 "lat": w.lat, "lon": w.lon})
risk = pd.DataFrame(rows).sort_values("Risk", ascending=False).reset_index(drop=True)
top  = risk.iloc[0]
red  = int((risk.Risk >= 75).sum())
amb  = int(((risk.Risk >= 50) & (risk.Risk < 75)).sum())
pop_at_risk = int(WARDS[WARDS.ward.isin(risk[risk.Risk >= 50].Ward)].density.sum() * 0.9 / 1000)

with L:
    st.markdown(f"<div class='band' style='--c:{top.Colour}'>HIGHEST · {top.Ward.upper()} · "
                f"{top.Band} · {top.Risk}/100</div>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("Red wards", red)
    m2.metric("Orange wards", amb)
    st.metric("Population exposed", f"{pop_at_risk}k")
    st.markdown(f"<div class='panel'><div class='h'>Source</div><div class='b'>{src}</div>"
                f"<div class='n'>Hazard threshold varies by ward drainage capacity; "
                f"lake-adjacent wards flood at 75% of design capacity.</div></div>",
                unsafe_allow_html=True)

# ---------------- CENTRE: MAP + TABLE -------------------------------------
with C:
    st.markdown("<div class='sec'>02 · Ward risk surface</div>", unsafe_allow_html=True)
    pts = risk[["lat", "lon"]].copy()
    pts["color"] = risk.Colour
    pts["size"]  = (risk.Risk * 7 + 150).astype(int)
    st.map(pts, color="color", size="size", zoom=10.4)

    st.dataframe(
        risk[["Ward", "Risk", "Band", "Hazard", "Exposure", "Vulnerability", "Informal %", "Action"]],
        use_container_width=True, hide_index=True, height=330,
        column_config={
            "Risk": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100,
                                                    format="%d", width="small"),
            "Band": st.column_config.TextColumn("Band", width="small"),
            "Hazard": st.column_config.NumberColumn("H", format="%.2f", width="small"),
            "Exposure": st.column_config.NumberColumn("E", format="%.2f", width="small"),
            "Vulnerability": st.column_config.NumberColumn("V", format="%.2f", width="small"),
            "Action": st.column_config.TextColumn("Recommended action", width="large"),
        })

# ---------------- RIGHT: ALERT ON THREE CHANNELS --------------------------
sms = (f"{top.Band} FLOOD ALERT {top.Ward}. {rain:.0f}mm rain in 24h. "
       f"Ground-floor homes move to ward relief centre before 6PM. "
       f"Keep documents in plastic. -BBMP")
ivr = (f"This is a flood warning from B B M P for {top.Ward}. {top.Band} alert. "
       f"Heavy rain is expected today. If water enters your home, go to the ward relief centre. "
       f"Press 1 to hear this again.")

with R:
    st.markdown("<div class='sec'>03 · Alert dispatch</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><div class='h'>01 · Officer dashboard</div><div class='b'>"
        f"{top.Ward}\nRISK {top.Risk}/100 · {top.Band}\n"
        f"H {top.Hazard}  ×  E {top.Exposure}  ×  V {top.Vulnerability}\n"
        f"Informal housing {top['Informal %']}%\nDrain capacity {top['Drain cap']}mm\n\n"
        f"{top.Action}</div>"
        f"<div class='n'>Full detail. Assumes a laptop and connectivity.</div></div>",
        unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><div class='h'>02 · SMS · {len(sms)} chars</div>"
        f"<div class='b'>{shorten(sms, 320, placeholder='…')}</div>"
        f"<div class='n'>Feature phone, no data connection. EN · KN · HI from one template.</div></div>",
        unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><div class='h'>03 · IVR voice call</div><div class='b'>{ivr}</div>"
        f"<div class='n'>No literacy requirement, no smartphone. Auto-dialled to the ward roll.</div></div>",
        unsafe_allow_html=True)
