[日本語](README.md) | English

# ComfyUI-Prompt-Order

A standalone ComfyUI custom node that classifies the tags in an existing prompt and rearranges them in your chosen order. You can pin tags to the beginning or end and add or override classifications with a user dictionary. It processes strings on the CPU using the Python standard library.

## Installation

Place this folder in `custom_nodes/ComfyUI-Prompt-Order` inside ComfyUI, then restart ComfyUI. Python 3.10 or later is required. No additional libraries or models are needed.

Add `Prompt Order` from the node list. When the ComfyUI interface language is Japanese, the node appears as `プロンプト順序整理` and its labels and tooltips are in Japanese. Other interface languages use English. The node category is `prompt/ordering`, and its registration name is `ComfyUIPromptOrder`.

## Basic usage

Connect the STRING output of the preceding prompt node to `prompt`, then connect `ordered_prompt` to the `text` input of CLIP Text Encode. The `prompt` input accepts connections only. Edit the prompt in the preceding node.

```text
Input: masterpiece, long_hair, smile, 1girl, solo
Output: 1girl, solo, long_hair, smile, masterpiece
```

Load the [example workflow](examples/prompt_order_workflow.json) in ComfyUI. The standard Text (Multiline) node supplies the prompt, and Prompt Order sends the result to CLIP Text Encode. Select a local checkpoint in Load Checkpoint. Connect the node to your generation workflow to generate images.

For workflows saved with the previous direct-input format, move the prompt to a preceding node, add a new Prompt Order node, and connect the STRING output. Transfer the preset, category order, pin settings, dictionary, and enabled setting as well.

## Settings

The table uses the stable input identifiers. Displayed labels follow the ComfyUI interface language.

| Setting | Meaning |
| --- | --- |
| `prompt` | Prompt received from the preceding node's STRING output |
| `preset` | Ordering preset: `Illustrious`, `Animagine XL 4.0`, or `Custom` |
| `category_order` | Comma-separated category order; leave blank to use the preset |
| `pin_front` | Pin tags present in the input to the beginning, in the specified order |
| `pin_back` | Pin tags present in the input to the end, in the specified order |
| `user_dictionary` | JSON that adds or overrides classifications |
| `enabled` | When `false`, return the input exactly, including whitespace and line breaks |

All settings are saved in the workflow as standard widget values. Settings are independent for each node. Changing a setting participates in ComfyUI's normal input cache checks. Restart ComfyUI after editing the bundled data files.

### Category order and presets

When `category_order` is blank, the following orders apply.

```text
Illustrious / Custom
subject, character, copyright, rating, artist_style, appearance, clothing, pose_expression, composition, background_lighting, general, quality, score, temporal

Animagine XL 4.0
subject, character, copyright, artist_style, rating, appearance, clothing, pose_expression, composition, background_lighting, general, quality, score, temporal
```

An explicit `category_order` takes precedence. Omitted categories are appended in the selected preset's order. For example, `quality, subject` places quality tags first and subject tags second, then appends the remaining categories. Duplicate categories, empty entries, and unknown names produce configuration errors. `Custom` uses the Illustrious order to fill omitted categories.

Changing the preset leaves an existing `category_order` unchanged. Clear this field to return to the preset order. The same rules apply after reloading a workflow. Stored preset values and category identifiers remain in English in every interface language; Japanese displays `Custom` as `カスタム`.

| Category | Content |
| --- | --- |
| `subject` | Subject counts, subjects, and solo |
| `character` | Character names specified in the dictionary |
| `copyright` | Work or franchise names specified in the dictionary |
| `artist_style` | Artists and visual styles |
| `rating` | Content ratings |
| `appearance` | Hair, eyes, faces, and body features |
| `clothing` | Clothing and accessories |
| `pose_expression` | Poses, actions, expressions, and gaze |
| `composition` | Framing, viewpoints, and composition |
| `background_lighting` | Backgrounds, locations, and lighting |
| `general` | Unclassified and other tags |
| `quality` | Quality and resolution |
| `score` | Scores |
| `temporal` | Time periods |

The Illustrious order is this node's sorting rule. The official model card referenced here is `Illustrious-xl-early-release-v0`; it does not guarantee this exact order for every category or its suitability for all derivative and merged models.

The Animagine XL 4.0 preset follows the official guide's placement of subject, character, work, and artist tags near the beginning and quality tags near the end. The rating position and finer ordering of general attributes are this node's sorting rules. Artist names and visual styles share one category. These categories organise prompts; they do not reproduce every tag sequence used during training.

Sorting does not guarantee better image quality. The node only rearranges existing tags. It does not add quality, rating, or time-period tags, delete tags, remove duplicates, translate tags, or change weights. Inputs longer than 77 tokens are preserved without truncation.

### Pinning tags to the beginning or end

```text
prompt: long hair, blue eyes, 1girl, long_hair, solo
pin_front: solo, long hair
pin_back: blue eyes
Output: solo, long hair, long_hair, 1girl, blue eyes
```

Tags follow the order of the pin list. If several input tags match the same entry, all are preserved in their original relative order. Entries absent from the input are ignored. Pinning the same tag to both the beginning and end produces a configuration error.

