# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import time
import json
import requests

# プライマリアカウントキー see: https://datamarket.azure.com/account
MS_TRANSLATOR_PRIMARY_KEY = os.getenv('MS_TRANSLATOR_PRIMARY_KEY')
# クライアントID see: https://datamarket.azure.com/developer/applications/
MS_TRANSLATOR_CLIENT_ID = os.getenv('MS_TRANSLATOR_CLIENT_ID')
# クライアントID see: 顧客の秘密
MS_TRANSLATOR_CLIENT_SECRET = os.getenv('MS_TRANSLATOR_CLIENT_SECRET')
MS_TRANSLATOR_ACCESSTOKEN_URL = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
MS_TRANSLATOR_SCOPE = 'http://api.microsofttranslator.com'
MS_TRANSLATOR_URL = 'http://api.microsofttranslator.com/V2/Http.svc/Translate'
MS_TRANSLATOR_GRANT_TYPE = 'client_credentials'

class TranslatorError(Exception):
    def __init__(self, message):
        self.message = message

class Translation:
    def __init__(self):
        self.cache = {}

    def getAccessTokenMessage(self):
        'POSTしてアクセストークンを取得する'
        response = requests.post(MS_TRANSLATOR_ACCESSTOKEN_URL, data={
            'client_id': MS_TRANSLATOR_CLIENT_ID,
            'client_secret': MS_TRANSLATOR_CLIENT_SECRET,
            'scope': MS_TRANSLATOR_SCOPE,
            'grant_type': MS_TRANSLATOR_GRANT_TYPE
        })
        if response.status_code == 200:
            self.updateTime = time.time()
            return json.loads(response.text)
        else:
            raise TranslatorError('access token acquisition failure')

    def getAccessToken(self, renew = false)
        'キャッシュから、もしくはPOSTしてアクセストークンを取得する'
        renewJson = true

        if self.updateTime and self.expiresIn:
            delta = time.time() - self.updateTime
            if delta <= self.expiresIn.to_i - 10:
                renewJson = false

        if renew:
            renewJson = true

        # puts "info: renew access token" if renewJson
        if renewJson:
            self.jsonResult = getAccessTokenMessage
        self.accessToken = self.jsonResult["access_token"]
        self.expiresIn = self.jsonResult["expires_in"]

        return self.accessToken

    def existsTransCache(self, word):
        return word in self.cache

    def setTransCache(self, word, resultWord):
        self.cache[word] = resultWord

    def getTransCache(self, word):
        self.cache[word]

    def trans(self, word, from='ja', to='en')
        'wordを翻訳する'
        if existsTransCache(word):
            return getTransCache(word)
        access_token = getAccessToken

        response = requests.get(MS_TRANSLATOR_URL, params={
            'text': word,
            'from': from,
            'to': to
        }, headers={
            'Authorization': 'Bearer {}'.format(access_token)
        })

        if response.status_code == 200:
            document = REXML::Document.new(response.body)
            result = document.root.text
            setTransCache(word, result)
        result

if __name__ == '__main__':
    import fileinput

    trans = Translation()
    puts "input English word ('!' to quit)"
    for line in fileinput.input():
        print("(word or '!'): ")
        if line == "!":
            break
        print(" => " + trans.trans(line))
