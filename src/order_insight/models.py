from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    customer_name: str
    product: str
    category: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("order_id cannot be empty")
        if not self.customer_name.strip():
            raise ValueError("customer_name cannot be empty")
        if not self.product.strip():
            raise ValueError("product cannot be empty")
        if not self.category.strip():
            raise ValueError("category cannot be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than zero")
        if self.unit_price < Decimal("0"):
            raise ValueError("unit_price cannot be negative")

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity

    @staticmethod
    def from_dict(payload: dict) -> "Order":
        try:
            return Order(
                order_id=str(payload["order_id"]).strip(),
                customer_name=str(payload["customer_name"]).strip(),
                product=str(payload["product"]).strip(),
                category=str(payload["category"]).strip(),
                quantity=int(payload["quantity"]),
                unit_price=Decimal(str(payload["unit_price"])),
            )
        except KeyError as exc:
            raise ValueError(f"Missing required field: {exc.args[0]}") from exc
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid order payload: {payload}") from exc


@dataclass(frozen=True, slots=True)
class ReportData:
    available_categories: list[str]
    customer_spend: dict[str, Decimal]
    customer_classifications: dict[str, str]
    high_value_customers: list[str]
    category_revenue: dict[str, Decimal]
    electronics_customers: list[str]
    top_customers: list[tuple[str, Decimal]]
    popular_products: list[str]
    multi_category_customers: list[str]
    electronics_and_clothing_customers: list[str]
    unique_products: list[str]
    product_category_map: dict[str, str]
    customer_products_map: dict[str, list[str]]
