# coding: utf8
from util import *
import time
import urllib2
import lxml.html
import datetime

def main():
    cur = connect_db()
    url = 'http://www.famitsu.com/rss/fcom_all.rdf'
    response = urllib2.urlopen(url)
    html = response.read()
    html = lxml.html.fromstring(html)
    items = html.xpath('//item')
    data = []
    for item in items:
        url = lxml.etree.tostring(item.xpath('link')[0]).replace("<link/>", "").replace("\n", "")
        title = item.xpath('title')[0].text.encode("utf8")
        description = item.xpath('description')[0].text.encode("utf8")
        pubdate = datetime.datetime.strptime(item.xpath('pubdate')[0].text, "%a, %d %b %Y %H:%M:%S +0900")
        thumbnail = get_thumbnail(url)
        print url, title, description, pubdate, thumbnail
        print type(url), type(title), type(description), type(pubdate), type(thumbnail)
        datum = (
                title,
                description,
                "ファミ通",
                pubdate,
                url,
                thumbnail
                )
        data.append(datum)
        time.sleep(.5)
    cur.executemany("INSERT IGNORE INTO article (title, description, source, pubdate, url, thumbnail) VALUES (%s, %s, %s, %s, %s, %s)", data)

if __name__ == "__main__":
    main()
