"""ComfyUI's standard widget adapter for Prompt Order."""

if __package__:
    from .core import order_prompt
else:
    from core import order_prompt


class PromptOrderNode:
    @classmethod
    def INPUT_TYPES(cls):
        def text(default, tooltip):
            return ("STRING", {"default": default, "multiline": True,
                               "dynamicPrompts": False, "tooltip": tooltip})
        return {"required": {
            "prompt": text("", "整理するタグ列。STRING接続にも対応します。"),
            "preset": (["Illustrious", "Animagine XL 4.0", "Custom"], {
                "default": "Illustrious", "tooltip": "空のcategory_orderに適用する整理順。Customの基準はIllustriousです。"}),
            "category_order": text("", "空欄はプリセット順。カンマ区切りで順を指定すると、省略カテゴリをプリセット順で末尾に補います。"),
            "pin_front": text("", "既存タグを指定順で先頭に固定。カンマ区切りで入力します。"),
            "pin_back": text("", "既存タグを指定順で末尾に固定。先頭との重複指定はエラーです。"),
            "user_dictionary": text("{}", "version=1とtagsのJSON。組み込み分類より優先します。空欄・{}も有効です。"),
            "enabled": ("BOOLEAN", {"default": True, "tooltip": "無効にすると空白・改行を含めて入力をそのまま返します。"}),
        }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ordered_prompt",)
    FUNCTION = "sort_prompt"
    CATEGORY = "prompt/ordering"
    DESCRIPTION = "既存タグを辞書とカテゴリ順で整理します。タグの表記・重み・重複を保持します。"

    def sort_prompt(self, prompt, preset="Illustrious", category_order="",
                    pin_front="", pin_back="", user_dictionary="{}", enabled=True):
        return (order_prompt(prompt, preset, category_order, pin_front,
                             pin_back, user_dictionary, enabled),)