For single tags, matching removes weights and outer brackets, so `long hair` also matches `(long_hair:1.2)`. The output preserves the original spelling. A group containing several tags, such as `(red dress, white gloves:1.2)`, can only be pinned by specifying the whole group with the same spelling. Leading and trailing whitespace around the group is ignored when matching.

### User dictionary

Enter JSON such as the following in `user_dictionary`.

```json
{
  "version": 1,
  "tags": {
    "my_original_character": "character",
    "my_costume_trigger": "clothing",
    "my_style_trigger": "artist_style",
    "long hair": "general"
  }
}
```

The user dictionary takes precedence over the bundled dictionary and subject-count rules. A blank field, `{}`, and `{"version": 1, "tags": {}}` are all valid empty dictionaries. Set `version` to the integer `1`. Invalid JSON, unknown categories, extra fields, duplicate keys, and tag names that collide during matching produce specific configuration errors. For example, defining both `long_hair` and `long hair` causes a collision even if they map to the same category.

Matching normalises letter case, underscores and spaces, repeated whitespace, and supported escaped symbols. Output tags retain their original spelling. Dictionary keys must represent single tags. Groups of several tags, embeddings, and special syntax cannot be dictionary entries.

## Classification coverage

The bundled [tag dictionary](data/tags.json) contains classifications for subjects, appearance, clothing, poses, composition, backgrounds, styles, quality, and related tags. Matching uses exact normalised tags rather than partial matches. Subject-count tags such as `1girl` and `3boys` also match a limited rule consisting of a positive integer followed by `girl`, `boy`, or `other`, with an optional final `s`.

Character, work, and artist names are supplied through the user dictionary. The node does not infer these names from brackets or word forms. Unlisted attributes and compound tags are kept as `general`. Tags within the same category retain their input order. The bundled dictionary is stored in `data/tags.json`, and ordering presets are stored separately in [data/presets.json](data/presets.json).

## Syntax and line breaks

The parser tracks escapes and the depth of round and square brackets, splitting only at top-level commas. It preserves `(long hair:1.2)`, `((long hair))`, `[long hair]`, escaped commas, and escaped brackets. Weighted expressions containing a single tag are matched by the inner tag.

Groups containing several tags, such as `(red dress, white gloves:1.2)`, are kept intact as one `general` unit. `embedding:name` is also preserved as one `general` unit.

For inputs that can be sorted safely, the node trims leading and trailing whitespace from each unit and joins units with `, `. Line breaks do not act as tag separators. Line breaks around units are removed, while those inside tags or groups are preserved. Use commas to separate tags if the input currently separates them only with line breaks.

The following inputs are returned completely unchanged, with a short warning in the standard log. The full prompt is not logged.

- Unescaped control words such as `BREAK`, `AND`, `ADDCOMM`, `ADDBASE`, `ADDCOL`, `ADDROW`, `REGION`, and `MASK`
- Dynamic prompts, wildcards, region syntax, LoRA syntax, and other syntax containing braces, angle brackets, `|`, or `__`
- Scheduling syntax such as `[red:blue:0.5]`
- Unescaped colon syntax other than numeric weights and `embedding:name`
- Mismatched or unclosed brackets, an incomplete trailing escape, or empty units caused by consecutive, leading, or trailing commas

The node handles ordinary tag lists. It does not fully parse every extension's custom syntax. Set `enabled=false` when support for a syntax is uncertain. The safety check and disabled-node passthrough happen before validation of other settings. For safe input, malformed pin syntax produces a configuration error.

This node processes the string it receives. If an upstream node expands dynamic prompts, the expanded string is the input to this node.

## Tests

Run the standard-library tests from the project folder.

```shell
python -m unittest discover -s tests -v
```

The tests cover expected outputs, preset orders, stable sorting, syntax preservation, pinning, dictionary overrides, configuration errors, unchanged passthrough, idempotence, and preservation of unit contents and occurrence counts.

With an existing ComfyUI environment, you can run this optional check using that environment's Python. It loads this source in a separate process through ComfyUI's loader.

```shell
<ComfyUI Python> tests/check_comfyui.py --comfyui-root <ComfyUI folder>
```

For browser verification after installation, add the node and check the STRING connection from the preceding node, the connection to CLIP Text Encode, multiple nodes with different settings, and workflow saving and reloading. Change the ComfyUI interface language to check Japanese and English labels.

## Official references

- [Animagine XL 4.0 official guide and update](https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update): guidance on artist and quality tag placement for 4.0 and 4.0-Opt.
- [Animagine XL 4.0 model card](https://huggingface.co/cagliostrolab/animagine-xl-4.0): guidance on subject, character, work, and quality tags.
- [Illustrious XL early release v0 model card](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0): official information for the model referenced by the Illustrious preset.
- [ComfyUI custom node inputs](https://docs.comfy.org/custom-nodes/backend/more_on_inputs): documentation for standard inputs and widgets.
- [ComfyUI custom node internationalisation](https://docs.comfy.org/custom-nodes/i18n): documentation for translated node labels and tooltips.
