# Architecture

## Overview

OrderInsight follows a small layered design:

1. `main.py` selects execution mode, initializes logging, and orchestrates the workflow.
2. `input_handler.py` collects and validates runtime user input.
3. `repository.py` stores runtime orders in memory.
4. `analytics.py` computes customer, product, and category insights.
5. `reporting.py` builds and formats the final report.
6. `logging_config.py` configures console and file logging.

## Execution modes

### Sample data mode
When the application is run with `--sample-data`, it loads the bundled sample dataset, stores it in memory, executes analytics, and prints the expected report.

### Interactive mode
When sample data is not requested, the application collects orders from user input. Input stops when the user enters `Change` as the customer name. The collected orders are stored in memory and then analyzed.

## Key design choices

### Interactive input + optional sample data
The application supports both:
- interactive runtime entry for realistic execution
- sample-data mode for predictable demos and expected output generation

This keeps the project practical while still making it easy to reproduce the report.

### In-memory storage
Orders are stored in an `InMemoryOrderStore` during execution. This keeps the design simple and avoids database or file-write complexity while preserving a clean boundary between input and analytics.

### Pure analytics layer
The analytics module accepts `Order` objects and returns computed values. It does not prompt for input, perform I/O, or print results. This makes the logic reusable and easy to test.

### Functional derivation of high-value customers
High-value customers are derived in the analytics layer using Python functional constructs such as `filter()` and `map()`. This highlights an additional Pythonic approach for transforming computed customer-spend data while keeping the logic isolated inside the analytics layer.

### Stable automated tests
Unit tests use a hardcoded dataset so they remain deterministic, repeatable, and independent of interactive input flow.

### Clean reporting boundary
`build_report_data()` prepares a structured report payload, and `generate_console_report()` formats it for display. This keeps presentation concerns separate from analytics logic.

### Thin orchestration layer
`main.py` is intentionally lightweight. Its role is to coordinate input loading, storage, analysis, reporting, and logging rather than hold business rules.

### Logging for traceability
The application writes logs to both console and file. This helps trace execution flow and debug issues in input handling, orchestration, and report generation.

## Runtime flow

### Sample-data flow
1. `main.py` starts the application and initializes logging.
2. Sample data is loaded from the bundled dataset.
3. Raw records are converted into `Order` objects.
4. Orders are stored in memory.
5. Analytics functions compute insights.
6. High-value customers are derived from spend totals using `filter()` and `map()`.
7. Reporting functions generate the final console output.

### Interactive flow
1. `main.py` starts the application and initializes logging.
2. `input_handler.py` prompts the user for order details.
3. Each valid entry is converted into an `Order` object.
4. Orders are stored in memory.
5. Input collection stops when the user enters `Change`.
6. Analytics functions compute insights.
7. High-value customers are derived from spend totals using `filter()` and `map()`.
8. Reporting functions generate the final console output.

## Main modules

### `main.py`
Coordinates the application lifecycle:
- initialize logging
- choose sample-data or interactive mode
- collect or load orders
- store orders
- invoke analytics
- invoke reporting

### `models.py`
Defines the domain model, primarily the `Order` object used throughout the application.

### `input_handler.py`
Handles interactive prompting, parsing, validation, and stop-condition handling for runtime input.

### `repository.py`
Provides the in-memory order store abstraction used to collect and retrieve runtime data.

### `analytics.py`
Contains business logic for:
- total spending per customer
- customer classification
- high-value customer derivation using `filter()` and `map()`
- revenue by category
- unique products
- electronics buyers
- multi-category buyers
- top spenders
- product frequency analysis

### `reporting.py`
Builds structured report data and renders the final human-readable report.

### `logging_config.py`
Configures console logging and rotating file logging.

## Testing approach

The application flow is dynamic, but the tests are intentionally static.

- Runtime execution uses interactive input or bundled sample data.
- Unit tests use hardcoded `Order` objects.
- This keeps analytics verification stable and independent of user input behavior.

## Why this design works

This architecture keeps the project:
- modular
- testable
- easy to debug
- easy to extend
- closer to production code than a single-script implementation

It also makes future enhancements straightforward, such as:
- CSV or JSON input
- file or database-backed repositories
- alternate report formats
- richer CLI support
