"""Optional loader smoke check using an existing ComfyUI installation."""

import argparse
import asyncio
import faulthandler
import importlib.metadata
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description="Check Prompt Order with ComfyUI's real loader in a separate CPU process.")
    parser.add_argument("--comfyui-root", required=True, type=Path)
    args = parser.parse_args()
    package_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(args.comfyui_root.resolve()))
    # ComfyUI reads its command-line options on import.
    sys.argv = [sys.argv[0], "--cpu"]
    import comfy.options
    comfy.options.enable_args_parsing()
    print("Loading ComfyUI in an isolated CPU process...", flush=True)
    faulthandler.dump_traceback_later(60)
    import nodes as comfy_nodes
    import comfyui_version
    faulthandler.cancel_dump_traceback_later()

    assert asyncio.run(comfy_nodes.load_custom_node(str(package_root)))
    node_class = comfy_nodes.NODE_CLASS_MAPPINGS["ComfyUIPromptOrder"]
    assert node_class().sort_prompt("masterpiece, long hair, 1girl") == (
        "1girl, long hair, masterpiece",
    )
    assert node_class.RETURN_TYPES == ("STRING",)
    encode_text = comfy_nodes.CLIPTextEncode.INPUT_TYPES()["required"]["text"][0]
    assert encode_text == "STRING"
    print("PASS: actual ComfyUI loader, node execution, CLIP Text Encode STRING contract")
    print("ComfyUI:", comfyui_version.__version__)
    print("Frontend:", importlib.metadata.version("comfyui-frontend-package"))


if __name__ == "__main__":
    main()
