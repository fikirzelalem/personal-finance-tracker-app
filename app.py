# =============================================================================
# app.py
# Author: Fikir Demeke
# Description: Streamlit entry point for the Personal Finance Tracker web app.
#              Configures the page layout and sets up multi-page navigation
#              across Overview, Transactions, Charts, and Budget pages.
# =============================================================================

import streamlit as st

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

overview = st.Page("pages/overview.py", title="Overview", icon="📊", default=True)
transactions = st.Page("pages/transactions.py", title="Transactions", icon="💳")
charts = st.Page("pages/charts.py", title="Charts", icon="📈")
budget = st.Page("pages/budget.py", title="Budget", icon="🎯")

pg = st.navigation([overview, transactions, charts, budget])

st.markdown("""
<style>
/* ── Global font ── */
html, body, [class*="css"], .stApp, .stMarkdown, .stText, button, input, select, textarea {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1117 50%, #0a1628 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #0a1628 100%);
    border-right: 1px solid rgba(76, 175, 80, 0.2);
}
[data-testid="stSidebar"] * {
    color: #e0e6f0 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1f3c, #0a2744);
    border: 1px solid rgba(76, 175, 80, 0.3);
    border-radius: 12px;
    padding: 16px !important;
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.08), 0 4px 15px rgba(0,0,0,0.4);
    transition: box-shadow 0.3s ease;
}
[data-testid="metric-container"]:hover {
    box-shadow: 0 0 30px rgba(76, 175, 80, 0.2), 0 4px 20px rgba(0,0,0,0.5);
}
[data-testid="metric-container"] label {
    color: #7ecfff !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #4CAF50 !important;
}

/* ── Page titles ── */
h1 {
    background: linear-gradient(90deg, #4CAF50, #7ecfff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}
h2, h3 {
    color: #c8d8f0 !important;
    font-weight: 600 !important;
}

/* ── Dividers ── */
hr {
    border-color: rgba(76, 175, 80, 0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a6b2e, #4CAF50);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.03em;
    transition: all 0.2s ease;
    box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    box-shadow: 0 4px 20px rgba(76, 175, 80, 0.5);
    transform: translateY(-1px);
}

/* ── Inputs and selects ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div,
[data-testid="stDateInput"] input {
    background-color: #0d1f3c !important;
    border: 1px solid rgba(76, 175, 80, 0.25) !important;
    border-radius: 8px !important;
    color: #e0e6f0 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(76, 175, 80, 0.2);
    border-radius: 10px;
    overflow: hidden;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0d1f3c;
    border: 1px solid rgba(76, 175, 80, 0.2) !important;
    border-radius: 10px !important;
}

/* ── Info / success / error boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left: 4px solid #4CAF50 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(76, 175, 80, 0.4) !important;
    color: #4CAF50 !important;
    border-radius: 8px;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(76, 175, 80, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 💰 Personal Finance Tracker")
st.sidebar.markdown("---")

pg.run()
