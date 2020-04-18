#!/usr/bin/python3
"""
ランダムで言葉を選ぶためのモジュール
"""

from random import choice

def get_excuse():
    lines = (
            '場所を特定できませんでしたが、',
            'とりあえず、',
            '場所がわからないけど、',
            )

    return choice(lines)

def get_suffix():
    lines = (
            "です。",
            "でごわす。",
            "であります。",
            "だ。",
            "だぜ！",
            "よ...",
            "ザマス",
            "やで。",
            "だってばよ！",
            "でヤンス！",
            "wwwwww",
            )
    return choice(lines)
