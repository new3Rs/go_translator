# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
try:
    xrange
    xrange = range
except:
    pass
import sys
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from pyquery import PyQuery as pq

def translate(text, fro, to='JA', model=None):
    url = 'https://www.excite.co.jp/world/'
    wb_lp = fro + to
    page_lang = to if fro == 'JA' else fro
    if page_lang == 'CH':
        url += 'chinese/'
    elif page_lang == 'KO':
        url += 'korean/'
    elif page_lang == 'EN':
        url += 'english/'
    elif page_lang == 'FR':
        url += 'french/'
    elif page_lang == 'DE':
        url += 'german/'

    for i in range(5):
        s = requests.Session()
        retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[ 500, 502, 503, 504 ])
        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.post(url, {
            "wb_lp": wb_lp,
            "before": text
        })
        if response.status_code == 200:
            break
        print(response)
    if response.status_code != 200:
        return None
    response.encoding = 'utf-8'
    d = pq(response.text)
    return d("#after").val()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python2 excite.py text LANG')
        sys.exit()
    print(translate(sys.argv[1], 'JA', sys.argv[2]))
