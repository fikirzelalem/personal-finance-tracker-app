import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_monthly_bar(df: pd.DataFrame) -> None:
    if df.empty:
        print("  No data to plot.")
        return

    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)

    months = [str(m) for m in summary.index]
    x = range(len(months))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))

    if "income" in summary.columns:
        ax.bar([i - width / 2 for i in x], summary["income"], width, label="Income", color="#4CAF50")
    if "expense" in summary.columns:
        ax.bar([i + width / 2 for i in x], summary["expense"], width, label="Expense", color="#F44336")

    ax.set_title("Monthly Income vs Expenses")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount ($)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_category_pie(df: pd.DataFrame) -> None:
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        print("  No expense data to plot.")
        return

    totals = expenses.groupby("category")["amount"].sum()

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        totals,
        labels=totals.index,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.82,
    )
    for at in autotexts:
        at.set_fontsize(9)

    ax.set_title("Spending by Category")
    plt.tight_layout()
    plt.show()


def plot_spending_trend(df: pd.DataFrame) -> None:
    expenses = df[df["type"] == "expense"].copy()
    if expenses.empty:
        print("  No expense data to plot.")
        return

    expenses["month"] = expenses["date"].dt.to_period("M")
    monthly = expenses.groupby("month")["amount"].sum()
    months = [str(m) for m in monthly.index]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, monthly.values, marker="o", color="#2196F3", linewidth=2, markersize=6)
    ax.fill_between(months, monthly.values, alpha=0.1, color="#2196F3")

    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Expenses ($)")
    ax.set_xticklabels(months, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.grid(linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()
