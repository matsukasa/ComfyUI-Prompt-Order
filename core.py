"""Offline, deterministic prompt ordering; no ComfyUI imports."""

import json
import logging
import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
CATEGORIES = (
    "subject", "character", "copyright", "artist_style", "rating",
    "appearance", "clothing", "pose_expression", "composition",
    "background_lighting", "general", "quality", "score", "temporal",
)
LOGGER = logging.getLogger(__name__)
WEIGHT = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z")
PARAGRAPH_BREAK = re.compile(r"(?:\r?\n[ \t]*){2,}")
CONTROL = re.compile(r"(?<![\w])(?:BREAK|AND|ADDCOMM|ADDBASE|ADDCOL|ADDROW|REGION|MASK)(?![\w])")


class ConfigError(ValueError):
    """An actionable setting error."""


class UnsafeSyntax(ValueError):
    """The supported grammar cannot preserve the input's semantics."""


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError("JSONのキーが重複しています: " + key)
        result[key] = value
    return result


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_json_object)


def load_presets():
    """Return fresh lists so node settings cannot mutate shared presets."""
    return _read_json(DATA_DIR / "presets.json")["presets"]


def split_units(prompt):
    """Split at top-level commas and blank lines; reject ambiguous syntax."""
    if not prompt.strip():
        return []
    stack = []
    units = []
    start = 0
    escaped = False
    visible = []
    paragraph_breaks = {match.start(): match.end() for match in PARAGRAPH_BREAK.finditer(prompt)}
    skip_until = 0
    after_paragraph = False
    after_comma = False
    for index, char in enumerate(prompt):
        if index < skip_until:
            continue
        if escaped:
            visible.append(" ")
            escaped = False
            if char == "\r" and prompt[index + 1:index + 2] == "\n":
                skip_until = index + 2
            continue
        if char == "\\":
            escaped = True
            visible.append(" ")
            continue
        visible.append(char)
        if not stack and index in paragraph_breaks:
            unit = prompt[start:index].strip()
            if unit:
                units.append(unit)
                after_paragraph = True
                after_comma = False
            skip_until = paragraph_breaks[index]
            start = skip_until
            continue
        if char in "{}<>|":
            raise UnsafeSyntax("動的・領域指定などの特殊構文")
        if char in "([":
            stack.append((char, index))
        elif char in ")]":
            if not stack or stack[-1][0] != {")": "(", "]": "["}[char]:
                raise UnsafeSyntax("括弧の対応不正")
            opener, opening = stack.pop()
            if opener == "[":
                inner = prompt[opening + 1:index]
                if re.search(r"(?<!\\)[:|]", inner):
                    raise UnsafeSyntax("スケジュール・交互切替構文")
        elif char == ":":
            if stack:
                if stack[-1][0] != "(" or not WEIGHT.fullmatch(
                    prompt[index + 1:].split(")", 1)[0]
                ):
                    raise UnsafeSyntax("未対応のコロン構文")
            else:
                # Only embedding:name is supported as an unescaped colon atom.
                atom_prefix = prompt[start:index].strip()
                if atom_prefix != "embedding":
                    raise UnsafeSyntax("未対応のコロン構文")
        elif char == "," and not stack:
            unit = prompt[start:index].strip()
            if not unit and not (after_paragraph and units):
                raise UnsafeSyntax("空の区切り単位")
            if unit:
                units.append(unit)
            start = index + 1
            after_paragraph = False
            after_comma = True
    if escaped or stack:
        raise UnsafeSyntax("括弧またはエスケープの終端不正")
    if CONTROL.search("".join(visible)) or "__" in "".join(visible):
        raise UnsafeSyntax("制御語またはワイルドカード構文")
    last = prompt[start:].strip()
    if not last and after_comma:
        raise UnsafeSyntax("空の区切り単位")
    if last:
        units.append(last)
    return units


def _outer_close(text):
    """Find the matching outer closing bracket without interpreting escapes."""
    stack = []
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char in "([":
            stack.append(char)
        elif char in ")]":
            stack.pop()
            if not stack:
                return index
    return -1


def _unescape(text):
    return re.sub(r"\\([\\,()\[\]{}:|<>])", r"\1", text)


def _normalized(text):
    return " ".join(_unescape(text).replace("_", " ").casefold().split())


def _strip_weight(text):
    colon = text.rfind(":")
    if colon < 0 or not WEIGHT.fullmatch(text[colon + 1:]):
        return text
    backslashes = 0
    index = colon - 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return text[:colon].strip() if backslashes % 2 == 0 else text


