import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta

st.set_page_config(page_title="BhuJal · Assam Flood Risk", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');
#MainMenu, footer, header {visibility:hidden;}
html, body, [class*="css"] {font-family:'Manrope',system-ui,sans-serif;}
.stApp {background:
  radial-gradient(1300px 620px at 50% 4%, rgba(34,217,232,.10), transparent 62%), #03080F;}
.block-container {padding-top:.6rem; padding-bottom:1.5rem; max-width:1860px;}
hr {border-color:#12303F;}

/* command bar */
.cmd {display:flex;justify-content:space-between;align-items:center;
  font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
  text-transform:uppercase;color:#4E7A8C;border-top:1px solid #22D9E8;
  border-bottom:1px solid #10293A;padding:9px 4px;margin-bottom:14px;
  background:linear-gradient(180deg, rgba(34,217,232,.08), transparent);}
.cmd b{color:#DFF6FA;font-weight:700;letter-spacing:.14em;}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22D9E8;
  margin-right:8px;box-shadow:0 0 9px #22D9E8;animation:bl 2.2s ease-in-out infinite;}
@keyframes bl{0%,100%{opacity:1}50%{opacity:.2}}
@media (prefers-reduced-motion:reduce){.dot{animation:none}}

h1{font-weight:800;letter-spacing:-.035em;font-size:2.05rem;margin:0;color:#EAF7FA;}
.sub{color:#5E8496;font-size:13px;margin:2px 0 0;}
.sec{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:700;
  letter-spacing:.22em;text-transform:uppercase;color:#22D9E8;
  border-bottom:1px solid #12303F;padding-bottom:7px;margin:0 0 12px;}

/* KPI tiles */
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:0 0 16px;}
.kpi{position:relative;background:rgba(9,20,30,.9);border:1px solid #12303F;
  border-left:3px solid var(--c);padding:12px 14px;}
.kpi .v{font-family:'IBM Plex Mono',monospace;font-size:2rem;font-weight:600;
  color:var(--c);line-height:1;text-shadow:0 0 22px color-mix(in srgb,var(--c) 55%,transparent);}
.kpi .k{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:#4E7A8C;margin-top:7px;}

/* district rows */
.rows{display:flex;flex-direction:column;gap:6px;max-height:560px;overflow-y:auto;padding-right:4px;}
.row{display:grid;grid-template-columns:150px 62px 1fr;gap:12px;align-items:center;
  background:color-mix(in srgb,var(--c) 7%,rgba(9,20,30,.9));
  border:1px solid color-mix(in srgb,var(--c) 30%,#12303F);
  border-left:3px solid var(--c);padding:9px 12px;}
.row.hot{box-shadow:0 0 20px color-mix(in srgb,var(--c) 26%,transparent);}
.nm{font-weight:700;font-size:14px;color:#EAF7FA;line-height:1.2;}
.nm span{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:500;letter-spacing:.1em;color:#5E8496;margin-top:3px;}
.sc{font-family:'IBM Plex Mono',monospace;font-size:1.55rem;font-weight:700;color:var(--c);
  text-align:right;line-height:1;text-shadow:0 0 16px color-mix(in srgb,var(--c) 50%,transparent);}
.sc span{display:block;font-size:8.5px;font-weight:600;letter-spacing:.18em;margin-top:4px;
  text-shadow:none;}
.bars{display:flex;flex-direction:column;gap:3px;}
.br{display:grid;grid-template-columns:14px 1fr 34px;gap:7px;align-items:center;}
.br .l{font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600;color:#4E7A8C;}
.br .t{height:5px;background:#0C1E2A;border:1px solid #12303F;}
.br .t i{display:block;height:100%;background:var(--bc);}
.br .n{font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#8FB5C4;text-align:right;}

/* alert + channel panels */
.pnl{position:relative;background:rgba(9,20,30,.9);border:1px solid #12303F;padding:14px 16px;height:100%;}
.pnl::before,.pnl::after{content:"";position:absolute;width:10px;height:10px;border:1px solid #22D9E8;}
.pnl::before{top:-1px;left:-1px;border-right:0;border-bottom:0;}
.pnl::after{bottom:-1px;right:-1px;border-left:0;border-top:0;}
.pnl .h{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;color:#22D9E8;margin-bottom:9px;}
.pnl .b{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#CFE6EE;
  line-height:1.7;white-space:pre-wrap;}
.pnl .n{font-size:10.5px;color:#4E7A8C;margin-top:9px;line-height:1.55;}

.alert{position:relative;background:color-mix(in srgb,var(--c) 12%,rgba(9,20,30,.9));
  border:1px solid var(--c);border-left:4px solid var(--c);padding:16px 18px;
  box-shadow:0 0 26px color-mix(in srgb,var(--c) 24%,transparent);}
.alert .tag{font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:700;
  letter-spacing:.22em;color:var(--c);}
.alert .ttl{font-size:1.5rem;font-weight:800;color:#EAF7FA;margin:6px 0 8px;letter-spacing:-.02em;}
.alert .act{font-size:14.5px;color:#DCEDF3;line-height:1.55;}
.alert .meta{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:#7FA8B8;
  margin-top:10px;letter-spacing:.06em;}

[data-testid="stMetric"]{background:rgba(9,20,30,.9);border:1px solid #12303F;padding:11px 13px;}
[data-testid="stMetricValue"]{font-family:'IBM Plex Mono',monospace;font-size:1.3rem;color:#EAF7FA;}
[data-testid="stMetricLabel"]{font-family:'IBM Plex Mono',monospace;font-size:.58rem;
  font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#4E7A8C;}
</style>
""", unsafe_allow_html=True)

# ---------------- ASSAM DISTRICTS -----------------------------------------
DISTRICTS = pd.DataFrame([
 {"district":"Dhemaji",      "lat":27.48,"lon":94.58,"pop":6.9, "char":34,"kutcha":61,"dep":29,"emb":"Weak"},
 {"district":"Lakhimpur",    "lat":27.23,"lon":94.10,"pop":10.4,"char":28,"kutcha":55,"dep":27,"emb":"Weak"},
 {"district":"Majuli",       "lat":26.95,"lon":94.17,"pop":1.7, "char":71,"kutcha":66,"dep":31,"emb":"Weak"},
 {"district":"Jorhat",       "lat":26.75,"lon":94.22,"pop":10.9,"char":12,"kutcha":34,"dep":22,"emb":"Moderate"},
 {"district":"Sivasagar",    "lat":26.98,"lon":94.63,"pop":11.5,"char": 9,"kutcha":31,"dep":21,"emb":"Moderate"},
 {"district":"Dibrugarh",    "lat":27.47,"lon":94.91,"pop":13.3,"char":14,"kutcha":33,"dep":23,"emb":"Moderate"},
 {"district":"Barpeta",      "lat":26.32,"lon":91.00,"pop":16.9,"char":42,"kutcha":58,"dep":30,"emb":"Weak"},
 {"district":"Nalbari",      "lat":26.44,"lon":91.44,"pop":7.7, "char":23,"kutcha":47,"dep":26,"emb":"Moderate"},
 {"district":"Morigaon",     "lat":26.25,"lon":92.34,"pop":9.6, "char":38,"kutcha":56,"dep":29,"emb":"Weak"},
 {"district":"Nagaon",       "lat":26.35,"lon":92.68,"pop":28.2,"char":26,"kutcha":49,"dep":27,"emb":"Moderate"},
 {"district":"Goalpara",     "lat":26.17,"lon":90.62,"pop":10.1,"char":36,"kutcha":54,"dep":28,"emb":"Weak"},
 {"district":"Dhubri",       "lat":26.02,"lon":89.98,"pop":19.5,"char":48,"kutcha":62,"dep":32,"emb":"Weak"},
 {"district":"Kamrup Metro", "lat":26.14,"lon":91.73,"pop":12.6,"char": 6,"kutcha":21,"dep":18,"emb":"Strong"},
 {"district":"Cachar",       "lat":24.83,"lon":92.78,"pop":17.4,"char":17,"kutcha":44,"dep":25,"emb":"Moderate"},
])

EMB_MM = {"Weak": 35, "Moderate": 62, "Strong": 88}
BANDS = [(75,"RED","#FF2D3F"), (50,"ORANGE","#FF8A1E"), (25,"YELLOW","#FFD21E"), (0,"GREEN","#00E08A")]
MEANING = {"RED":"Take action","ORANGE":"Be prepared","YELLOW":"Be updated","GREEN":"No warning"}

def band_for(s):
    for cut, name, col in BANDS:
        if s >= cut:
            return name, col

def assess(d, mm):
    cap  = EMB_MM[d.emb] * (1 - 0.30 * d.char / 100)
    H    = min(max((mm - cap) / 95.0, 0.0), 1.0)
    E    = min(d.pop / 28.0, 1.0)
    V    = min((0.45*d.char + 0.35*d.kutcha + 0.20*d.dep) / 100.0, 1.0)
    return round(min(100 * H * (0.30 + 0.70*(0.45*E + 0.55*V)), 100)), round(H,2), round(E,2), round(V,2), round(cap)

def action_for(b, d):
    if b == "RED":    return (f"Evacuate char and riverine settlements — {d.char}% of habitation — to "
                              f"raised relief camps now. Move livestock to embankment high ground.")
    if b == "ORANGE": return "Pre-position country boats and dry ration. Issue village-level warning tonight."
    if b == "YELLOW": return "Alert circle officers. Inspect embankment breach points. Monitor gauge hourly."
    return "Routine monitoring. No action required."

@st.cache_data(ttl=900, show_spinner=False)
def fetch_rain(lats, lons, day=None):
    try:
        url = ("https://archive-api.open-meteo.com/v1/archive" if day
               else "https://api.open-meteo.com/v1/forecast")
        p = {"latitude": ",".join(f"{x:.3f}" for x in lats),
             "longitude": ",".join(f"{x:.3f}" for x in lons),
             "daily": "precipitation_sum", "timezone": "Asia/Kolkata"}
        if day: p["start_date"] = p["end_date"] = str(day)
        else:   p["forecast_days"] = 3
        j = requests.get(url, timeout=12, params=p).json()
        if isinstance(j, dict): j = [j]
        out = [float(max([v for v in l["daily"]["precipitation_sum"] if v is not None] or [0])) for l in j]
        return out if len(out) == len(lats) else None
    except Exception:
        return None

LATS, LONS = tuple(DISTRICTS.lat), tuple(DISTRICTS.lon)

# ---------------- HEADER + CONTROLS ---------------------------------------
st.markdown("<div class='cmd'><span><span class='dot'></span><b>BhuJal</b> &nbsp;·&nbsp; "
            "Assam district flood risk &amp; early warning</span>"
            "<span>ERA5 / ECMWF rainfall &nbsp;·&nbsp; ASDMA district profiles (illustrative)</span></div>",
            unsafe_allow_html=True)

h1, h2, h3 = st.columns([1.5, 1.15, 1.35])
with h1:
    st.markdown("<h1>Flood risk · live</h1>"
                "<p class='sub'>Risk = Hazard × Exposure × Vulnerability · 14 districts</p>",
                unsafe_allow_html=True)
with h2:
    mode = st.radio("Rainfall source", ["Scenario", "Live forecast", "Verify past event"],
                    horizontal=True, label_visibility="collapsed")
rains, src = None, ""
with h3:
    if mode == "Live forecast":
        rains = fetch_rain(LATS, LONS); src = "Open-Meteo forecast · peak of next 3 days"
    elif mode == "Verify past event":
        d = st.date_input("Replay date", value=date(2022, 6, 18), label_visibility="collapsed",
                          min_value=date(1990,1,1), max_value=date.today()-timedelta(days=6))
        rains = fetch_rain(LATS, LONS, d); src = f"ERA5 reanalysis · recorded {d}"
    if rains is None:
        mmv = st.slider("Rainfall next 24h (mm)", 0, 200, 95, 5)
        rains = [mmv]*len(DISTRICTS); src = (src + " — unreachable, scenario") if src else "Scenario · uniform rainfall"

# ---------------- SCORE ----------------------------------------------------
rows = []
for i, d in enumerate(DISTRICTS.itertuples()):
    mm = rains[i]
    sc, H, E, V, cap = assess(d, mm)
    nm, col = band_for(sc)
    rows.append({"District": d.district, "mm": round(mm), "Risk": sc, "Band": nm, "C": col,
                 "H": H, "E": E, "V": V, "cap": cap, "char": d.char, "kutcha": d.kutcha,
                 "pop": d.pop, "emb": d.emb, "Action": action_for(nm, d),
                 "lat": d.lat, "lon": d.lon})
R = pd.DataFrame(rows).sort_values("Risk", ascending=False).reset_index(drop=True)
top = R.iloc[0]
cnt = {b: int((R.Band == b).sum()) for b in ["RED","ORANGE","YELLOW","GREEN"]}
pop_exp = round(float(R[R.Risk >= 50]["pop"].sum()), 1)

st.markdown(f"""<div class='kpis'>
<div class='kpi' style='--c:#FF2D3F'><div class='v'>{cnt['RED']}</div><div class='k'>Red · take action</div></div>
<div class='kpi' style='--c:#FF8A1E'><div class='v'>{cnt['ORANGE']}</div><div class='k'>Orange · be prepared</div></div>
<div class='kpi' style='--c:#FFD21E'><div class='v'>{cnt['YELLOW']}</div><div class='k'>Yellow · be updated</div></div>
<div class='kpi' style='--c:#00E08A'><div class='v'>{cnt['GREEN']}</div><div class='k'>Green · no warning</div></div>
<div class='kpi' style='--c:#22D9E8'><div class='v'>{pop_exp}L</div><div class='k'>Population exposed</div></div>
</div>""", unsafe_allow_html=True)

# ---------------- MAP + DISTRICT RISK LIST --------------------------------
mapcol, listcol = st.columns([1.05, 1.15], gap="medium")

with mapcol:
    st.markdown("<div class='sec'>Risk surface · Assam</div>", unsafe_allow_html=True)
    pts = R[["lat","lon"]].copy()
    pts["color"] = R.C
    pts["size"] = (R.Risk * 300 + 6000).astype(int)
    st.map(pts, color="color", size="size", zoom=6.3)
    st.caption(f"Source: {src}")

with listcol:
    st.markdown("<div class='sec'>District risk score · Hazard × Exposure × Vulnerability</div>",
                unsafe_allow_html=True)
    html = "<div class='rows'>"
    for r in R.itertuples():
        hot = " hot" if r.Risk >= 50 else ""
        bars = "".join(
            f"<div class='br' style='--bc:{r.C}'><span class='l'>{lab}</span>"
            f"<span class='t'><i style='width:{val*100:.0f}%'></i></span>"
            f"<span class='n'>{val:.2f}</span></div>"
            for lab, val in (("H", r.H), ("E", r.E), ("V", r.V)))
        html += (f"<div class='row{hot}' style='--c:{r.C}'>"
                 f"<div class='nm'>{r.District}<span>{r.mm}MM · {r.emb.upper()} · CHAR {r.char}%</span></div>"
                 f"<div class='sc'>{r.Risk}<span>{r.Band}</span></div>"
                 f"<div class='bars'>{bars}</div></div>")
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ---------------- ACTIVE ALERT --------------------------------------------
st.markdown("<div class='sec'>Active alert · highest risk district</div>", unsafe_allow_html=True)
a1, a2 = st.columns([1.5, 1])
with a1:
    st.markdown(
        f"<div class='alert' style='--c:{top.C}'>"
        f"<div class='tag'>{top.Band} · {MEANING[top.Band].upper()} · RISK {top.Risk}/100</div>"
        f"<div class='ttl'>{top.District} district</div>"
        f"<div class='act'>{top.Action}</div>"
        f"<div class='meta'>{top.mm}MM RAIN &nbsp;·&nbsp; {top.emb.upper()} EMBANKMENT "
        f"(THRESHOLD {top.cap}MM) &nbsp;·&nbsp; CHAR {top.char}% &nbsp;·&nbsp; "
        f"KUTCHA {top.kutcha}% &nbsp;·&nbsp; {top.pop} LAKH PEOPLE</div></div>",
        unsafe_allow_html=True)
with a2:
    st.markdown(
        "<div class='pnl'><div class='h'>Escalation chain</div><div class='b'>"
        "T−24h  District Commissioner + Circle Officer\n"
        "T−18h  Village volunteers, ASHA workers\n"
        "T−12h  Household SMS + IVR wave 1\n"
        "T−6h   Relief camps open, boats positioned\n"
        "T−3h   Loudspeaker in char villages</div>"
        "<div class='n'>Riverine flooding gives you this lead time. Landslides do not — which is "
        "why this system targets flooding.</div></div>", unsafe_allow_html=True)

# ---------------- LAST MILE -----------------------------------------------
st.markdown("<div class='sec'>Last mile · one alert, four renderings</div>", unsafe_allow_html=True)
sms = (f"{top.Band} FLOOD ALERT {top.District}. {top.mm}mm rain in 24h. Char and riverine "
       f"villages move to raised relief camp before dark. Take livestock and documents. -ASDMA")
ivr = (f"Flood warning from A S D M A for {top.District} district. {top.Band} alert. "
       f"Heavy rain expected. If you live on char land or near the embankment, move to the "
       f"relief camp today. Press 1 to repeat.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='pnl'><div class='h'>01 · Officer dashboard</div><div class='b'>"
                f"{top.District}\nRISK {top.Risk}/100 · {top.Band}\n"
                f"H {top.H} × E {top.E} × V {top.V}</div>"
                f"<div class='n'>DC office and circle officers. Needs a laptop and a connection.</div></div>",
                unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='pnl'><div class='h'>02 · SMS · {len(sms)} chars</div>"
                f"<div class='b'>{sms}</div>"
                f"<div class='n'>Any feature phone, no data. Cell broadcast reaches unregistered "
                f"numbers. Assamese · Bengali · Bodo · Hindi from one template.</div></div>",
                unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='pnl'><div class='h'>03 · IVR voice call</div><div class='b'>{ivr}</div>"
                f"<div class='n'>No literacy needed, no smartphone. Auto-dialled to the panchayat "
                f"roll, repeats until answered.</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='pnl'><div class='h'>04 · Off-grid</div><div class='b'>"
                "· ASHA worker — printed slip\n· Panchayat loudspeaker\n· Red flag at the ghat</div>"
                "<div class='n'>Char villages lose tower coverage as the river rises. The system "
                "degrades to paper and cloth by design.</div></div>", unsafe_allow_html=True)

with st.expander("How the score is computed"):
    st.markdown("""
**Hazard** — forecast rainfall against what the district's embankments tolerate.
Weak overtops near 35 mm/24h, Strong near 88 mm. More *char* (riverine sandbar) habitation lowers
the threshold proportionally.
**Exposure** — district population, normalised to the largest in the set.
**Vulnerability** — 45% char habitation, 35% kutcha housing, 20% dependents.
**Multiplied by hazard**, so no rain means no risk however vulnerable the district — vulnerability
decides ranking among districts actually threatened, it never invents a threat.
Bands follow the IMD convention: Red 75+, Orange 50–74, Yellow 25–49, Green below 25.
    """)
