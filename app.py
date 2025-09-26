from asyncio import tasks
from datetime import datetime
from types import NoneType

from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, request, redirect, url_for, render_template

import db
from db import *
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func = db.check_deadline, trigger = "interval", minutes = 1)
scheduler.start()
@app.route('/')
def index():
    con = db.get_conn()
    db.check_deadline()
    tasks = fetch_all_tasks()
    return render_template("index.html", tasks=tasks, edit_id = None)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline'] if request.form['deadline'] else None
    deadline = parse_deadline(deadline)
    db.add_task(title, description, deadline)
    return redirect("/")


@app.route('/delete/<int:id>')
def delete(id):
    db.delete_task(id)
    return redirect("/")


@app.route('/done/<int:id>')
def done(id):
    db.mark_done(id)
    return redirect("/")


@app.route('/check')
def check():
    return redirect("/")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline'] if request.form['deadline'] else None
        deadline = parse_deadline(deadline)
        db.edit_task(id, title, description, deadline)
        return redirect("/")
    else:
        con = db.get_conn()
        db.check_deadline()
        tasks = fetch_all_tasks()
        return render_template("index.html", tasks = tasks, edit_id = id)


@app.route('/sort', methods=['GET'])
def sort_by_done():

    filter = request.args.get('filter')
    if filter == 'pending':
        tasks = list_not_done()
    elif filter == 'deadline':
        tasks = tasks_before_deadline()
    else:
        tasks = fetch_all_tasks()

    return render_template("index.html", tasks = tasks)



if __name__ == '__main__':
    app.run(debug=True)