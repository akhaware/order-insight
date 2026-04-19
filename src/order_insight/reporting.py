from __future__ import annotations

from decimal import Decimal

from .analytics import (
    build_customer_products_map,
    build_product_category_map,
    classify_customers,
    common_customers_across_categories,
    customer_total_spend,
    customers_who_bought_electronics,
    customers_with_multiple_categories,
    high_value_customers,
    most_frequently_purchased_products,
    revenue_by_category,
    top_n_customers_by_spend,
    unique_product_categories,
    unique_products,
)
from .constants import CLOTHING, ELECTRONICS
from .models import Order, ReportData


def _format_money(value: Decimal) -> str:
    return f"${value:.2f}"


def build_report_data(orders: list[Order]) -> ReportData:
    spend = customer_total_spend(orders)
    category_revenue = revenue_by_category(orders)
    return ReportData(
        available_categories=sorted(unique_product_categories(orders)),
        customer_spend=spend,
        customer_classifications=classify_customers(spend),
        high_value_customers=high_value_customers(spend),
        category_revenue=category_revenue,
        electronics_customers=customers_who_bought_electronics(orders),
        top_customers=top_n_customers_by_spend(spend, limit=3),
        popular_products=most_frequently_purchased_products(orders),
        multi_category_customers=sorted(customers_with_multiple_categories(orders)),
        electronics_and_clothing_customers=sorted(
            common_customers_across_categories(orders, ELECTRONICS, CLOTHING)
        ),
        unique_products=sorted(unique_products(orders)),
        product_category_map=build_product_category_map(orders),
        customer_products_map=build_customer_products_map(orders),
    )


def generate_console_report(orders: list[Order]) -> str:
    report = build_report_data(orders)

    lines: list[str] = []
    lines.append("=== ORDERINSIGHT CUSTOMER ORDER ANALYTICS REPORT ===")
    lines.append("")
    lines.append("Available Product Categories:")
    for category in report.available_categories:
        lines.append(f"- {category}")

    lines.append("")
    lines.append("Customer Summary:")
    for customer_name in sorted(report.customer_spend):
        lines.append(
            f"- {customer_name}: {_format_money(report.customer_spend[customer_name])} "
            f"({report.customer_classifications[customer_name]})"
        )

    lines.append("")
    lines.append("High-Value Customers:")
    for customer_name in report.high_value_customers:
        lines.append(f"- {customer_name}")

    lines.append("")
    lines.append("Revenue by Category:")
    for category_name in sorted(report.category_revenue):
        lines.append(
            f"- {category_name}: {_format_money(report.category_revenue[category_name])}"
        )

    lines.append("")
    lines.append("Customers Who Purchased Electronics:")
    for customer_name in report.electronics_customers:
        lines.append(f"- {customer_name}")

    lines.append("")
    lines.append("Top 3 Highest-Spending Customers:")
    for customer_name, total in report.top_customers:
        lines.append(f"- {customer_name}: {_format_money(total)}")

    lines.append("")
    lines.append("Most Frequently Purchased Products:")
    for product_name in report.popular_products:
        lines.append(f"- {product_name}")

    lines.append("")
    lines.append("Customers Who Purchased from Multiple Categories:")
    for customer_name in report.multi_category_customers:
        lines.append(f"- {customer_name}")

    lines.append("")
    lines.append("Customers Who Bought Both Electronics and Clothing:")
    for customer_name in report.electronics_and_clothing_customers:
        lines.append(f"- {customer_name}")

    lines.append("")
    lines.append("Unique Products:")
    for product_name in report.unique_products:
        lines.append(f"- {product_name}")

    lines.append("")
    lines.append("Product to Category Mapping:")
    for product_name in sorted(report.product_category_map):
        lines.append(f"- {product_name}: {report.product_category_map[product_name]}")

    lines.append("")
    lines.append("Customer to Ordered Products Mapping:")
    for customer_name in sorted(report.customer_products_map):
        products = ", ".join(report.customer_products_map[customer_name])
        lines.append(f"- {customer_name}: {products}")

    return "\n".join(lines)
