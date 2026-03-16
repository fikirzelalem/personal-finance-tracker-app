from tracker import (
    add_transaction,
    import_from_csv,
    load_transactions,
    load_categories,
    add_category,
    get_monthly_summary,
    get_category_totals,
)
from budget import set_budget, show_budget_status
from visualizations import (
    plot_monthly_bar,
    plot_category_pie,
    plot_spending_trend,
)


def print_menu():
    print("\n========== Personal Finance Tracker ==========")
    print("1. Add a transaction")
    print("2. Import transactions from CSV")
    print("3. View monthly summary")
    print("4. View category totals")
    print("5. Manage categories")
    print("6. Set budget limit")
    print("7. View budget status")
    print("8. Show monthly spending chart")
    print("9. Show category pie chart")
    print("10. Show spending trend")
    print("0. Exit")
    print("==============================================")


def handle_add_transaction():
    print("\n-- Add Transaction --")
    date = input("Date (YYYY-MM-DD): ").strip()
    amount = float(input("Amount: $"))
    tx_type = input("Type (income/expense): ").strip().lower()

    categories = load_categories()
    print("Categories:", ", ".join(categories))
    category = input("Category: ").strip()
    description = input("Description (optional): ").strip()

    add_transaction(date, amount, tx_type, category, description)


def handle_import():
    filepath = input("\nPath to CSV file: ").strip()
    added = import_from_csv(filepath)
    print(f"  Imported {added} new transaction(s).")


def handle_monthly_summary():
    df = load_transactions()
    if df.empty:
        print("  No transactions found.")
        return
    summary = get_monthly_summary(df)
    print("\n-- Monthly Summary --")
    print(summary.to_string())


def handle_category_totals():
    df = load_transactions()
    if df.empty:
        print("  No transactions found.")
        return
    tx_type = input("Type to view (income/expense) [expense]: ").strip().lower() or "expense"
    totals = get_category_totals(df, tx_type)
    print(f"\n-- {tx_type.title()} by Category --")
    for cat, amt in totals.items():
        print(f"  {cat:<20} ${amt:.2f}")


def handle_manage_categories():
    cats = load_categories()
    print("\nCurrent categories:", ", ".join(cats))
    name = input("Add new category (or press Enter to skip): ").strip()
    if name:
        add_category(name)


def handle_set_budget():
    categories = load_categories()
    print("\nCategories:", ", ".join(categories))
    category = input("Category: ").strip()
    limit = float(input("Monthly limit: $"))
    set_budget(category, limit)


def handle_budget_status():
    df = load_transactions()
    if df.empty:
        print("  No transactions found.")
        return
    month = input("Month to check (YYYY-MM) [current month]: ").strip()
    show_budget_status(df, month if month else None)


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_add_transaction()
        elif choice == "2":
            handle_import()
        elif choice == "3":
            handle_monthly_summary()
        elif choice == "4":
            handle_category_totals()
        elif choice == "5":
            handle_manage_categories()
        elif choice == "6":
            handle_set_budget()
        elif choice == "7":
            handle_budget_status()
        elif choice == "8":
            plot_monthly_bar(load_transactions())
        elif choice == "9":
            plot_category_pie(load_transactions())
        elif choice == "10":
            plot_spending_trend(load_transactions())
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("  Invalid option, try again.")


if __name__ == "__main__":
    main()
