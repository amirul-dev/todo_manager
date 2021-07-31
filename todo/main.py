from flask import Flask
import os

def create_app():                       
	app = Flask("todo")     
	app.config.from_mapping(        
		DATABASE=os.path.join(app.instance_path, 'todo.sqlite')	
	)

	from . import db,todo,auth,functions             
	app.register_blueprint(todo.bp)  
	app.register_blueprint(auth.bp)
	app.register_blueprint(functions.bp)
           
	db.init_app(app)

	return app
