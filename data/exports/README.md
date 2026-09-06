# 全量出力

`v3/` は改良版の許可条件を満たす **12,069,539件すべて**を実体化したCSV gzipです。
13シャードで合計53,984,785バイト。範囲マニフェストだけで行の出力を代用していません。
一方、旧v2の25,171,059,494通りは粗い比較用の探索空間で、全量実体化はしていません。

`manifest.json` は定義のSHA-256、各ファイルの行数・半開区間・バイト数・SHA-256を記録します。
`dictionary.json` が整数IDを食品・料理構造・味付・経路へ対応させます。CSVの列は
`ordinal,template,main,support1,support2,support3,flavor,route`。
辞書参照は0始まり、副材の空欄は不在を意味します。

```bash
uv run recipeweave count
uv run recipeweave show --ordinal 5182376
uv run recipeweave export --output data/exports/v3 --shard-size 1000000
uv run recipeweave verify-export --output data/exports/v3 --definition data/catalog/v3_reviewed.json
uv run recipeweave verify-export --output data/exports/v3 --definition data/catalog/v3_reviewed.json --full
```

同一出力先へのexportは完了シャードのSHAを照合して再開します。定義変更時は別versionへ出力します。
再開前にmanifestの範囲・順序・重複・ファイル名・辞書と全完了ファイルを検査します。
破損時は既存状態を書き換えずに停止します。completeと記録された出力の欠落も拒否します。
verify-exportは全行の連番・参照・ファイルSHAを検査し、定義指定時には辞書全体と
抽出1,024件＋各シャード境界を照合します。`--full`は定義指定を必須とし、
全行を定義の列挙結果と逐次照合します。全量をメモリへ読み込む処理ではありません。
1つの出力先を複数プロセスで同時更新しないでください。現在のライターは単一プロセス用です。
レシピの分量・工程詳細・食品取扱い・食味を検証したデータではありません。

CSVは1行ずつ列挙した仮説です。料理構造と入力の同値は整理していますが、完成レシピ同士の
意味上の近似重複は後段のレシピ生成・比較で測る必要があります。
