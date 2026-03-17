# Personal Finance Tracker

A multi-page personal finance dashboard built with Python, Streamlit, and Plotly. Track income and expenses, visualize spending patterns, and manage budgets — all in an interactive web app.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.43-red) ![Plotly](https://img.shields.io/badge/Plotly-5.9-purple) ![Pandas](https://img.shields.io/badge/Pandas-1.5-green)

---

## Features

- **Overview Dashboard** — KPI cards for total income, expenses, net savings, and savings rate with interactive monthly charts
- **Transaction Management** — Add transactions, import from CSV with automatic deduplication, filter and export data
- **Interactive Charts** — Spending trend line, category donut pie, stacked monthly bar chart, and a daily spending heatmap
- **Budget Tracking** — Set monthly limits per category with color-coded progress bars (on track / warning / over budget)
- **Custom Categories** — Add and manage your own spending categories
- **CSV Export** — Download any filtered view of your transactions

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data loading, cleaning, and aggregation |
| Streamlit | Multi-page web app framework |
| Plotly | Interactive charts |
| CSV | Lightweight persistent data store |

---

## Project Structure

```
personal-finance-tracker/
├── app.py                  # Entry point — page config and navigation
├── tracker.py              # Core logic — load, add, save, deduplicate transactions
├── budget.py               # Budget logic — set limits, compare actuals
├── visualizations.py       # Original matplotlib charts (CLI version)
├── main.py                 # Original CLI menu (terminal version)
├── requirements.txt
├── data/
│   ├── transactions.csv    # Transaction records
│   ├── budgets.csv         # Monthly budget limits
│   └── categories.csv      # User-defined categories
└── pages/
    ├── overview.py         # KPI dashboard
    ├── transactions.py     # Transaction table, add form, CSV import
    ├── charts.py           # Interactive visualizations
    └── budget.py           # Budget status and management
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/fikirzelalem/personal-finance-tracker-app.git
cd personal-finance-tracker-app
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Screenshots

> will add screenshots of the Overview, Charts, and Budget pages here.

---

## How It Works

- All data is stored locally in CSV files inside the `data/` folder
- When you import a CSV, the app deduplicates against existing records so importing the same file twice never creates duplicate entries
- Budget progress bars update automatically when you add new transactions
- All charts are interactive — hover for exact values, click the legend to toggle series, scroll to zoom
