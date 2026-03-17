# =============================================================================
# File: pages/transactions.py
# Author: Fikir Zelalem
# Description: Transactions management page for the Personal Finance Tracker.
#              Displays a filterable transaction table with CSV export,
#              a form to add new transactions, a CSV file importer with
#              deduplication, and a category manager.
# =============================================================================

import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tracker import load_transactions, add_transaction, import_from_csv, load_categories, add_category, delete_transaction

st.title("💳 Transactions")

@st.cache_data
def get_data():
    return load_transactions()

df = get_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    tx_type_filter = st.selectbox("Type", ["All", "income", "expense"])
    if not df.empty:
        selected_cats = st.multiselect(
            "Categories",
            options=sorted(df["category"].unique()),
            default=sorted(df["category"].unique()),
        )
    else:
        selected_cats = []

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = df.copy()
if tx_type_filter != "All":
    filtered = filtered[filtered["type"] == tx_type_filter]
if selected_cats:
    filtered = filtered[filtered["category"].isin(selected_cats)]

# ── Transaction table ─────────────────────────────────────────────────────────
st.markdown("### All Transactions")

if not filtered.empty:
    display = filtered.sort_values("date", ascending=False).reset_index(drop=True)
    display["date"] = display["date"].dt.strftime("%Y-%m-%d")
    display["amount"] = display["amount"].apply(lambda x: f"${x:,.2f}")

    st.dataframe(
        display[["date", "type", "category", "amount", "description"]],
        use_container_width=True,
        column_config={
            "date":        st.column_config.TextColumn("Date"),
            "type":        st.column_config.TextColumn("Type"),
            "category":    st.column_config.TextColumn("Category"),
            "amount":      st.column_config.TextColumn("Amount"),
            "description": st.column_config.TextColumn("Description"),
        },
        hide_index=True,
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download filtered data", csv_data, "transactions_export.csv", "text/csv")
else:
    st.info("No transactions match the selected filters.")

st.markdown("---")

# ── Add transaction form ──────────────────────────────────────────────────────
st.markdown("### Add a Transaction")

categories = load_categories()

with st.form("add_transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    date     = col1.date_input("Date")
    amount   = col2.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    tx_type  = col1.selectbox("Type", ["expense", "income"])
    category = col2.selectbox("Category", categories)
    description = st.text_input("Description (optional)")
    submitted = st.form_submit_button("Add Transaction")

if submitted:
    if amount <= 0:
        st.error("Amount must be greater than $0.")
    else:
        add_transaction(str(date), amount, tx_type, category, description)
        st.success(f"Added {tx_type} of ${amount:.2f} in '{category}'.")
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# ── Import CSV ────────────────────────────────────────────────────────────────
st.markdown("### Import from CSV")
st.caption("CSV must have columns: date, amount, type, category, description")

uploaded = st.file_uploader("Choose a CSV file", type="csv")
if uploaded:
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name
    added = import_from_csv(tmp_path)
    st.success(f"Imported {added} new transaction(s).")
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# ── Delete a transaction ──────────────────────────────────────────────────────
st.markdown("### Delete a Transaction")

all_tx = load_transactions()
if not all_tx.empty:
    all_tx["label"] = all_tx.apply(
        lambda r: f"#{int(r['id'])} — {r['date'].strftime('%Y-%m-%d')} | {r['type']} | ${r['amount']:.2f} | {r['category']} | {r['description']}",
        axis=1,
    )
    selected_label = st.selectbox("Select transaction to delete", all_tx["label"])
    selected_id = int(all_tx.loc[all_tx["label"] == selected_label, "id"].values[0])

    if st.button("🗑 Delete Transaction", type="primary"):
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = selected_id

if "confirm_delete" in st.session_state:
    st.warning(f"Are you sure you want to delete transaction #{st.session_state.confirm_delete}? This cannot be undone.")
    col1, col2 = st.columns(2)
    if col1.button("Yes, delete it"):
        delete_transaction(st.session_state.confirm_delete)
        del st.session_state.confirm_delete
        st.cache_data.clear()
        st.success("Transaction deleted.")
        st.rerun()
    if col2.button("Cancel"):
        del st.session_state.confirm_delete
        st.rerun()

st.markdown("---")

# ── Manage categories ─────────────────────────────────────────────────────────
st.markdown("### Manage Categories")
with st.expander("View / Add Categories"):
    st.write(", ".join(categories))
    new_cat = st.text_input("New category name")
    if st.button("Add Category"):
        if new_cat.strip():
            add_category(new_cat.strip())
            st.success(f"Category '{new_cat.strip().title()}' added.")
            st.rerun()
        else:
            st.error("Please enter a category name.")
