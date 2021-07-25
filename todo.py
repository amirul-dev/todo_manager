from flask import Blueprint, g, render_template
from . import db

bp = Blueprint('todo', 'todo', url_prefix='/')

@bp.route('/')
def index():
	#conn = db.get_db
	#cursor = conn.cursor()
	#cursor.execute('select title, company_name, jd_text from openings')
	#jobs = cursor.fetchall()
	return render_template('todo/index.html')

@bp.route('/signin')       
def signin():
	return render_template('todo/signin.html')

@bp.route('/signup')       
def signup():
	return render_template('todo/signup.html')

@bp.route('/todos/')       
def todos():
	return render_template('todo/todos.html')


