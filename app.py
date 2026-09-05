import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta, datetime

st.set_page_config(page_title="BhuJal · Assam Flood Risk", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');
#MainMenu, footer, header {visibility:hidden;}
html, body, [class*="css"] {font-family:'Manrope',system-ui,sans-serif;}
.stApp {background: radial-gradient(1300px 620px at 50% 4%, rgba(34,217,232,.10), transparent 62%), #03080F;}
.block-container {padding-top:.6rem; padding-bottom:1.5rem; max-width:1880px;}

.cmd{display:flex;justify-content:space-between;align-items:center;
  font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
  text-transform:uppercase;color:#4E7A8C;border-top:1px solid #22D9E8;
  border-bottom:1px solid #10293A;padding:9px 4px;margin-bottom:14px;
  background:linear-gradient(180deg,rgba(34,217,232,.08),transparent);}
.cmd b{color:#DFF6FA;font-weight:700;letter-spacing:.14em;}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22D9E8;
  margin-right:8px;box-shadow:0 0 9px #22D9E8;animation:bl 2.2s ease-in-out infinite;}
@keyframes bl{0%,100%{opacity:1}50%{opacity:.2}}
@media (prefers-reduced-motion:reduce){.dot{animation:none}}

h1{font-weight:800;letter-spacing:-.035em;font-size:1.95rem;margin:0;color:#EAF7FA;}
.sub{color:#5E8496;font-size:12.5px;margin:3px 0 0;}
.sec{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:700;
  letter-spacing:.22em;text-transform:uppercase;color:#22D9E8;
  border-bottom:1px solid #12303F;padding-bottom:7px;margin:2px 0 12px;}

.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:1px solid #12303F;margin-bottom:6px;}
.stTabs [data-baseweb="tab"]{font-family:'IBM Plex Mono',monospace;font-size:10.5px;
  font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#4E7A8C;
  background:transparent;border-radius:0;padding:12px 22px;}
.stTabs [aria-selected="true"]{color:#22D9E8;border-bottom:2px solid #22D9E8;
  background:linear-gradient(180deg,transparent,rgba(34,217,232,.07));}

.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:2px 0 16px;}
.kpi{background:rgba(9,20,30,.9);border:1px solid #12303F;border-left:3px solid var(--c);padding:13px 15px;}
.kpi .v{font-family:'IBM Plex Mono',monospace;font-size:2.1rem;font-weight:600;color:var(--c);
  line-height:1;text-shadow:0 0 22px color-mix(in srgb,var(--c) 55%,transparent);}
.kpi .k{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:600;
  letter-spacing:.2em;text-transform:uppercase;color:#4E7A8C;margin-top:8px;}

.row{display:grid;grid-template-columns:160px 66px 1fr;gap:14px;align-items:center;
  background:color-mix(in srgb,var(--c) 7%,rgba(9,20,30,.9));
  border:1px solid color-mix(in srgb,var(--c) 30%,#12303F);
  border-left:3px solid var(--c);padding:9px 13px;}
.row.hot{box-shadow:0 0 20px color-mix(in srgb,var(--c) 26%,transparent);}
.nm{font-weight:700;font-size:14.5px;color:#EAF7FA;line-height:1.2;}
.nm span{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:500;letter-spacing:.1em;color:#5E8496;margin-top:3px;}
.sc{font-family:'IBM Plex Mono',monospace;font-size:1.6rem;font-weight:700;color:var(--c);
  text-align:right;line-height:1;text-shadow:0 0 16px color-mix(in srgb,var(--c) 50%,transparent);}
.sc span{display:block;font-size:8.5px;font-weight:600;letter-spacing:.18em;margin-top:4px;text-shadow:none;}
.bars{display:flex;flex-direction:column;gap:3px;}
.br{display:grid;grid-template-columns:14px 1fr 34px;gap:7px;align-items:center;}
.br .l{font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600;color:#4E7A8C;}
.br .t{height:5px;background:#0C1E2A;border:1px solid #12303F;}
.br .t i{display:block;height:100%;background:var(--bc);}
.br .n{font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#8FB5C4;text-align:right;}

.pnl{position:relative;background:rgba(9,20,30,.9);border:1px solid #12303F;padding:15px 17px;height:100%;}
.pnl::before,.pnl::after{content:"";position:absolute;width:10px;height:10px;border:1px solid #22D9E8;}
.pnl::before{top:-1px;left:-1px;border-right:0;border-bottom:0;}
.pnl::after{bottom:-1px;right:-1px;border-left:0;border-top:0;}
.pnl .h{font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:700;
  letter-spacing:.2em;text-transform:uppercase;color:#22D9E8;margin-bottom:10px;}
.pnl .b{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#CFE6EE;line-height:1.7;white-space:pre-wrap;}
.pnl .n{font-size:10.5px;color:#4E7A8C;margin-top:10px;line-height:1.55;}

.alert{background:color-mix(in srgb,var(--c) 12%,rgba(9,20,30,.9));border:1px solid var(--c);
  border-left:4px solid var(--c);padding:17px 19px;
  box-shadow:0 0 26px color-mix(in srgb,var(--c) 24%,transparent);}
.alert .tag{font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:700;letter-spacing:.22em;color:var(--c);}
.alert .ttl{font-size:1.55rem;font-weight:800;color:#EAF7FA;margin:6px 0 8px;letter-spacing:-.02em;}
.alert .act{font-size:14.5px;color:#DCEDF3;line-height:1.55;}
.alert .meta{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:#7FA8B8;margin-top:11px;letter-spacing:.06em;}

div[data-testid="column"] .stButton>button{font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:700;letter-spacing:.14em;padding:.6rem .2rem;border-radius:0;border:1px solid #1C4257;
  background:rgba(9,20,30,.9);color:#22D9E8;}
div[data-testid="column"] .stButton>button:hover{border-color:#22D9E8;color:#DFF6FA;}
div[role="dialog"]{background:#05101A !important;border:1px solid #22D9E8 !important;}

table{font-family:'IBM Plex Mono',monospace !important;font-size:12px !important;}
</style>
""", unsafe_allow_html=True)

# ---------------- DISTRICTS ------------------------------------------------
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

def _EV(d):
    E = min(d["pop"] / 28.0, 1.0)
    V = min((0.45*d["char"] + 0.35*d["kutcha"] + 0.20*d["dep"]) / 100.0, 1.0)
    return E, V, 0.45*E + 0.55*V

# most exposed+vulnerable district in the set — used to normalise, so the worst
# district reaches 100 at full hazard and the rest scale beneath it
MAXCOMP = max(_EV(d)[2] for _, d in DISTRICTS.iterrows())

def assess(d, mm):
    cap = EMB_MM[d["emb"]] * (1 - 0.30 * d["char"] / 100)
    H = min(max((mm - cap) / 55.0, 0.0), 1.0)      # ~55mm above threshold saturates hazard
    E, V, comp = _EV(d)
    score = 100 * H * (0.35 + 0.65 * (comp / MAXCOMP))
    return round(min(score, 100)), round(H,2), round(E,2), round(V,2), round(cap)

def action_for(b, char):
    if b == "RED":    return (f"Evacuate char and riverine settlements — {char}% of habitation — to raised "
                              f"relief camps now. Move livestock to embankment high ground.")
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

@st.cache_data(ttl=3600, show_spinner=False)
def archive_range(lats, lons, d0, d1):
    """Recorded daily rainfall for every district across a date range (ERA5)."""
    try:
        p = {"latitude": ",".join(f"{x:.3f}" for x in lats),
             "longitude": ",".join(f"{x:.3f}" for x in lons),
             "start_date": str(d0), "end_date": str(d1),
             "daily": "precipitation_sum", "timezone": "Asia/Kolkata"}
        j = requests.get("https://archive-api.open-meteo.com/v1/archive",
                         timeout=15, params=p).json()
        if isinstance(j, dict): j = [j]
        days = j[0]["daily"]["time"]
        cols = {}
        for i, loc in enumerate(j):
            cols[i] = [0.0 if v is None else float(v) for v in loc["daily"]["precipitation_sum"]]
        return days, cols
    except Exception:
        return None, None

LATS, LONS = tuple(DISTRICTS.lat), tuple(DISTRICTS.lon)

def sms_for(r):
    return (f"{r['Band']} FLOOD ALERT {r['District']}. {r['mm']}mm rain in 24h. Char and riverine "
            f"villages move to raised relief camp before dark. Take livestock and documents. -ASDMA")

def ivr_for(r):
    return (f"Flood warning from A S D M A for {r['District']} district. {r['Band']} alert. "
            f"Heavy rain expected. If you live on char land or near the embankment, move to the "
            f"relief camp today. Press 1 to repeat.")

# ---------------- FLOATING WINDOW -----------------------------------------
@st.dialog("District detail", width="large")
def district_window(r):
    st.markdown(f"<div class='alert' style='--c:{r['C']}'>"
                f"<div class='tag'>{r['Band']} · {MEANING[r['Band']].upper()} · RISK {r['Risk']}/100</div>"
                f"<div class='ttl'>{r['District']} district</div>"
                f"<div class='act'>{r['Action']}</div></div>", unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2)
    with a:
        st.markdown(f"<div class='pnl'><div class='h'>Why this score</div><div class='b'>"
                    f"Rainfall        {r['mm']} mm / 24h\n"
                    f"Embankment      {r['emb']} → holds {r['cap']} mm\n"
                    f"Char habitation {r['char']}% → threshold cut\n"
                    f"─────────────────────────────\n"
                    f"HAZARD        H = {r['H']}\n"
                    f"EXPOSURE      E = {r['E']}\n"
                    f"VULNERABILITY V = {r['V']}\n"
                    f"─────────────────────────────\n"
                    f"RISK          {r['Risk']} / 100</div>"
                    f"<div class='n'>Hazard multiplies. No rain means no risk however vulnerable the "
                    f"district.</div></div>", unsafe_allow_html=True)
    with b:
        st.markdown(f"<div class='pnl'><div class='h'>Who is at risk</div><div class='b'>"
                    f"Population       {r['pop']} lakh\n"
                    f"On char land     {r['char']}%  ≈ {round(r['pop']*r['char']/100,1)} lakh\n"
                    f"Kutcha housing   {r['kutcha']}%  ≈ {round(r['pop']*r['kutcha']/100,1)} lakh\n"
                    f"Children/elderly {r['dep']}%  ≈ {round(r['pop']*r['dep']/100,1)} lakh\n"
                    f"─────────────────────────────\n"
                    f"HIGHEST PRIORITY\n"
                    f"{round(r['pop']*r['char']/100,1)} lakh on char land</div>"
                    f"<div class='n'>Char settlements are riverine sandbars — first to inundate, "
                    f"last to be reached.</div></div>", unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    s, v = sms_for(r), ivr_for(r)
    with c1:
        st.markdown(f"<div class='pnl'><div class='h'>SMS · {len(s)} chars</div><div class='b'>{s}</div>"
                    f"<div class='n'>Feature phone, no data.</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='pnl'><div class='h'>IVR voice call</div><div class='b'>{v}</div>"
                    f"<div class='n'>No literacy needed.</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='pnl'><div class='h'>Off-grid</div><div class='b'>"
                    "· ASHA worker printed slip\n· Panchayat loudspeaker\n· Red flag at the ghat</div>"
                    "<div class='n'>Char villages lose tower coverage as the river rises.</div></div>",
                    unsafe_allow_html=True)


# ================= LOGIN ==================================================
USERS = {
    "ASDMA-01": {"role": "District officer",
                 "name": "O. Baruah", "desig": "District Commissioner · ASDMA"},
    "CHAR-77":  {"role": "Resident",
                 "name": "Resident", "desig": "Household account · Dhubri"},
}

if "auth" not in st.session_state:
    st.session_state.auth = None

if st.session_state.auth is None:
    st.markdown("<div class='cmd'><span><span class='dot'></span><b>BhuJal</b> &nbsp;·&nbsp; "
                "Assam district flood risk &amp; early warning</span>"
                "<span>restricted access &nbsp;·&nbsp; ASDMA prototype</span></div>",
                unsafe_allow_html=True)
    L, Rr = st.columns([1.15, 1])
    with L:
        st.markdown("<h1>Sign in</h1><p class='sub'>Two doors into the same warning. "
                    "The officer decides. The resident is told.</p>", unsafe_allow_html=True)
        u = st.text_input("User ID", placeholder="ASDMA-01")
        if st.button("SIGN IN", type="primary", use_container_width=True):
            rec = None
            for k, v in USERS.items():
                if k.lower() == u.strip().lower():
                    rec = v
            if rec:
                st.session_state.auth = dict(rec, uid=u.strip().upper())
                st.rerun()
            else:
                st.error("UNKNOWN USER ID · use ASDMA-01 or CHAR-77.")
        st.caption("No password on the prototype. Deployment sits behind the state SSO.")
    with Rr:
        st.markdown(
            "<div class='pnl'><div class='h'>District officer</div><div class='b'>ASDMA-01</div>"
            "<div class='n'>Full board: every district, risk breakdown, map, dispatch log. "
            "Sees the whole state and authorises nothing by hand — the broadcast is automatic."
            "</div></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(
            "<div class='pnl'><div class='h'>Resident</div><div class='b'>CHAR-77</div>"
            "<div class='n'>One screen. Your district, your risk, what to do tonight. "
            "If your district is in warning the alert is on screen before you touch anything."
            "</div></div>", unsafe_allow_html=True)
    st.stop()

AUTH = st.session_state.auth

# ---------------- HEADER + MODE -------------------------------------------
st.markdown("<div class='cmd'><span><span class='dot'></span><b>BhuJal</b> &nbsp;·&nbsp; "
            "Assam district flood risk &amp; early warning</span>"
            "<span>ECMWF / ERA5 rainfall — live &nbsp;·&nbsp; district profiles illustrative</span></div>",
            unsafe_allow_html=True)

view = AUTH["role"]
h0, h1, h2, h3 = st.columns([1.05, 1.3, 1.05, 1.25])
with h0:
    st.markdown(f"<div class='pnl' style='padding:10px 14px'><div class='h'>{AUTH['role']}</div>"
                f"<div class='b'>{AUTH['name']}</div>"
                f"<div class='n'>{AUTH['desig']}</div></div>", unsafe_allow_html=True)
    if st.button("Sign out", use_container_width=True):
        st.session_state.auth = None
        st.rerun()
with h1:
    st.markdown("<h1>Flood risk · live</h1>"
                "<p class='sub'>Reads the ECMWF forecast automatically — no operator input.</p>",
                unsafe_allow_html=True)
with h2:
    mode = st.radio("Mode", ["Live", "Replay past event", "Simulate"],
                    horizontal=True, label_visibility="collapsed")
rains, src = None, ""
with h3:
    if mode == "Live":
        rains = fetch_rain(LATS, LONS)
        src = "LIVE · ECMWF forecast via Open-Meteo · peak of next 3 days"
    elif mode == "Replay past event":
        dd = st.date_input("Replay date", value=date(2022, 6, 18), label_visibility="collapsed",
                           min_value=date(1990,1,1), max_value=date.today()-timedelta(days=6))
        rains = fetch_rain(LATS, LONS, dd)
        src = f"REPLAY · ERA5 reanalysis · recorded {dd}"
    if rains is None:
        mmv = st.slider("Simulated rainfall, next 24h (mm)", 0, 200, 95, 5)
        rains = [mmv]*len(DISTRICTS)
        src = (src + " — feed unreachable, simulating") if src else "SIMULATION · planning mode"

# ---------------- SCORE ----------------------------------------------------
rows = []
for i, d in DISTRICTS.iterrows():
    mm = rains[i]
    sc, H, E, V, cap = assess(d, mm)
    nm, col = band_for(sc)
    rows.append({"District": d["district"], "mm": round(mm), "Risk": sc, "Band": nm, "C": col,
                 "H": H, "E": E, "V": V, "cap": cap, "char": d["char"], "kutcha": d["kutcha"],
                 "dep": d["dep"], "pop": d["pop"], "emb": d["emb"],
                 "Action": action_for(nm, d["char"]), "lat": d["lat"], "lon": d["lon"]})
R = pd.DataFrame(rows).sort_values("Risk", ascending=False).reset_index(drop=True)
top = R.iloc[0].to_dict()
cnt = {b: int((R.Band == b).sum()) for b in ["RED","ORANGE","YELLOW","GREEN"]}
pop_exp = round(float(R[R.Risk >= 50]["pop"].sum()), 1)

# ---------------- RESIDENT VIEW -------------------------------------------
@st.dialog("Flood warning", width="large")
def citizen_alert(r):
    plain = {"RED":   "LEAVE NOW. Water is coming.",
             "ORANGE":"GET READY. Water may reach you.",
             "YELLOW":"STAY ALERT. Watch the river.",
             "GREEN": "NO WARNING. Normal day."}[r["Band"]]
    steps = {
        "RED":   ["Go to the ward relief camp before dark",
                  "Take your livestock to the embankment",
                  "Put documents and phone in a plastic bag",
                  "Tell your neighbours — do not wait to be told again"],
        "ORANGE":["Pack a bag: documents, medicine, dry food",
                  "Move valuables to the upper floor or a raised platform",
                  "Charge your phone now",
                  "Find out where your nearest relief camp is"],
        "YELLOW":["Keep listening for the next announcement",
                  "Check that your boat and rope are ready",
                  "Keep documents together in one place"],
        "GREEN": ["No action needed today"]}[r["Band"]]
    st.markdown(
        f"<div class='alert' style='--c:{r['C']};padding:26px 28px'>"
        f"<div class='tag' style='font-size:12px'>{r['Band']} ALERT · {r['District'].upper()} DISTRICT</div>"
        f"<div style='font-size:2.7rem;font-weight:800;color:{r['C']};letter-spacing:-.03em;"
        f"margin:10px 0 6px;line-height:1.05'>{plain}</div>"
        f"<div class='act' style='font-size:16px'>{r['mm']} mm of rain expected in the next 24 hours.</div>"
        f"</div>", unsafe_allow_html=True)
    st.write("")
    a, b = st.columns([1.25, 1])
    with a:
        st.markdown("<div class='pnl'><div class='h'>What to do</div><div class='b'>"
                    + "\n".join(f"{i+1}.  {s}" for i, s in enumerate(steps))
                    + "</div><div class='n'>Written for reading aloud. No jargon, no numbers you "
                      "cannot act on.</div></div>", unsafe_allow_html=True)
    with b:
        st.markdown(f"<div class='pnl'><div class='h'>The SMS you receive</div>"
                    f"<div class='b'>{sms_for(r)}</div>"
                    f"<div class='n'>Sent to every number on the {r['District']} cell tower, "
                    f"registered or not.</div></div>", unsafe_allow_html=True)


# ---------------- RESIDENT VIEW -------------------------------------------
if view == "Resident":
    my = st.selectbox("Your district", list(R.District.sort_values()), key="mydist")
    r = R[R.District == my].iloc[0].to_dict()

    # The app tells you. It fires the moment your district escalates, and resets
    # once you are back to safe, so the next escalation alerts you again.
    key = f"alerted::{my}"
    if r["Band"] in ("RED", "ORANGE"):
        if st.session_state.get(key) != r["Band"]:
            st.session_state[key] = r["Band"]
            citizen_alert(r)
    else:
        st.session_state.pop(key, None)

    plain = {"RED":   "LEAVE NOW. Water is coming.",
             "ORANGE":"GET READY. Water may reach you.",
             "YELLOW":"STAY ALERT. Watch the river.",
             "GREEN": "Normal day."}[r["Band"]]
    steps = {
        "RED":   ["Go to the ward relief camp before dark",
                  "Take your livestock to the embankment",
                  "Put documents and phone in a plastic bag",
                  "Tell your neighbours — do not wait to be told again"],
        "ORANGE":["Pack a bag: documents, medicine, dry food",
                  "Move valuables to the upper floor or a raised platform",
                  "Charge your phone now",
                  "Find out where your nearest relief camp is"],
        "YELLOW":["Keep listening for the next announcement",
                  "Check that your boat and rope are ready",
                  "Keep documents together in one place"],
        "GREEN": ["Nothing to do today"]}[r["Band"]]

    st.markdown(
        f"<div class='alert' style='--c:{r['C']};padding:34px 36px'>"
        f"<div class='tag' style='font-size:12px'>{r['Band']} ALERT · {r['District'].upper()} DISTRICT</div>"
        f"<div style='font-size:3.4rem;font-weight:800;color:{r['C']};letter-spacing:-.035em;"
        f"margin:12px 0 10px;line-height:1.02'>{plain}</div>"
        f"<div class='act' style='font-size:17px'>{r['mm']} mm of rain expected in the next 24 hours.</div>"
        f"</div>", unsafe_allow_html=True)
    st.write("")

    a, b = st.columns([1.3, 1])
    with a:
        st.markdown("<div class='pnl'><div class='h'>What to do</div><div class='b'>"
                    + "\n".join(f"{i+1}.  {s_}" for i, s_ in enumerate(steps))
                    + "</div><div class='n'>Written to be read aloud. No jargon, no numbers you "
                      "cannot act on.</div></div>", unsafe_allow_html=True)
    with b:
        if r["Band"] in ("RED", "ORANGE"):
            st.markdown(f"<div class='pnl'><div class='h'>The SMS you receive</div>"
                        f"<div class='b'>{sms_for(r)}</div>"
                        f"<div class='n'>Sent to every number on the {r['District']} cell tower, "
                        f"registered or not.</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='pnl'><div class='h'>You will be told</div><div class='b'>"
                        "The app reads the forecast every hour.\n\n"
                        "You do not need to open it.\n"
                        "If your district escalates, you get an\n"
                        "SMS, a voice call, and this screen.</div>"
                        "<div class='n'>Silence means safe.</div></div>", unsafe_allow_html=True)
    st.stop()


# ================= AUTO-BROADCAST ENGINE ==================================
# No operator presses send. The moment a district crosses into ORANGE or RED
# the roll for that district is dispatched. The flag clears when it drops back
# to safe, so the next escalation broadcasts again.

SEED_ROLL = {d: [f"+9194{abs(hash(d))%10:1d}{i:07d}" for i in range(1, 5)]
             for d in DISTRICTS.index}

if "roll" not in st.session_state:
    st.session_state.roll = {d: list(v) for d, v in SEED_ROLL.items()}
if "log" not in st.session_state:
    st.session_state.log = []
if "sent_band" not in st.session_state:
    st.session_state.sent_band = {}

def _gateway(number, body):
    """Real numbers go to the gateway. Seeded roll entries are fan-out
    placeholders and are never transmitted — they are marked as such."""
    if number.startswith("+9194"):
        return "SIMULATED", "roll placeholder — not transmitted"
    key = "textbelt"
    try:
        key = st.secrets.get("TEXTBELT_KEY", "textbelt")
    except Exception:
        pass
    try:
        j = requests.post("https://textbelt.com/text", timeout=12,
                          data={"phone": number, "message": body, "key": key}).json()
    except Exception as e:
        return "FAILED", f"network unreachable — {e}"
    return ("TRANSMITTED", str(j.get("textId", "—"))) if j.get("success") \
           else ("REFUSED", str(j.get("error", "unknown")))

def auto_broadcast(frame):
    fired = []
    for _, row in frame.iterrows():
        d, band = row["District"], row["Band"]
        if band in ("RED", "ORANGE"):
            if st.session_state.sent_band.get(d) != band:
                st.session_state.sent_band[d] = band
                body = sms_for(row.to_dict())
                stamp = datetime.now().strftime("%H:%M:%S")
                for num in st.session_state.roll.get(d, []):
                    status, note = _gateway(num, body)
                    st.session_state.log.insert(0, {
                        "Time": stamp, "District": d, "Band": band,
                        "Number": num[:6] + "\u2022" * 4 + num[-3:],
                        "Chars": len(body), "Status": status, "Gateway": note})
                fired.append((d, band, len(st.session_state.roll.get(d, []))))
        else:
            st.session_state.sent_band.pop(d, None)
    return fired

FIRED = auto_broadcast(R)

# ---------------- OFFICER VIEW · THREE TABS -------------------------------
T1, T2, T3 = st.tabs(["Warning", "Risk map", "Alert dispatch"])

# ================= WARNING ================================================
with T1:
    st.markdown(f"""<div class='kpis'>
    <div class='kpi' style='--c:#FF2D3F'><div class='v'>{cnt['RED']}</div><div class='k'>Red · take action</div></div>
    <div class='kpi' style='--c:#FF8A1E'><div class='v'>{cnt['ORANGE']}</div><div class='k'>Orange · be prepared</div></div>
    <div class='kpi' style='--c:#FFD21E'><div class='v'>{cnt['YELLOW']}</div><div class='k'>Yellow · be updated</div></div>
    <div class='kpi' style='--c:#00E08A'><div class='v'>{cnt['GREEN']}</div><div class='k'>Green · no warning</div></div>
    <div class='kpi' style='--c:#22D9E8'><div class='v'>{pop_exp}L</div><div class='k'>Population exposed</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<div class='alert' style='--c:{top['C']};padding:22px 26px'>"
                f"<div class='tag'>{top['Band']} · {MEANING[top['Band']].upper()} · "
                f"{'HIGHEST RISK' if top['Band'] != 'GREEN' else 'NO DISTRICT UNDER WARNING'}</div>"
                f"<div class='ttl' style='font-size:2.1rem'>{top['District']} · {top['Risk']}/100</div>"
                f"<div class='act'>{top['Action']}</div>"
                f"<div class='meta'>{top['mm']}MM RAIN · {top['emb'].upper()} EMBANKMENT · "
                f"CHAR {top['char']}% · {top['pop']} LAKH PEOPLE · "
                f"{round(top['pop']*top['char']/100,1)} LAKH ON CHAR LAND</div></div>",
                unsafe_allow_html=True)
    st.write("")

    warn = R[R.Risk >= 25].to_dict("records")
    if warn:
        st.markdown("<div class='sec'>Districts under warning · preparedness action</div>",
                    unsafe_allow_html=True)
        cols = st.columns(min(3, len(warn)))
        for i, r in enumerate(warn[:6]):
            with cols[i % len(cols)]:
                st.markdown(f"<div class='alert' style='--c:{r['C']};margin-bottom:12px'>"
                            f"<div class='tag'>{r['Band']} · {r['Risk']}/100</div>"
                            f"<div class='ttl' style='font-size:1.25rem'>{r['District']}</div>"
                            f"<div class='act' style='font-size:13.5px'>{r['Action']}</div>"
                            f"<div class='meta'>{r['mm']}MM · {round(r['pop']*r['char']/100,1)} LAKH "
                            f"ON CHAR LAND</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert' style='--c:#00E08A;padding:22px 26px'>"
                    "<div class='tag'>ALL CLEAR</div>"
                    "<div class='ttl' style='font-size:1.7rem'>No district above the warning threshold</div>"
                    "<div class='act'>Routine monitoring. The system re-reads the forecast every hour "
                    "and raises a warning on its own.</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='pnl'><div class='h'>Escalation chain · once a district turns Orange</div>"
                "<div class='b'>"
                "T−24h  District Commissioner + Circle Officer notified\n"
                "T−18h  Village volunteers and ASHA workers alerted\n"
                "T−12h  Household SMS + IVR wave 1\n"
                "T−6h   Relief camps opened, country boats positioned\n"
                "T−3h   Loudspeaker announcement in char villages</div>"
                "<div class='n'>Riverine flooding gives this much lead time. Landslides do not — which "
                "is why this system targets flooding.</div></div>", unsafe_allow_html=True)

# ================= RISK MAP ===============================================
with T2:
    m, s = st.columns([1, 1.3], gap="medium")
    with m:
        pts = R[["lat","lon"]].copy()
        pts["color"] = R.C
        pts["size"] = (R.Risk * 320 + 6000).astype(int)
        st.map(pts, color="color", size="size", zoom=6.3)
        st.caption(f"Source: {src}")

        if mode == "Replay past event":
            d0 = dd - timedelta(days=12)
            d1 = min(dd + timedelta(days=12), date.today() - timedelta(days=6))
            days, cols_ = archive_range(LATS, LONS, d0, d1)
            if days:
                series, peak = [], []
                for k, day in enumerate(days):
                    red = org = 0; mx = 0
                    for i, drow in DISTRICTS.iterrows():
                        mmv = cols_[i][k]; mx = max(mx, mmv)
                        sc, *_ = assess(drow, mmv)
                        if sc >= 75: red += 1
                        elif sc >= 50: org += 1
                    series.append({"date": day, "Orange": org, "Red": red}); peak.append(mx)
                fired = [x for x in series if x["Red"] > 0]
                st.markdown("<div class='sec'>Event replay · would the model have warned?</div>",
                            unsafe_allow_html=True)
                st.bar_chart(pd.DataFrame(series).set_index("date"),
                             color=["#FF8A1E", "#FF2D3F"], height=200)
                if fired:
                    worst = max(series, key=lambda x: (x["Red"], x["Orange"]))
                    st.markdown(f"<div class='alert' style='--c:#FF2D3F'>"
                                f"<div class='tag'>MODEL WOULD HAVE FIRED</div>"
                                f"<div class='ttl' style='font-size:1.3rem'>First RED · {fired[0]['date']}</div>"
                                f"<div class='act' style='font-size:13.5px'>Peak {worst['Red']} districts "
                                f"on Red and {worst['Orange']} on Orange, {worst['date']}. Peak recorded "
                                f"rainfall {max(peak):.0f} mm/24h.</div></div>", unsafe_allow_html=True)
                    st.caption("Run on recorded rainfall alone — no tuning to this event. The model "
                               "does not claim the flood was preventable, only that a warning was "
                               "available in advance.")
    with s:
        st.markdown("<div class='sec'>Risk score per district · click OPEN for the breakdown</div>",
                    unsafe_allow_html=True)
        for r in R.to_dict("records"):
            rc, bc = st.columns([11, 1.6])
            with rc:
                bars = "".join(
                    f"<div class='br' style='--bc:{r['C']}'><span class='l'>{lab}</span>"
                    f"<span class='t'><i style='width:{val*100:.0f}%'></i></span>"
                    f"<span class='n'>{val:.2f}</span></div>"
                    for lab, val in (("H", r['H']), ("E", r['E']), ("V", r['V'])))
                st.markdown(f"<div class='row{' hot' if r['Risk']>=50 else ''}' style='--c:{r['C']}'>"
                            f"<div class='nm'>{r['District']}<span>{r['mm']}MM · {r['emb'].upper()} · "
                            f"CHAR {r['char']}%</span></div>"
                            f"<div class='sc'>{r['Risk']}<span>{r['Band']}</span></div>"
                            f"<div class='bars'>{bars}</div></div>", unsafe_allow_html=True)
            with bc:
                if st.button("OPEN", key=f"o_{r['District']}", use_container_width=True):
                    district_window(r)

# ================= ALERT DISPATCH =========================================
with T3:
    st.markdown("<div class='sec'>Alert dispatch · one alert, four renderings</div>", unsafe_allow_html=True)
    pick = st.selectbox("District", list(R.District), index=0)
    r = R[R.District == pick].iloc[0].to_dict()
    st.markdown(f"<div class='alert' style='--c:{r['C']}'>"
                f"<div class='tag'>{r['Band']} · {MEANING[r['Band']].upper()} · RISK {r['Risk']}/100</div>"
                f"<div class='ttl'>{r['District']} district</div>"
                f"<div class='act'>{r['Action']}</div>"
                f"<div class='meta'>{round(r['pop']*r['char']/100,1)} LAKH ON CHAR LAND · "
                f"{round(r['pop']*r['kutcha']/100,1)} LAKH IN KUTCHA HOUSING · "
                f"{round(r['pop']*r['dep']/100,1)} LAKH CHILDREN AND ELDERLY</div></div>",
                unsafe_allow_html=True)
    st.write("")
    s_, v_ = sms_for(r), ivr_for(r)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='pnl'><div class='h'>01 · Officer dashboard</div><div class='b'>"
                    f"{r['District']}\nRISK {r['Risk']}/100 · {r['Band']}\n"
                    f"H {r['H']} × E {r['E']} × V {r['V']}</div>"
                    f"<div class='n'>DC office, circle officers.</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='pnl'><div class='h'>02 · SMS · {len(s_)} chars</div><div class='b'>{s_}</div>"
                    f"<div class='n'>Any feature phone, no data. Cell broadcast reaches unregistered "
                    f"numbers. Assamese · Bengali · Bodo · Hindi.</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='pnl'><div class='h'>03 · IVR voice call</div><div class='b'>{v_}</div>"
                    f"<div class='n'>No literacy requirement. Auto-dialled to the panchayat roll.</div></div>",
                    unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='pnl'><div class='h'>04 · Off-grid</div><div class='b'>"
                    "· ASHA worker — printed slip\n· Panchayat loudspeaker\n· Red flag at the ghat</div>"
                    "<div class='n'>Char villages lose tower coverage as the river rises. The system "
                    "degrades to paper and cloth by design.</div></div>", unsafe_allow_html=True)

    # ---------- AUTO-BROADCAST ---------------------------------------------
    st.write("")
    st.markdown("<div class='sec'>Auto-broadcast · fired without an operator</div>",
                unsafe_allow_html=True)

    live = R[R.Band.isin(["RED", "ORANGE"])]
    reach = sum(len(st.session_state.roll.get(d, [])) for d in live.District)
    st.markdown(
        f"<div class='alert' style='--c:#22D9E8'>"
        f"<div class='tag'>BROADCAST ENGINE · ARMED</div>"
        f"<div class='ttl'>{len(live)} districts under warning &middot; {reach} numbers on roll</div>"
        f"<div class='act'>Nobody presses send. When a district crosses into ORANGE or RED the "
        f"engine dispatches that district's roll immediately, and re-arms once the district "
        f"returns to safe.</div></div>", unsafe_allow_html=True)

    if FIRED:
        for d, band, n in FIRED:
            st.toast(f"BROADCAST · {d} · {band} · {n} numbers")

    e1, e2 = st.columns([2, 3])
    with e1:
        mynum = st.text_input("Add a number to a district roll",
                              placeholder="+919xxxxxxxxx", key="enrol_num")
        mydist = st.selectbox("District roll", list(R.District.sort_values()), key="enrol_dist")
        if st.button("ENROL", use_container_width=True):
            n = mynum.strip()
            if n and n not in st.session_state.roll.get(mydist, []):
                st.session_state.roll.setdefault(mydist, []).append(n)
                st.session_state.sent_band.pop(mydist, None)   # re-arm for this roll
                st.rerun()
    with e2:
        st.markdown(
            f"<div class='pnl'><div class='h'>How the fan-out works</div><div class='b'>"
            f"Roll placeholders are marked SIMULATED and never transmitted.\n"
            f"A number you enrol is dispatched through a live SMS gateway.\n"
            f"In deployment the roll is the cell-broadcast tower list, not a\n"
            f"phone book — every handset in the district cell receives it.</div>"
            f"<div class='n'>Enrol your own number, then push the district into RED with the "
            f"rainfall control. The broadcast fires on its own.</div></div>",
            unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='sec'>Dispatch log</div>", unsafe_allow_html=True)
    if st.session_state.log:
        st.dataframe(pd.DataFrame(st.session_state.log[:60]),
                     use_container_width=True, hide_index=True)
    else:
        st.markdown("<div class='pnl'><div class='b'>No district has crossed into warning. "
                    "Nothing dispatched.</div></div>", unsafe_allow_html=True)
