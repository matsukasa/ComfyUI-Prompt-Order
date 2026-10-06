"""Pure-Python checks of the ComfyUI node contract."""

import unittest

from nodes import PromptOrderNode


class PromptOrderNodeTests(unittest.TestCase):
    def test_string_output_and_standard_widget_contract(self):
        self.assertEqual(PromptOrderNode.RETURN_TYPES, ("STRING",))
        self.assertEqual(PromptOrderNode.RETURN_NAMES, ("ordered_prompt",))
        self.assertEqual(PromptOrderNode.FUNCTION, "sort_prompt")
        inputs = PromptOrderNode.INPUT_TYPES()["required"]
        self.assertEqual(set(inputs), {"prompt", "preset", "category_order", "pin_front", "pin_back", "user_dictionary", "enabled"})
        self.assertEqual(inputs["prompt"][0], "STRING")
        self.assertTrue(inputs["prompt"][1].get("forceInput"))
        self.assertNotIn("multiline", inputs["prompt"][1])
        self.assertNotIn("default", inputs["prompt"][1])
        self.assertEqual(list(inputs["preset"][0]), ["Illustrious", "Animagine XL 4.0", "Custom"])
        for name, definition in inputs.items():
            with self.subTest(name=name):
                self.assertTrue(definition[1].get("tooltip"))

    def test_connected_string_processing(self):
        node = PromptOrderNode()
        upstream_string = "long hair, 1girl"
        self.assertEqual(node.sort_prompt(prompt=upstream_string), ("1girl, long hair",))

    def test_multiple_instances_do_not_share_settings(self):
        first, second = PromptOrderNode(), PromptOrderNode()
        self.assertEqual(first.sort_prompt(prompt="long hair, 1girl", pin_front="long hair"), ("long hair, 1girl",))
        self.assertEqual(second.sort_prompt(prompt="long hair, 1girl"), ("1girl, long hair",))
        self.assertEqual(first.sort_prompt(prompt="long hair, 1girl"), ("1girl, long hair",))

    def test_settings_affect_output_on_next_call(self):
        node = PromptOrderNode()
        self.assertEqual(node.sort_prompt(prompt="long hair, 1girl"), ("1girl, long hair",))
        self.assertEqual(node.sort_prompt(prompt="long hair, 1girl", category_order="appearance, subject"), ("long hair, 1girl",))
        self.assertEqual(node.sort_prompt(prompt="long hair, 1girl", pin_front="long hair"), ("long hair, 1girl",))
        self.assertEqual(node.sort_prompt(prompt="long hair, 1girl", user_dictionary='{"version":1,"tags":{"long hair":"subject","1girl":"quality"}}'), ("long hair, 1girl",))

    def test_disabled_node_preserves_exact_input(self):
        prompt = "  long hair,\n1girl \t"
        self.assertEqual(PromptOrderNode().sort_prompt(prompt=prompt, enabled=False), (prompt,))


if __name__ == "__main__":
    unittest.main()
