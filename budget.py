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
