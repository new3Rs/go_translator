# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import urllib2
import HTMLParser

def unescape(string):
    string = urllib2.unquote(string)
    return HTMLParser.HTMLParser().unescape(string)

if __name__ == '__main__':
    print(unescape('&copy;'))
