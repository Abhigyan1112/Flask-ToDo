from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request,redirect

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

@app.route("/", methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo=ToDo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=ToDo.query.all()
    return render_template('index.html',allTodo=allTodo)    #passing allTodo(all entries) to the index.html which will be rendered.

@app.route("/show")     #to show all the entries present in the database
def show():
    allToDo=ToDo.query.all()
    print(allToDo)
    return 'check terminal'

@app.route("/Update/<int:sno>", methods=['GET','POST'])     #to show all the entries present in the database
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=db.get_or_404(ToDo,sno)
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=db.get_or_404(ToDo,sno)
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")     #to show all the entries present in the database
def delete(sno):
    todo=db.get_or_404(ToDo,sno)
    db.session.delete(todo)
    db.session.commit()
    allTodo=ToDo.query.all()
    return render_template('index.html',allTodo=allTodo)
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)

