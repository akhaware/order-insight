from __future__ import annotations

from decimal import Decimal, InvalidOperation

from .models import Order


class InteractiveOrderCollector:
    """Collects order data from stdin and returns validated Order objects."""

    def __init__(self) -> None:
        self._next_index = 1

    def collect_orders(self) -> list[Order]:
        orders: list[Order] = []
        print("Enter customer orders. Type 'Exit' for customer name when finished.")
        while True:
            customer_name = input("Customer name: ").strip()
            if customer_name.casefold() == "exit":
                break
            if not customer_name:
                print("Customer name cannot be empty.")
                continue

            try:
                order = self._collect_single_order(customer_name)
            except ValueError as exc:
                print(f"Invalid order: {exc}")
                continue

            orders.append(order)
            self._next_index += 1
            print(f"Recorded order {order.order_id} for {order.customer_name}.\n")

        return orders

    def _collect_single_order(self, customer_name: str) -> Order:
        product = self._prompt_required("Product: ")
        category = self._prompt_required("Category: ")
        quantity = self._prompt_positive_int("Quantity: ")
        unit_price = self._prompt_money("Unit price: ")

        return Order(
            order_id=f"USR-{self._next_index:04d}",
            customer_name=customer_name,
            product=product,
            category=category,
            quantity=quantity,
            unit_price=unit_price,
        )

    @staticmethod
    def _prompt_required(prompt: str) -> str:
        value = input(prompt).strip()
        if not value:
            raise ValueError(f"{prompt.rstrip(': ')} cannot be empty")
        return value

    @staticmethod
    def _prompt_positive_int(prompt: str) -> int:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError("quantity must be a whole number") from exc
        if value <= 0:
            raise ValueError("quantity must be greater than zero")
        return value

    @staticmethod
    def _prompt_money(prompt: str) -> Decimal:
        raw = input(prompt).strip()
        try:
            value = Decimal(raw)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("unit price must be a valid number") from exc
        if value < Decimal("0"):
            raise ValueError("unit price cannot be negative")
        return value.quantize(Decimal("0.01"))
