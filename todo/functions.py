from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from . import db, datetimeCalc as dt

bp = Blueprint('functions', 'functions')

@bp.route('/firstitem/<userid>')       
def firstitem(userid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select id, title, due_date, due_time, status from todos where userid=? order by due_date, due_time ",[userid])
    data = cursor.fetchone()
    if data : 
        first_todo = data[1]
        rem_time, status = dt.rem_time_calc(data)
    else:
        first_todo = ''
        rem_time, status = '',''
    data = {'first_todo':first_todo, 'rem_time':status+rem_time}
    return jsonify(data)

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
