import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tracker import load_transactions

st.title("📊 Overview")

@st.cache_data
def get_data():
    return load_transactions()

df = get_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    if not df.empty:
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        selected_cats = st.multiselect("Categories", options=sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    else:
        date_range = None
        selected_cats = []

# ── Filter data ───────────────────────────────────────────────────────────────
if not df.empty and date_range and len(date_range) == 2:
    mask = (
        (df["date"].dt.date >= date_range[0]) &
        (df["date"].dt.date <= date_range[1]) &
        (df["category"].isin(selected_cats))
    )
    df = df[mask]

# ── KPI cards ─────────────────────────────────────────────────────────────────
st.markdown("### At a Glance")

total_income  = df[df["type"] == "income"]["amount"].sum()
total_expense = df[df["type"] == "expense"]["amount"].sum()
net_savings   = total_income - total_expense
savings_rate  = (net_savings / total_income * 100) if total_income > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Income",   f"${total_income:,.2f}")
col2.metric("Total Expenses", f"${total_expense:,.2f}")
col3.metric("Net Savings",    f"${net_savings:,.2f}", delta=f"{savings_rate:.1f}% savings rate")
col4.metric("Transactions",   len(df))

st.markdown("---")

# ── Monthly income vs expenses bar chart ─────────────────────────────────────
if not df.empty:
    st.markdown("### Monthly Income vs Expenses")
    monthly = df.copy()
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    monthly_grouped = monthly.groupby(["month", "type"])["amount"].sum().reset_index()

    fig = px.bar(
        monthly_grouped,
        x="month", y="amount", color="type",
        barmode="group",
        color_discrete_map={"income": "#4CAF50", "expense": "#EF5350"},
        labels={"amount": "Amount ($)", "month": "Month", "type": "Type"},
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-45,
        legend_title_text="",
        hovermode="x unified",
    )
    fig.update_yaxes(tickprefix="$", gridcolor="rgba(128,128,128,0.15)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Top spending categories ───────────────────────────────────────────────
    st.markdown("### Top Spending Categories")
    top_cats = (
        df[df["type"] == "expense"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig2 = px.bar(
        top_cats, x="amount", y="category",
        orientation="h",
        color="amount",
        color_continuous_scale="Reds",
        labels={"amount": "Total Spent ($)", "category": ""},
    )
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
    )
    fig2.update_xaxes(tickprefix="$", gridcolor="rgba(128,128,128,0.15)")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No transactions found for the selected filters.")
