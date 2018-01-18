# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import os
import re
import traceback
import mojimoji
import hanja as H
from kanconvit import ja2zh
import excite as web
# import google_cloud_translate as web
from mongo import setup_mongo

try:
    chr = unichr
except:
    pass

class TranslationError(Exception):
    pass


class GoTranslator:
    def __init__(self, db=None):
        if db is None:
            no_db = True
            client, db = setup_mongo(os.getenv('MIMIAKA_MONGO_URL'))
        else:
            no_db = False
        # "&"はexciteで誤訳する。"'"はmojimojiによる全角"’"以外の文字"′"に変換される。"<"はGoogleで誤訳する
        self.DELIMITER = 'qwrt'
        # Excite翻訳は、韓国語翻訳で全角＆を半角に変換するので両方加味する
        self.DELIMITER_RE = '({}|{})'.format(
            self.DELIMITER,
            mojimoji.han_to_zen(self.DELIMITER)
        )
        dic = db.constants.find_one({'category': 'translation'})
        self.CHINESE_DICTIONARY = dic['chinese']
        self.KOREAN_DICTIONARY = dic['korean']
        self.POST_DICTIONARY = dic['post']
        self.PLAYERS = list(db.players.find())
        if no_db:
            client.close()

    def chinese2symbols(self, text):
        table = {}
        symbol = "A"
        NAME = re.compile(r'.*\(|\).*')
        for player in self.PLAYERS:
            if "name" in player:
                name = NAME.sub("", player["name"])
            else:
                name = player["mamumamuName"]
            ch_name = ja2zh(name)
            if ch_name != "" and ch_name in text:
                text = text.replace(
                    ch_name,
                    self.DELIMITER + symbol + self.DELIMITER
                )
                table[symbol] = name
                symbol = chr(ord(symbol) + 1)

        for zh, ja in self.CHINESE_DICTIONARY.items():
            if zh in text:
                text = text.replace(
                    zh,
                    self.DELIMITER + symbol + self.DELIMITER
                )
                table[symbol] = ja
                symbol = chr(ord(symbol) + 1)
        return (text, table)

    def korean2symbols(self, text):
        table = {}
        symbol = "A"
        for player in filter(
            lambda e: "organization" in e and e["organization"] == "韓国棋院",
            self.PLAYERS
        ):
            if "name" in player:
                match = re.match(r'(.*)\((.+)\)', player["name"])
                hangul = match.group(1)
                hanja = match.group(2)
            else:
                hanja = player["mamumamuName"]
                hangul = H.translate(hanja, mode='substitution')
            if hangul in text:
                text = text.replace(
                    hangul,
                    self.DELIMITER + symbol + self.DELIMITER
                )
                table[symbol] = hanja
                symbol = chr(ord(symbol) + 1)
        for ko, ja in self.KOREAN_DICTIONARY.items():
            if ko in text:
                text = text.replace(
                    ko,
                    self.DELIMITER + symbol + self.DELIMITER
                )
                table[symbol] = ja
                symbol = chr(ord(symbol) + 1)

        return (text, table)

    def symbols2names(self, text, table):
        for symbol, name in table.items():
            text = re.sub('{}({}|{}){}'.format(
                self.DELIMITER_RE,
                symbol,
                mojimoji.han_to_zen(symbol),
                self.DELIMITER_RE
            ), name, text)
        return text

    def translate_chinese(self, text):
        text, table = self.chinese2symbols(text)
        text = web.translate(text, 'CH', 'JA', 'NMT_VIA_EN')
        if text is None:
            raise TranslationError()
        return self.symbols2names(text, table)

    def translate_korean(self, text):
        text, table = self.korean2symbols(text)
        text = web.translate(text, 'KO', 'JA', 'PBMT')
        if text is None:
            raise TranslationError()
        return self.symbols2names(text, table)

    def translate(self, text, wb_lp):
        try:
            if 'CH' in wb_lp:
                text = self.translate_chinese(text)
            elif 'KO' in wb_lp:
                text = self.translate_korean(text)
            else:
                raise NotImplementedError()
            for pre, post in self.POST_DICTIONARY.items():
                text = text.replace(pre, post)
            return text
        except:
            print('translate failed', text.encode('utf-8'))
            traceback.print_exc()
            return '******'


if __name__ == '__main__':
    db_client, db = setup_mongo(os.getenv('MIMIAKA_MONGO_URL'))
    translator = GoTranslator(db)
    print(translator.translate('新奥杯柯洁惊世昏招 彭立尧再度半目险胜', 'CHJA'))
    print(translator.translate("[대주배] 여자바둑 '30대 트로이카' 본선 합류", 'KOJA'))
