import json
import tempfile
import unittest
from pathlib import Path
from src.domain import load_domain

class DomainTest(unittest.TestCase):
    def test_fixture_is_complete(self):
        value = load_domain(Path("fixtures/domain.json"))
        self.assertEqual(value["domain"], "airline-meal")
        self.assertGreater(len(value["entities"]), 2)
        self.assertGreater(len(value["rules"]), 2)

    def test_fulfillment_chain_entities_present(self):
        value = load_domain(Path("fixtures/domain.json"))
        chain = ["航段", "舱位", "餐食选择", "配餐截止时间", "供应批次",
                 "食品安全资格", "装机清单", "实际发放", "履约记录"]
        for name in chain:
            self.assertIn(name, value["entities"])

    def test_duplicate_entries_rejected(self):
        value = load_domain(Path("fixtures/domain.json"))
        value["entities"].append(value["entities"][0])
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(value, tmp)
            tmp_path = Path(tmp.name)
        try:
            with self.assertRaises(ValueError):
                load_domain(tmp_path)
        finally:
            tmp_path.unlink()

if __name__ == "__main__":
    unittest.main()
