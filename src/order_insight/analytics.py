from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal
from typing import Iterable

from .constants import HIGH_VALUE_THRESHOLD, MODERATE_VALUE_THRESHOLD, ELECTRONICS
from .models import Order


def list_customer_names(orders: Iterable[Order]) -> list[str]:
    return sorted({order.customer_name for order in orders})


def build_customer_products_map(orders: Iterable[Order]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    for order in orders:
        mapping[order.customer_name].append(order.product)
    return dict(mapping)


def build_product_category_map(orders: Iterable[Order]) -> dict[str, str]:
    return {order.product: order.category for order in orders}


def unique_product_categories(orders: Iterable[Order]) -> set[str]:
    return {order.category for order in orders}


def customer_total_spend(orders: Iterable[Order]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for order in orders:
        totals[order.customer_name] += order.line_total
    return dict(totals)


def classify_buyer(total_spend: Decimal) -> str:
    if total_spend > HIGH_VALUE_THRESHOLD:
        return "High-Value Buyer"
    if MODERATE_VALUE_THRESHOLD <= total_spend <= HIGH_VALUE_THRESHOLD:
        return "Moderate Buyer"
    return "Low-Value Buyer"


def classify_customers(spend_by_customer: dict[str, Decimal]) -> dict[str, str]:
    return {
        customer_name: classify_buyer(total)
        for customer_name, total in spend_by_customer.items()
    }


def high_value_customers(spend_by_customer: dict[str, Decimal]) -> list[str]:
    return sorted(
        map(
            lambda item: item[0],
            filter(
                lambda item: item[1] > HIGH_VALUE_THRESHOLD,
                spend_by_customer.items(),
            ),
        )
    )


def revenue_by_category(orders: Iterable[Order]) -> dict[str, Decimal]:
    revenue: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for order in orders:
        revenue[order.category] += order.line_total
    return dict(revenue)


def unique_products(orders: Iterable[Order]) -> set[str]:
    return {order.product for order in orders}


def customers_by_category(orders: Iterable[Order], category: str) -> set[str]:
    return {
        order.customer_name
        for order in orders
        if order.category == category
    }


def customers_who_bought_electronics(orders: Iterable[Order]) -> list[str]:
    return sorted(customers_by_category(orders, ELECTRONICS))


def top_n_customers_by_spend(
    spend_by_customer: dict[str, Decimal],
    limit: int = 3,
) -> list[tuple[str, Decimal]]:
    return sorted(
        spend_by_customer.items(),
        key=lambda item: (-item[1], item[0]),
    )[:limit]


def product_purchase_frequency(orders: Iterable[Order]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for order in orders:
        counter[order.product] += order.quantity
    return dict(counter)


def most_frequently_purchased_products(orders: Iterable[Order]) -> list[str]:
    frequency = product_purchase_frequency(orders)
    if not frequency:
        return []
    max_frequency = max(frequency.values())
    return sorted(
        [product for product, qty in frequency.items() if qty == max_frequency]
    )


def customers_with_multiple_categories(orders: Iterable[Order]) -> set[str]:
    categories_by_customer: dict[str, set[str]] = defaultdict(set)
    for order in orders:
        categories_by_customer[order.customer_name].add(order.category)

    return {
        customer_name
        for customer_name, categories in categories_by_customer.items()
        if len(categories) > 1
    }


def common_customers_across_categories(
    orders: Iterable[Order],
    left_category: str,
    right_category: str,
) -> set[str]:
    return customers_by_category(orders, left_category) & customers_by_category(
        orders, right_category
    )
