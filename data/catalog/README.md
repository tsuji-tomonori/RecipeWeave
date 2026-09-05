# 食品同一性と候補生成の正本

- `source_foods.json`: 前回のGoogle Sheetsから引き継いだ1,005件。食品と購買形態が混在した入力記録。
- `policy.json`: 編集対象。食品同一性、用途別の許可リスト、料理構造、味付、工程の適合規則。
- `normalization.json`: 生成物。936の料理用食品ID、元商品形態への対応、採用/保留理由。
- `v3_reviewed.json`: 生成物。21テンプレート、248の主材・副材IDからなる全量出力の定義。
- `v2_baseline.json`: 前回の粗い計算を再現する比較用定義。新規生成の既定には使用しない。
- `identity_audit.json`: Lunaの監査提案。採否はpolicyのaliasとrejected_audit_mergesが決定する。

めんつゆ2/3/4倍は1つの「めんつゆ」IDへ統合し、濃縮倍率は商品形態の属性に保存します。
倍率表示だけで異なる商品の塩分・糖分・質量を推定しません。調理時の換算には商品版と根拠が必要です。
白あんと小豆あん、粒アーモンドと粉末など、調理機能の違いは自動統合しません。

今回の248件は主材・副材として適合条件を具体化できた集合です。残りは調味料、未整備の料理分野、
入手性や役割をまだ確認していない候補として保持します。食品自体を削除したわけではありません。
commonは設計上の入手性であり、特定店舗の現在在庫を確認した結果ではありません。

```bash
uv run recipeweave compile
uv run recipeweave count
```

元の[カタログ](https://docs.google.com/spreadsheets/d/1eRAdzVescQchfsVMZliYSS9VYwUoDP-tnu5zodrJN5c/edit)と
[DB設計](https://docs.google.com/spreadsheets/d/1SyBFR8o5b8H4PxM8lowEvPBFadqggErimT2d6hjnbTA/edit)は設計経緯です。
本実装の同一性と列挙規則はリポジトリ内のpolicyを正本とし、旧Sheetの候補数と混同しません。
