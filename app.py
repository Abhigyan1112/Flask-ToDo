from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'     #this is the way to defince the database URI
db=SQLAlchemy(app)      #this creates a database for app

# on terminal enter python and then enter the following to create the todo.db database
# from app import db
# db.create_all

class ToDo(db.Model):       #creating a class for every entry in the database. An instance of this will be created every time an entry as filled and will be stored in the file todo.db we created in the instance folder
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/")
def hello_world():
    todo=ToDo(title="Enter the Title",desc="Enter the Description")
    db.session.add(todo)
    db.session.commit()
    return render_template('index.html')

@app.route("/products")
def products(): 
    return "This is Products Page"

@app.route("/show")     #to show all the entries present in the database
def prod():
    allToDo=ToDo.query.all()
    print(allToDo)
    return 'check terminal'

if __name__ == "__main__":
    app.run(debug=True, port=8000)

