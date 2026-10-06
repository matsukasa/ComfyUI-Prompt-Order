"""Package registration and shipped data checks."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest

from core import CATEGORIES, ConfigError, _normalized, order_prompt
from nodes import PromptOrderNode


ROOT = Path(__file__).resolve().parents[1]


class ArtifactTests(unittest.TestCase):
    def test_package_import_and_registration(self):
        name = "prompt_order_package_check"
        spec = importlib.util.spec_from_file_location(
            name, ROOT / "__init__.py", submodule_search_locations=[str(ROOT)]
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
            node = module.NODE_CLASS_MAPPINGS["ComfyUIPromptOrder"]()
            self.assertEqual(node.sort_prompt("masterpiece, 1girl"), ("1girl, masterpiece",))
        finally:
            for key in list(sys.modules):
                if key == name or key.startswith(name + "."):
                    del sys.modules[key]

    def test_dictionary_has_no_normalized_collisions(self):
        data = json.loads((ROOT / "data/tags.json").read_text(encoding="utf-8"))
        self.assertEqual(set(data["categories"]), set(CATEGORIES))
        seen = set()
        for category, tags in data["categories"].items():
            for tag in tags:
                key = _normalized(tag)
                self.assertNotIn(key, seen)
                seen.add(key)
                self.assertEqual(order_prompt("unknown, " + tag, category_order=category), tag + ", unknown")

    def test_literal_numeric_colon_is_not_a_weight(self):
        prompt = r"(foo\:1.2), 1girl"
        self.assertEqual(order_prompt(prompt, pin_front=r"foo\:1.2"), prompt)
        dictionary = json.dumps({"version": 1, "tags": {r"foo\:1.2": "character"}})
        self.assertEqual(order_prompt(prompt, user_dictionary=dictionary), r"1girl, (foo\:1.2)")
        with self.assertRaisesRegex(ConfigError, "pin_front / pin_back"):
            order_prompt(prompt, pin_front=r"foo\:1.2", pin_back=r"(foo\:1.2)")

    def test_count_rule_and_explicit_general_override(self):
        self.assertEqual(order_prompt("unknown, 3boys, 12girls, magicalgirl"),
                         "3boys, 12girls, unknown, magicalgirl")
        dictionary = json.dumps({"version": 1, "tags": {"3boys": "general"}})
        self.assertEqual(order_prompt("unknown, 3boys", user_dictionary=dictionary), "unknown, 3boys")


if __name__ == "__main__":
    unittest.main()
