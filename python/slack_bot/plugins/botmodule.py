#!/usr/bin/python3
"""
bot ちゃんがどんな単語で反応するかを書く

note:
  検出単語に対して定型文で返す場合は replyDictionary.py をに追加する
"""

from slackbot.bot import respond_to     # メンションで反応する
from slackbot.bot import listen_to      # メンション無しで反応する
from slackbot.bot import default_reply  # メンションで該当する単語がないと反応
from datetime import datetime           # 日付,時間情報を取得する
from random import choice
from random import randrange
import re

from plugins.botmessage import botSend             # message.send() の代わりの関数
from plugins.botmessage import botReply            # message.reply() の代わりの関数
from plugins.replyDictionary import getReplyMsg    # 頭脳(辞書)
from plugins.replyDictionary import getListenWord  # 頭脳(辞書)

#########################################
# 「respond_to」はメンションする
#  (@でターゲットを指定すること)と応答する
#########################################


@respond_to('今何時')
def get_time_now(message):
    # 現在の日時を取得
    dt_now = datetime.now()
    # メンションつけて応答
    botReply(message, str(dt_now.hour) + "時" + str(dt_now.minute) + "分だZ！")


@respond_to('.')
def reply_dict_Msg(message):
    # メッセージを取り出す.
    text = message.body['text']
    # 辞書にキーワードがあれば返答する
    msg = ['none', 'none']
    getReplyMsg(text, msg)
    replyMsg = msg[0]
    type     = msg[1]
    if 'NoReplyMsg' != replyMsg:
        if 'Reply' in type:
            botReply(message, replyMsg)
        else:
            botSend(message, replyMsg)
    else:
        default_func(message)

#########################################
# 「listen_to」はメンションがなくても応答する
#########################################


@listen_to('仕事終わり')
def end_job(message):
    message.react('party_parrot')
    botReply(message, '\n今日も1日お疲れ様でした。\n')


@listen_to('今何時')
def get_time_now(message):
    # 現在の日時を取得
    dt_now = datetime.now()
    # メンションつけずに応答
    botSend(message, str(dt_now.hour) + "時" + str(dt_now.minute) + "分だZ！")


@listen_to('酒')
def liquar_func(message):
    drink = ('水', 'お茶', '青汁', 'カレー', 'サーモン')
    response = '\n飲みましょう！\n\n各自...\n自宅で...\n{}などを...'.format(choice(drink))
    botReply(message, response)


@listen_to('.')
def dict_msg(message):
    # メッセージを取り出す.
    text = message.body['text']
    # 辞書にキーワードがあれば返答する
    msg = ['none', 'none']
    getListenWord(text, msg)
    replyMsg = msg[0]
    type     = msg[1]
    if 'NoListenWord' != replyMsg:
        if 'Reply' in type:
            botReply(message, replyMsg)
        else:
            botSend(message, replyMsg)
    else:
        de_func(message)


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

#########################################
# 「default_reply」はデフォルトの応答
#########################################


@default_reply()
def default_func(message):
    # 改行コードされるとDEFAULT_REPLYに流れる。
    text = message.body['text']     # メッセージを取り出す.
    msg = 'さん\n' + text + '?\nすみません。言ってる意味がよく分かりません(●´ω｀●)\nで？\n'
    botReply(message, msg)


