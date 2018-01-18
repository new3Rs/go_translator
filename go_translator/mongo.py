# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
try:
    from urllib.parse import urlsplit as urlsplit
except:
    from urlparse import urlsplit as urlsplit
from pymongo import MongoClient

def setup_mongo(url):
    parsed = urlsplit(url)
    db_name = parsed.path[1:]
    try:
        client = MongoClient(url)
        db = client[db_name]
        if '@' in url:
            user, password = parsed.netloc.split('@')[0].split(':')
            db.authenticate(user, password)
        return (client, db)
    except:
        return None
