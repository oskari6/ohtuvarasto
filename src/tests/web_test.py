"""Route-level tests for the warehouse web interface."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from web import create_app


class TestWarehouseWeb(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def create(self, name="Tools", capacity="10"):
        return self.client.post(
            "/storages", data={"name": name, "capacity": capacity}
        )

    def test_home_lists_empty_state(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No storages yet", response.data)

    def test_create_storage_and_display_capacity(self):
        response = self.create()

        self.assertEqual(response.status_code, 303)
        page = self.client.get("/")
        self.assertIn(b"Tools", page.data)
        self.assertIn(b"<strong>0.00</strong> / 10.00", page.data)

    def test_stock_can_be_added_and_taken(self):
        self.create()
        self.client.post("/storages/1/stock", data={"quantity": "7", "action": "add"})
        self.client.post("/storages/1/stock", data={"quantity": "2", "action": "take"})

        page = self.client.get("/")
        self.assertIn(b"<strong>5.00</strong> / 10.00", page.data)

    def test_invalid_capacity_is_rejected(self):
        response = self.create(capacity="-1")

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"valid non-negative capacity", response.data)

    def test_unknown_storage_is_not_found(self):
        response = self.client.post(
            "/storages/999/stock", data={"quantity": "1", "action": "add"}
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
