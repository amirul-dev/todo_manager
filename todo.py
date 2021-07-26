from flask import Blueprint, g, render_template, request, redirect, url_for
from . import db

bp = Blueprint('todo', 'todo', url_prefix='/')

@bp.route('/')
def index():
	#conn = db.get_db
	#cursor = conn.cursor()
	#cursor.execute('select title, company_name, jd_text from openings')
	#jobs = cursor.fetchall()
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
                cursor.execute("select password from users where email = ?", [email])
                db_password = cursor.fetchone()
                if password == db_password[0]:
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
        name = request.form.get('name')
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

@bp.route('/todos/')       
def todos():
	return render_template('todo/todos.html')


