import sqlite3

from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from forms import AddTaskForm

app = Flask(__name__)
app.config.from_object('_config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("로그인 하셈요")
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash("바이바이")
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config["USERNAME"] or request.form['password'] != app.config['PASSWORD']:
            error = '다시 한번 확인 부탁'
            return render_template("login.html", error=error)
        else:
            session['logged_in'] = True
            flash("안뇽!")
            return redirect(url_for('tasks'))
    return render_template('login.html')

@app.route('/tasks/')
@login_required
def tasks():
    g.db = connect_db()
    
    cursor = g.db.execute('SELECT name, due_date, priority, task_id from tasks where status=1')
    open_tasks = [
        dict(name = row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cursor.fetchall()
    ]

    cursor = g.db.execute('SELECT name, due_date, priority, task_id from tasks where status=0')
    closed_tasks = [
        dict(name = row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cursor.fetchall()
    ]

    g.db.close()
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )

@app.route("/add/", methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['name']
    date = request.form['date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash("모든 칸을 입력해야한답니다...")
        return redirect(url_for('tasks'))
    else:
        g.db.execute("insert into tasks (name, due_date, priority, status) values(?, ?, ?, 1)", [
            request.form['name'],
            request.form['date'],
            request.form['priority']
        ])
        g.db.commit()
        g.db.close()
        flash('새로운 task가 추가되었습니다.')
        return redirect(url_for('tasks'))

@app.route("/complete/<int:task_id>")
@login_required
def complete(taks_id):
    g.db = connect_db()
    g.db.execute('UPDATE tasks SET status=0 where task_id=?', [taks_id])
    g.db.commit()
    g.db.close()
    flash('task 완료!!')
    return redirect(url_for('tasks'))

@app.route("/delete/<int:task_id>")
@login_required
def delete(task_id):
    g.db = connect_db()
    g.db.execute("DELETE FROM tasks where task_id=?", [task_id])
    g.db.commit()
    g.db.close()
    flash("삭제 완료!!")
    return redirect(url_for('tasks'))
