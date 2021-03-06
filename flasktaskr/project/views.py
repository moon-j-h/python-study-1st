
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from forms import AddTaskForm, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User

import sqlite3

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("login first.")
            return redirect(url_for('login'))
    return wrap

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"%s 필드를 다시 확인해주세요. - %s" % (getattr(form, field).label.text, error), 'error')

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash("Goodbye!")
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                flash("안뇽!")
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password'
        else:
            error = 'id와 비밀번호는 필수!!'
    return render_template("login.html", form=form, error=error)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering. Please login.")
                return redirect(url_for('login'))
            except:
                error = "already exist."
        else:
            error = "조건 불만족"
    return render_template('register.html', form=form, error=error)

def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

@app.route('/tasks/')
@login_required
def tasks():
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )

@app.route("/add/", methods=['GET', 'POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form['due_date'].data,
                form.priority.data,
                datetime.datetime.utcnow(),
                '1',
                session['user_id']
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Successfully posted.")
            return redirect(url_for('tasks'))
    return render_template(
        'tasks.html',
        form=form,
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )

@app.route("/complete/<int:task_id>")
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id:
        task.update({"status" : 0})
        db.session.commit()
        flash("Complete!")
        return redirect(url_for('tasks'))
    else:
        flash("You can only update tasks that belong to you.")
        return redirect(url_for('tasks'))

@app.route("/delete/<int:task_id>")
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id:
        task.delete()
        db.session.commit()
        flash("Successfully Deleted")
        return redirect(url_for('tasks'))
    else:
        flash("You can only update tasks that belong to you.")
        return redirect(url_for('tasks'))
