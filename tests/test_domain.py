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
        entities = set(value["entities"])
        for name in ["航段", "舱位", "餐食选择", "配餐截止时间", "供应批次",
                     "食品安全资格", "装机清单", "实际发放", "履约记录", "旅客权益"]:
            self.assertIn(name, entities)

    def test_key_rules_recorded(self):
        value = load_domain(Path("fixtures/domain.json"))
        rules = "".join(value["rules"])
        self.assertIn("确认未装餐后到账", rules)
        self.assertIn("唯一有效的餐食名单", rules)
        self.assertIn("同一食品安全底线", rules)
        self.assertIn("第二份有效结果", rules)

if __name__ == "__main__":
    unittest.main()
