# こばちゃ専用タクシーダッシュボード（鉄道情報追加版）

- `index.html`: 既存カメラに鉄道情報パネルを追加
- `.github/workflows/update-rail-status.yml`: 10分ごとにデータ取得を実行
- `scripts/update_rail_status.py`: Yahoo!路線情報（関東）のページを解析
- `data/rail-status.json`: ダッシュボードが読むデータ

## 導入メモ
この仕組みはYahoo!路線情報の公開ページの表示構造に依存するため、ページ側の変更やアクセス制限で取得に失敗することがあります。取得失敗時は正常運転と表示せずエラーにします。公開ページの自動取得が利用規約等に適合することを確認してから運用してください。GitHub Actionsの初回実行はリポジトリの Actions タブから `Update railway service information` を選んで `Run workflow` でも実行できます。
