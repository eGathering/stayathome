#!/usr/bin/python3

"""
天気予報文字列生成モジュール。
与えられた文字列から地名と日付を抜き出し、
天気予報を取得する。
"""

from .publish import request
from .complihend import rounddate
from .complihend import date2idx
from .complihend import search_available_name
from .spokenword import get_excuse
from .spokenword import get_suffix

_NAMELIST = None

def _get_namelist(string):
    global _NAMELIST
    namelist = search_available_name(string)

    # ヒットしない場合も、前回の結果が残っていればこれを使う
    if not namelist:
        namelist = _NAMELIST

    # 前回結果がない場合は、野球を考慮し、ハマスタ
    if namelist is None:
        namelist = {'神奈川'}

    # 前回結果を保存
    _NAMELIST = namelist

    return namelist

def _get_temp(result, side):
    degree = result['temperature'][side]
    line = '不明'
    if degree:
        line = '{}度'.format(degree['celsius'])

    return line

def _create_mainlines(namelist, datelist, suffix):
    for name in namelist:
        resultlist = request(name)
        for date in datelist:
            result = resultlist[date2idx(date)]
            line = '\n'
            line += '{}の{}の天気は{}{}\n'.format(name, date, result['telop'], suffix)
            line += '最低気温は、{}{}\n'.format(_get_temp(result, 'min'), suffix)
            line += '最高気温は、{}{}'.format(_get_temp(result, 'max'), suffix)

            yield line

def forecast(string):
    # 地名取得
    namelist = _get_namelist(string)
    # 日付取得
    datelist = rounddate(string)

    # 語尾取得
    suffix = get_suffix()

    for line in _create_mainlines(namelist, datelist, suffix):
        yield line


if __name__ == '__main__':
    string = '今日明日明後日東京神奈川'
    for line in forecast(string):
        print(line)

