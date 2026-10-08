"""Import Prompt Workbench catalog tags into Prompt-Order categories."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


CATEGORIES = (
    "subject",
    "character",
    "copyright",
    "artist_style",
    "rating",
    "appearance",
    "clothing",
    "pose_expression",
    "composition",
    "background_lighting",
    "general",
    "quality",
    "score",
    "temporal",
)

SMALL_CATEGORY_OVERRIDES = {
    "person_count": "subject",
    "person_age": "subject",
    "person_role": "subject",
    "person_species": "subject",
    "animals": "subject",
    "adult_rating": "rating",
    "quality_format": "quality",
    "pony_score": "quality",
    "negative_quality": "quality",
    "negative_body": "quality",
    "work_style": "artist_style",
    "art_technique": "artist_style",
    "art_movement": "artist_style",
    "artist_style": "artist_style",
    "photo_real": "artist_style",
    "drawing_tools": "artist_style",
    "lighting": "background_lighting",
    "visual_effects": "background_lighting",
    "color_tone": "appearance",
    "adult_genitals": "appearance",
    "adult_breasts": "appearance",
    "adult_crotch": "appearance",
    "adult_nudity": "appearance",
    "adult_fluids": "appearance",
    "adult_sex_acts": "pose_expression",
    "adult_touch": "pose_expression",
    "adult_self_touch": "pose_expression",
    "adult_fetish": "pose_expression",
    "adult_pose": "pose_expression",
    "adult_expression": "pose_expression",
    "adult_attire": "clothing",
    "adult_clothing_shift": "clothing",
}

MAJOR_CATEGORY_DEFAULTS = {
    "person_body": "appearance",
    "expression_action": "pose_expression",
    "clothing_accessory": "clothing",
    "place_nature": "background_lighting",
    "objects_living": "general",
    "composition_view": "composition",
    "style_quality": "general",
    "adult": "general",
}


def _short_id(identifier: str) -> str:
    return identifier.rsplit(":", 1)[-1]


def prompt_order_name(name: str) -> str:
    """Make catalog spellings safe for Prompt-Order's supported tag grammar."""
    if name == "(watercolor_pencil)":
        return "watercolor_pencil"
    if name.startswith("embedding:"):
        return name.replace(":", r"\:", 1)
    if name.startswith(":"):
        return "".join("\\" + character if character in r"\\,()[]{}:|<>" else character for character in name)
    return name


def classify_tag(small_id: str, medium_id: str, major_id: str) -> str:
    """Return the stable Prompt-Order category for a Workbench small category."""
    small_key = _short_id(small_id)
    if small_key in SMALL_CATEGORY_OVERRIDES:
        return SMALL_CATEGORY_OVERRIDES[small_key]
    return MAJOR_CATEGORY_DEFAULTS.get(_short_id(major_id), "general")


def import_catalog(catalog_path: Path) -> tuple[dict, dict]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    categories = {category: [] for category in CATEGORIES}
    seen: set[str] = set()
    records = 0
    duplicate_names = []
    source_categories: Counter[str] = Counter()
    output_categories: Counter[str] = Counter()
    category_rows = []
    fallback_small_categories = []
    transformed_names = []

    for major in catalog["major_categories"]:
        major_id = major["id"]
        for medium in major["medium_categories"]:
            medium_id = medium["id"]
            for small in medium["small_categories"]:
                small_id = small["id"]
                target = classify_tag(small_id, medium_id, major_id)
                category_rows.append(
                    (small_id, small["label_ja"], target, len(small.get("tags", [])))
                )
                if (
                    _short_id(small_id) not in SMALL_CATEGORY_OVERRIDES
                    and _short_id(major_id) not in MAJOR_CATEGORY_DEFAULTS
                ):
                    fallback_small_categories.append(small_id)
                for tag in small.get("tags", []):
                    name = prompt_order_name(tag["name"])
                    if name != tag["name"]:
                        transformed_names.append((tag["name"], name))
                    records += 1
                    source_categories[small_id] += 1
                    if name in seen:
                        duplicate_names.append(name)
                        continue
                    seen.add(name)
                    categories[target].append(name)
                    output_categories[target] += 1

    result = {"version": 1, "categories": categories}
    report = {
        "records": records,
        "unique_names": len(seen),
        "duplicate_names": duplicate_names,
        "source_categories": source_categories,
        "output_categories": output_categories,
        "category_rows": category_rows,
        "fallback_small_categories": fallback_small_categories,
        "transformed_names": transformed_names,
    }
    return result, report


def write_report(report: dict, report_path: Path) -> None:
    lines = [
        "# Prompt Workbench分類取り込みレポート",
        "",
        "- 取り込み元: Prompt Workbench `data/tag_catalog.json`",
        "- 取り込み対象: 各小分類のcanonicalな`tags[].name`",
        f"- 取り込みレコード数: {report['records']}",
        f"- ユニークタグ数: {report['unique_names']}",
        f"- 重複タグ数: {len(report['duplicate_names'])}",
        f"- 未対応小分類のgeneral fallback件数: {len(report['fallback_small_categories'])}",
        f"- Prompt-Order用に表記を安全化したタグ数: {len(report['transformed_names'])}",
        "",
        "## Prompt-Orderカテゴリ別件数",
        "",
        "| カテゴリ | 件数 |",
        "| --- | ---: |",
    ]
    for category in CATEGORIES:
        lines.append(f"| `{category}` | {report['output_categories'][category]} |")
    lines.extend(["", "## Workbench小分類からの対応表", "", "| 小分類ID | 表示名 | 対応先 | タグ数 |", "| --- | --- | --- | ---: |"])
    for small_id, label, target, count in report["category_rows"]:
        lines.append(f"| `{small_id}` | {label} | `{target}` | {count} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a Prompt Workbench catalog.")
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result, report = import_catalog(args.catalog)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(report, args.report)


if __name__ == "__main__":
    main()
