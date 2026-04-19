from decimal import Decimal
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from order_insight.analytics import (
    build_customer_products_map,
    build_product_category_map,
    classify_buyer,
    classify_customers,
    common_customers_across_categories,
    customer_total_spend,
    customers_who_bought_electronics,
    customers_with_multiple_categories,
    high_value_customers,
    list_customer_names,
    most_frequently_purchased_products,
    revenue_by_category,
    top_n_customers_by_spend,
    unique_product_categories,
    unique_products,
)
from order_insight.constants import CLOTHING, ELECTRONICS
from order_insight.models import Order
from order_insight.reporting import build_report_data, generate_console_report
from order_insight.repository import InMemoryOrderStore


TEST_ORDERS = [
    Order("ORD-1001", "Aarav Sharma", "Bluetooth Speaker", "Electronics", 1, Decimal("72.00")),
    Order("ORD-1002", "Aarav Sharma", "Kurta", "Clothing", 2, Decimal("24.00")),
    Order("ORD-1003", "Aarav Sharma", "Storage Basket", "Home Essentials", 1, Decimal("18.00")),
    Order("ORD-1004", "Diya Iyer", "Jeans", "Clothing", 1, Decimal("34.00")),
    Order("ORD-1005", "Diya Iyer", "Coffee Maker", "Home Essentials", 1, Decimal("18.00")),
    Order("ORD-1006", "Kunal Patel", "Headphones", "Electronics", 1, Decimal("58.00")),
    Order("ORD-1007", "Kunal Patel", "Desk Lamp", "Home Essentials", 1, Decimal("14.00")),
    Order("ORD-1008", "Meera Nair", "Bedsheet", "Home Essentials", 2, Decimal("16.00")),
    Order("ORD-1009", "Meera Nair", "Phone Charger", "Electronics", 1, Decimal("12.00")),
    Order("ORD-1010", "Rohan Joshi", "Smartwatch", "Electronics", 1, Decimal("118.00")),
    Order("ORD-1011", "Rohan Joshi", "Jacket", "Clothing", 1, Decimal("42.00")),
    Order("ORD-1012", "Saanvi Desai", "Sneakers", "Clothing", 1, Decimal("28.00")),
    Order("ORD-1013", "Saanvi Desai", "Tablet", "Electronics", 1, Decimal("84.00")),
    Order("ORD-1014", "Ishaan Kulkarni", "Vacuum Cleaner", "Home Essentials", 1, Decimal("46.00")),
    Order("ORD-1015", "Ishaan Kulkarni", "Wireless Mouse", "Electronics", 1, Decimal("16.00")),
    Order("ORD-1016", "Priya Reddy", "Dress", "Clothing", 1, Decimal("22.00")),
    Order("ORD-1017", "Priya Reddy", "USB Cable", "Electronics", 2, Decimal("8.00")),
]


class TestCustomerOrdersAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orders = TEST_ORDERS

    def test_list_customer_names(self) -> None:
        self.assertEqual(
            list_customer_names(self.orders),
            [
                "Aarav Sharma",
                "Diya Iyer",
                "Ishaan Kulkarni",
                "Kunal Patel",
                "Meera Nair",
                "Priya Reddy",
                "Rohan Joshi",
                "Saanvi Desai",
            ],
        )

    def test_build_customer_products_map(self) -> None:
        customer_products = build_customer_products_map(self.orders)
        self.assertEqual(
            customer_products["Aarav Sharma"],
            ["Bluetooth Speaker", "Kurta", "Storage Basket"],
        )

    def test_build_product_category_map(self) -> None:
        product_map = build_product_category_map(self.orders)
        self.assertEqual(product_map["Tablet"], ELECTRONICS)
        self.assertEqual(product_map["Jacket"], CLOTHING)

    def test_unique_product_categories(self) -> None:
        self.assertEqual(
            unique_product_categories(self.orders),
            {"Electronics", "Clothing", "Home Essentials"},
        )

    def test_customer_total_spend(self) -> None:
        spend = customer_total_spend(self.orders)
        self.assertEqual(spend["Aarav Sharma"], Decimal("138.00"))
        self.assertEqual(spend["Diya Iyer"], Decimal("52.00"))
        self.assertEqual(spend["Meera Nair"], Decimal("44.00"))

    def test_classify_buyer(self) -> None:
        self.assertEqual(classify_buyer(Decimal("150.00")), "High-Value Buyer")
        self.assertEqual(classify_buyer(Decimal("100.00")), "Moderate Buyer")
        self.assertEqual(classify_buyer(Decimal("49.99")), "Low-Value Buyer")

    def test_classify_customers(self) -> None:
        spend = customer_total_spend(self.orders)
        classifications = classify_customers(spend)
        self.assertEqual(classifications["Aarav Sharma"], "High-Value Buyer")
        self.assertEqual(classifications["Kunal Patel"], "Moderate Buyer")
        self.assertEqual(classifications["Meera Nair"], "Low-Value Buyer")

    def test_high_value_customers(self) -> None:
        spend = customer_total_spend(self.orders)
        self.assertEqual(
            high_value_customers(spend),
            ["Aarav Sharma", "Rohan Joshi", "Saanvi Desai"],
        )

    def test_revenue_by_category(self) -> None:
        revenue = revenue_by_category(self.orders)
        self.assertEqual(revenue["Electronics"], Decimal("376.00"))
        self.assertEqual(revenue["Clothing"], Decimal("174.00"))
        self.assertEqual(revenue["Home Essentials"], Decimal("128.00"))

    def test_unique_products(self) -> None:
        products = unique_products(self.orders)
        self.assertIn("Smartwatch", products)
        self.assertIn("Vacuum Cleaner", products)
        self.assertEqual(len(products), 17)

    def test_customers_who_bought_electronics(self) -> None:
        self.assertEqual(
            customers_who_bought_electronics(self.orders),
            [
                "Aarav Sharma",
                "Ishaan Kulkarni",
                "Kunal Patel",
                "Meera Nair",
                "Priya Reddy",
                "Rohan Joshi",
                "Saanvi Desai",
            ],
        )

    def test_top_n_customers_by_spend(self) -> None:
        spend = customer_total_spend(self.orders)
        top_customers = top_n_customers_by_spend(spend, limit=3)
        self.assertEqual(
            top_customers,
            [
                ("Rohan Joshi", Decimal("160.00")),
                ("Aarav Sharma", Decimal("138.00")),
                ("Saanvi Desai", Decimal("112.00")),
            ],
        )

    def test_most_frequently_purchased_products(self) -> None:
        self.assertEqual(
            most_frequently_purchased_products(self.orders),
            ["Bedsheet", "Kurta", "USB Cable"],
        )

    def test_customers_with_multiple_categories(self) -> None:
        self.assertEqual(
            customers_with_multiple_categories(self.orders),
            {
                "Aarav Sharma",
                "Diya Iyer",
                "Ishaan Kulkarni",
                "Kunal Patel",
                "Meera Nair",
                "Priya Reddy",
                "Rohan Joshi",
                "Saanvi Desai",
            },
        )

    def test_common_customers_across_categories(self) -> None:
        self.assertEqual(
            common_customers_across_categories(self.orders, ELECTRONICS, CLOTHING),
            {"Aarav Sharma", "Priya Reddy", "Rohan Joshi", "Saanvi Desai"},
        )

    def test_in_memory_store(self) -> None:
        store = InMemoryOrderStore()
        store.extend(self.orders[:2])
        self.assertEqual(len(store), 2)
        self.assertEqual(store.list_all()[0].customer_name, "Aarav Sharma")

    def test_build_report_data(self) -> None:
        report = build_report_data(self.orders)
        self.assertEqual(report.top_customers[0], ("Rohan Joshi", Decimal("160.00")))
        self.assertEqual(
            report.high_value_customers,
            ["Aarav Sharma", "Rohan Joshi", "Saanvi Desai"],
        )
        self.assertIn("Electronics", report.available_categories)

    def test_generate_console_report(self) -> None:
        report = generate_console_report(self.orders)
        self.assertIn("=== ORDERINSIGHT CUSTOMER ORDER ANALYTICS REPORT ===", report)
        self.assertIn("High-Value Customers:", report)
        self.assertIn("- Rohan Joshi: $160.00", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
