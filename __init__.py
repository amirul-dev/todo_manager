from flask import Flask
import os

def create_app():                       
	app = Flask("todo", instance_path='/home/amirul/genskill/todo/instance')     
	app.config.from_mapping(        
		DATABASE=os.path.join(app.instance_path, 'todo.sqlite')
	)

	from . import todo              
	app.register_blueprint(todo.bp)  

	from . import db               
	db.init_app(app) 

	return app
