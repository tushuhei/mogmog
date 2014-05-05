# coding: utf8
from util import *
import urllib2
import lxml.html
cur = connect_db()
url = 'http://www.4gamer.net/rss/index.xml'
response = urllib2.urlopen(url)
html = lxml.html.fromstring(response.read())
items = html.xpath('//item')
data = []
for item in items:
    title = item.xpath('title')[0].text
    description = item.xpath('description')[0].text
    date = item.xpath('date')[0].text
    url = lxml.etree.tostring(item.xpath("link")[0]).replace("<link/>", "").replace("\n", "")
    thumbnail = "%sTN/001.jpg"%url
    datum = (title,
            description.replace("\n", "") if description else "",
            "4Gamer.net",
            date,
            url,
            thumbnail)
    data.append(datum)
cur.executemany("INSERT IGNORE INTO article (title, description, source, pubdate, url, thumbnail) VALUES (%s, %s, %s, %s, %s, %s)", data)
