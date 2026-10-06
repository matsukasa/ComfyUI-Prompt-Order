# ComfyUI-Prompt-Order

日本語 | [English](README_EN.md)

既存のプロンプトをタグごとに分類し、選択した順番へ並べ替える独立したComfyUIカスタムノードです。先頭・末尾への固定と、ユーザー辞書による分類の追加・上書きに対応します。CPUで文字列だけを処理し、Python標準ライブラリを使用します。

## インストール

このフォルダをComfyUIの`custom_nodes/ComfyUI-Prompt-Order`に配置し、ComfyUIを再起動してください。Python 3.10以上を使用します。追加ライブラリやモデルの導入は不要です。

ノード一覧から`プロンプト順序整理`を追加します。カテゴリは`prompt/ordering`、登録名は`ComfyUIPromptOrder`です。ComfyUIの言語設定が日本語ならノード名・入力名・出力名・説明を日本語で表示し、その他の言語では英語で表示します。英語のノード名は`Prompt Order`です。内部の入力名、プリセット値、カテゴリ名は表示言語によらず共通です。

## 基本的な使い方

前段のプロンプトノードのSTRING出力を`prompt`へ接続し、`ordered_prompt`をCLIP Text Encodeの`text`入力へ接続します。`prompt`は接続専用です。プロンプトは前段ノードで編集してください。

入力ソケットは`prompt`だけです。プリセットやカテゴリ順などの設定は、ノード内の設定欄で編集します。

```text
入力: masterpiece, long_hair, smile, 1girl, solo
出力: 1girl, solo, long_hair, smile, masterpiece
```

以前の直接入力形式で保存したワークフローを使う場合は、プロンプトを前段ノードへ移し、このノードを追加し直してSTRING出力を接続してください。プリセット・カテゴリ順・固定・辞書などの設定も移してください。

## 設定

| 設定 | 意味 |
| --- | --- |
| `prompt` | 前段ノードのSTRING出力から受け取るプロンプト |
| `preset` | `Illustrious`、`Animagine XL 4.0`、`Custom`の整理順 |
| `category_order` | カテゴリ名をカンマ区切りで指定する順番。空欄ならプリセット順 |
| `pin_front` | 入力中に存在するタグを、指定順に先頭へ固定 |
| `pin_back` | 入力中に存在するタグを、指定順に末尾へ固定 |
| `user_dictionary` | 分類を追加・上書きするJSON |
| `enabled` | `false`なら空白と改行を含む入力文字列をそのまま返す |

設定はすべて標準ウィジェットの値としてワークフローに保存されます。ノードごとに設定を受け取り、別のノードへ共有しません。設定値の変更はComfyUIの通常の入力キャッシュ判定に反映されます。組み込みデータファイルを編集した場合はComfyUIを再起動してください。

### カテゴリ順とプリセット

`category_order`が空欄の場合に使用する順番は次のとおりです。

```text
Illustrious / Custom
subject, character, copyright, rating, artist_style, appearance, clothing, pose_expression, composition, background_lighting, general, quality, score, temporal

Animagine XL 4.0
subject, character, copyright, artist_style, rating, appearance, clothing, pose_expression, composition, background_lighting, general, quality, score, temporal
```

`category_order`を入力すると、その順番を優先します。省略したカテゴリは選択中のプリセット順で末尾へ補います。例えば`quality, subject`なら品質、主体の順に置き、その後へ残りのカテゴリを補います。カテゴリの重複、空の項目、不明な名前は設定エラーです。`Custom`の補完基準はIllustriousです。

プリセットを変更しても入力済みの`category_order`は書き換えません。プリセット順へ戻す場合はこの欄を空にしてください。この適用規則は再読込後も同じです。

| カテゴリ | 内容 |
| --- | --- |
| `subject` | 人数・主体・solo |
| `character` | 辞書で指定したキャラクター名 |
| `copyright` | 辞書で指定した作品名 |
| `artist_style` | 作者・画風 |
| `rating` | レーティング |
| `appearance` | 髪・目・顔・体の特徴 |
| `clothing` | 衣装・装飾 |
| `pose_expression` | 姿勢・動作・表情・視線 |
| `composition` | 画角・視点・構図 |
| `background_lighting` | 背景・場所・光 |
| `general` | 未分類・その他 |
| `quality` | 品質・解像度 |
| `score` | スコア |
| `temporal` | 年代 |

Illustriousのカテゴリ順は、このノードの整理ルールです。公式の`Illustrious-xl-early-release-v0`モデルカードを参照していますが、全カテゴリの厳密な順番を公式推奨として扱いません。派生・マージモデルでは、使用するモデルに合わせて順番を調整してください。

Animagine XL 4.0では、公式ガイドにある主体・キャラクター・作品・作者タグの前方配置と、品質タグの後方配置を反映しています。レーティングの位置や一般属性内の細かな順番は、ノードの整理ルールです。作者名と画風は同じカテゴリにまとめています。これらのカテゴリは整理用であり、学習時の全タグ順の再現を目的としません。

順番による画質向上は保証しません。入力済みのタグの配置だけを変更し、品質・レーティング・年代タグの自動追加、削除、重複除去、翻訳、重み変更は行いません。77トークンを超えた入力も削除・切り詰めません。

### 先頭・末尾への固定

```text
prompt: long hair, blue eyes, 1girl, long_hair, solo
pin_front: solo, long hair
pin_back: blue eyes
出力: solo, long hair, long_hair, 1girl, blue eyes
```

