#!/usr/bin/python3

"""
bot ちゃんの定型文をjsonファイルに読み書きする

note:
  日本語ファイルを開く時は
   codecs.open() でコーデック指定する
  jsonファイルに書く時は
   json.dump の第二引数に ensure_ascii=False を付けてASCII指定にする
"""

import json
import codecs
import os

# メンション有りで反応するキーワード辞書
reply_Msg = {
    'NoReplyMsg': ['NoReplyMsg', 'Reply'],
}

# メンション無しで反応するキーワード辞書
listen_Msg = {
    'NoListenWord': ['NoListenWord', 'Reply'],
}

#########################################
# json ファイル操作
#########################################

_reply_fileName = '/plugins/jsonDict/reply_Msg.json'
_listen_fileName = '/plugins/jsonDict/listen_Msg.json'
#_reply_fileName = '/jsonDict/reply_Msg.json'
#_listen_fileName = '/jsonDict/listen_Msg.json'

def _write_json(mention, key, msg, type):
    textMsg = {key : [msg, type],}

    if 'reply' in mention:
        path = os.getcwd() + _reply_fileName
    else:
        path = os.getcwd() + _listen_fileName

    # ファイルが存在してサイズが0じゃなければ　read & verify
    if os.path.exists(path) == True:
        if os.path.getsize(path) > 1:
            readFp = codecs.open(path,'r','utf-8')
            json_data = json.load(readFp)
            textMsg.update(json_data)

    writeFp = codecs.open(path,'w','utf-8')
    json.dump(textMsg, writeFp, ensure_ascii=False, indent=4)


def load_json():
    replyFp = codecs.open(os.getcwd() + _reply_fileName,'r','utf-8')
    json_data = json.load(replyFp)
    reply_Msg.update(json_data)

    listenFp = codecs.open(os.getcwd() + _listen_fileName,'r','utf-8')
    json_data = json.load(listenFp)
    listen_Msg.update(json_data)


def add_dict(string):
    _text = string.replace(' ', '').replace('addWord:', '')
    try:
        _word = _text.split(',')
    except ValueError:
        # Error
        return False

    if 4 != len(_word):
        # Error
        return False

    _write_json(_word[0], _word[1], _word[2], _word[3])
    load_json()
    return True

