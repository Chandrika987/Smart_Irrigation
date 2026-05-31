import streamlit as st
import numpy as np
import joblib

import streamlit.components.v1 as components


# =========================
# UI CONFIGURATION & STYLES
# =========================
st.set_page_config(
    page_title="AI Smart Irrigation Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary-green: #16a34a;
        --deep-green: #166534;
        --soft-green: #dcfce7;
        --blue: #0ea5e9;
        --deep-blue: #075985;
        --soft-blue: #e0f2fe;
        --white: #ffffff;
        --ink: #102a43;
        --muted: #62748e;
        --border: rgba(22, 101, 52, 0.14);
        --shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(14, 165, 233, 0.16), transparent 34%),
            linear-gradient(180deg, #f8fffb 0%, #eef9ff 45%, #ffffff 100%);
        color: var(--ink);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #073b2a 0%, #075985 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.14);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.4rem;
        border-radius: 8px;
        background:
            linear-gradient(135deg, rgba(5, 150, 105, 0.94), rgba(14, 165, 233, 0.88)),
            url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.24);
        margin-bottom: 1.5rem;
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(6, 78, 59, 0.72), rgba(7, 89, 133, 0.22));
        z-index: 0;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 760px;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.18);
        color: #f0fdf4;
        font-weight: 700;
        letter-spacing: 0;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.24);
    }

    .hero h1 {
        margin: 0;
        color: #ffffff;
        font-size: clamp(2rem, 5vw, 4.2rem);
        line-height: 1.02;
        font-weight: 800;
        letter-spacing: 0;
    }

    .hero p {
        margin: 1rem 0 0;
        color: #ecfeff;
        font-size: 1.08rem;
        line-height: 1.7;
        max-width: 700px;
    }

    .metric-card,
    .content-card,
    .result-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid var(--border);
        border-radius: 8px;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .metric-card:hover,
    .content-card:hover,
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.13);
        border-color: rgba(14, 165, 233, 0.32);
    }

    .metric-card {
        padding: 1.1rem 1.2rem;
        min-height: 132px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.86rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0;
    }

    .metric-value {
        color: var(--ink);
        font-size: 2rem;
        line-height: 1.1;
        font-weight: 800;
        margin-top: 0.45rem;
    }

    .metric-help {
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: 0.45rem;
    }

    .content-card {
        padding: 1.35rem;
        margin-top: 1.1rem;
    }

    .section-title {
        color: var(--ink);
        font-size: 1.35rem;
        font-weight: 800;
        margin: 0 0 0.35rem;
        letter-spacing: 0;
    }

    .section-subtitle {
        color: var(--muted);
        margin: 0 0 1rem;
        line-height: 1.6;
    }

    .stSlider {
        padding: 0.3rem 0.45rem 0.65rem;
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(240, 253, 244, 0.78), rgba(224, 242, 254, 0.46));
        border: 1px solid rgba(22, 163, 74, 0.10);
        margin-bottom: 0.55rem;
    }

    div[data-testid="stSlider"] label p {
        color: var(--ink);
        font-weight: 700;
        font-size: 0.92rem;
    }

    .stButton > button {
        width: 100%;
        min-height: 3.35rem;
        border: 0;
        border-radius: 8px;
        background: linear-gradient(135deg, #16a34a 0%, #0ea5e9 100%);
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 800;
        box-shadow: 0 14px 30px rgba(14, 165, 233, 0.26);
        transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        filter: saturate(1.08);
        box-shadow: 0 18px 40px rgba(22, 163, 74, 0.28);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
        gap: 0.85rem;
        margin-top: 1rem;
    }

    .result-card {
        padding: 1rem;
    }

    .result-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        color: var(--ink);
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 66px;
        padding: 0.32rem 0.62rem;
        border-radius: 999px;
        color: #ffffff;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0;
    }

    .badge-on {
        background: linear-gradient(135deg, #16a34a, #22c55e);
        box-shadow: 0 8px 18px rgba(22, 163, 74, 0.28);
    }

    .badge-off {
        background: linear-gradient(135deg, #dc2626, #ef4444);
        box-shadow: 0 8px 18px rgba(220, 38, 38, 0.22);
    }

    .parcel-name {
        color: var(--muted);
        font-size: 0.9rem;
        font-weight: 600;
    }

    .success-pulse {
        padding: 1rem 1.1rem;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(220, 252, 231, 0.95), rgba(224, 242, 254, 0.92));
        border: 1px solid rgba(22, 163, 74, 0.22);
        color: var(--deep-green);
        font-weight: 800;
        animation: pulseGlow 1.8s ease-in-out infinite;
        margin-bottom: 0.9rem;
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(22, 163, 74, 0); }
        50% { box-shadow: 0 0 28px rgba(22, 163, 74, 0.20); }
    }

    .footer {
        margin-top: 2rem;
        padding: 1.1rem;
        text-align: center;
        color: var(--muted);
        border-top: 1px solid rgba(15, 23, 42, 0.08);
    }

    div[data-testid="stMetricValue"] {
        color: var(--deep-green);
        font-weight: 800;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 1.6rem;
        }

        .metric-card {
            min-height: auto;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🌿 Smart Sprinkler")
    st.markdown("AI-powered irrigation control for healthier crops and smarter water usage.")
    st.markdown("---")
    st.markdown("### Project Info")
    st.markdown("**Domain:** Precision Agriculture")
    st.markdown("**Sensors:** 20 soil moisture inputs")
    st.markdown("**Output:** Sprinkler ON/OFF status")
    st.markdown("**Goal:** Optimize parcel-level irrigation")
    st.markdown("---")
    st.markdown("### Dashboard Guide")
    st.markdown("Adjust scaled sensor values from **0.00** to **1.00**, then run prediction to view sprinkler recommendations.")


# =========================
# HERO & DASHBOARD SUMMARY
# =========================
st.markdown(
    """
    <section class="hero">
        <div class="hero-content">
            <div class="hero-kicker">🌾 AI Agriculture Dashboard</div>
            <h1>Smart Sprinkler System</h1>
            <p>
                Water wisely, grow better. Monitor 20 sensor zones and predict parcel-level
                sprinkler activation with a clean, production-ready irrigation dashboard.
            </p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="content-card">
        <div class="section-title">🌱 Intelligent Irrigation Management</div>
        <p class="section-subtitle">
            The Smart Sprinkler System is an AI-powered irrigation management solution designed
            to help farmers and gardeners optimize water usage and enhance crop health. Using
            real-time soil moisture sensor data, the system predicts which sprinklers need to be
            activated, ensuring precise watering for each plot.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# MODEL LOADING
# =========================
#Load the trained model
model = joblib.load("Farm_Irrigation_system.pkl")


# =========================
# SENSOR INPUT UI
# =========================
st.markdown(
    """
    <div class="content-card">
        <div class="section-title">🎛️ Sensor Control Panel</div>
        <p class="section-subtitle">
            Enter scaled sensor values from 0 to 1 to predict sprinkler status across all 20 parcels.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

#Collect sensor inputs (scaled values)
sensor_values = []
sensor_columns = st.columns(4)
for i in range(20):
    with sensor_columns[i % 4]:
        val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        sensor_values.append(val)


# =========================
# IRRIGATION STATISTICS
# =========================
avg_sensor_value = float(np.mean(sensor_values))
min_sensor_value = float(np.min(sensor_values))
max_sensor_value = float(np.max(sensor_values))

stat_col_1, stat_col_2, stat_col_3, stat_col_4 = st.columns(4)
with stat_col_1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Sensor Network</div>
            <div class="metric-value">20</div>
            <div class="metric-help">Active parcel sensors</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with stat_col_2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Average Reading</div>
            <div class="metric-value">{avg_sensor_value:.2f}</div>
            <div class="metric-help">Mean scaled moisture value</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with stat_col_3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Lowest Reading</div>
            <div class="metric-value">{min_sensor_value:.2f}</div>
            <div class="metric-help">Driest current sensor input</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with stat_col_4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Highest Reading</div>
            <div class="metric-value">{max_sensor_value:.2f}</div>
            <div class="metric-help">Wettest current sensor input</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# PREDICTION LOGIC & RESULTS UI
# =========================
#Predict button
st.markdown('<div class="content-card">', unsafe_allow_html=True)
predict_clicked = st.button("🚀 Predict Sprinklers")
st.markdown("</div>", unsafe_allow_html=True)

if predict_clicked:
    input_array = np.array(sensor_values).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    sprinklers_on = int(np.sum(prediction))
    sprinklers_off = int(len(prediction) - sprinklers_on)

    st.markdown(
        f"""
        <div class="content-card">
            <div class="success-pulse">✅ Prediction complete. Irrigation recommendation generated successfully.</div>
            <div class="section-title">💧 Modern Prediction Results</div>
            <p class="section-subtitle">
                Sprinklers recommended ON: <strong>{sprinklers_on}</strong> ·
                Sprinklers recommended OFF: <strong>{sprinklers_off}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result_html = '<div class="status-grid">'
    for i, status in enumerate(prediction):
        label = "ON" if status == 1 else "OFF"
        badge_class = "badge-on" if status == 1 else "badge-off"
        result_html += (
            f'<div class="result-card">'
            f'<div class="result-title">'
            f'<span>Sprinkler {i}</span>'
            f'<span class="badge {badge_class}">{label}</span>'
            f'</div>'
            f'<div class="parcel-name">parcel_{i}</div>'
            f'</div>'
        )
    result_html += "</div>"
    st.markdown(result_html, unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown(
    """
    <div class="footer">
        Built for precision agriculture portfolios, internships, hackathons, and AI-powered farm automation demos.
    </div>
    """,
    unsafe_allow_html=True,
)
