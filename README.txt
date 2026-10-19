こばちゃ専用タクシーダッシュボード（再作成版）

同梱ファイル
- index.html : 既存の八重洲2カメラ・羽田2カメラを維持し、鉄道運行情報パネルを追加した全体版
- scripts/fetch_rail_status.py : JR東日本・関東エリア公式ページから異常情報を抽出するスクリプト
- .github/workflows/rail-status.yml : GitHub Actionsで15分ごとにJSONを更新する設定

設置手順
1. GitHubリポジトリ kobacha-taxi-dashboard2 の index.html を、この index.html で置き換える。
2. scripts/fetch_rail_status.py と .github/workflows/rail-status.yml を、同じパスで追加する。
3. 変更をコミット・プッシュする。
4. GitHubのActionsで「Update JR East rail status」を開き、Run workflowを実行する。
5. https://kobacha9658.github.io/kobacha-taxi-dashboard2/data/rail-status.json を開き、JSONが生成されたか確認する。

重要な制限
- 自動取得対象はJR東日本の関東エリア公式ページのみ。西武線・東京メトロ・都営地下鉄・他の私鉄・モノレールはこのスクリプトでは対象外です。
- HTML構造変更や取得失敗の際、平常運転と誤表示しないよう、異常情報を抽出できない旨を表示します。
- 実際にサイトへ反映するには、このファイル一式をGitHubリポジトリへ反映する必要があります。こちらからリポジトリ自体は変更していません。
- 継続運用前に、情報元サイトの利用条件を確認してください。