固定一覧の順番に配置し、同じ指定に一致する入力が複数ある場合はすべて保持します。その中では入力順を維持します。入力に存在しない指定は無視します。先頭と末尾へ同じタグを指定すると設定エラーになります。

単一タグは重みと外側の括弧を照合時に外すため、`long hair`の指定で`(long_hair:1.2)`も固定できます。出力には元の表記を残します。複数タグのグループは、例えば`(red dress, white gloves:1.2)`全体を同じ表記で指定した場合だけ固定できます。グループの先頭・末尾空白は照合対象から外します。

### ユーザー辞書

`user_dictionary`に次のようなJSONを入力します。

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

ユーザー辞書は組み込み辞書と人数規則より優先します。空欄、`{}`、`{"version": 1, "tags": {}}`はいずれも空の辞書として有効です。`version`は整数の`1`を指定します。JSON形式不正、不明なカテゴリ、余分な項目、重複キー、照合上競合するタグ名は具体的な設定エラーになります。例えば`long_hair`と`long hair`を両方定義すると、同じカテゴリでも競合します。

照合時だけ、大文字・小文字、アンダースコアと空白、連続する空白、対応するエスケープ済み記号を正規化します。出力のタグは元の表記を維持します。辞書のキーには単一タグを指定してください。複数タググループ、embedding、特殊構文は辞書項目にできません。

## 分類できる範囲

`data/tags.json`には主体、容姿、衣装、姿勢、構図、背景、画風、品質などの分類を収録しています。正規化後の完全一致で照合し、部分一致は使いません。`1girl`や`3boys`のような人数タグだけ、正の整数と`girl`、`boy`、`other`および末尾の`s`からなる限定規則で補います。

キャラクター名、作品名、作者名は初期辞書に収録していません。括弧や語形から推測せず、ユーザー辞書で明示します。収録していない属性や複合タグは`general`として保持します。同一カテゴリでは入力順を維持します。組み込み辞書は`data/tags.json`、整理順は`data/presets.json`で別々に管理します。

## 構文と改行の扱い

エスケープと丸括弧・角括弧の深さを確認し、トップレベルのカンマだけで分割します。`(long hair:1.2)`、`((long hair))`、`[long hair]`、エスケープされたカンマや括弧は、その表記を保持します。単一タグの重み付き表現は内部タグで照合します。

`(red dress, white gloves:1.2)`のような複数タググループは分解せず、一単位として`general`に分類します。`embedding:name`も一単位の`general`として保持します。

安全に整理できる入力は、各単位の前後の空白を取り除き、区切りを`, `へ統一します。改行そのものをタグ区切りにはしません。単位の前後にある改行は取り除き、タグやグループ内部の改行はそのまま残します。改行だけでタグを並べた入力は、カンマ区切りへ書き直して使用してください。

次の入力はプロンプト全体を変更せず返し、標準ログに短い警告を出します。ログにプロンプト全文は出しません。

- エスケープされていない`BREAK`、`AND`、`ADDCOMM`、`ADDBASE`、`ADDCOL`、`ADDROW`、`REGION`、`MASK`などの制御語
- 波括弧、山括弧、`|`、`__`を含む動的プロンプト、ワイルドカード、領域・LoRAなどの構文
- `[red:blue:0.5]`などのスケジュール構文
- 数値重みと`embedding:name`以外のエスケープされていないコロン構文
- 対応が不正な括弧、閉じていない括弧、末尾の未完了エスケープ、連続・先頭・末尾カンマによる空の単位

対象は一般的なタグ列です。拡張機能ごとの独自構文を完全に解析するものではありません。対応範囲が不明な構文には`enabled=false`を使用してください。安全性確認と無効設定による全文維持は、他の設定の検証より先に行います。安全な入力に対して固定設定の構文が不正な場合は、設定エラーになります。

このノードは受け取った文字列を処理します。接続元で動的プロンプトを展開した場合は、展開後の文字列が処理対象です。

## テスト

プロジェクトフォルダで次を実行すると、標準ライブラリの自動テストを実行できます。

```shell
python -m unittest discover -s tests -v
```

テストでは期待する出力、プリセット順、安定ソート、構文保持、固定、辞書上書き、設定エラー、全文維持、再処理時の同一結果、単位の内容と出現数の保持を確認します。

既存のComfyUI環境を使う場合は、その環境のPythonから次の任意チェックを実行できます。ComfyUIのローダーでこのソースを読み込む別プロセスを使用します。

```shell
<ComfyUIのPython> tests/check_comfyui.py --comfyui-root <ComfyUIフォルダ>
```

ブラウザでの確認は、インストール後にノードを追加し、前段からのSTRING接続、CLIP Text Encodeとの接続、設定が異なる複数ノード、ワークフロー保存・再読込を順に確認してください。

## 公式資料

- [Animagine XL 4.0公式ガイドと更新情報](https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update)。4.0と4.0-Optの作者タグ・品質タグの配置を確認しています。
- [Animagine XL 4.0モデルカード](https://huggingface.co/cagliostrolab/animagine-xl-4.0)。主体・キャラクター・作品と品質タグの推奨を確認しています。
- [Illustrious XL early release v0モデルカード](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0)。品質タグやベースモデルの使い方を説明しています。
- [ComfyUIカスタムノードの入力](https://docs.comfy.org/custom-nodes/backend/more_on_inputs)。標準入力とウィジェットを使用しています。
- [ComfyUIカスタムノードの翻訳仕様](https://docs.comfy.org/custom-nodes/i18n)。ノードの表示言語に使用しています。
