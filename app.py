"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🛡️  S E A   G U A R D  🛡️                         ║
║             Monitoring Maritime Safety in India's EEZ                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Main Streamlit application — UI, navigation, detection logic, alerts.
Enhanced v2.0 — custom alerts, map overlays, severity levels, notify button.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_generator import generate_dataset

# ─────────────────────────────────────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEA GUARD — Maritime EEZ Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  Custom CSS — premium dark-navy theme with enhanced alert styles
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ─────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0f2035 50%, #0a1628 100%);
    border-right: 1px solid rgba(0,200,255,0.15);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #00d4ff !important;
}

/* ── Metric cards ───────────────────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,120,200,0.12), rgba(0,200,255,0.06));
    border: 1px solid rgba(0,200,255,0.18);
    border-radius: 12px;
    padding: 16px 20px;
    backdrop-filter: blur(6px);
}
div[data-testid="stMetric"] label {
    color: #7ec8e3 !important;
    font-weight: 600;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700;
}

/* ── Dataframe styling ──────────────────────────────────────────────────── */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* ── CUSTOM ALERT BOXES — dark text on light backgrounds ────────────────── */
.custom-alert-red {
    background-color: #F8D7DA;
    color: #721C24;
    border: 1px solid #F5C6CB;
    border-left: 6px solid #DC3545;
    border-radius: 10px;
    padding: 20px 28px;
    margin: 14px 0;
    font-weight: 700;
    font-size: 1.15rem;
    line-height: 1.6;
    animation: alert-pulse 2.5s ease-in-out infinite;
}
@keyframes alert-pulse {
    0%, 100% { box-shadow: 0 0 6px rgba(220,53,69,0.2); }
    50%      { box-shadow: 0 0 22px rgba(220,53,69,0.45); }
}

.custom-alert-yellow {
    background-color: #FFF3CD;
    color: #856404;
    border: 1px solid #FFEEBA;
    border-left: 6px solid #FFC107;
    border-radius: 10px;
    padding: 20px 28px;
    margin: 14px 0;
    font-weight: 700;
    font-size: 1.1rem;
    line-height: 1.6;
}

.custom-alert-green {
    background-color: #D4EDDA;
    color: #155724;
    border: 1px solid #C3E6CB;
    border-left: 6px solid #28A745;
    border-radius: 10px;
    padding: 20px 28px;
    margin: 14px 0;
    font-weight: 700;
    font-size: 1.1rem;
    line-height: 1.6;
}

.custom-alert-blue {
    background-color: #D1ECF1;
    color: #0C5460;
    border: 1px solid #BEE5EB;
    border-left: 6px solid #17A2B8;
    border-radius: 10px;
    padding: 20px 28px;
    margin: 14px 0;
    font-weight: 600;
    font-size: 1.05rem;
    line-height: 1.6;
}

