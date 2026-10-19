# こばちゃ専用タクシーダッシュボード（統合版）

## 含まれるファイル
- `index.html` — 八重洲・羽田の既存カメラと鉄道情報パネルを統合
- `.github/workflows/update-rail-status.yml` — 日本時間の朝6時ごろ〜翌2時ごろまで10分間隔で取得。Actionsから手動実行も可能
- `scripts/update_rail_status.py` — Yahoo!路線情報（関東）ページから運行情報を取得
- `data/rail-status.json` — ページ表示用データ。初回は未取得状態

## GitHubへの反映
1. ZIPを展開する。
2. 中身の4項目（`index.html`、`.github`、`scripts`、`data`）をリポジトリのルートにアップロードする。
3. `index.html` は既存のものと置き換える。
4. `.github/workflows/update-rail-status.yml` が `main` ブランチに入ったことを確認する。
5. Actionsタブで `Update railway service information` を選び、`Run workflow` を実行する。
6. 成功したら `data/rail-status.json` が更新され、ダッシュボードに反映される。

## 注意
- GitHub Actionsの定期実行は遅延することがあります。画面の情報を最終確認に使う前に、Yahoo!路線情報のページも確認してください。
- Yahoo!路線情報の公開ページの構造・アクセス制限が変わると取得に失敗することがあります。その場合は「平常運転」と表示せずエラーになります。
- Yahoo!のページを自動取得して利用する前に、利用規約等への適合を確認してください。
- GitHub Pagesのリポジトリにすでにあるファイルを削除せず、上記ファイルだけ追加・置換してください。
