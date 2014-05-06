#coding:utf8
from flask import Flask,request,jsonify,render_template
import ConfigParser
import MySQLdb
from os import path

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preview")
def preview():
    article_id = request.args.get('article_id', None)
    if not article_id: return jsonfy({"res":{}})
    cur = connect_db()
    cur.execute("""
    SELECT 
    id,
    title,
    description,
    source,
    pubdate,
    thumbnail,
    url
    FROM article
    WHERE id = %s
    LIMIT 1
    """, [article_id])
    data = cur.fetchall()
    if len(data) == 0: return jsonfy({"res":{}})
    return render_template("preview.html", dev=False, url=data[0]["url"])

@app.route("/api/latest")
def latest():
    cur = connect_db()
    cur.execute("""
    SELECT 
    id,
    title,
    source,
    pubdate,
    thumbnail
    FROM article
    ORDER BY pubdate DESC
    LIMIT 30
    """)
    return jsonify({"res": cur.fetchall()})

@app.route("/api/article")
def article():
    article_id = request.args.get('article_id', None)
    if not article_id: return jsonify({"res":{}})
    cur = connect_db()
    cur.execute("""
    SELECT 
    id,
    title,
    description,
    source,
    pubdate,
    thumbnail,
    url
    FROM article
    WHERE id = %s
    """, [article_id])
    data = cur.fetchall()
    if len(data) == 0: return jsonfy({"res":{}})
    return jsonify({"res": data[0]})

@app.route("/api/pick", methods=['GET', 'POST'])
def pick():
    cur = connect_db()
    if request.method == 'POST':
        article_id = request.args.get('article_id', None)
        user_id = request.args.get('user_id', None)
        cur.execute("""
        INSERT IGNORE INTO pick
        (article_id, user_id)
        VALUES (%s, %s)
        """, [article_id, user_id])
        return jsonify({"res": "ok"})
    else:
        user_id = request.args.get('user_id', None)
        cur.execute("""
        SELECT 
        id
        FROM article a
        LEFT JOIN pick p
        ON a.id=p.article_id
        WHERE p.user_id=%s;
        """, [user_id])
        data = [x["id"] for x in cur.fetchall()]
        return jsonify({"res": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=80)

