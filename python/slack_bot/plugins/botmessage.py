#!/usr/bin/python3
"""
チャンネルかスレッドかどうかで応答先を切り替える
"""

"""
message.send() の代わりの関数
  :param messsage: slackbotのmessageオブジェクト
  :param text    : 送信するテキストメッセージ
"""
def botSend(message, text):
    if 'thread_ts' in message.body:
        # スレッド内のメッセージの場合
        message.send(text, thread_ts=message.thread_ts)
    else:
        # 親メッセージの場合
        message.send(text, thread_ts=None)


"""
message.reply() の代わりの関数
  :param messsage: slackbotのmessageオブジェクト
  :param text    : 送信するテキストメッセージ
"""
def botReply(message, text):
    if 'thread_ts' in message.body:
        # スレッド内のメッセージの場合
        message.reply(text, in_thread=True)
    else:
        # 親メッセージの場合
        message.reply(text)

