"""Validate localisation against the stable node and workflow contract."""

import json
from pathlib import Path
import unittest

from nodes import PromptOrderNode


ROOT = Path(__file__).resolve().parents[1]


class LocaleTests(unittest.TestCase):
    def test_locales_cover_all_inputs_outputs_and_preset_values(self):
        inputs = PromptOrderNode.INPUT_TYPES()["required"]
        for language in ("en", "ja"):
            with self.subTest(language=language):
                locale = json.loads((ROOT / "locales" / language / "nodeDefs.json").read_text(encoding="utf-8"))
                self.assertEqual(set(locale), {"ComfyUIPromptOrder"})
                text = locale["ComfyUIPromptOrder"]
                self.assertTrue(text["display_name"])
                self.assertTrue(text["description"])
                self.assertEqual(set(text["inputs"]), set(inputs))
                self.assertEqual(set(text["outputs"]), {"0"})
                self.assertEqual(set(text["inputs"]["preset"]["options"]), set(inputs["preset"][0]))
                for slot in [*text["inputs"].values(), *text["outputs"].values()]:
                    self.assertTrue(slot["name"])
                    self.assertTrue(slot["tooltip"])

    def test_backend_is_english_fallback_and_matches_english_locale(self):
        locale = json.loads((ROOT / "locales/en/nodeDefs.json").read_text(encoding="utf-8"))["ComfyUIPromptOrder"]
        self.assertEqual(PromptOrderNode.DESCRIPTION, locale["description"])
        self.assertTrue(PromptOrderNode.DESCRIPTION.isascii())
        for name, definition in PromptOrderNode.INPUT_TYPES()["required"].items():
            with self.subTest(input=name):
                tooltip = definition[1]["tooltip"]
                self.assertTrue(tooltip.isascii())
                self.assertEqual(tooltip, locale["inputs"][name]["tooltip"])


if __name__ == "__main__":
    unittest.main()
