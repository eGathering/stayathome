#!/usr/bin/python3
"""
bot ちゃんがどんな単語で反応するかを書く

note:
  検出単語に対して定型文で返す場合は replyDictionary.py に追加する
"""

from slackbot.bot import respond_to      # メンションで反応する
from slackbot.bot import listen_to       # メンション無しで反応する
from slackbot.bot import default_reply   # メンションで該当する単語がないと反応
from datetime import datetime            # 日付,時間情報を取得する
from random import choice
from random import randrange
import re

from .botmessage import botSend          # message.send() の代わりの関数
from .botmessage import botReply         # message.reply() の代わりの関数
from .replyDictionary import reply_Msg   # 頭脳(辞書)
from .replyDictionary import listen_Msg  # 頭脳(辞書)
from .replyDictionary import add_dict    # 賢くなーれ
from .wf import weather                  # 天気予報

#########################################
# カスタム定型文の関数
#########################################


def get_time_now(message):
    dt_now = datetime.now()  # 現在の日時を取得
    botReply(message, str(dt_now.hour) + "時" + str(dt_now.minute) + "分だZ！")


def end_job(message):
    message.react('party_parrot')
    botReply(message, '\n今日も1日お疲れ様でした。\n')


def weather_forecast(message):
    text = message.body['text']
    for line in weather.forecast(text):
        botReply(message, line)


def liquar_func(message):
    drink = ('水', 'お茶', '青汁', 'カレー', 'サーモン')
    response = '\n飲みましょう！\n\n各自...\n自宅で...\n{}などを...'.format(choice(drink))
    botReply(message, response)


def add_word(message):
    text = message.body['text']
    if False == add_dict(text):
        botReply(message, "[ERROR] usage\n addWord : mention(reply/listen), key, replyMsg, Reply/Send \n例) addWord : reply, 名前, ボクサッチー,ヨロシクネ,Reply")
    else:
        botReply(message, "[success] レベルアップ!!")


def de_func(message):
    """
    ランダムで反応させる
    """
    # デフォルトでは1/25の確率
    denomi = 25

    text = message.body['text']

    # 疑問文の場合は1/3の確率
    matched = re.search(r'(\?|？)$', text)
    if matched:
        denomi = 3

    # 草は1/5の確率
    matched = re.search(r'(Ｗ|W|ｗ|w|笑|\(笑\)|（笑）)$', text)
    if matched:
        denomi = 5

    rangevalue = denomi - 1 if denomi > 0 else 0
    if not rangevalue or not randrange(rangevalue):
        botReply(message, '\nで？')
        return True
    return False

# 関数テーブル
func_Msg = {
    # 受けたメッセージ: 関数名
    'addWord': add_word,
    '今何時': get_time_now,
    '仕事終わ': end_job,
    '天気': weather_forecast,
    '酒': liquar_func,
}

"""
bot ちゃんのカスタム定型文
"""


def request_Func_Msg(message, keyword):
    for key in func_Msg.keys():
        if key in keyword:
            func_Msg[key](message)
            return True
    # No Hit
    return False

#########################################
# 定型文の関数
#########################################


message_func = {
    'Reply': botReply,
    'Send': botSend,
}

"""
メンション有りメッセージに定型文を返す
"""


def request_Reply_Msg(message, keyword):
    for key in reply_Msg.keys():
        if key in keyword:
            replyMsg = reply_Msg[key][0]
            msgType = reply_Msg[key][1]
            message_func[msgType](message, replyMsg)
            return True
    # No Hit
    return False

"""
メンション無しメッセージに反応する定型文を返す
"""


def request_ListenWord(message, keyword):
    for key in listen_Msg.keys():
        if key in keyword:
            replyMsg = listen_Msg[key][0]
            msgType = listen_Msg[key][1]
            message_func[msgType](message, replyMsg)
            return
    # No Hit
    de_func(message)
    return

#########################################
# 「respond_to」はメンションする
#  (@でターゲットを指定すること)と応答する
#########################################


@respond_to('.')
def reply_dict_Msg(message):
    # メッセージを取り出す.
    text = message.body['text']
    # 辞書にキーワードがあれば返答する
    # 関数化辞書
    if True == request_Func_Msg(message, text):
        return            # 処理終了

    # 定型文辞書
    if False == request_Reply_Msg(message, text):
        default_func(message)

#########################################
# 「listen_to」はメンションがなくても応答する
#########################################


@listen_to('.')
def dict_msg(message):
    # メッセージを取り出す.
    text = message.body['text']
    # 辞書にキーワードがあれば返答する
    # 関数化辞書
    if False == request_Func_Msg(message, text):
        # 定型文辞書
        request_ListenWord(message, text)

#########################################
# 「default_reply」はデフォルトの応答
#########################################


@default_reply()
def default_func(message):
    # 改行されるとDEFAULT_REPLYに流れる。
    text = message.body['text']     # メッセージを取り出す.
    msg = 'さん\n' + text + '?\nすみません。言ってる意味がよく分かりません(●´ω｀●)\nで？\n'
    botReply(message, msg)


