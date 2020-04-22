#!/usr/bin/python3
"""
bot ちゃんの命の源

note:
"""


from slackbot.bot import Bot
from plugins.replyDictionary import load_json

# Botを起動する
def main():
    load_json()
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
