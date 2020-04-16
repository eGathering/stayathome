# slackbot の設定ファイル
#
# note:
#   API トークンはネットワーク上に上げると無効化されるため環境変数から呼び出す
#   環境変数 SLACK_BOT_API_TOKEN に APIトークンを設定しておくこと

import os

# slack から取得したapiトークン
API_TOKEN = os.environ["SLACK_BOT_API_TOKEN"]

# 知らない言葉を聞いた時の応答
DEFAULT_REPLY = "すみません。言ってる意味がよく分かりません(●´ω｀●)"

# 外部ファイルを読み込む。
PLUGINS = [
    'plugins',
]
