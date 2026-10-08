"""Tests for the checked-in Workbench classification import tool."""

import json
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from import_workbench_catalog import classify_tag, import_catalog  # noqa: E402


class WorkbenchImportTests(unittest.TestCase):
    def test_representative_category_mapping(self):
        self.assertEqual(classify_tag("catalog_small:person_count", "", ""), "subject")
        self.assertEqual(classify_tag("catalog_small:hair_color", "", "person_body"), "appearance")
        self.assertEqual(classify_tag("catalog_small:smile", "", "expression_action"), "pose_expression")
        self.assertEqual(classify_tag("catalog_small:dress_skirt", "", "clothing_accessory"), "clothing")
        self.assertEqual(classify_tag("catalog_small:shot_size", "", "composition_view"), "composition")
        self.assertEqual(classify_tag("catalog_small:lighting", "", "style_quality"), "background_lighting")
        self.assertEqual(classify_tag("catalog_small:work_style", "", "style_quality"), "artist_style")
        self.assertEqual(classify_tag("catalog_small:quality_format", "", "style_quality"), "quality")
        self.assertEqual(classify_tag("catalog_small:adult_rating", "", "adult"), "rating")
        self.assertEqual(classify_tag("catalog_small:unknown", "", "unknown"), "general")

    def test_catalog_has_unique_names_and_all_output_categories(self):
        catalog = {
            "major_categories": [{
                "id": "catalog_major:person_body",
                "medium_categories": [{
                    "id": "catalog_medium:person_body:01",
                    "small_categories": [{
                        "id": "catalog_small:person_count",
                        "label_ja": "人数・性別",
                        "tags": [{"name": "1girl"}, {"name": "2girls"}],
                    }],
                }],
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            result, report = import_catalog(catalog_path)
        self.assertEqual(report["records"], report["unique_names"])
        self.assertEqual(report["duplicate_names"], [])
        self.assertEqual(set(result["categories"]), {
            "subject", "character", "copyright", "artist_style", "rating",
            "appearance", "clothing", "pose_expression", "composition",
            "background_lighting", "general", "quality", "score", "temporal",
        })
        names = [name for tags in result["categories"].values() for name in tags]
        self.assertEqual(len(names), len(set(names)))

    def test_generated_json_is_utf8_and_preserves_version(self):
        data = json.loads((ROOT / "data/tags.json").read_text(encoding="utf-8"))
        self.assertEqual(data["version"], 1)
        self.assertIn("1girl", data["categories"]["subject"])
        self.assertIn("long_hair", data["categories"]["appearance"])
        self.assertIn("masterpiece", data["categories"]["quality"])


if __name__ == "__main__":
    unittest.main()