/* ── Hero / Intro styling ──────────────────────────────────────────────── */
.hero-title {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #0077ff, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: shimmer 3s linear infinite;
    margin-bottom: 0;
    letter-spacing: 8px;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.hero-tagline {
    text-align: center;
    font-size: 1.3rem;
    color: #7ec8e3;
    margin-top: 4px;
    letter-spacing: 2px;
}

.hero-divider {
    width: 120px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    margin: 20px auto;
    border-radius: 2px;
}

/* ── Status badges ──────────────────────────────────────────────────────── */
.badge-on {
    display: inline-block;
    background: rgba(0,200,80,0.2);
    color: #00e050;
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
    border: 1px solid rgba(0,200,80,0.3);
}
.badge-off {
    display: inline-block;
    background: rgba(255,40,40,0.2);
    color: #ff5050;
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
    border: 1px solid rgba(255,40,40,0.3);
}

/* ── Section headers ────────────────────────────────────────────────────── */
.section-header {
    font-size: 1.8rem;
    font-weight: 700;
    color: #00d4ff;
    border-bottom: 2px solid rgba(0,200,255,0.2);
    padding-bottom: 10px;
    margin-bottom: 20px;
    letter-spacing: 1px;
}

/* ── Severity badges ────────────────────────────────────────────────────── */
.severity-high {
    display: inline-block;
    background: #DC3545;
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
}
.severity-medium {
    display: inline-block;
    background: #FFC107;
    color: #333;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
}
.severity-low {
    display: inline-block;
    background: #17A2B8;
    color: #fff;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
}

/* ── Ship detail card ───────────────────────────────────────────────────── */
.ship-card {
    background: linear-gradient(145deg, rgba(0,100,180,0.12), rgba(0,60,120,0.08));
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 14px;
    padding: 24px;
    margin: 12px 0;
}

/* ── Notify button special styling ──────────────────────────────────────── */
.notify-success {
    background-color: #D4EDDA;
    color: #155724;
    border: 2px solid #28A745;
    border-radius: 12px;
    padding: 18px 28px;
    margin: 14px 0;
    font-weight: 700;
    font-size: 1.1rem;
    text-align: center;
    animation: notify-flash 1s ease-in-out;
}
@keyframes notify-flash {
    0%   { opacity: 0; transform: scale(0.95); }
    50%  { opacity: 1; transform: scale(1.02); }
    100% { opacity: 1; transform: scale(1); }
}

/* ── Map container ──────────────────────────────────────────────────────── */
.map-label {
    font-size: 1.15rem;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 8px;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Session state defaults
# ─────────────────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "page" not in st.session_state:
    st.session_state.page = "🏠 Intro"
if "notified" not in st.session_state:
    st.session_state.notified = False


# ─────────────────────────────────────────────────────────────────────────────
#  Load / cache data
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    return generate_dataset()

df_all = load_data()


# ─────────────────────────────────────────────────────────────────────────────
#  Credential store (simple dict — no DB)
# ─────────────────────────────────────────────────────────────────────────────
CREDENTIALS = {
    "coastguard01": "cg@2026",
    "navy01":       "navy@2026",
    "port01":       "port@2026",
    "fishery01":    "fish@2026",
    "admin":        "admin",
}

ROLES = ["Coast Guard", "Navy", "Port Authorities", "Fishery Department", "Others"]


# ─────────────────────────────────────────────────────────────────────────────
#  Detection helpers
# ─────────────────────────────────────────────────────────────────────────────
def detect_suspicious(df: pd.DataFrame) -> pd.DataFrame:
    """Flag ships meeting any suspicious criterion. Adds *reason* and *severity* columns."""
    reasons = []
    severities = []
    for _, row in df.iterrows():
        flags = []
        sev = "Low"
        if row["speed"] < 1:
            flags.append("🐟 Possible illegal fishing (speed < 1 kn)")
            sev = "Medium"
        if row["speed"] > 30:
            flags.append("⚡ Abnormal speed (speed > 30 kn)")
            if sev != "High":
                sev = "Medium"
        if str(row["ais_status"]).upper() == "OFF":
            flags.append("📡 Dark activity (AIS OFF)")
            sev = "High"
        reasons.append(" | ".join(flags) if flags else "")
        severities.append(sev if flags else "")
    df = df.copy()
    df["reason"] = reasons
    df["severity"] = severities
    return df[df["reason"] != ""]


def time_filter(df: pd.DataFrame, window: str) -> pd.DataFrame:
    """Return rows whose timestamp falls within *window*."""
    now = datetime.now()
    mapping = {
        "Now (latest)":  timedelta(minutes=5),
        "1 hour ago":    timedelta(hours=1),
        "1 day ago":     timedelta(days=1),
        "1 week ago":    timedelta(weeks=1),
        "1 month ago":   timedelta(days=30),
        "All data":      timedelta(days=365),
    }
    delta = mapping.get(window, timedelta(days=365))
    cutoff = now - delta
    return df[df["timestamp"] >= cutoff]


# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🛡️ SEA GUARD")
    st.markdown("---")

    if st.session_state.logged_in:
        st.markdown(f"**👤  {st.session_state.user_id}**")
        st.markdown(f"**🏷️  {st.session_state.role}**")
        st.markdown("---")

        page = st.radio(
            "Navigate",
            ["🏠 Intro", "📊 Dashboard", "📡 AIS Status",
             "🛰️ SAR Tracking", "🚨 Suspicious Ships", "🔍 Ship Tracking"],
            index=0,
            key="nav_radio",
        )
        st.session_state.page = page
        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "🏠 Intro"
            st.session_state.notified = False
            st.rerun()
    else:
        page = st.radio(
            "Navigate",
            ["🏠 Intro", "🔐 Login"],
            index=0,
            key="nav_radio_out",
        )
        st.session_state.page = page

    st.markdown("---")
    st.caption("© 2026 SEA GUARD · v2.0")


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: INTRO
# ═════════════════════════════════════════════════════════════════════════════
def page_intro():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="hero-title">🛡️ SEA GUARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-tagline">Monitoring Maritime Safety in India\'s EEZ</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚢 Total Ships", df_all["ship_id"].nunique())
    c2.metric("📡 AIS ON", int((df_all["ais_status"] == "ON").sum()))
    c3.metric("🔴 AIS OFF", int((df_all["ais_status"] == "OFF").sum()))
    susp = detect_suspicious(df_all)
    c4.metric("🚨 Suspicious", susp["ship_id"].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Intro Map — all ships at a glance ───────────────────────────────────
    st.markdown('<div class="map-label">🗺️ Fleet Overview — India\'s EEZ</div>', unsafe_allow_html=True)
    latest = df_all.sort_values("timestamp").groupby("ship_id").tail(1)
    map_data = latest[["latitude", "longitude"]].rename(
        columns={"latitude": "lat", "longitude": "lon"}
    )
    st.map(map_data)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        > **SEA GUARD** is an intelligent maritime surveillance prototype that
        > analyses AIS transponder data across India's Exclusive Economic Zone.
        > It detects *dark ships*, *illegal fishing*, and *abnormal movement*
        > in near real-time — empowering the Coast Guard, Navy, and port
        > authorities to act instantly.
        """,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("#### 📡 AIS Monitoring")
        st.markdown("Track transponder status across the fleet in real time.")
    with col_b:
        st.markdown("#### 🛰️ SAR Integration")
        st.markdown("Simulated SAR data cross-references AIS for dark-ship detection.")
    with col_c:
        st.markdown("#### 🚨 Instant Alerts")
        st.markdown("Automated rule-based alerts for authorities the moment threats surface.")


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: LOGIN
# ═════════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2.4rem;">🔐 Secure Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form("login_form"):
            uid = st.text_input("🆔 User ID", placeholder="e.g. coastguard01")
            pwd = st.text_input("🔑 Password", type="password", placeholder="••••••••")
            role = st.selectbox("🏷️ Role", ROLES)
            submitted = st.form_submit_button("🚀 Enter System", use_container_width=True)

            if submitted:
                if uid in CREDENTIALS and CREDENTIALS[uid] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.user_id = uid
                    st.session_state.role = role
                    st.session_state.page = "📊 Dashboard"
                    st.rerun()
                else:
                    st.markdown(
                        '<div class="custom-alert-red">❌ Invalid credentials. Please try again.</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("---")
        with st.expander("ℹ️ Demo credentials"):
            st.code(
                "coastguard01 / cg@2026\n"
                "navy01       / navy@2026\n"
                "port01       / port@2026\n"
                "fishery01    / fish@2026\n"
                "admin        / admin",
                language=None,
            )


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    st.markdown('<div class="section-header">📊 Maritime Dashboard</div>', unsafe_allow_html=True)

    # ── instant alert banner (custom styled) ────────────────────────────────
    susp = detect_suspicious(df_all)
    if not susp.empty:
        n = susp["ship_id"].nunique()
        st.markdown(
            '<div class="custom-alert-red">'
            '🚨 ALERT: Suspicious ship detected! Immediate review required.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="custom-alert-yellow">'
            f'⚠️ {n} suspicious ships detected! '
            f'Navigate to the <b>Suspicious Ships</b> page for detailed analysis.'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── time filter ─────────────────────────────────────────────────────────
    time_opt = st.selectbox(
        "🕒 Time filter",
        ["All data", "Now (latest)", "1 hour ago", "1 day ago", "1 week ago", "1 month ago"],
    )
    filtered = time_filter(df_all, time_opt)

    # ── KPIs ────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚢 Ships", filtered["ship_id"].nunique())
    c2.metric("📍 Records", len(filtered))
    c3.metric("📡 AIS ON", int((filtered["ais_status"] == "ON").sum()))
    c4.metric("🔴 AIS OFF", int((filtered["ais_status"] == "OFF").sum()))

    st.markdown("---")

    # ── Map Visualization ───────────────────────────────────────────────────
    st.markdown("#### 🗺️ Ship Locations Map")

    latest_filtered = filtered.sort_values("timestamp").groupby("ship_id").tail(1)

    # Separate normal vs suspicious for map
    susp_filtered = detect_suspicious(latest_filtered)
    susp_ids = set(susp_filtered["ship_id"].unique()) if not susp_filtered.empty else set()
    normal_ships = latest_filtered[~latest_filtered["ship_id"].isin(susp_ids)]
    suspicious_ships = latest_filtered[latest_filtered["ship_id"].isin(susp_ids)]

    map_tab_all, map_tab_normal, map_tab_suspicious = st.tabs(
        ["🗺️ All Ships", "✅ Normal Ships", "🔴 Suspicious Ships"]
    )

    with map_tab_all:
        all_map = latest_filtered[["latitude", "longitude"]].rename(
            columns={"latitude": "lat", "longitude": "lon"}
        )
        st.map(all_map)
        st.caption(f"Showing {len(latest_filtered)} ships on map")

    with map_tab_normal:
        if normal_ships.empty:
            st.markdown(
                '<div class="custom-alert-yellow">No normal ships in this time window.</div>',
                unsafe_allow_html=True,
            )
        else:
            normal_map = normal_ships[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            )
            st.map(normal_map)
            st.caption(f"Showing {len(normal_ships)} normal ships")

    with map_tab_suspicious:
        if suspicious_ships.empty:
            st.markdown(
                '<div class="custom-alert-green">✅ No suspicious ships in this time window.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="custom-alert-red">'
                f'🔴 {len(suspicious_ships)} suspicious ships plotted below!'
                '</div>',
                unsafe_allow_html=True,
            )
            susp_map = suspicious_ships[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            )
            st.map(susp_map)

    st.markdown("---")

    # ── data table ──────────────────────────────────────────────────────────
    st.markdown("#### 📋 Ship Records")
    st.dataframe(
        filtered.sort_values("timestamp", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=460,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: AIS STATUS
# ═════════════════════════════════════════════════════════════════════════════
def page_ais_status():
    st.markdown('<div class="section-header">📡 AIS Status Monitor</div>', unsafe_allow_html=True)

    # latest record per ship
    latest = df_all.sort_values("timestamp").groupby("ship_id").tail(1)

    ais_on  = latest[latest["ais_status"] == "ON"]
    ais_off = latest[latest["ais_status"] == "OFF"]

    c1, c2 = st.columns(2)
    c1.metric("✅ AIS ON", len(ais_on))
    c2.metric("🔴 AIS OFF", len(ais_off))

    st.markdown("---")

    tab_on, tab_off = st.tabs(["✅ AIS ON Ships", "🔴 AIS OFF (Dark Ships)"])

    with tab_on:
        if ais_on.empty:
            st.markdown(
                '<div class="custom-alert-blue">ℹ️ No ships with AIS ON in current data.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="custom-alert-green">'
                f'✅ {len(ais_on)} ships operating normally with AIS transponders active.'
                '</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                ais_on[["ship_id", "latitude", "longitude", "speed", "timestamp"]]
                .reset_index(drop=True),
                use_container_width=True,
            )
            # map of AIS ON ships
            st.markdown("#### 🗺️ AIS ON — Ship Locations")
            st.map(ais_on[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            ))

    with tab_off:
        if ais_off.empty:
            st.markdown(
                '<div class="custom-alert-green">🎉 No dark ships detected! All transponders active.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="custom-alert-red">'
                f'🚨 {len(ais_off)} ships have AIS turned OFF — potential dark activity!'
                '</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                ais_off[["ship_id", "latitude", "longitude", "speed", "timestamp"]]
                .reset_index(drop=True),
                use_container_width=True,
            )
            # map of dark ships
            st.markdown("#### 🗺️ Dark Ships — Last Known Locations")
            st.map(ais_off[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            ))


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: SAR TRACKING
# ═════════════════════════════════════════════════════════════════════════════
def page_sar():
    st.markdown('<div class="section-header">🛰️ SAR Simulation & Tracking</div>', unsafe_allow_html=True)

    st.markdown(
        """
        > **SAR (Synthetic Aperture Radar)** is assumed to detect **all** ships
        > regardless of AIS status.  If a vessel appears on SAR but has AIS OFF,
        > it is flagged as a **dark ship** — possible smuggling, illegal fishing,
        > or evasion.
        """,
    )

    latest = df_all.sort_values("timestamp").groupby("ship_id").tail(1)

    sar_detected = latest.copy()
    sar_detected["sar_detected"] = True
    sar_detected["dark_flag"] = sar_detected["ais_status"].apply(
        lambda s: "⚠️ DARK SHIP" if s == "OFF" else "✅ Normal"
    )

    dark = sar_detected[sar_detected["ais_status"] == "OFF"]

    c1, c2, c3 = st.columns(3)
    c1.metric("🛰️ SAR Detections", len(sar_detected))
    c2.metric("✅ AIS Verified", int((sar_detected["ais_status"] == "ON").sum()))
    c3.metric("⚠️ Dark Ships", len(dark))

    if not dark.empty:
        st.markdown(
            '<div class="custom-alert-red">'
            f'🚨 SAR detected {len(dark)} ships with AIS OFF — dark activity suspected!'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── SAR Map ─────────────────────────────────────────────────────────────
    st.markdown("#### 🛰️ SAR Detection Map")
    sar_tab_all, sar_tab_dark = st.tabs(["🛰️ All SAR Contacts", "⚠️ Dark Ships Only"])

    with sar_tab_all:
        st.map(sar_detected[["latitude", "longitude"]].rename(
            columns={"latitude": "lat", "longitude": "lon"}
        ))

    with sar_tab_dark:
        if dark.empty:
            st.markdown(
                '<div class="custom-alert-green">✅ No dark ships detected by SAR.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.map(dark[["latitude", "longitude"]].rename(
                columns={"latitude": "lat", "longitude": "lon"}
            ))

    st.markdown("---")
    st.markdown("#### 📋 SAR Detection Results")
    st.dataframe(
        sar_detected[["ship_id", "latitude", "longitude", "speed",
                       "ais_status", "dark_flag", "timestamp"]]
        .sort_values("dark_flag")
        .reset_index(drop=True),
        use_container_width=True,
        height=460,
    )


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: SUSPICIOUS SHIPS
# ═════════════════════════════════════════════════════════════════════════════
def page_suspicious():
    st.markdown('<div class="section-header">🚨 Suspicious Ships</div>', unsafe_allow_html=True)

    susp = detect_suspicious(df_all)

    if susp.empty:
        st.markdown(
            '<div class="custom-alert-green">🎉 No suspicious ships detected. All clear!</div>',
            unsafe_allow_html=True,
        )
        return

    n_ships = susp["ship_id"].nunique()
    n_records = len(susp)

    # ── instant alerts (custom styled) ──────────────────────────────────────
    st.markdown(
        '<div class="custom-alert-red">'
        '🚨 ALERT: Suspicious ship detected! Immediate review required.'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="custom-alert-yellow">'
        f'⚠️ {n_ships} suspicious ships detected across {n_records} records!'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── KPIs ────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚨 Suspicious Ships", n_ships)
    c2.metric("📄 Flagged Records", n_records)
    fishing = susp[susp["reason"].str.contains("fishing", case=False)]
    c3.metric("🐟 Illegal Fishing", fishing["ship_id"].nunique())
    high_sev = susp[susp["severity"] == "High"]
    c4.metric("🔴 High Severity", high_sev["ship_id"].nunique())

    st.markdown("---")

    # ── Severity breakdown ──────────────────────────────────────────────────
    st.markdown("#### 📊 Severity Breakdown")
    sev_c1, sev_c2, sev_c3 = st.columns(3)
    with sev_c1:
        high_count = susp[susp["severity"] == "High"]["ship_id"].nunique()
        st.markdown(
            f'<div class="custom-alert-red" style="text-align:center; font-size:1.3rem;">'
            f'<span class="severity-high">HIGH</span><br><br>'
            f'<b>{high_count}</b> ships<br>'
            f'<small>AIS OFF — Dark Activity</small></div>',
            unsafe_allow_html=True,
        )
    with sev_c2:
        med_count = susp[susp["severity"] == "Medium"]["ship_id"].nunique()
        st.markdown(
            f'<div class="custom-alert-yellow" style="text-align:center; font-size:1.3rem;">'
            f'<span class="severity-medium">MEDIUM</span><br><br>'
            f'<b>{med_count}</b> ships<br>'
            f'<small>Abnormal Speed / Fishing</small></div>',
            unsafe_allow_html=True,
        )
    with sev_c3:
        low_count = susp[susp["severity"] == "Low"]["ship_id"].nunique()
        st.markdown(
            f'<div class="custom-alert-blue" style="text-align:center; font-size:1.3rem;">'
            f'<span class="severity-low">LOW</span><br><br>'
            f'<b>{low_count}</b> ships<br>'
            f'<small>Minor Issues</small></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Map of suspicious ships ─────────────────────────────────────────────
    st.markdown("#### 🗺️ Suspicious Ship Locations")
    susp_latest = susp.sort_values("timestamp").groupby("ship_id").tail(1)
    st.map(susp_latest[["latitude", "longitude"]].rename(
        columns={"latitude": "lat", "longitude": "lon"}
    ))

    st.markdown("---")

    # ── Suspicious ship table with severity ─────────────────────────────────
    st.markdown("#### 📋 Suspicious Ship Details")
    st.dataframe(
        susp[["ship_id", "severity", "reason", "latitude", "longitude", "speed",
              "ais_status", "timestamp"]]
        .sort_values(["severity", "ship_id"], ascending=[True, True])
        .reset_index(drop=True),
        use_container_width=True,
        height=460,
    )

    # ── breakdown chart ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📊 Breakdown by Reason")

    reasons_flat = []
    for r in susp["reason"]:
        for part in r.split(" | "):
            reasons_flat.append(part.strip())
    rc = pd.Series(reasons_flat).value_counts()
    st.bar_chart(rc)

    # ── Notify Authorities button ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📢 Authority Notification")

    if st.button("🚨 Notify Authorities", use_container_width=True, type="primary"):
        st.session_state.notified = True

    if st.session_state.notified:
        st.markdown(
            '<div class="notify-success">'
            '✅ Notification sent successfully!<br>'
            f'📋 {n_ships} suspicious ship reports dispatched to '
            f'<b>{st.session_state.role}</b> command center.<br>'
            f'📅 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            '</div>',
            unsafe_allow_html=True,
        )
        st.balloons()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: SHIP TRACKING
# ═════════════════════════════════════════════════════════════════════════════
def page_tracking():
    st.markdown('<div class="section-header">🔍 Ship Tracking</div>', unsafe_allow_html=True)

    ships = sorted(df_all["ship_id"].unique())
    selected = st.selectbox("🚢 Select a ship", ships)

    ship_df = df_all[df_all["ship_id"] == selected].sort_values("timestamp", ascending=False)

    if ship_df.empty:
        st.markdown(
            '<div class="custom-alert-yellow">⚠️ No data available for this ship.</div>',
            unsafe_allow_html=True,
        )
        return

    latest = ship_df.iloc[0]

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚢 Ship ID", selected)
    c2.metric("⚓ Speed (kn)", latest["speed"])
    c3.metric("📍 Lat / Lon", f"{latest['latitude']}, {latest['longitude']}")
    c4.metric("📡 AIS", latest["ais_status"])

    st.markdown(f"**🕒 Last seen:** {latest['timestamp']}")

    # check suspicious
    susp = detect_suspicious(ship_df)
    if not susp.empty:
        st.markdown(
            '<div class="custom-alert-red">'
            '🚨 This ship has suspicious activity!'
            '</div>',
            unsafe_allow_html=True,
        )
        for _, row in susp.iterrows():
            severity = row["severity"]
            if severity == "High":
                css_class = "custom-alert-red"
            elif severity == "Medium":
                css_class = "custom-alert-yellow"
            else:
                css_class = "custom-alert-blue"
            st.markdown(
                f'<div class="{css_class}">'
                f'⚠️ <b>[{severity}]</b> {row["reason"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="custom-alert-green">'
            '✅ No suspicious activity detected for this ship.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 📜 Full History")
    st.dataframe(
        ship_df[["timestamp", "latitude", "longitude", "speed", "ais_status"]]
        .reset_index(drop=True),
        use_container_width=True,
    )

    # ship location map
    st.markdown("#### 🗺️ Location Map")
    map_data = ship_df[["latitude", "longitude"]].rename(
        columns={"latitude": "lat", "longitude": "lon"}
    )
    st.map(map_data)


# ═════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ═════════════════════════════════════════════════════════════════════════════
page = st.session_state.page

if page == "🏠 Intro":
    page_intro()
elif page == "🔐 Login":
    page_login()
elif page == "📊 Dashboard":
    if not st.session_state.logged_in:
        st.markdown(
            '<div class="custom-alert-yellow">🔒 Please log in first to access the dashboard.</div>',
            unsafe_allow_html=True,
        )
        page_login()
    else:
        page_dashboard()
elif page == "📡 AIS Status":
    if not st.session_state.logged_in:
        st.markdown(
            '<div class="custom-alert-yellow">🔒 Please log in first.</div>',
            unsafe_allow_html=True,
        )
        page_login()
    else:
        page_ais_status()
elif page == "🛰️ SAR Tracking":
    if not st.session_state.logged_in:
        st.markdown(
            '<div class="custom-alert-yellow">🔒 Please log in first.</div>',
            unsafe_allow_html=True,
        )
        page_login()
    else:
        page_sar()
elif page == "🚨 Suspicious Ships":
    if not st.session_state.logged_in:
        st.markdown(
            '<div class="custom-alert-yellow">🔒 Please log in first.</div>',
            unsafe_allow_html=True,
        )
        page_login()
    else:
        page_suspicious()
elif page == "🔍 Ship Tracking":
    if not st.session_state.logged_in:
        st.markdown(
            '<div class="custom-alert-yellow">🔒 Please log in first.</div>',
            unsafe_allow_html=True,
        )
        page_login()
    else:
        page_tracking()
