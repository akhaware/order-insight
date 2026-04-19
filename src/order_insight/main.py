from __future__ import annotations

import argparse
import logging

from .input_handler import InteractiveOrderCollector
from .logging_config import configure_logging
from .reporting import generate_console_report
from .repository import InMemoryOrderStore, get_default_data_file, load_orders_from_json

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="order-insight",
        description=(
            "Analyze customer orders either from interactive input or from the bundled sample dataset."
        ),
    )
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Load the bundled sample dataset and generate the expected demo report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    log_file = configure_logging()
    LOGGER.info("File logging enabled: %s", log_file)

    store = InMemoryOrderStore()

    try:
        if args.sample_data:
            sample_file = get_default_data_file()
            orders = load_orders_from_json(sample_file)
            LOGGER.info("Loaded %d sample orders from %s", len(orders), sample_file)
        else:
            collector = InteractiveOrderCollector()
            orders = collector.collect_orders()

        if not orders:
            print("No orders were entered. Nothing to analyze.")
            LOGGER.info("Application ended with no input orders")
            return 0

        store.extend(orders)
        LOGGER.info("Prepared %d orders in in-memory store", len(store))
        report = generate_console_report(store.list_all())
        print()
        print(report)
        return 0
    except KeyboardInterrupt:
        print("\nInput interrupted by user.")
        LOGGER.warning("Interactive session interrupted by user")
        return 130
    except Exception:
        LOGGER.exception("Application failed while generating OrderInsight analytics")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
