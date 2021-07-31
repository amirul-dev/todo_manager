from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from . import db, datetimeCalc as dt

bp = Blueprint('todo', 'todo', url_prefix='/')

@bp.route('/')
def index():
	return render_template('todo/index.html')  

@bp.route('/todos/<userid>', methods=['GET', 'POST'])       
def todos(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select name from users where id=?",[userid])
        userdata = cursor.fetchone()
        username = userdata[0]
        cursor.execute("select id, title, due_date, due_time, status from todos where userid=? order by due_date, due_time ",[userid])
        data = cursor.fetchall()
        if data:
                first_todo = data[0][1]
                rem_time, status = dt.rem_time_calc(data[0])
        else:
                first_todo = ''
                rem_time, status = '',''
        return render_template('todo/todos.html', data=data, first_todo=first_todo, rem_time=rem_time, status=status, format_date=dt.format_date, format_time=dt.format_time, check_overdue=dt.check_overdue, nav_right_text=username, userid=userid)
    elif request.method == "POST":
        newtodo = request.form.get('new-todo').capitalize()
        newtodo_date = request.form.get('new-todo-date')
        newtodo_time = request.form.get('new-todo-time')
        cursor.execute("insert into todos (title, due_date, due_time, userid) values (?,?,?,?)", [newtodo, newtodo_date, newtodo_time, userid])
        conn.commit()
        return redirect(url_for("todo.todos", userid=userid), 302)

@bp.route('/shopping/<userid>', methods=['GET', 'POST'])       
def shopping(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select name from users where id=?",[userid])
        userdata = cursor.fetchone()
        username = userdata[0]
        cursor.execute("select id, item, status from shopping where userid=?",[userid])
        data = cursor.fetchall()
        return render_template('todo/shopping.html', data=data, nav_right_text=username, userid=userid)
    elif request.method == "POST":
        newitem = request.form.get('new-item')
        cursor.execute("insert into shopping (item, userid) values (?,?)", [newitem,userid])
        conn.commit()
        return redirect(url_for("todo.shopping", userid=userid), 302)


