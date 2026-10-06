"""Expected-output tests for the independent prompt ordering engine."""

from collections import Counter
import json
import unittest

from core import ConfigError, UnsafeSyntax, load_presets, order_prompt, split_units


def dictionary(**tags):
    return json.dumps({"version": 1, "tags": tags})


class PromptOrderTests(unittest.TestCase):
    def test_presets_have_all_categories_once(self):
        expected = {
            "subject", "character", "copyright", "artist_style", "rating",
            "appearance", "clothing", "pose_expression", "composition",
            "background_lighting", "general", "quality", "score", "temporal",
        }
        presets = load_presets()
        for preset in ("Illustrious", "Animagine XL 4.0"):
            with self.subTest(preset=preset):
                self.assertEqual(set(presets[preset]), expected)
                self.assertEqual(len(presets[preset]), len(expected))

    def test_stable_sort_and_unknown_tags(self):
        self.assertEqual(
            order_prompt("unknown second, blue eyes, 1girl, long hair, unknown first, blue eyes"),
            "1girl, blue eyes, long hair, blue eyes, unknown second, unknown first",
        )

    def test_model_presets_have_explicit_expected_output(self):
        prompt = "year 2023, high score, masterpiece, unknown, outdoors, from above, smile, red dress, long hair, style trigger, safe, series trigger, character trigger, 1girl"
        user_dictionary = json.dumps({"version": 1, "tags": {
            "year 2023": "temporal", "high score": "score", "style trigger": "artist_style",
            "safe": "rating", "series trigger": "copyright", "character trigger": "character",
        }})
        self.assertEqual(order_prompt(prompt, preset="Illustrious", user_dictionary=user_dictionary),
            "1girl, character trigger, series trigger, safe, style trigger, long hair, red dress, smile, from above, outdoors, unknown, masterpiece, high score, year 2023")
        self.assertEqual(order_prompt(prompt, preset="Animagine XL 4.0", user_dictionary=user_dictionary),
            "1girl, character trigger, series trigger, style trigger, safe, long hair, red dress, smile, from above, outdoors, unknown, masterpiece, high score, year 2023")

    def test_empty_inputs(self):
        for prompt in ("", "   ", "\n\t"):
            with self.subTest(prompt=repr(prompt)):
                self.assertEqual(order_prompt(prompt), "")

    def test_normalization_does_not_change_output_spelling(self):
        self.assertEqual(
            order_prompt("long_hair, 1girl, long hair, LONG HAIR"),
            "1girl, long_hair, long hair, LONG HAIR",
        )

    def test_weights_nested_brackets_and_escapes_are_preserved(self):
        prompt = r"(long hair:1.2), ((blue eyes)), [long hair], tag\,with\,commas, name \(series\), 1girl"
        self.assertEqual(
            order_prompt(prompt),
            r"1girl, (long hair:1.2), ((blue eyes)), [long hair], tag\,with\,commas, name \(series\)",
        )

    def test_groups_are_not_split_or_classified_by_their_first_tag(self):
        prompt = "(red dress, white gloves:1.2), blue eyes, 1girl"
        self.assertEqual(
            split_units(prompt), ["(red dress, white gloves:1.2)", "blue eyes", "1girl"]
        )
        self.assertEqual(order_prompt(prompt), "1girl, blue eyes, (red dress, white gloves:1.2)")

    def test_pins_follow_requested_order_and_keep_all_duplicates(self):
        self.assertEqual(
            order_prompt(
                "long hair, blue eyes, 1girl, long_hair, solo, unknown",
                pin_front="solo, long hair, missing",
                pin_back="blue eyes, unknown",
            ),
            "solo, long hair, long_hair, 1girl, blue eyes, unknown",
        )

    def test_weighted_pin_matches_normalized_inner_tag(self):
        self.assertEqual(
            order_prompt("1girl, (long_hair:1.25), ((long hair)), blue eyes", pin_front="long hair"),
            "(long_hair:1.25), ((long hair)), 1girl, blue eyes",
        )

    def test_group_pin_requires_complete_group_match(self):
        prompt = "1girl, (red dress, white gloves:1.2), blue eyes"
        self.assertEqual(order_prompt(prompt, pin_front="red dress"), "1girl, blue eyes, (red dress, white gloves:1.2)")
        self.assertEqual(
            order_prompt(prompt, pin_front="(red dress, white gloves:1.2)"),
            "(red dress, white gloves:1.2), 1girl, blue eyes",
        )

    def test_user_dictionary_overrides_builtin(self):
        self.assertEqual(
            order_prompt("1girl, long hair", category_order="quality, subject", user_dictionary=dictionary(long_hair="quality")),
            "long hair, 1girl",
        )

    def test_dictionary_exact_matching_and_no_name_guessing(self):
        self.assertEqual(
            order_prompt("magicalgirl, someone (series), 1girl, embedding:example"),
            "1girl, magicalgirl, someone (series), embedding:example",
        )

    def test_escaped_character_parentheses_match_explicit_dictionary(self):
        self.assertEqual(
            order_prompt(r"unknown, hero \(series\), 1girl", user_dictionary=json.dumps({
                "version": 1, "tags": {r"hero \(series\)": "character"}
            })),
            r"1girl, hero \(series\), unknown",
        )

    def test_long_prompts_are_not_truncated_or_augmented(self):
        prompt = ", ".join(["unclassified " + str(index) for index in range(200)] + ["1girl"])
        self.assertEqual(order_prompt(prompt), "1girl, " + ", ".join("unclassified " + str(index) for index in range(200)))

    def test_custom_order_appends_omitted_categories_in_preset_order(self):
        self.assertEqual(
            order_prompt("blue eyes, 1girl, masterpiece, unknown", category_order="general, appearance"),
            "unknown, blue eyes, 1girl, masterpiece",
        )
        self.assertEqual(order_prompt("masterpiece, 1girl", preset="Custom"), order_prompt("masterpiece, 1girl"))

    def test_empty_dictionaries_are_valid(self):
        for user_dictionary in ("", "{}", '{"version":1,"tags":{}}'):
            with self.subTest(user_dictionary=user_dictionary):
                self.assertEqual(order_prompt("long hair, 1girl", user_dictionary=user_dictionary), "1girl, long hair")

    def test_invalid_configuration_has_specific_errors(self):
        cases = [
            ({"user_dictionary": "{"}, r"JSON|json"),
            ({"user_dictionary": '{"version":1,"tags":{"x":"nonexistent"}}'}, r"nonexistent"),
            ({"user_dictionary": '{"version":1,"tags":{"long hair":"appearance","long_hair":"clothing"}}'}, r"long|conflict|duplicate|競合|重複"),
            ({"user_dictionary": '{"version":2,"tags":{}}'}, r"version|バージョン"),
            ({"user_dictionary": '{"version":1,"tags":{},"unknown":true}'}, r"unknown"),
            ({"user_dictionary": '{"version":1,"tags":{"long hair":"appearance","long_hair":"appearance"}}'}, r"long|conflict|duplicate|競合|重複"),
            ({"category_order": "subject, subject"}, r"subject|duplicate|重複"),
            ({"category_order": "nonexistent"}, r"nonexistent"),
            ({"pin_front": "long hair", "pin_back": "long_hair"}, r"long|pin|固定"),
        ]
        for kwargs, message in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ConfigError, message):
                    order_prompt("1girl, long hair", **kwargs)

    def test_unsupported_syntax_returns_original_and_warns_without_prompt(self):
        prompts = [
            "  1girl, BREAK, long hair\n",
            "1girl AND long hair",
            "1girl, [red:blue:0.5]",
            "1girl, [red:0.5]",
            "1girl, {red|blue}",
            "1girl, __costume__",
            "1girl, ADDCOMM, long hair",
            "1girl, ADDROW, long hair",
            "1girl, (long hair",
            "1girl, long hair]",
            "1girl, ([long hair)]",
            "1girl,, long hair",
        ]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                with self.assertLogs(level="WARNING") as logs:
                    self.assertEqual(order_prompt(prompt), prompt)
                self.assertNotIn(prompt, "\n".join(logs.output))

    def test_broken_brackets_raise_from_parser(self):
        with self.assertRaises(UnsafeSyntax):
            split_units("1girl, (long hair")

    def test_disabled_is_exact_passthrough_even_for_invalid_settings(self):
        prompt = " \n1girl , (long hair:1.2),\t 1girl\n"
        self.assertEqual(
            order_prompt(prompt, enabled=False, category_order="invalid", user_dictionary="{"), prompt
        )

    def test_enabled_separator_whitespace_and_internal_newlines(self):
        self.assertEqual(order_prompt(" long hair,\n 1girl, (blue\n eyes:1.2) "), "1girl, long hair, (blue\n eyes:1.2)")

    def test_blank_lines_separate_paragraphs_without_missing_commas(self):
        prompt = "masterpiece, close-up\n\nA quiet garden with white flowers. Soft light falls over the leaves.\n\nwatercolor \\(medium\\)"
        self.assertEqual(order_prompt(prompt),
            "close-up, A quiet garden with white flowers. Soft light falls over the leaves., watercolor \\(medium\\), masterpiece")

    def test_paragraph_separators_preserve_groups_and_line_endings(self):
        prompt = "masterpiece\r\n \t\r\n1girl, (red dress,\n\nwhite gloves:1.2)\n\nblue eyes"
        self.assertEqual(order_prompt(prompt), "1girl, blue eyes, (red dress,\n\nwhite gloves:1.2), masterpiece")
        self.assertEqual(split_units(prompt), ["masterpiece", "1girl", "(red dress,\n\nwhite gloves:1.2)", "blue eyes"])

    def test_paragraph_boundaries_next_to_commas_and_outer_whitespace(self):
        prompt = "\n\nlong hair,\n\n 1girl\n\n"
        self.assertEqual(order_prompt(prompt), "1girl, long hair")
        ordered = order_prompt("masterpiece\n\nunknown\n\n1girl")
        self.assertEqual(ordered, "1girl, unknown, masterpiece")
        self.assertEqual(order_prompt(ordered), ordered)
        self.assertEqual(order_prompt("long hair\n\n, 1girl"), "1girl, long hair")
        for malformed in ("long hair,\n\n", "long hair,\n\n, 1girl"):
            with self.subTest(prompt=malformed), self.assertLogs(level="WARNING"):
                self.assertEqual(order_prompt(malformed), malformed)

    def test_escaped_paragraph_break_is_not_a_separator(self):
        prompt = "unknown\\\n\ncontinued, 1girl"
        self.assertEqual(order_prompt(prompt), "1girl, unknown\\\n\ncontinued")
        prompt = "unknown\\\r\n\r\ncontinued, 1girl"
        self.assertEqual(order_prompt(prompt), "1girl, unknown\\\r\n\r\ncontinued")
        self.assertEqual(split_units("unknown\r\ncontinued, 1girl"), ["unknown\r\ncontinued", "1girl"])

    def test_idempotence_and_unit_multiplicity(self):
        prompt = r"(red dress, white gloves:1.2), long_hair, 1girl, unknown, 1girl, tag\,comma, ((blue eyes))"
        kwargs = {"pin_front": "unknown", "pin_back": "long hair"}
        ordered = order_prompt(prompt, **kwargs)
        self.assertEqual(ordered, r"unknown, 1girl, 1girl, ((blue eyes)), (red dress, white gloves:1.2), tag\,comma, long_hair")
        self.assertEqual(order_prompt(ordered, **kwargs), ordered)
        self.assertEqual(Counter(split_units(prompt)), Counter(split_units(ordered)))


if __name__ == "__main__":
    unittest.main()
