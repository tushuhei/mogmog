# coding: utf8
from util import *
import urllib2

cur = connect_db()
cur.execute("SELECT id, thumbnail FROM article WHERE thumbnail IS NOT NULL")
for row in cur.fetchall():
    url = row["thumbnail"]
    if not url: continue
    try:
        connection = urllib2.urlopen(url)
        print url, connection.getcode()
        connection.close()
    except urllib2.HTTPError, e:
        print url, e.getcode(), "error"
        cur.execute("UPDATE article SET thumbnail = NULL WHERE id = %s", [row["id"]])
