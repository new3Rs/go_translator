# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import sys
try:
    import html
    html.unescape
except:
    import html2 as html
import requests

def translate(text, lang_from, lang_to='ja', model='NMT_VIA_EN'):
    if lang_from == 'CH':
        lang_from = 'zh'
    if lang_to == 'CH':
        lang_to = 'zh'
    response = requests.post('https://mimiaka-weibo.appspot.com/',
        params={
        "from": lang_from,
        "to": lang_to,
        "model": model,
        "text": text
    })
    return html.unescape(response.text) if response.status_code == 200 else None

if __name__ == '__main__':
    print(translate("彭立尧再度柯洁险胜", 'CH', 'EN', 'NMT'))
