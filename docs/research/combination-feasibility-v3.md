# RecipeWeave v3 組み合わせ成立見込み確認報告

## 結論

v3 は、指定食材・構造・味付け・経路を通常調理で一料理に具体化できそうか、という **Luna モデル判定**では v2 より高かった。主指標は「2評価者とも `pass`」で、v2 は 164/400 = 41.00%（Wilson 95% CI: 36.29–45.88%）、v3 は 398/400 = 99.50%（98.20–99.86%）だった。事前に定めた差の向き（v3 − v2）は +58.50ポイント（Newcombe hybrid score 95% CI: +53.45–63.23）、両側 pooled two-proportion z 検定は p = 3.37×10⁻⁷³（α=.05）だった。

これは統計的にモデル判定の差が明瞭だったことを示す。実際の料理の正しさ、味、食品安全、消費者受容、または人間がレシピを完成できる確率を示さない。判定対象は生成集合の違う母集団であり、同じ Luna 系統のバイアスは除かれない。

| 指標 | v2 baseline | v3 revised |
|---|---:|---:|
| 両者 pass（主指標） | 164/400 = 41.00% (36.29–45.88%) | 398/400 = 99.50% (98.20–99.86%) |
| 少なくとも一者 pass | 254/400 = 63.50% | 399/400 = 99.75% |
| 3分類一致 | 310/400 = 77.50% | 399/400 = 99.75% |
| Judge A pass | 212/400 = 53.00% | 398/400 = 99.50% |
| Judge B pass | 206/400 = 51.50% | 399/400 = 99.75% |
| Cohen κ | 0.551 | 0.666 |

## 設計と再現性

各集合から単純無作為非復元抽出 400 件、各行を独立した Luna コンテキスト 2 個で評価した。開発 pilot 100 件は v2 確認母集団から除外し、確認仮説の検定には使っていない。seed、定義、プロトコルの固定後に評価を行った。

- baseline 確認母集団: 25,171,059,394（全 v2 25,171,059,494 から pilot 100 件を除外）
- revised 確認母集団: 12,069,539
- v3 定義 SHA-256: `495dc6b22638ff029c75913a13aef616c425049eacddc6389a6a26257e56da36`
- プロトコル SHA-256: `641c8cf2917cd5a1a9c1ef5421c268b571cd731286a3e3a3cf5ee085b3d7d465`
- Wilson 95% CI、差は Newcombe hybrid score CI、検定は pooled two-proportion z。400 件は最悪比率 .5 で半幅約 4.9 ポイント。母集団が大きいため有限母集団補正は省略した（比率 CI の説明は [NIST](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)）。

seed から復元した ordinal 集合、定義との記述、ID coverage、4 rating ファイルの verdict coverage は CLI で検証済みである。機械的な evidence と hash は [analysis.json](../../experiments/confirmation/analysis.json) と [evidence.json](../../experiments/confirmation/evidence.json) に保存した。

## 候補空間と生成物

カタログは source 1,005 件、culinary identity 936 件、active primary/support identity 248 件、21 template である。v3 は 12,069,539 件の **仮説候補**を全件列挙し、13 個の CSV gzip shard、合計 53,984,785 bytes として出力した。これは 1,000 万件の候補空間目標を超えるが、数量・工程を持つレシピ生成ではない。重複・近似重複、数量妥当性、味、調理完成性、安全性を検証した 1,000 万レシピは作られていない。

template 別の確認 n は、baseline では「3副材を使う完成品アレンジ」307 件に偏り、1–2 件の template もある。revised では主材と野菜の煮物 104 件、炒め物 88 件、オーブン焼き 87 件などである。少数 template や珍しい食材について、個別の成立保証や精度は主張しない。flavor と route を明示する方針は判定の明瞭さを高めた可能性があるが、v2 と v3 は別集合なので、同じ料理に対する因果効果とは解釈できない。

v3 の designated uncertain ケースは次の二つで、いずれも `チーズ黒こしょう` を含む煮物である。

- `C0380`: さわら・セロリ・いんげんの煮物。両 judge が uncertain。
- `C0762`: がんもどき・まいたけ・水菜の煮物。Judge A は uncertain、Judge B は pass。

## Pilot と限界

開発 pilot は両者 pass 78/100 = 78% だったのに対し、確認 baseline は 164/400 = 41% だった。この大きな差は、pilot が改良・文脈・評価条件に依存した感度を示す。偶然の標本揺らぎだけで説明したり、都合よく隠したりしない。pilot は開発用であり、確認結果から pilot を再解釈しない。

2 judge は n を 800 や 1,600 に倍増しない。共有する Luna のモデルバイアスは除去されず、人間の gold calibration もない。したがって本 CI を外部の料理成立率や physical feasibility の母集団へ外挿できない。exact/near recipe uniqueness、taste、quantity、工程、食品安全の検証も未実施である。

## 次回の事前固定案

holdout 後に現行 policy を変更しない。必要なら新 version と未使用 ordinal、事前に固定した新 seed で、専門的な `cheese-sauce` template を別研究として新規 calibration する。次回 ADR には次を固定する。

1. **停止規則**: 主指標と v3 下限 0.85 の設計目標を採用し、CI が目標を満たすかを固定 n で判定する。ラベルを見て sample を差し替えたり、都合よく早期停止したりしない。
2. **seed と対象**: policy/version、定義 digest、除外集合、未使用 ordinal、seed、rating prompt/context hash を label 前に記録する。
3. **多重性**: primary 以外の比較や複数 template の検定を行うなら、検定数と Holm などの調整を label 前に決める。主指標の一回検定を、結果を見て secondary に置き換えない。
4. **実物検証**: モデル判定とは別に、数量・工程・安全性を含む人間または実調理の gold set を作り、外部妥当性を新たに推定する。
