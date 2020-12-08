from flask import Flask, request, render_template
from mbiiez import settings
from mbiiez.db import db

import sqlite3

app = Flask(__name__, static_url_path="/assets", static_folder="web/static", template_folder="web/templates")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/pages/tables/basic-table.html', methods=['GET', 'POST'])
def log():

    conn = db().connect()
    cur = conn.cursor()  
    q = ''' SELECT * FROM logs ORDER BY added DESC LIMIT 100; '''
    cur.execute(q)
    rows = cur.fetchall()

    return render_template("pages/tables/basic-table.html", rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.web_service.port)

