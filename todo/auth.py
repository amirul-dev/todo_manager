from flask import Blueprint, render_template, request, redirect, url_for, jsonify, app
from . import db

bp = Blueprint('auth', 'auth')
     
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
                app.username=userdata[1]
                username = userdata[1]
                if password == userdata[0]:
                        return redirect(url_for("todo.todos", userid=userdata[2]), 302)
                else:
                        alert='Invalid password' 
                        return render_template('todo/signin.html', alert=alert) 
        else:	
                alert='It seems that you dont have an account'
                return render_template('todo/signin.html',alert=alert) 

@bp.route('/signup', methods=['GET', 'POST'])       
def signup():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        return render_template('todo/signup.html')
    elif request.method == "POST":
        username = request.form.get('name').capitalize()
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        remember = request.form.get('remember')
        cursor.execute("select email from users")
        emails = cursor.fetchall()
        emails = [x[0] for x in emails]
        if email in emails:
                alert='You already have an account'
                return render_template('todo/signup.html',alert=alert)
        elif password!=password2: 
                alert='Passwords do not match'
                return render_template('todo/signup.html',alert=alert) 
        else:
                app.username=username
                cursor.execute("insert into users (name, email, password) values (?,?,?)", [username, email, password])
                conn.commit()
                cursor.execute("select id from users where email = ?",[email])
                userid = cursor.fetchone()[0]
                return redirect(url_for("todo.todos",userid=userid), 302)
