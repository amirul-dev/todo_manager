from flask import Blueprint, g, render_template, request, redirect, url_for
from . import db
import datetime
import passlib

global username
username=''

bp = Blueprint('todo', 'todo', url_prefix='/')

def rem_time_calc(f):
	if f[4]=='checked':
		return '', 'Done'
	else:
		due_date = datetime.datetime.strptime(f[2], '%Y-%m-%d')
		dt = f[3].split(':')
		due_time = datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]))
		due_datetime = due_date+due_time
		current_datetime = datetime.datetime.now()
		rem_time = due_datetime - current_datetime
		days = abs(rem_time.days)
		seconds = rem_time.seconds
		hours = seconds//3600
		minutes = (seconds//60)%60
		if days==0:
			rem_time = f'{hours}hrs, {minutes}mins'
		else:
			rem_time = f'{days}days, {hours}hrs, {minutes}mins'
		if due_datetime > current_datetime:
			status = 'Due'
		else:
			status = 'Overdue'
		return ' by : '+rem_time, status

def check_overdue(due_date, due_time,status):
	if status=='checked':
		return ''
	else:
		due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d')
		dt = due_time.split(':')
		due_time = datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]))
		due_datetime = due_date+due_time
		current_datetime = datetime.datetime.now()
		if due_datetime < current_datetime:
			status = 'Overdue'
			return status
	
def format_date(d):
	d = datetime.datetime.strptime(str(d), '%Y-%m-%d')
	d = d.strftime("%a - %b %d, %Y")
	return d

def format_time(t):
	t = datetime.datetime.strptime(t, "%H:%M")
	t = t.strftime("%I:%M %p")
	return t

@bp.route('/')
def index():
	global username
	username = ''
	return render_template('todo/index.html')

@bp.route('/signin', methods=['GET', 'POST'])       
def signin():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        return render_template('todo/signin.html')
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        cursor.execute("select email from users")
        emails = cursor.fetchall()
        emails = [x[0] for x in emails]
        if email in emails:
                cursor.execute("select password, name, id from users where email = ?", [email])
                userdata = cursor.fetchone()
                global username
                username = userdata[1]
                if password == userdata[0]:
	                return redirect(url_for("todo.todos", userid=userdata[2]), 302)
                else:
                        return render_template('todo/signin.html') 
        else:
                return redirect(url_for("todo.signup"), 302) 
        
@bp.route('/signup', methods=['GET', 'POST'])       
def signup():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        return render_template('todo/signup.html')
    elif request.method == "POST":
        global username
        username = request.form.get('name').capitalize()
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        remember = request.form.get('remember')
        cursor.execute("select email from users")
        emails = cursor.fetchall()
        emails = [x[0] for x in emails]
        if email in emails:
                return redirect(url_for("todo.signin"), 302)
        elif password!=password2: 
                return render_template('todo/signup.html') 
        else:
                cursor.execute("insert into users (name, email, password) values (?,?,?)", [username, email, password])
                conn.commit()
                cursor.execute("select id from users where email = ?",[email])
                userid = cursor.fetchone()[0]
                return redirect(url_for("todo.todos",userid=userid), 302)

@bp.route('/todos/<userid>', methods=['GET', 'POST'])       
def todos(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        if username=='':
                return redirect(url_for("todo.index"), 302)
        cursor.execute("select id, title, due_date, due_time, status from todos where userid=? order by due_date, due_time ",[userid])
        data = cursor.fetchall()
        if data : 
                first_todo = data[0][1]
                rem_time, status = rem_time_calc(data[0])
        else:
                first_todo = ''
                rem_time, status = '',''
        return render_template('todo/todos.html', data=data, first_todo=first_todo, rem_time=rem_time, status=status, format_date=format_date, format_time=format_time, check_overdue=check_overdue, nav_right_text=username, userid=userid)
    elif request.method == "POST":
        newtodo = request.form.get('new-todo').capitalize()
        newtodo_date = request.form.get('new-todo-date')
        newtodo_time = request.form.get('new-todo-time')
        cursor.execute("insert into todos (title, due_date, due_time, userid) values (?,?,?,?)", [newtodo, newtodo_date, newtodo_time, userid])
        conn.commit()
        return redirect(url_for("todo.todos", userid=userid), 302)

@bp.route('/firstitem/<userid>')       
def firstitem(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select id, title, due_date, due_time, status from todos where userid=? order by due_date, due_time ",[userid])
    data = cursor.fetchone()
    if data : 
        first_todo = data[1]
        rem_time, status = rem_time_calc(data)
    else:
        first_todo = ''
        rem_time, status = '',''
    return f'{first_todo};{status}{rem_time}'

@bp.route('/shopping/<userid>', methods=['GET', 'POST'])       
def shopping(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        if username=='':
                return redirect(url_for("todo.index"), 302)
        cursor.execute("select id, item, status from shopping where userid=?",[userid])
        data = cursor.fetchall()
        return render_template('todo/shopping.html', data=data, nav_right_text=username, userid=userid)
    elif request.method == "POST":
        newitem = request.form.get('new-item')
        cursor.execute("insert into shopping (item, userid) values (?,?)", [newitem,userid])
        conn.commit()
        return redirect(url_for("todo.shopping", userid=userid), 302)

@bp.route('/delete/<id>/<table>/<userid>', methods=['POST'])   
def delete(id,table,userid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"delete from {table} where id = (?)", [id])
    conn.commit()
    return redirect(url_for(f"todo.{table}", userid=userid), 302)

@bp.route('/tick/<id>/<table>/<userid>/<status>', methods=['POST'])   
def tick(id,table,userid,status):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"update {table} set status = (?) where id = (?)", [status, id])
    conn.commit()
    return redirect(url_for("todo.todos", userid=userid), 302)


