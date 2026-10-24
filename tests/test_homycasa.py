import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tracker import homycasa


class HomycasaTests(unittest.TestCase):
    def product(self, **changes):
        variant = {
            "id": int(homycasa.VARIANT_ID),
            "price": 89900,
            "compare_at_price": 119900,
            "available": True,
        }
        variant.update(changes)
        return {"variants": [{"id": 1, "price": 100}, variant]}

    def test_selects_exact_variant_and_calculates_discount(self):
        result = homycasa.parse_variant(self.product())
        self.assertEqual(result["price_eur"], "899.00")
        self.assertEqual(result["compare_at_price_eur"], "1199.00")
        self.assertEqual(result["discount_percent"], "25.02")
        self.assertEqual(result["available"], "true")

    def test_no_discount_and_unavailable(self):
        for reference in (None, 0, 89900, 79900):
            with self.subTest(reference=reference):
                result = homycasa.parse_variant(
                    self.product(compare_at_price=reference, available=False)
                )
                self.assertEqual(result["discount_percent"], "0.00")
                self.assertEqual(result["available"], "false")

    def test_rejects_missing_variant_and_malformed_data(self):
        for payload in (None, [], {}, {"variants": []}, self.product(id=2)):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                homycasa.parse_variant(payload)
        for changes in (
            {"price": None}, {"price": "89900"}, {"price": True},
            {"price": -1}, {"price": 0}, {"compare_at_price": -1},
            {"compare_at_price": "119900"}, {"available": "true"},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                homycasa.parse_variant(self.product(**changes))

    def test_fetch_uses_json_endpoint_and_timeout(self):
        payload = (
            '{"variants":[{"id":57783062004095,"price":89900,'
            '"compare_at_price":null,"available":true}]}'
        )
        with patch.object(homycasa, "urlopen", return_value=io.StringIO(payload)) as fetch:
            result = homycasa.fetch_observation()
        self.assertEqual(result["price_eur"], "899.00")
        self.assertEqual(fetch.call_args.args[0].full_url, homycasa.PRODUCT_URL + ".js")
        self.assertEqual(fetch.call_args.kwargs["timeout"], 30)

    def test_history_appends_and_reports_price_drop(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data/history.csv"
            first = homycasa.parse_variant(self.product())
            self.assertIsNone(homycasa.record_observation(path, first))
            second = homycasa.parse_variant(self.product(price=79900))
            previous = homycasa.record_observation(path, second)
            self.assertEqual(previous, first)
            self.assertIn("-100.00 EUR", homycasa.describe(second, previous))
            with path.open(newline="", encoding="utf-8") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 2)

    def test_invalid_history_is_not_modified(self):
        first = homycasa.parse_variant(self.product())
        for contents in ("wrong,header\n", ",".join(homycasa.FIELDS) + "\nnow,2,1,,,true\n"):
            with self.subTest(contents=contents), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "history.csv"
                path.write_text(contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    homycasa.record_observation(path, first)
                self.assertEqual(path.read_text(encoding="utf-8"), contents)

    def test_request_failure_does_not_write_history(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.csv"
            with (
                patch("sys.argv", ["homycasa", "--history", str(path)]),
                patch.object(homycasa, "fetch_observation", side_effect=OSError("offline")),
                patch("sys.stderr", new_callable=io.StringIO),
            ):
                self.assertEqual(homycasa.main(), 1)
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
