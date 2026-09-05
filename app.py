import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta
from textwrap import shorten

st.set_page_config(page_title="BhuJal · Assam Flood Risk", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
#MainMenu, footer, header {visibility:hidden;}
html, body, [class*="css"] {font-family:'Manrope',system-ui,sans-serif;}
.stApp {background:
  radial-gradient(1200px 600px at 50% 6%, rgba(34,217,232,.10), transparent 60%),
  radial-gradient(700px 400px at 6% 0%, rgba(34,217,232,.06), transparent 60%), #040A12;}
.block-container {padding-top:.8rem; padding-bottom:2rem; max-width:1780px;}

.cmdbar {display:flex;justify-content:space-between;align-items:center;
  font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:#4E7A8C;border-top:1px solid #22D9E8;
  border-bottom:1px solid #10293A;padding:10px 4px;margin-bottom:16px;
  background:linear-gradient(180deg, rgba(34,217,232,.07), transparent);}
.cmdbar b {color:#D6F3F8;font-weight:600;letter-spacing:.12em;}
.dot {display:inline-block;width:6px;height:6px;border-radius:50%;background:#22D9E8;
  margin-right:9px;vertical-align:1px;box-shadow:0 0 8px #22D9E8;animation:blink 2.2s ease-in-out infinite;}
@keyframes blink {0%,100%{opacity:1}50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.dot{animation:none}}

.panel {position:relative;background:rgba(10,21,32,.85);border:1px solid #12303F;
  padding:14px 16px;margin-bottom:12px;}
.panel::before,.panel::after {content:"";position:absolute;width:11px;height:11px;border:1px solid #22D9E8;}
.panel::before {top:-1px;left:-1px;border-right:0;border-bottom:0;}
.panel::after {bottom:-1px;right:-1px;border-left:0;border-top:0;}
.panel .h {font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:#22D9E8;margin-bottom:9px;}
.panel .b {font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:#CFE6EE;
  line-height:1.65;white-space:pre-wrap;}
.panel .n {font-size:11px;color:#4E7A8C;margin-top:9px;line-height:1.5;}

h1 {font-weight:800;letter-spacing:-.03em;font-size:2.2rem;margin:0 0 .1rem;color:#EAF7FA;}
.eyebrow {font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;
  letter-spacing:.22em;text-transform:uppercase;color:#22D9E8;margin:0 0 6px;}
.sec {font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:#7FA8B8;
  border-bottom:1px solid #12303F;padding-bottom:8px;margin:0 0 14px;}
.lede {color:#6E93A3;font-size:14px;margin:0 0 14px;max-width:60ch;}
.formula {font-family:'IBM Plex Mono',monospace;font-size:15px;color:#22D9E8;
  letter-spacing:.02em;margin:0 0 14px;}

[data-testid="stMetric"] {position:relative;background:rgba(10,21,32,.85);
  border:1px solid #12303F;padding:13px 15px;border-radius:0;}
[data-testid="stMetric"]::before,[data-testid="stMetric"]::after {
  content:"";position:absolute;width:9px;height:9px;border:1px solid #22D9E8;}
[data-testid="stMetric"]::before {top:-1px;left:-1px;border-right:0;border-bottom:0;}
[data-testid="stMetric"]::after {bottom:-1px;right:-1px;border-left:0;border-top:0;}
[data-testid="stMetricValue"] {font-family:'IBM Plex Mono',monospace;font-size:1.55rem;color:#EAF7FA;}
[data-testid="stMetricLabel"] {font-family:'IBM Plex Mono',monospace;font-size:.62rem;
  font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#4E7A8C;}
[data-testid="stMetricDelta"] {font-family:'IBM Plex Mono',monospace;font-size:.74rem;}

.stTabs [data-baseweb="tab-list"] {gap:2px;border-bottom:1px solid #12303F;}
.stTabs [data-baseweb="tab"] {font-family:'IBM Plex Mono',monospace;font-size:11px;
  font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#4E7A8C;
  background:transparent;border-radius:0;padding:10px 18px;}
.stTabs [aria-selected="true"] {color:#22D9E8;border-bottom:2px solid #22D9E8;}

.band {position:relative;font-family:'IBM Plex Mono',monospace;font-size:12px;
  font-weight:600;letter-spacing:.16em;color:var(--c);border:1px solid var(--c);
  background:color-mix(in srgb,var(--c) 14%,transparent);padding:11px 14px;margin:8px 0 14px;
  box-shadow:0 0 18px color-mix(in srgb,var(--c) 22%,transparent);}
</style>
""", unsafe_allow_html=True)

# ---------------- ASSAM DISTRICTS -----------------------------------------
# Real districts of the Brahmaputra / Barak valleys. Rainfall is real (ERA5).
# District profiles are ILLUSTRATIVE pending ASDMA + Census integration.
DISTRICTS = pd.DataFrame([
 {"district":"Dhemaji",       "lat":27.48,"lon":94.58,"pop_lakh":6.9, "char":34,"kutcha":61,"dependents":29,"embankment":"Weak"},
 {"district":"Lakhimpur",     "lat":27.23,"lon":94.10,"pop_lakh":10.4,"char":28,"kutcha":55,"dependents":27,"embankment":"Weak"},
 {"district":"Majuli",        "lat":26.95,"lon":94.17,"pop_lakh":1.7, "char":71,"kutcha":66,"dependents":31,"embankment":"Weak"},
 {"district":"Jorhat",        "lat":26.75,"lon":94.22,"pop_lakh":10.9,"char":12,"kutcha":34,"dependents":22,"embankment":"Moderate"},
 {"district":"Sivasagar",     "lat":26.98,"lon":94.63,"pop_lakh":11.5,"char": 9,"kutcha":31,"dependents":21,"embankment":"Moderate"},
 {"district":"Dibrugarh",     "lat":27.47,"lon":94.91,"pop_lakh":13.3,"char":14,"kutcha":33,"dependents":23,"embankment":"Moderate"},
 {"district":"Barpeta",       "lat":26.32,"lon":91.00,"pop_lakh":16.9,"char":42,"kutcha":58,"dependents":30,"embankment":"Weak"},
 {"district":"Nalbari",       "lat":26.44,"lon":91.44,"pop_lakh":7.7, "char":23,"kutcha":47,"dependents":26,"embankment":"Moderate"},
 {"district":"Morigaon",      "lat":26.25,"lon":92.34,"pop_lakh":9.6, "char":38,"kutcha":56,"dependents":29,"embankment":"Weak"},
 {"district":"Nagaon",        "lat":26.35,"lon":92.68,"pop_lakh":28.2,"char":26,"kutcha":49,"dependents":27,"embankment":"Moderate"},
 {"district":"Goalpara",      "lat":26.17,"lon":90.62,"pop_lakh":10.1,"char":36,"kutcha":54,"dependents":28,"embankment":"Weak"},
 {"district":"Dhubri",        "lat":26.02,"lon":89.98,"pop_lakh":19.5,"char":48,"kutcha":62,"dependents":32,"embankment":"Weak"},
 {"district":"Kamrup Metro",  "lat":26.14,"lon":91.73,"pop_lakh":12.6,"char": 6,"kutcha":21,"dependents":18,"embankment":"Strong"},
 {"district":"Cachar",        "lat":24.83,"lon":92.78,"pop_lakh":17.4,"char":17,"kutcha":44,"dependents":25,"embankment":"Moderate"},
])

EMB_MM = {"Weak": 35, "Moderate": 62, "Strong": 88}   # rainfall (mm/24h) tolerated before overtopping
BANDS = [(75,"RED","#FF4D4F","Take action"), (50,"ORANGE","#FF9F45","Be prepared"),
         (25,"YELLOW","#F5D547","Be updated"), (0,"GREEN","#2FE08A","No warning")]

def band_for(s):
    for cut, name, col, mean in BANDS:
        if s >= cut:
            return name, col, mean

def assess(d, rain_mm):
    """Risk = Hazard x Exposure x Vulnerability."""
    cap      = EMB_MM[d.embankment] * (1 - 0.30 * d.char / 100)   # char-heavy districts inundate sooner
    hazard   = min(max((rain_mm - cap) / 95.0, 0.0), 1.0)
    exposure = min(d.pop_lakh / 28.0, 1.0)
    vuln     = min((0.45*d.char + 0.35*d.kutcha + 0.20*d.dependents) / 100.0, 1.0)
    score    = 100 * hazard * (0.30 + 0.70 * (0.45*exposure + 0.55*vuln))
    return round(min(score, 100)), round(hazard, 2), round(exposure, 2), round(vuln, 2), round(cap)

def action_for(band, d):
    if band == "RED":
        return (f"Evacuate char and riverine settlements ({d.char}% of habitation) to raised "
                f"relief camps now; move livestock to embankment high ground")
    if band == "ORANGE":
        return "Pre-position country boats and dry ration; issue village-level warning tonight"
    if band == "YELLOW":
        return "Alert circle officers; inspect embankment breach points; monitor gauge hourly"
    return "Routine monitoring"

# ---------------- REAL RAINFALL: Open-Meteo / ERA5 -------------------------
@st.cache_data(ttl=900, show_spinner=False)
def fetch_rain(lats, lons, day=None):
    """Rainfall (mm) per district. Live forecast peak, or recorded ERA5 for one past date."""
    try:
        url = ("https://archive-api.open-meteo.com/v1/archive" if day
               else "https://api.open-meteo.com/v1/forecast")
        params = {"latitude": ",".join(f"{x:.3f}" for x in lats),
                  "longitude": ",".join(f"{x:.3f}" for x in lons),
                  "daily": "precipitation_sum", "timezone": "Asia/Kolkata"}
        if day:
            params["start_date"] = str(day)
            params["end_date"] = str(day)
        else:
            params["forecast_days"] = 3
        j = requests.get(url, timeout=12, params=params).json()
        if isinstance(j, dict):
            j = [j]
        out = []
        for loc in j:
            vals = [v for v in loc["daily"]["precipitation_sum"] if v is not None]
            out.append(float(max(vals)) if vals else 0.0)
        return out if len(out) == len(lats) else None
    except Exception:
        return None

LATS = tuple(DISTRICTS.lat)
LONS = tuple(DISTRICTS.lon)

# ---------------- COMMAND BAR + CONTROL STRIP -----------------------------
st.markdown(
    "<div class='cmdbar'><span><span class='dot'></span><b>BhuJal</b> &nbsp;·&nbsp; "
    "District flood risk &amp; early warning &nbsp;·&nbsp; Assam</span>"
    "<span>Rainfall: ERA5 / ECMWF via Open-Meteo &nbsp;·&nbsp; district profiles illustrative</span></div>",
    unsafe_allow_html=True)

st.markdown("<div class='eyebrow'>Climate risk mapping · early warning</div>", unsafe_allow_html=True)
st.markdown("<h1>We don't predict the rain. We predict who it hurts.</h1>", unsafe_allow_html=True)

k1, k2, k3 = st.columns([1.1, 1.4, 1.2])
with k1:
    mode = st.radio("Rainfall source", ["Scenario", "Live forecast", "Verify past event"],
                    horizontal=True, index=0)
src, rains = "", None

with k2:
    if mode == "Live forecast":
        rains = fetch_rain(LATS, LONS)
        src = "Open-Meteo forecast · peak of next 3 days"
        if rains is None:
            st.warning("Forecast API unreachable — using scenario.")
    elif mode == "Verify past event":
        d = st.date_input("Replay date", value=date(2022, 6, 18),
                          min_value=date(1990, 1, 1), max_value=date.today() - timedelta(days=6))
        rains = fetch_rain(LATS, LONS, d)
        src = f"ERA5 reanalysis · recorded {d}"
        if rains is None:
            st.warning("Archive unreachable — using scenario.")
with k3:
    if rains is None:
        uniform = st.slider("Rainfall, next 24h (mm)", 0, 200, 95, 5)
        rains = [uniform] * len(DISTRICTS)
        src = src or "scenario · uniform rainfall"

# ---------------- SCORING --------------------------------------------------
rows = []
for i, d in enumerate(DISTRICTS.itertuples()):
    mm = rains[i]
    sc, h, e, v, cap = assess(d, mm)
    nm, col, mean = band_for(sc)
    rows.append({"District": d.district, "Rain mm": round(mm), "Risk": sc, "Band": nm,
                 "Colour": col, "Meaning": mean, "Hazard": h, "Exposure": e, "Vulnerability": v,
                 "Embankment": d.embankment, "Threshold": cap, "Char %": d.char,
                 "Kutcha %": d.kutcha, "Pop (lakh)": d.pop_lakh,
                 "Action": action_for(nm, d), "lat": d.lat, "lon": d.lon})
R = pd.DataFrame(rows).sort_values("Risk", ascending=False).reset_index(drop=True)
top = R.iloc[0]
red = int((R.Risk >= 75).sum())
org = int(((R.Risk >= 50) & (R.Risk < 75)).sum())
pop_exposed = round(float(R[R.Risk >= 50]["Pop (lakh)"].sum()), 1)

st.caption(f"Source: {src}")

t1, t2, t3, t4 = st.tabs(["01 · Risk model", "02 · Risk map", "03 · Alert", "04 · Last mile"])

# ================= TAB 1 — THE MODEL ======================================
with t1:
    st.markdown("<div class='sec'>Deliverable 1 · Risk scoring approach, in plain terms</div>",
                unsafe_allow_html=True)
    a, b = st.columns([1.15, 1])
    with a:
        st.markdown("<div class='formula'>RISK  =  HAZARD  ×  EXPOSURE  ×  VULNERABILITY</div>",
                    unsafe_allow_html=True)
        st.markdown("""
**Hazard — will this district actually get water?**
Forecast rainfall measured against what its embankments tolerate. Weak embankments overtop at
about 35 mm in 24 h, strong ones near 88 mm. Districts with more *char* (riverine sandbar)
habitation inundate sooner, so their threshold is reduced proportionally.

**Exposure — how many people are in the way?**
District population, normalised against the largest district in the set.

**Vulnerability — how badly do those people cope?**
45% char-area habitation, 35% kutcha (non-permanent) housing, 20% dependents — children and elderly.

**Why multiply by hazard rather than add it.**
No rain means no risk, however vulnerable the district. A district can be the poorest in Assam
and still be Green on a dry day. Vulnerability decides *ranking* among districts that are
actually threatened — it never manufactures a threat on its own.
        """)
        st.markdown("""
| Band | Score | Meaning (IMD convention) |
|---|---|---|
| 🔴 RED | 75–100 | Take action |
| 🟠 ORANGE | 50–74 | Be prepared |
| 🟡 YELLOW | 25–49 | Be updated |
| 🟢 GREEN | 0–24 | No warning |
        """)
    with b:
        st.markdown("<div class='sec'>Worked example</div>", unsafe_allow_html=True)
        pick = st.selectbox("District", list(R.District), index=0)
        r = R[R.District == pick].iloc[0]
        st.markdown(
            f"<div class='panel'><div class='h'>{r.District}</div><div class='b'>"
            f"Rainfall            {r['Rain mm']} mm\n"
            f"Embankment          {r.Embankment} → threshold {r.Threshold} mm\n"
            f"Char habitation     {r['Char %']}%\n"
            f"Kutcha housing      {r['Kutcha %']}%\n"
            f"Population          {r['Pop (lakh)']} lakh\n"
            f"────────────────────────────────\n"
            f"HAZARD          H = {r.Hazard}\n"
            f"EXPOSURE        E = {r.Exposure}\n"
            f"VULNERABILITY   V = {r.Vulnerability}\n"
            f"────────────────────────────────\n"
            f"RISK            {r.Risk} / 100   → {r.Band}</div>"
            f"<div class='n'>Every term is inspectable. A district officer can see why the score "
            f"moved before acting on it.</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='band' style='--c:{r.Colour}'>{r.Band} · {r.Meaning.upper()}</div>",
                    unsafe_allow_html=True)

# ================= TAB 2 — THE MAP ========================================
with t2:
    st.markdown("<div class='sec'>Deliverable 2 · Who is at risk, and how much</div>",
                unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Red districts", red)
    m2.metric("Orange districts", org)
    m3.metric("Population exposed", f"{pop_exposed} lakh")
    m4.metric("Highest risk", top.District, f"{top.Risk}/100 · {top.Band}", delta_color="off")

    st.write("")
    left, right = st.columns([1.25, 1])
    with left:
        pts = R[["lat", "lon"]].copy()
        pts["color"] = R.Colour
        pts["size"] = (R.Risk * 260 + 5000).astype(int)
        st.map(pts, color="color", size="size", zoom=6.4)
    with right:
        st.dataframe(
            R[["District", "Rain mm", "Risk", "Band", "Hazard", "Exposure", "Vulnerability"]],
            use_container_width=True, hide_index=True, height=430,
            column_config={
                "Risk": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100,
                                                        format="%d", width="small"),
                "Rain mm": st.column_config.NumberColumn("Rain", format="%d mm", width="small"),
                "Hazard": st.column_config.NumberColumn("H", format="%.2f", width="small"),
                "Exposure": st.column_config.NumberColumn("E", format="%.2f", width="small"),
                "Vulnerability": st.column_config.NumberColumn("V", format="%.2f", width="small"),
            })

# ================= TAB 3 — THE ALERT ======================================
with t3:
    st.markdown("<div class='sec'>Deliverable 3 · Preparedness action for a specific community</div>",
                unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown(
            f"<div class='panel'><div class='h'>Community profile</div><div class='b'>"
            f"{top.District} district\n"
            f"Population            {top['Pop (lakh)']} lakh\n"
            f"Char habitation       {top['Char %']}%\n"
            f"Kutcha housing        {top['Kutcha %']}%\n"
            f"Embankment            {top.Embankment}\n"
            f"Rainfall (24h)        {top['Rain mm']} mm\n"
            f"Risk                  {top.Risk}/100 · {top.Band}</div>"
            f"<div class='n'>The action below is derived from this profile — not a generic template.</div></div>",
            unsafe_allow_html=True)
        st.markdown(f"<div class='band' style='--c:{top.Colour}'>{top.Band} · {top.Meaning.upper()}</div>",
                    unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"<div class='panel'><div class='h'>Preparedness action issued</div><div class='b'>"
            f"{top.Action}</div>"
            f"<div class='n'>Why this action: {top['Char %']}% of habitation is on char land, which "
            f"floods first and is cut off once the river rises. {top['Kutcha %']}% of housing is "
            f"non-permanent and will not survive sustained inundation. Livestock is the primary "
            f"household asset, so it is named explicitly.</div></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='panel'><div class='h'>Escalation chain</div><div class='b'>"
            "T-24h   District Commissioner + Circle Officer notified\n"
            "T-18h   Village volunteers and ASHA workers alerted\n"
            "T-12h   Household SMS + IVR wave 1\n"
            "T-6h    Relief camps opened, boats positioned\n"
            "T-3h    Loudspeaker announcement in char villages</div>"
            "<div class='n'>Each step has a named owner. Lead time is what riverine flooding gives "
            "you and landslides do not.</div></div>", unsafe_allow_html=True)

# ================= TAB 4 — LAST MILE ======================================
with t4:
    st.markdown("<div class='sec'>Deliverable 4 · Reaching people with limited connectivity</div>",
                unsafe_allow_html=True)
    st.markdown("<p class='lede'>The households at highest risk are the least likely to own a "
                "smartphone or have data. The same warning is rendered for every channel that "
                "reaches them.</p>", unsafe_allow_html=True)

    sms = (f"{top.Band} FLOOD ALERT {top.District}. {top['Rain mm']}mm rain in 24h. "
           f"Char and riverine villages move to raised relief camp before dark. "
           f"Take livestock and documents. -ASDMA")
    ivr = (f"This is a flood warning from the Assam State Disaster Management Authority "
           f"for {top.District} district. {top.Band} alert. Heavy rain is expected. "
           f"If you live on char land or near the embankment, move to the relief camp today. "
           f"Press 1 to hear this again.")

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(
            f"<div class='panel'><div class='h'>01 · Officer dashboard</div><div class='b'>"
            f"{top.District}\nRISK {top.Risk}/100 · {top.Band}\n"
            f"H {top.Hazard} × E {top.Exposure} × V {top.Vulnerability}\n"
            f"Char {top['Char %']}% · Kutcha {top['Kutcha %']}%\n\n{top.Action}</div>"
            f"<div class='n'>Reaches: DC office, circle officers. Requires a laptop and a connection.</div></div>",
            unsafe_allow_html=True)
    with d2:
        st.markdown(
            f"<div class='panel'><div class='h'>02 · SMS · {len(sms)} chars</div>"
            f"<div class='b'>{shorten(sms, 320, placeholder='…')}</div>"
            f"<div class='n'>Reaches: any feature phone, no data required. Cell broadcast to the "
            f"district tower reaches unregistered numbers too. Assamese, Bengali, Bodo and Hindi "
            f"from one template.</div></div>", unsafe_allow_html=True)
    with d3:
        st.markdown(
            f"<div class='panel'><div class='h'>03 · IVR voice call</div><div class='b'>{ivr}</div>"
            f"<div class='n'>Reaches: households with no literacy requirement. Auto-dialled to the "
            f"panchayat roll; repeats until answered.</div></div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='panel'><div class='h'>Where the network ends</div><div class='b'>"
        "Char villages lose tower coverage when the river rises and towers are cut off.\n"
        "The last mile is therefore not digital:\n\n"
        "  · ASHA and Anganwadi workers carry the alert on foot — one printed slip per household\n"
        "  · Panchayat loudspeaker announcement, scripted from the same IVR text\n"
        "  · Colour flag at the ghat — red cloth is understood without literacy or power\n\n"
        "One alert object, five renderings. The system degrades to paper and cloth by design.</div>"
        "<div class='n'>This is why the alert is generated as structured data rather than a message: "
        "the channel is chosen at delivery, not at authoring.</div></div>", unsafe_allow_html=True)
