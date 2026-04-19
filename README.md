# OrderInsight

OrderInsight is a small Python analytics application that can collect customer orders interactively, store them in memory, and generate a business-friendly summary report. It also ships with a bundled sample dataset so you can reproduce the expected demo report instantly.

## What this project does

- collects customer orders from runtime input
- stores validated orders in memory
- analyzes customer spending and product/category trends
- derives high-value customers using `filter()` and `map()`
- prints a structured report to the console
- logs execution details to a rotating log file
- supports a bundled sample-data mode for repeatable demo output
- keeps unit tests deterministic with hardcoded test data

## Project layout

```text
order-insight/
├── .gitignore
├── README.md
├── pyproject.toml
├── data/
│   └── sample_orders.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── sample_output.txt
├── logs/
├── src/
│   └── order_insight/
│       ├── __init__.py
│       ├── analytics.py
│       ├── constants.py
│       ├── input_handler.py
│       ├── logging_config.py
│       ├── main.py
│       ├── models.py
│       ├── reporting.py
│       └── repository.py
└── tests/
    └── test_order_insight.py
```

## Run the app

Create and activate a virtual environment, then install the package in editable mode.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Run with interactive input

```bash
python -m order_insight.main
```

The app prompts for:

- customer name
- product
- category
- quantity
- unit price

Type `Change` for the customer name when you have finished entering orders.

## Run with bundled sample data

```bash
python -m order_insight.main --sample-data
```

This loads `data/sample_orders.json` into memory and prints the expected demo report. The full example output is stored in:

```text
docs/sample_output.txt
```

## Example interactive session

```text
Customer name: Alice
Product: Laptop
Category: Electronics
Quantity: 1
Unit price: 1200

Customer name: Bob
Product: T-Shirt
Category: Clothing
Quantity: 2
Unit price: 25

Customer name: Change
```

After that, the application prints the analytics report.

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Logging

Application logs are written to:

```text
logs/order_insight.log
```

The log file uses rotation and keeps up to 3 backups.

## Design notes

- runtime order input is stored in `InMemoryOrderStore`
- analytics functions remain pure and reusable
- high-value customer extraction uses `filter()` and `map()`
- reporting is separated from data collection
- tests use hardcoded `Order` objects instead of interactive input
- sample-data mode helps reproduce the expected report quickly
