# coding: utf8
import urllib2
import lxml.html
from datetime import datetime
from util import *
url = 'http://www.gamespark.jp/'
response = urllib2.urlopen(url)
html = response.read()
html = lxml.html.fromstring(html)
items = html.xpath("//div[@id='mainBottomLeft']/div[3]/ul/li")
cur = connect_db()
for item in items:
    datum = {
            "title": item.xpath("h3/a")[0].text,
            "link": u"http://www.gamespark.jp"+item.xpath("a/@href")[0],    
            "description": item.xpath("p[@class='newsSummary']/a")[0].text,      
            "pubdate": datetime.strptime(item.xpath("p[@class='newsDate']/a")[0].text.replace(u"年", u"/").replace(u"月", u"/").replace(u"日", u""), u"%Y/%m/%d %H:%M:%S"),
            "thumbnail": u"http://www.gamespark.jp"+item.xpath("a/img/@src")[0],
            }
    cur.execute("""
    INSERT IGNORE INTO article 
    (title, description, source, pubdate, url, thumbnail) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """, [datum["title"], datum["description"], "Game Spark", datum["pubdate"], datum["link"], datum["thumbnail"]])
