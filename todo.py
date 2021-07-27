from flask import Blueprint, g, render_template, request, redirect, url_for
from . import db
import datetime

bp = Blueprint('todo', 'todo', url_prefix='/')

global username

def rem_time_calc(f):
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
	return rem_time, status

def check_overdue(due_date, due_time):
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
                cursor.execute("select password, name from users where email = ?", [email])
                userdata = cursor.fetchone()
                global username
                username = userdata[1].capitalize()
                if password == userdata[0]:
	                return redirect(url_for("todo.todos"), 302)
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
                cursor.execute("insert into users (name, email, password) values (?,?,?)", [name, email, password])
                conn.commit()
                return redirect(url_for("todo.todos"), 302)

@bp.route('/todos/', methods=['GET', 'POST'])       
def todos():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select id, title, due_date, due_time from todo order by due_date, due_time")
        data = cursor.fetchall()
        first_data = data[0]
        rem_time, status = rem_time_calc(first_data)
        return render_template('todo/todos.html', data=data, first_data=first_data, rem_time=rem_time, status=status, format_date=format_date, format_time=format_time, check_overdue=check_overdue)#nav_right_text=username
    elif request.method == "POST":
        newtodo = request.form.get('new-todo')
        newtodo_date = request.form.get('new-todo-date')
        newtodo_time = request.form.get('new-todo-time')
        cursor.execute("insert into todo (title, due_date, due_time) values (?,?,?)", [newtodo, newtodo_date, newtodo_time])
        conn.commit()
        return redirect(url_for("todo.todos"), 302)

@bp.route('/shopping/', methods=['GET', 'POST'])       
def shopping():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select id, title from todo")
        data = cursor.fetchall()
        return render_template('todo/shopping.html', data=data, )#nav_right_text=username
    elif request.method == "POST":
        newtodo = request.form.get('new-todo')
        cursor.execute("insert into todo (title,) values (?)", [newtodo])
        conn.commit()
        return redirect(url_for("todo.shopping"), 302)

@bp.route('/delete/<id>', methods=['POST'])   
def delete(id):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("delete from todo where id = (?)", [id])
    conn.commit()
    return redirect(url_for("todo.todos"), 302)

@bp.route('/tick/<id>', methods=['POST'])   
def tick(id):
    conn = db.get_db()
    cursor = conn.cursor()
    status = request.form.get('tick')
    cursor.execute("upgrade todo set status = (?) where id = (?)", [id])
    conn.commit()
    return redirect(url_for("todo.todos"), 302)


