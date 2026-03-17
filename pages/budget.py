import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tracker import load_transactions, load_categories
from budget import load_budgets, set_budget

st.title("🎯 Budget")

@st.cache_data
def get_data():
    return load_transactions()

df = get_data()

# ── Sidebar: pick month ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    if not df.empty:
        months = sorted(df["date"].dt.to_period("M").astype(str).unique(), reverse=True)
        selected_month = st.selectbox("Month", months)
    else:
        selected_month = None

st.markdown("### Budget Status")

budgets = load_budgets()

if budgets.empty:
    st.info("No budgets set yet. Use the form below to set your first budget.")
elif selected_month is None:
    st.info("No transaction data found.")
else:
    month_expenses = df[
        (df["type"] == "expense") &
        (df["date"].dt.to_period("M").astype(str) == selected_month)
    ]
    actuals = month_expenses.groupby("category")["amount"].sum()

    for _, row in budgets.iterrows():
        cat   = row["category"]
        limit = row["monthly_limit"]
        spent = actuals.get(cat, 0.0)
        pct   = min(spent / limit, 1.0) if limit > 0 else 0

        if pct >= 1.0:
            color  = "#EF5350"
            status = "🔴 Over budget"
        elif pct >= 0.8:
            color  = "#FFA726"
            status = "🟡 Warning"
        else:
            color  = "#66BB6A"
            status = "🟢 On track"

        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{cat}**")
        col2.markdown(f"${spent:,.2f} / ${limit:,.2f}")
        col3.markdown(status)

        fig = go.Figure(go.Bar(
            x=[spent], y=[""],
            orientation="h",
            marker_color=color,
            width=0.4,
        ))
        fig.add_shape(type="line", x0=limit, x1=limit, y0=-0.5, y1=0.5, line=dict(color="white", width=2, dash="dash"))
        fig.update_layout(
            height=50,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, max(limit * 1.1, spent * 1.1)], showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True}, key=f"budget_bar_{cat}")

    # ── Summary table ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Summary Table")

    rows = []
    for _, row in budgets.iterrows():
        cat      = row["category"]
        limit    = row["monthly_limit"]
        spent    = actuals.get(cat, 0.0)
        remaining = limit - spent
        pct      = (spent / limit * 100) if limit > 0 else 0
        rows.append({"Category": cat, "Spent": f"${spent:,.2f}", "Limit": f"${limit:,.2f}", "Remaining": f"${remaining:,.2f}", "Used %": f"{pct:.1f}%"})

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.markdown("---")

# ── Set / update budget form ──────────────────────────────────────────────────
st.markdown("### Set a Budget")
categories = load_categories()

with st.form("set_budget_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    category = col1.selectbox("Category", categories)
    limit    = col2.number_input("Monthly limit ($)", min_value=1.0, step=10.0, format="%.2f")
    submitted = st.form_submit_button("Save Budget")

if submitted:
    set_budget(category, limit)
    st.success(f"Budget for '{category}' set to ${limit:,.2f}/month.")
    st.cache_data.clear()
    st.rerun()
