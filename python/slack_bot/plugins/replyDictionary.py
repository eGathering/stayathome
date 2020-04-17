#!/usr/bin/python3

"""
bot ちゃんの定型文
"""
# メンション有りで反応するキーワード辞書
reply_Msg = {
    # 受けたメッセージ: [返すメッセージ, メンション有り反応(Reply) or メンション無し反応(Send)]
    'NoReplyMsg': ['NoReplyMsg', 'Reply'],
    'こんにちは': ['こんにちは!', 'Reply'],
    'お疲れ様です': ['おつかー', 'Reply'],
    '嫌い': ['なんとも思わないです。', 'Reply'],
    'キライ': ['奇遇ですね。私もです・・・', 'Reply'],
    '励ます': ['ハゲるんですか？頑張って下さい。', 'Reply'],
    'かわいい': ['あんたバカァ⁈', 'Reply'],
    'おやすみ': ['おやすみなさい。\nまた明日。\n一周回ってまた来週。\n明日が来ない日なんてこないから。\n全部コロナが悪いから。\n', 'Reply'],
}

# メンション無しで反応するキーワード辞書
listen_Msg = {
    # 受けたメッセージ: [返すメッセージ, メンション有り反応(Reply) or メンション無し反応(Send)]
    'NoListenWord': ['NoListenWord', 'Reply'],
    'ツンデレ': ['ツンツンデレデレパッパラパ〜٩( ᐛ )و', 'Reply'],
    'かわいい': ['私のことですね？知ってますよ。', 'Reply'],
    'botちゃん': ['呼びましたか？', 'Reply'],
    'かしこい': ['かわいい!!エリーチカ!!', 'Send'],
}


"""
メンション有りメッセージに定型文を返す
"""


def getReplyMsg(keyword, msg):
    for key in reply_Msg.keys():
        if key in keyword:
            msg[0] = reply_Msg[key][0]
            msg[1] = reply_Msg[key][1]
            return
    # No Hit
    msg[0] = 'NoReplyMsg'

"""
メンション無しメッセージに反応する定型文を返す
"""


def getListenWord(keyword, msg):
    for key in listen_Msg.keys():
        if key in keyword:
            msg[0] = listen_Msg[key][0]
            msg[1] = listen_Msg[key][1]
            return
    # No Hit
    msg[0] = 'NoListenWord'
