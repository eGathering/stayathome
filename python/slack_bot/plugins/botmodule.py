#!/usr/bin/python3
"""
bot ちゃんがどんな単語で反応するかを書く

note:
  検出単語を table 化して table に追加すると賢くなる仕組みにしたい。
"""

from slackbot.bot import respond_to    # メンションで反応する
from slackbot.bot import listen_to     # メンション無しで反応する
from slackbot.bot import default_reply # メンションで該当する単語がないと反応
from datetime import datetime          # 日付,時間情報を取得する
from random import choice
from random import randrange
import re

#########################################
# 「respond_to」はメンションする
#  (@でターゲットを指定すること)と応答する
#########################################
@respond_to('こんにちは')
def sample_1(message):
    """
    サンプルの関数
    """
    # メンションをつけて応答
    message.reply('こんにちは!')

@respond_to('今何時')
def get_time_now(message):
    # 現在の日時を取得
    dt_now = datetime.now()
    # メンションつけて応答
    message.reply(str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + 'だZ！')

@respond_to('嫌い')
def hate_func(message):
    # メンションをつけて応答
    message.reply('なんとも思わないです。')

@respond_to('キライ')
def hate_func(message):
    # メンションをつけて応答
    message.reply('奇遇ですね。私もです・・・')
    message.react('party_parrot')

@respond_to('励ます')
def ha_func(message):
    message.reply('ハゲるんですか？頑張って下さい。')

@respond_to('かわいい')
def ka_func(message):
    message.reply('あんたバカァ⁈')

@respond_to('あたかもを使って文章')
def ata_func(message):
    message.reply('冷蔵庫にソーミンチャンプルーがあたかも知れない。')

@respond_to('おやすみ')
def oya_func(message):
    message.reply('おやすみなさい。また明日。一周回ってまた来週。明日が来ない日なんてこないから。全部コロナが悪いから。')
    
#########################################
# 「listen_to」はメンションがなくても応答する
#########################################
@listen_to('仕事終わり')
def sample_2(message):
    message.react('party_parrot')

    msg = 'さん\n' + '今日も1日お疲れ様でした。\n' # 送信メッセージを作る。
    message.reply(msg)                        # メンション

@listen_to('今何時')
def get_time_now(message):
    # 現在の日時を取得
    dt_now = datetime.now()
    # メンションつけずに応答
#    message.send(dt_now.strftime('%H時%M分') + 'だZ！')
    message.send(str(dt_now.hour) + "時" + str(dt_now.minute) + "分" + 'だZ！')

@listen_to('ツンデレ')
def tu_func(message):
    message.reply('ツンツンデレデレパッパラパ〜٩( ᐛ )و')

@listen_to('かしこい')
def kashi_func(message):
    message.send('かわいい!!エリーチカ!!')

@listen_to('かわいい')
def ka_func(message):
    message.reply('はｯ？')

@listen_to('酒')
def liquar_func(message):
    drink = ('水', 'お茶', '青汁', 'カレー', 'サーモン')
    response = '\n飲みましょう！\n\n各自...\n自宅で...\n{}などを...'.format(choice(drink))
    message.reply(response)

@listen_to('.')
def de_func(message):
    """
    ランダムで反応させる
    """
    #デフォルトでは1/25の確率
    denomi = 25

    text = message.body['text']

    #疑問文の場合は1/3の確率
    matched = re.search(r'(\?|？)$', text)
    if matched:
        denomi = 2

    matched = re.search(r'(w|笑|\(笑\)|（笑）)$', text)
    if matched:
        print('foo')
        denomi = 0

    if not denomi or not randrange(denomi):
        message.reply('\nで？')

#########################################
# 「default_reply」はデフォルトの応答
#########################################
@default_reply()
def default_func(message):
    # 改行コードされるとDEFAULT_REPLYに流れる。
    text = message.body['text']     # メッセージを取り出す.
    msg = 'さん\n' + text + '?\n' + 'すみません。言ってる意味がよく分かりません(●´ω｀●)\n' + 'で？\n' 
    message.reply(msg)              # メンション


