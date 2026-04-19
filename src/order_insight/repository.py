from __future__ import annotations

import json
from pathlib import Path

from .models import Order


class InMemoryOrderStore:
    """Simple in-memory store for runtime-entered orders."""

    def __init__(self) -> None:
        self._orders: list[Order] = []

    def add(self, order: Order) -> None:
        self._orders.append(order)

    def extend(self, orders: list[Order]) -> None:
        self._orders.extend(orders)

    def list_all(self) -> list[Order]:
        return list(self._orders)

    def clear(self) -> None:
        self._orders.clear()

    def __len__(self) -> int:
        return len(self._orders)


def load_orders_from_json(file_path: str | Path) -> list[Order]:
    path = Path(file_path)
    raw_data = json.loads(path.read_text(encoding="utf-8"))
    return [Order.from_dict(record) for record in raw_data]


def get_default_data_file() -> Path:
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "data" / "sample_orders.json"
