import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.csv")


def load_budgets() -> pd.DataFrame:
    df = pd.read_csv(BUDGETS_FILE)
    return df


def set_budget(category: str, monthly_limit: float) -> None:
    df = load_budgets()
    category = category.strip().title()

    if category in df["category"].values:
        df.loc[df["category"] == category, "monthly_limit"] = monthly_limit
        print(f"  Updated budget for '{category}': ${monthly_limit:.2f}/month")
    else:
        new_row = pd.DataFrame([{"category": category, "monthly_limit": monthly_limit}])
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"  Set budget for '{category}': ${monthly_limit:.2f}/month")

    df.to_csv(BUDGETS_FILE, index=False)


def show_budget_status(df: pd.DataFrame, month: str = None) -> None:
    from datetime import datetime

    if month is None:
        month = datetime.today().strftime("%Y-%m")

    budgets = load_budgets()
    if budgets.empty:
        print("  No budgets set. Use option 6 to set one.")
        return

    # Filter transactions to the chosen month
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    month_expenses = df[(df["type"] == "expense") & (df["month"].astype(str) == month)]
    actuals = month_expenses.groupby("category")["amount"].sum()

    print(f"\n-- Budget Status for {month} --")
    print(f"{'Category':<20} {'Spent':>10} {'Limit':>10} {'Status'}")
    print("-" * 55)

    for _, row in budgets.iterrows():
        cat = row["category"]
        limit = row["monthly_limit"]
        spent = actuals.get(cat, 0.0)
        pct = (spent / limit * 100) if limit > 0 else 0

        if pct >= 100:
            status = "OVER BUDGET"
        elif pct >= 80:
            status = "WARNING"
        else:
            status = "OK"

        print(f"  {cat:<18} ${spent:>9.2f} ${limit:>9.2f}   {status}")
