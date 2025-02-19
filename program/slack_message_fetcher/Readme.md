## これまでの開発内容

*   **Slack API連携の基本機能:**
    *   Slack APIを利用して、指定されたチャンネルのメッセージを取得する機能
    *   特定のキーワード（`<稼働予定>`）を含むメッセージを検出する機能
    *   検出したメッセージのパーマリンクを取得する機能
    *   取得したパーマリンクを別のチャンネルに投稿する機能
    *   元のメッセージに特定のスタンプ（`white_check_mark`）を付与する機能
*   **メッセージ投稿機能の改善:**
    *   メッセージを投稿する際、投稿者の表示名を取得し、メンション形式（`<@Uxxxxxxxxxx>`）で表示する機能
    *   投稿メッセージを本日の予定チャンネルのスレッドにまとめる機能
     *  スレッドの親となる投稿がなければ自動作成し、既にあればそのスレッドにメッセージを追加する機能
      * スレッドの親となる投稿には、`yyyy/mm/dd (曜日)`形式で日付と曜日を追加する機能
*   **エラーハンドリングとログ出力の改善:**
    *   Slack API呼び出し時のエラーを捕捉し、ログに出力する機能
    *   すでにスタンプが付与されている場合の `already_reacted` エラーをスキップする機能
    *  投稿処理時のエラーログ出力改善
    *  APIから`permalink`が取得できない場合の処理を追加
     * メッセージのHTMLエンティティをデコードする処理の追加
    *   ログ出力を必要最低限に抑制
*  **DM除外の対応**
    * DMは処理しないように変更
*   **ローカル実行環境の構築:**
    *   Pythonスクリプトの作成
    *   `.env` ファイルを使った環境変数の管理
    *   必要なライブラリのインストール手順の明記
    *   ローカル環境での実行手順の説明
    *  Slack API設定手順の説明
* **その他**
    * 細かな修正や改善

## 現状のアプリの使い方

1.  **対象チャンネルに「<稼働予定>」を含むメッセージを投稿:**
    *   所属プロジェクトのチャンネルに、稼働予定を記載したメッセージを投稿します。
2.  **スクリプトの実行:**
    *   ローカル環境でスクリプト `slack_message_fetcher.py` を実行します。
3.  **本日の予定チャンネルの確認:**
    *   本日の予定チャンネルに、該当メッセージへのリンクがスレッド形式で投稿されます。
    *  投稿メッセージは下記のような形式になります。
     ```
     <@Uxxxxxxxxxx> さん
     https://testdheadquarters.slack.com/archives/C08A2JMNY8H/p1737517237674189
     ```
4.  **スタンプの確認:**
    *   元のメッセージに `white_check_mark` スタンプが付与されます。

## 今後のTODO

*   **実行環境のクラウド化:**
    *   GitHub Actionsなどを用いて、スクリプトの定期実行を自動化する。
* **コードリファクタリング:**
    *  可読性・保守性を上げるためのリファクタリング
        * 関数分割
        * 型ヒントの追加

*   **柔軟な設定項目の追加:**
    *   実行時間、対象チャンネル、投稿メッセージ形式などを設定ファイルや環境変数から変更できるようにする。
        やりたい
*   **エラーハンドリングの強化:**
    *   エラー発生時の再試行処理やSlackへの通知機能を実装する。
    *    詳細なログ出力レベルを設定可能にする。
*  **確認済スタンプの動的変更:**
    * 確認済みのスタンプを動的に変更できるようにする。
* **APIレート制限の考慮**
  * 必要に応じて、API呼び出しの間隔を調整する処理を追加する。
*   **テストコードの追加:**
    *   ユニットテストや統合テストを追加し、コードの品質を向上させる。
