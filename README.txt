こばちゃ専用ダッシュボード：JR東日本・関東の運行情報 自動取得パッチ

今回の表示デザイン
- JRアプリ風の、見やすい白基調・緑のヘッダー・路線情報行・ステータス表示にしています。
- JR東日本アプリの画面やロゴをそのまま複製したものではなく、雰囲気を参考にした独自表示です。

重要な範囲
- このパッチが対象にするのは、指定されたJR東日本「関東エリア」公式ページです。
- このページには西武線などの私鉄は含まれません。西武線も自動表示したい場合は、別の正式利用可能なデータ元が必要です。
- GitHub Actions は15分ごとにページを取得し、data/rail-status.jsonを更新します。
- ページ構造変更・アクセス制限・取得失敗時には「平常運転」と誤表示しないよう設計しています。
- 運行情報ページを機械的に取得する運用がサイト利用条件に適合するか、継続運用前にJR東日本の利用条件を確認してください。

GitHubに配置するファイル
1. scripts/fetch_rail_status.py
2. .github/workflows/rail-status.yml
3. rail-panel-snippet.html の内容を、index.html の既存 .rail-status-panel の中身と置き換える

注意：rail-panel-snippet.html は、既存HTMLの .rail-status-panel 内に貼るための断片です。index.html全体ではありません。
このスニペットのJSON URLは現在の公開サイトURLを前提にしています：
https://kobacha9658.github.io/kobacha-taxi-dashboard2/data/rail-status.json

配置後の確認
1. GitHubリポジトリで上記ファイルを追加・コミット
2. Actionsタブ > Update JR East rail status > Run workflow を実行
3. 実行成功後、次のURLを開いてJSONが表示されることを確認
   https://kobacha9658.github.io/kobacha-taxi-dashboard2/data/rail-status.json
4. GitHub Pagesで数分後にダッシュボードを再読み込み

GitHub Actionsのpush権限が制限されている場合は、リポジトリ設定のActions permissionsを確認してください。
