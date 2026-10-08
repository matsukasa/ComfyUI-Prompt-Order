# Prompt Workbench分類取り込みレポート

- 取り込み元: Prompt Workbench `data/tag_catalog.json`
- 取り込み対象: 各小分類のcanonicalな`tags[].name`
- 取り込みレコード数: 3231
- ユニークタグ数: 3231
- 重複タグ数: 0
- 未対応小分類のgeneral fallback件数: 0
- Prompt-Order用に表記を安全化したタグ数: 8

## Prompt-Orderカテゴリ別件数

| カテゴリ | 件数 |
| --- | ---: |
| `subject` | 98 |
| `character` | 0 |
| `copyright` | 0 |
| `artist_style` | 73 |
| `rating` | 7 |
| `appearance` | 508 |
| `clothing` | 879 |
| `pose_expression` | 552 |
| `composition` | 90 |
| `background_lighting` | 632 |
| `general` | 323 |
| `quality` | 69 |
| `score` | 0 |
| `temporal` | 0 |

## Workbench小分類からの対応表

| 小分類ID | 表示名 | 対応先 | タグ数 |
| --- | --- | --- | ---: |
| `catalog_small:person_count` | 人数・性別 | `subject` | 31 |
| `catalog_small:person_age` | 年齢 | `subject` | 14 |
| `catalog_small:person_role` | 職業・役柄 | `subject` | 23 |
| `catalog_small:person_species` | 種族 | `subject` | 4 |
| `catalog_small:review_64d7202e926c` | 人物像・性格 | `appearance` | 13 |
| `catalog_small:hair_style` | 髪型 | `appearance` | 30 |
| `catalog_small:hair_color` | 髪色 | `appearance` | 25 |
| `catalog_small:hair_texture` | 髪質 | `appearance` | 9 |
| `catalog_small:face_shape` | 顔の形 | `appearance` | 10 |
| `catalog_small:face_makeup` | メイク・顔の特徴 | `appearance` | 19 |
| `catalog_small:eyes` | 目 | `appearance` | 34 |
| `catalog_small:pupils` | 瞳・瞳孔 | `appearance` | 30 |
| `catalog_small:ears` | 耳 | `appearance` | 27 |
| `catalog_small:mouth` | 口 | `appearance` | 14 |
| `catalog_small:teeth_tongue` | 歯・舌・口内 | `appearance` | 16 |
| `catalog_small:nose_brows` | 鼻・眉 | `appearance` | 12 |
| `catalog_small:head_horns` | 頭部・角 | `appearance` | 9 |
| `catalog_small:body_build` | 体型・身長 | `appearance` | 18 |
| `catalog_small:skin` | 肌の色・質感 | `appearance` | 30 |
| `catalog_small:skin_marks` | 傷・ほくろ | `appearance` | 11 |
| `catalog_small:chest_body` | 胸・上半身 | `appearance` | 37 |
| `catalog_small:waist_belly` | 腰・お腹 | `appearance` | 12 |
| `catalog_small:neck_shoulders` | 首・肩・鎖骨・脇 | `appearance` | 8 |
| `catalog_small:arms_hands` | 腕・手 | `appearance` | 3 |
| `catalog_small:legs_feet` | 脚・足 | `appearance` | 24 |
| `catalog_small:nails` | 爪・ネイル | `appearance` | 11 |
| `catalog_small:wings_tail` | 翼・尻尾 | `appearance` | 25 |
| `catalog_small:review_475571cc7c54` | タトゥー | `appearance` | 4 |
| `catalog_small:review_6606422cecba` | 身体全体・関節 | `appearance` | 3 |
| `catalog_small:smile` | 笑顔 | `pose_expression` | 16 |
| `catalog_small:sad_tears` | 悲しみ・涙 | `pose_expression` | 16 |
| `catalog_small:anger_tension` | 怒り・緊張 | `pose_expression` | 14 |
| `catalog_small:dislike` | 嫌悪・軽蔑 | `pose_expression` | 8 |
| `catalog_small:blush_reaction` | 赤面・反応 | `pose_expression` | 19 |
| `catalog_small:other_expression` | その他の表情 | `pose_expression` | 17 |
| `catalog_small:gaze` | 視線・目の動き | `pose_expression` | 47 |
| `catalog_small:basic_pose` | 基本姿勢 | `pose_expression` | 22 |
| `catalog_small:standing_sitting` | 立ち・座り・寝姿勢 | `pose_expression` | 25 |
| `catalog_small:arm_pose` | 腕・手のポーズ | `pose_expression` | 35 |
| `catalog_small:leg_pose` | 脚のポーズ | `pose_expression` | 18 |
| `catalog_small:face_mouth_action` | 顔・口の動作 | `pose_expression` | 30 |
| `catalog_small:holding` | 物を持つ | `pose_expression` | 31 |
| `catalog_small:grab_touch` | つかむ・触れる | `pose_expression` | 42 |
| `catalog_small:move_sport` | 移動・運動 | `pose_expression` | 20 |
| `catalog_small:daily_action` | 日常動作 | `pose_expression` | 27 |
| `catalog_small:combat_action` | 戦闘・道具操作 | `pose_expression` | 15 |
| `catalog_small:performance_action` | 演技・遊び | `pose_expression` | 9 |
| `catalog_small:review_ee3575f30333` | 拘束状態 | `pose_expression` | 6 |
| `catalog_small:person_contact` | 接触・抱擁 | `pose_expression` | 38 |
| `catalog_small:person_interaction` | 対人動作 | `pose_expression` | 21 |
| `catalog_small:outfit_general` | 衣装 | `clothing` | 27 |
| `catalog_small:costume_style` | 制服・民族衣装 | `clothing` | 36 |
| `catalog_small:casual_roomwear` | 普段着・部屋着 | `clothing` | 12 |
| `catalog_small:sportswear` | スポーツ衣装 | `clothing` | 12 |
| `catalog_small:tops` | トップス・シャツ | `clothing` | 30 |
| `catalog_small:coat_jacket` | コート・ジャケット | `clothing` | 28 |
| `catalog_small:dress_skirt` | ドレス・スカート | `clothing` | 31 |
| `catalog_small:bottoms` | パンツ・ショートパンツ | `clothing` | 28 |
| `catalog_small:apron_waist` | エプロン・腰回り | `clothing` | 19 |
| `catalog_small:armor` | 鎧・防具 | `clothing` | 23 |
| `catalog_small:clothes_state` | 衣服の状態・着脱 | `clothing` | 82 |
| `catalog_small:review_a5737bf00ac1` | 袖・衣服の形状 | `clothing` | 38 |
| `catalog_small:swimwear` | 水着 | `clothing` | 29 |
| `catalog_small:underwear` | 下着 | `clothing` | 18 |
| `catalog_small:legwear` | 靴下・レッグウェア | `clothing` | 33 |
| `catalog_small:legwear_state` | レッグウェア状態 | `clothing` | 8 |
| `catalog_small:shoes` | 靴・裸足 | `clothing` | 27 |
| `catalog_small:boots` | ブーツ | `clothing` | 21 |
| `catalog_small:soles` | 靴底 | `clothing` | 3 |
| `catalog_small:head_accessory` | 頭部アクセサリー | `clothing` | 59 |
| `catalog_small:hair_accessory` | 髪飾り | `clothing` | 29 |
| `catalog_small:glasses_mask` | メガネ・マスク | `clothing` | 49 |
| `catalog_small:neck_accessory` | 襟・首元 | `clothing` | 47 |
| `catalog_small:gloves` | 手袋 | `clothing` | 30 |
| `catalog_small:arm_wrist_accessory` | 手首・腕の装飾 | `clothing` | 8 |
| `catalog_small:leg_arm_accessory` | 脚・腕の装飾 | `clothing` | 15 |
| `catalog_small:jewelry_small` | 指輪・宝飾 | `clothing` | 13 |
| `catalog_small:earrings` | イヤリング・耳飾り | `clothing` | 16 |
| `catalog_small:review_8fe207a543d8` | 包帯・絆創膏 | `clothing` | 8 |
| `catalog_small:material_pattern` | 素材・柄 | `clothing` | 41 |
| `catalog_small:clothing_decoration` | 衣服の装飾 | `clothing` | 23 |
| `catalog_small:review_61fff4a527f2` | 紋章・シンボル | `clothing` | 7 |
| `catalog_small:city_street` | 街・都市 | `background_lighting` | 39 |
| `catalog_small:buildings` | 建物 | `background_lighting` | 27 |
| `catalog_small:facilities` | 施設 | `background_lighting` | 50 |
| `catalog_small:indoor_place` | 屋内 | `background_lighting` | 47 |
| `catalog_small:bathroom` | 浴室・水回り | `background_lighting` | 7 |
| `catalog_small:floor_paving` | 床・舗装 | `background_lighting` | 5 |
| `catalog_small:review_572afad19d98` | 建築部材・街の設備 | `background_lighting` | 26 |
| `catalog_small:nature_landscape` | 自然風景・地形 | `background_lighting` | 50 |
| `catalog_small:sky_space` | 空・月・星 | `background_lighting` | 27 |
| `catalog_small:clouds` | 雲 | `background_lighting` | 33 |
| `catalog_small:water_surface` | 水・水面 | `background_lighting` | 8 |
| `catalog_small:plants_flowers` | 植物・花 | `background_lighting` | 34 |
| `catalog_small:review_d8f7cd5c1e3c` | 火・煙・粒子 | `background_lighting` | 24 |
| `catalog_small:season` | 季節 | `background_lighting` | 30 |
| `catalog_small:time_weather` | 時間帯・天候 | `background_lighting` | 30 |
| `catalog_small:event` | 行事 | `background_lighting` | 15 |
| `catalog_small:background_effect` | 背景・画面効果 | `background_lighting` | 87 |
| `catalog_small:daily_objects` | 日用品 | `general` | 37 |
| `catalog_small:books_stationery` | 本・学用品 | `general` | 11 |
| `catalog_small:electronics` | 電子機器 | `general` | 17 |
| `catalog_small:tableware_cookware` | 食器・調理器具 | `general` | 17 |
| `catalog_small:furniture_bedding` | 家具・寝具 | `general` | 25 |
| `catalog_small:review_b5d7e4adeeb7` | 玩具・遊具 | `general` | 7 |
| `catalog_small:food_drink` | 食べ物・飲み物 | `general` | 30 |
| `catalog_small:music_instruments` | 楽器・音楽 | `general` | 5 |
| `catalog_small:weapons` | 武器・武具 | `general` | 32 |
| `catalog_small:vehicles` | 乗り物 | `general` | 5 |
| `catalog_small:animals` | 動物・生き物 | `subject` | 26 |
| `catalog_small:shot_size` | 撮影範囲・人物の大きさ | `composition` | 11 |
| `catalog_small:close_crop` | 接写・見切れ | `composition` | 19 |
| `catalog_small:camera_angle` | カメラアングル | `composition` | 29 |
| `catalog_small:special_view` | 特殊な視点 | `composition` | 9 |
| `catalog_small:review_553db6c58d66` | 画面配置・枠・挿絵 | `composition` | 22 |
| `catalog_small:quality_format` | 画質・画像形式 | `quality` | 19 |
| `catalog_small:pony_score` | Pony系 | `quality` | 17 |
| `catalog_small:negative_quality` | 画質・文字・透かしの除外 | `quality` | 12 |
| `catalog_small:negative_body` | 人物・身体崩れの除外 | `quality` | 21 |
| `catalog_small:work_style` | 作品形式・作風 | `artist_style` | 26 |
| `catalog_small:art_technique` | 絵画技法 | `artist_style` | 18 |
| `catalog_small:art_movement` | 美術様式 | `artist_style` | 6 |
| `catalog_small:artist_style` | 特定作家風 | `artist_style` | 2 |
| `catalog_small:photo_real` | 写実・写真表現 | `artist_style` | 5 |
| `catalog_small:drawing_tools` | 画材・描画道具 | `artist_style` | 16 |
| `catalog_small:lighting` | 光・照明 | `background_lighting` | 47 |
| `catalog_small:color_tone` | 配色・色調 | `appearance` | 22 |
| `catalog_small:color_names:achromatic` | 色名・無彩色系 | `general` | 12 |
| `catalog_small:color_names:white_ivory` | 色名・白・アイボリー系 | `general` | 17 |
| `catalog_small:color_names:brown_earth` | 色名・茶・アースカラー系 | `general` | 11 |
| `catalog_small:color_names:red_pink` | 色名・赤・ピンク系 | `general` | 20 |
| `catalog_small:color_names:orange_yellow_gold` | 色名・橙・黄・金系 | `general` | 11 |
| `catalog_small:color_names:green` | 色名・緑系 | `general` | 22 |
| `catalog_small:color_names:blue_cyan` | 色名・青・シアン系 | `general` | 26 |
| `catalog_small:color_names:purple_magenta` | 色名・紫・マゼンタ系 | `general` | 18 |
| `catalog_small:visual_effects` | レンズ・動きの効果 | `background_lighting` | 46 |
| `catalog_small:adult_rating` | レーティング | `rating` | 7 |
| `catalog_small:adult_genitals` | 性器・性的部位 | `appearance` | 12 |
| `catalog_small:adult_breasts` | 乳首・性的な胸部 | `appearance` | 13 |
| `catalog_small:adult_crotch` | 股間・下半身 | `appearance` | 5 |
| `catalog_small:adult_nudity` | 裸体・露出 | `appearance` | 16 |
| `catalog_small:adult_fluids` | 体液・痕跡 | `appearance` | 6 |
| `catalog_small:adult_sex_acts` | 性行為 | `pose_expression` | 20 |
| `catalog_small:adult_touch` | 愛撫・性的接触 | `pose_expression` | 22 |
| `catalog_small:adult_self_touch` | 自慰 | `pose_expression` | 5 |
| `catalog_small:adult_fetish` | フェチ・支配 | `pose_expression` | 6 |
| `catalog_small:adult_pose` | 性的ポーズ | `pose_expression` | 15 |
| `catalog_small:adult_expression` | 性的表情・視線 | `pose_expression` | 8 |
| `catalog_small:adult_attire` | 性的衣装・小物 | `clothing` | 6 |
| `catalog_small:adult_clothing_shift` | 透け・衣装ずれ | `clothing` | 23 |
