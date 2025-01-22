import os
import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import html
import pytz

# .envファイルから環境変数を読み込むためのライブラリ
load_dotenv()

# 環境変数からSlack Botのトークンを取得
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
# 対象とするチャンネルのプレフィックスのリスト
TARGET_CHANNELS = ["pj", "si", "bibo"]
# 投稿先のチャンネルIDを環境変数から取得
TARGET_CHANNEL_FOR_POST = os.getenv('TARGET_CHANNEL_FOR_POST')
# チェックマークのスタンプ名を定数として定義
CHECK_MARK_STAMP = "white_check_mark"

# Slack Webクライアントの初期化
client = WebClient(token=SLACK_BOT_TOKEN)

def fetch_messages_and_post():
    # スクリプトの開始をログに出力
    print("スクリプト開始")
    # 今日の日付を取得
    today = datetime.date.today()
    # 今日の0時0分0秒のタイムスタンプを取得
    ts_start = datetime.datetime.combine(today, datetime.time.min).timestamp()
    # 今日の23時59分59秒のタイムスタンプを取得
    ts_end = datetime.datetime.combine(today, datetime.time.max).timestamp()

    # JSTタイムゾーンを設定
    jst = pytz.timezone('Asia/Tokyo')
    # 現在時刻をJSTで取得
    now_jst = datetime.datetime.now(jst)
    # 日付をyyyy/mm/dd形式で取得
    date_str = now_jst.strftime('%Y/%m/%d')
    # 曜日を英語の略称で取得
    day_of_week_str = now_jst.strftime('%a')
    # 曜日を日本語の漢字1文字に変換
    day_of_week_jp = {
        'Mon': '月',
        'Tue': '火',
        'Wed': '水',
        'Thu': '木',
        'Fri': '金',
        'Sat': '土',
        'Sun': '日'
    }.get(day_of_week_str, '')  # デフォルトは空文字

    # スレッドの親となる投稿メッセージを作成
    thread_parent_message = f"{date_str}({day_of_week_jp}) の全体報告スレッドです。\n今日も一日よろしくお願いします！"

    # 本日の予定チャンネルのメッセージ履歴を取得し、親となる投稿を探す
    try:
       response = client.conversations_history(
           channel=TARGET_CHANNEL_FOR_POST,
           oldest = ts_start,
           latest = ts_end
       )
       messages = response.data['messages']
       thread_ts = None
       for message in messages:
           if message['text'] == thread_parent_message:
              thread_ts = message['ts']
              break

       # 親となる投稿がない場合は作成
       if not thread_ts:
        response = client.chat_postMessage(
            channel=TARGET_CHANNEL_FOR_POST,
            text=thread_parent_message
        )
        thread_ts = response.data['ts']
        print("本日のスレッド親投稿を作成しました")

    except SlackApiError as e:
       print(f"Error fetching history or posting thread parent message: {e} 投稿先のチャンネル:{TARGET_CHANNEL_FOR_POST}")
       return


    # Slackのチャンネルリストを取得（パブリックチャンネルとプライベートチャンネル）
    for channel in client.conversations_list(types="public_channel,private_channel").data["channels"]:
        # チャンネル名がTARGET_CHANNELSのいずれかのプレフィックスで始まらない場合はスキップ
        if not any(channel["name"].startswith(prefix) for prefix in TARGET_CHANNELS):
            continue

        try:
            # チャンネルのメッセージ履歴を取得
            response = client.conversations_history(
                channel=channel["id"],
                oldest=ts_start,
                latest=ts_end
            )
            # 取得したメッセージをループ処理
            messages = response.data['messages']
            for message in messages:
                 # メッセージのテキストに含まれるHTMLエンティティをデコード
                normalized_text = html.unescape(message['text'])
                # メッセージに '<稼働予定>' が含まれるかチェック
                if '<稼働予定>' in normalized_text:
                    # メッセージにすでにチェックマークのスタンプが付与されているか確認
                    if "reactions" in message and any(reaction["name"] == CHECK_MARK_STAMP for reaction in message["reactions"]):
                        print(f"メッセージ '{message['text']}' は既に確認済です")
                        continue
                    try:
                        # メッセージにpermalinkが含まれている場合はそのまま利用、含まれていない場合はAPIで取得
                        if 'permalink' in message:
                            permalink = message['permalink']
                        else:
                            permalink_response = client.chat_getPermalink(
                                channel=channel['id'],
                                message_ts=message['ts']
                            )
                            permalink = permalink_response.data['permalink']
                        # ユーザー情報を取得
                        user_id = message['user']
                        user_info_response = client.users_info(user=user_id)
                        user_info = user_info_response.data['user']
                        # メンションUI形式のユーザー名を作成
                        user_mention = f"<@{user_info['id']}>"
                        # 稼働予定を投稿するチャンネルにメッセージをスレッドとして投稿
                        client.chat_postMessage(
                            channel=TARGET_CHANNEL_FOR_POST,
                            text=f"{user_mention} さん\n{permalink}",
                            thread_ts = thread_ts
                        )
                         # 元の投稿にチェックマークのスタンプを付与
                        client.reactions_add(
                            channel=channel["id"],
                            name=CHECK_MARK_STAMP,
                            timestamp=message["ts"]
                        )
                        # 投稿が成功したことをログに出力
                        print(f"メッセージ '{message['text']}' の稼働予定をスレッドに投稿しました")
                    # Slack API のエラーが発生した場合の処理
                    except SlackApiError as e:
                        # 既にリアクションが付与されている場合はエラーとして扱わない
                        if e.response.data['error'] == 'already_reacted':
                            print(f"メッセージ '{message['text']}' には既にスタンプが付与されています")
                        # その他のエラーの場合はログ出力
                        else:
                            print(f"Error posting message or getting permalink: {e} 投稿先のチャンネル:{TARGET_CHANNEL_FOR_POST}")
        # Slack API のエラーが発生した場合の処理
        except SlackApiError as e:
            # エラー内容をログ出力
            print(f"Error fetching history: {e}")
    # スクリプトの完了をログに出力
    print("スクリプト完了")


# 直接実行された場合に `fetch_messages_and_post` 関数を実行
if __name__ == "__main__":
    fetch_messages_and_post()