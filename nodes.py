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
            "prompt": ("STRING", {"forceInput": True,
                                  "tooltip": "Connect the STRING output of the preceding prompt node."}),
            "preset": (["Illustrious", "Animagine XL 4.0", "Custom"], {
                "default": "Illustrious", "tooltip": "Order used when category_order is empty. Custom uses Illustrious as its base."}),
            "category_order": text("", "Leave empty for the preset order. Enter comma-separated categories; omitted categories follow in preset order."),
            "pin_front": text("", "Move existing tags to the front in the specified order. Separate entries with commas."),
            "pin_back": text("", "Move existing tags to the back in the specified order. A tag pinned at both ends is an error."),
            "user_dictionary": text("{}", "JSON with version=1 and tags. Overrides built-in classifications. Empty input and {} are valid."),
            "enabled": ("BOOLEAN", {"default": True, "tooltip": "When disabled, return the input unchanged, including whitespace and line breaks."}),
        }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ordered_prompt",)
    FUNCTION = "sort_prompt"
    CATEGORY = "prompt/ordering"
    DESCRIPTION = "Arrange existing tags using dictionaries and category order. Preserve spelling, weights, and duplicates."

    def sort_prompt(self, prompt, preset="Illustrious", category_order="",
                    pin_front="", pin_back="", user_dictionary="{}", enabled=True):
        return (order_prompt(prompt, preset, category_order, pin_front,
                             pin_back, user_dictionary, enabled),)
