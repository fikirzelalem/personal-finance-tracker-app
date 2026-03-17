# =============================================================================
# File: pages/charts.py
# Author: Fikir Zelalem
# Description: Interactive charts page for the Personal Finance Tracker.
#              Includes a monthly spending trend line, a category donut pie
#              chart, a stacked monthly bar chart by category, and a daily
#              spending heatmap. All charts are filterable via the sidebar.
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tracker import load_transactions

st.title("📈 Charts")

@st.cache_data
def get_data():
    return load_transactions()

df = get_data()

if df.empty:
    st.info("No transaction data found. Add some transactions first.")
    st.stop()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    selected_cats = st.multiselect(
        "Categories",
        options=sorted(df["category"].unique()),
        default=sorted(df["category"].unique()),
    )
    chart_type = st.radio("View", ["Expenses", "Income", "Both"])

# ── Apply filters ─────────────────────────────────────────────────────────────
if len(date_range) == 2:
    df = df[(df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])]
if selected_cats:
    df = df[df["category"].isin(selected_cats)]

expenses = df[df["type"] == "expense"]
income   = df[df["type"] == "income"]

# ── Monthly spending trend ────────────────────────────────────────────────────
st.markdown("### Monthly Spending Trend")

trend_df = df.copy()
trend_df["month"] = trend_df["date"].dt.to_period("M").astype(str)

if chart_type == "Both":
    trend = trend_df.groupby(["month", "type"])["amount"].sum().reset_index()
    fig = px.line(
        trend, x="month", y="amount", color="type",
        markers=True,
        color_discrete_map={"income": "#4CAF50", "expense": "#EF5350"},
        labels={"amount": "Amount ($)", "month": "Month", "type": "Type"},
    )
else:
    filter_type = "expense" if chart_type == "Expenses" else "income"
    color = "#EF5350" if filter_type == "expense" else "#4CAF50"
    trend = trend_df[trend_df["type"] == filter_type].groupby("month")["amount"].sum().reset_index()
    fig = px.line(trend, x="month", y="amount", markers=True, labels={"amount": "Amount ($)", "month": "Month"})
    fig.update_traces(line_color=color, fill="tozeroy", fillcolor=f"rgba(239,83,80,0.08)" if filter_type == "expense" else "rgba(76,175,80,0.08)")

fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", hovermode="x unified", xaxis_tickangle=-45, legend_title_text="")
fig.update_yaxes(tickprefix="$", gridcolor="rgba(128,128,128,0.15)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Category pie chart ────────────────────────────────────────────────────────
st.markdown("### Spending by Category")

col1, col2 = st.columns(2)

if not expenses.empty:
    cat_totals = expenses.groupby("category")["amount"].sum().reset_index()
    fig2 = px.pie(
        cat_totals, values="amount", names="category",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig2.update_traces(textposition="outside", textinfo="percent+label")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False, margin=dict(t=20, b=20))
    col1.plotly_chart(fig2, use_container_width=True)
else:
    col1.info("No expense data.")

# ── Monthly breakdown stacked bar ─────────────────────────────────────────────
if not expenses.empty:
    stacked = expenses.copy()
    stacked["month"] = stacked["date"].dt.to_period("M").astype(str)
    stacked_grouped = stacked.groupby(["month", "category"])["amount"].sum().reset_index()

    fig3 = px.bar(
        stacked_grouped, x="month", y="amount", color="category",
        labels={"amount": "Amount ($)", "month": "Month", "category": "Category"},
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis_tickangle=-45, hovermode="x unified", legend_title_text="Category")
    fig3.update_yaxes(tickprefix="$", gridcolor="rgba(128,128,128,0.15)")
    col2.plotly_chart(fig3, use_container_width=True)
else:
    col2.info("No expense data.")

st.markdown("---")

# ── Daily spending heatmap ────────────────────────────────────────────────────
st.markdown("### Daily Spending Heatmap")

if not expenses.empty:
    heat = expenses.copy()
    heat["week"]    = heat["date"].dt.isocalendar().week.astype(str)
    heat["weekday"] = heat["date"].dt.day_name()
    heat_grouped = heat.groupby(["week", "weekday"])["amount"].sum().reset_index()

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_grouped["weekday"] = pd.Categorical(heat_grouped["weekday"], categories=day_order, ordered=True)
    heat_pivot = heat_grouped.pivot(index="weekday", columns="week", values="amount").fillna(0)

    fig4 = px.imshow(
        heat_pivot,
        color_continuous_scale="Reds",
        labels=dict(x="Week", y="Day", color="Spent ($)"),
        aspect="auto",
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20))
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No expense data for heatmap.")
