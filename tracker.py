import pandas as pd
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.csv")


def load_transactions() -> pd.DataFrame:
    df = pd.read_csv(TRANSACTIONS_FILE, parse_dates=["date"])
    df.dropna(subset=["amount", "type", "category"], inplace=True)
    df.drop_duplicates(inplace=True)
    return df


def save_transactions(df: pd.DataFrame) -> None:
    df.to_csv(TRANSACTIONS_FILE, index=False)


def add_transaction(date: str, amount: float, tx_type: str, category: str, description: str = "") -> None:
    df = load_transactions()

    tx_type = tx_type.lower()
    if tx_type not in ("income", "expense"):
        raise ValueError("type must be 'income' or 'expense'")

    new_row = {
        "id": int(df["id"].max() + 1) if not df.empty else 1,
        "date": pd.to_datetime(date),
        "amount": float(amount),
        "type": tx_type,
        "category": category.strip().title(),
        "description": description.strip(),
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_transactions(df)
    print(f"  Added: {tx_type} of ${amount:.2f} in '{category}' on {date}")


def import_from_csv(filepath: str) -> int:
    """Import transactions from an external CSV and deduplicate against existing data."""
    new_df = pd.read_csv(filepath, parse_dates=["date"])
    new_df.dropna(subset=["amount", "type", "category"], inplace=True)

    existing = load_transactions()
    combined = pd.concat([existing, new_df], ignore_index=True)
    combined.drop_duplicates(subset=["date", "amount", "type", "category", "description"], inplace=True)

    combined.reset_index(drop=True, inplace=True)
    combined["id"] = combined.index + 1

    added = len(combined) - len(existing)
    save_transactions(combined)
    return added


def get_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    return summary


def get_category_totals(df: pd.DataFrame, tx_type: str = "expense") -> pd.Series:
    filtered = df[df["type"] == tx_type]
    return filtered.groupby("category")["amount"].sum().sort_values(ascending=False)


def load_categories() -> list:
    df = pd.read_csv(CATEGORIES_FILE)
    return df["name"].tolist()


def add_category(name: str) -> None:
    cats = load_categories()
    name = name.strip().title()
    if name not in cats:
        cats.append(name)
        pd.DataFrame({"name": cats}).to_csv(CATEGORIES_FILE, index=False)
        print(f"  Category '{name}' added.")
    else:
        print(f"  Category '{name}' already exists.")
