#!/usr/bin/python3
"""
与えられた文字列を解釈するためのモジュール
"""

from .location import Location

def rounddate(string):
    """ 日付を丸めて、リスト化する """
    wordstbl = {
            ('今日', 'きょう'): '今日',
            ('明日', 'あす', 'あした'): '明日',
            ('明後日', 'あさって'): '明後日',
            }

    roundedlist = list()
    for words in wordstbl:
        for word in words:
            if word in string:
                roundedlist.append(wordstbl[words])
    if not roundedlist:
        roundedlist.append('今日')
    return set(roundedlist)

def date2idx(date):
    return {
            '今日': 0,
            '明日': 1,
            '明後日': 2,
            }[date]



def search_available_name(string):
    """
    文字列から、利用可能な名前を見つける
    見つからない場合、空のリストを返す
    """

    target_names = list()
    for name in Location().getAvailableNames():
        if name in string:
            target_names.append(name)
    return target_names

