# blog.py - controller

from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '\xb3\x04\x0b7\x16\xdb\xf5?G(\x1f\xb7N\x85\xc9mT\xdcv%\xb4\x04Po'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("로그인 하셈요")
            return redirect(url_for('login'))
    return wrap

@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = "다시 하셈"
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template("login.html", error = error), status_code

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("로그아웃 완료")
    return redirect(url_for('login'))

@app.route("/main")
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute("SELECT * from posts")
    posts = [dict(title = row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("main.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)