def _identity(unit):
    """Single atoms match by content; multi-atom groups match exact spelling."""
    original = unit.strip()
    text = original
    while text and text[0] in "([" and _outer_close(text) == len(text) - 1:
        opener = text[0]
        text = text[1:-1].strip()
        if opener == "(":
            text = _strip_weight(text)
    # A comma at any nesting depth makes the entire group opaque.
    if re.search(r"(?<!\\)(?:\\\\)*,", text):
        return ("group", original)
    if text.startswith("embedding:"):
        return ("opaque", original)
    return ("tag", _normalized(text))


def _dictionary(source):
    if not source.strip():
        return {}
    try:
        data = json.loads(source, object_pairs_hook=_json_object)
    except json.JSONDecodeError as error:
        raise ConfigError(f"user_dictionary: JSON形式不正（行{error.lineno}、列{error.colno}）") from error
    if not isinstance(data, dict):
        raise ConfigError("user_dictionary: JSONオブジェクトを指定してください")
    if data == {}:
        return {}
    extra = set(data) - {"version", "tags"}
    if extra:
        raise ConfigError("user_dictionary: 不明な項目（" + ", ".join(sorted(extra)) + "）")
    if set(data) != {"version", "tags"} or type(data["version"]) is not int or data["version"] != 1:
        raise ConfigError("user_dictionary: version=1 と tags が必要です")
    if not isinstance(data["tags"], dict):
        raise ConfigError("user_dictionary: tags はタグ名とカテゴリのオブジェクトです")
    result = {}
    for tag, category in data["tags"].items():
        if not isinstance(category, str) or category not in CATEGORIES:
            raise ConfigError("user_dictionary: 不明なカテゴリ " + repr(category) + "（タグ " + tag + "）")
        try:
            units = split_units(tag)
        except UnsafeSyntax as error:
            raise ConfigError("user_dictionary: 単一の通常タグを指定してください（" + tag + "）") from error
        if len(units) != 1 or _identity(units[0])[0] != "tag":
            raise ConfigError("user_dictionary: 単一の通常タグを指定してください（" + tag + "）")
        key = _identity(units[0])[1]
        if not key:
            raise ConfigError("user_dictionary: 空のタグ名は使えません")
        if key in result:
            raise ConfigError("user_dictionary: 照合上競合するタグ（" + tag + "）")
        result[key] = category
    return result


def resolve_order(preset, category_order):
    presets = load_presets()
    if preset not in presets:
        raise ConfigError("preset: 不明なプリセット")
    base = presets[preset]
    if not category_order.strip():
        return base
    specified = [part.strip() for part in category_order.split(",")]
    for category in specified:
        if category not in CATEGORIES:
            raise ConfigError("category_order: 不明なカテゴリ（" + category + "）")
    if len(set(specified)) != len(specified):
        raise ConfigError("category_order: カテゴリが重複しています")
    return specified + [category for category in base if category not in specified]


def _pins(value, field):
    try:
        units = split_units(value)
    except UnsafeSyntax as error:
        raise ConfigError(field + ": 固定タグの構文を確認してください（" + str(error) + "）") from error
    keys = []
    for unit in units:
        key = _identity(unit)
        if key not in keys:
            keys.append(key)
    return keys


def order_prompt(prompt, preset="Illustrious", category_order="", pin_front="",
                 pin_back="", user_dictionary="", enabled=True):
    if not enabled:
        return prompt
    try:
        units = split_units(prompt)
    except UnsafeSyntax as error:
        LOGGER.warning("Prompt Order: 並べ替えを省略しました（%s）", error)
        return prompt
    order = resolve_order(preset, category_order)
    user_tags = _dictionary(user_dictionary)
    front = _pins(pin_front, "pin_front")
    back = _pins(pin_back, "pin_back")
    if set(front) & set(back):
        raise ConfigError("pin_front / pin_back: 同じタグを先頭と末尾に固定できません")
    builtin = _read_json(DATA_DIR / "tags.json")["categories"]
    tags = {_normalized(tag): category for category, entries in builtin.items() for tag in entries}
    tags.update(user_tags)
    front_buckets = {key: [] for key in front}
    back_buckets = {key: [] for key in back}
    ordinary = {category: [] for category in order}
    for unit in units:
        key = _identity(unit)
        if key in front_buckets:
            front_buckets[key].append(unit)
        elif key in back_buckets:
            back_buckets[key].append(unit)
        else:
            category = tags.get(key[1], "general") if key[0] == "tag" else "general"
            if category == "general" and key[0] == "tag" and re.fullmatch(r"[1-9]\d*(?:girl|boy|other)s?", key[1]):
                # Explicit dictionary entries, including a general override, take priority.
                if key[1] not in tags:
                    category = "subject"
            ordinary[category].append(unit)
    result = [unit for key in front for unit in front_buckets[key]]
    result.extend(unit for category in order for unit in ordinary[category])
    result.extend(unit for key in back for unit in back_buckets[key])
    return ", ".join(result)
