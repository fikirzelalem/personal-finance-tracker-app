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

st.sidebar.markdown("## Personal Finance Tracker")
st.sidebar.markdown("---")

pg.run()
