from flask import Blueprint, g, render_template, request, redirect, url_for
from . import db
import datetime

bp = Blueprint('todo', 'todo', url_prefix='/')

global username

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
        return render_template('todo/todos.html', data=data, format_date=format_date, format_time=format_time)#nav_right_text=username
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


