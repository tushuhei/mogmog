# -*- coding: utf-8 -*-

import MySQLdb
import urllib
import urllib2
import lxml.html
import re
import ConfigParser
from os import path
from urlparse import urlparse,parse_qs

APP_ROOT = path.dirname(path.abspath( __file__ )) + "/../"
config = ConfigParser.SafeConfigParser()
config.read("%sapp.conf"%APP_ROOT)

def connect_db(db="database"):
    con = MySQLdb.connect(db=config.get(db, "db"),
            host=config.get(db, "host"),
            user=config.get(db, "user"),
            passwd=config.get(db, "passwd"),
            charset=config.get(db, "charset"),
            use_unicode=False)
    con.autocommit(True)
    return con.cursor(MySQLdb.cursors.DictCursor)

def getHTML(url, post=None, encode=None):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 \
            (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 \
            Chrome/12.0.742.112 Safari/534.30'}
    data = urllib.urlencode(post) if post else None
    request = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(request)
        html = response.read()
        if encode:
            #sjis で文字化けする時は 'cp932' を試すべし
            #euc で文字化けする時は 'windows-1252' を試すべし
            html = unicode(html, encode)
        return lxml.html.fromstring(html)
    except urllib2.HTTPError as e:
        print e
        return None
    except urllib2.URLError as e:
        print e

def get_search_rank_from_referrer(referrer):
    try:
        return int(re.search("&cd=(\d+)", referrer).group(1))
    except:
        return None

def get_hit_count_from_query(query):
    html = getHTML("http://www.google.co.jp/search?q=%s"%(urllib.quote(query)), encode="utf8")
    hit_count = html.xpath("//div[@id='resultStats']")[0].text
    hit_count = int(hit_count.replace(u"約", "").replace(u"件", "").replace(u",",""))
    return hit_count

def getcolor(color, msg):
    colors = {
            'clear': '\033[0m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m'
            }
    return colors[color] + msg + colors['clear']

def smoothing(a, n):
    result = []
    for i in range(len(a)):
        result.append(sum([a[(i+j)%len(a)] for j in range(-n, n + 1)]) / (2 * n + 1))
    return result

def get_thumbnail(url):
    response = urllib2.urlopen(url)
    html = response.read()
    html = lxml.html.fromstring(html)
    data = html.xpath("//meta[@property='og:image']/@content")
    if not data: return None
    return data[0].encode("utf8")

