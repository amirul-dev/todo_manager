from flask import Blueprint, g, render_template
from . import db

bp = Blueprint('todo', 'todo', url_prefix='/')

@bp.route('/')
def todos():
	#conn = db.get_db
	#cursor = conn.cursor()
	#cursor.execute('select title, company_name, jd_text from openings')
	#jobs = cursor.fetchall()
	return render_template('todo/todos.html')

@bp.route('/<id>')        # <> to take whatever comes in 
def detail(id):
	return render_template('todo/tododetails.html', id=id)
