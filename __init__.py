from .nodes import PromptOrderNode

NODE_CLASS_MAPPINGS = {"ComfyUIPromptOrder": PromptOrderNode}
NODE_DISPLAY_NAME_MAPPINGS = {"ComfyUIPromptOrder": "Prompt Order"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
