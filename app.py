from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
# initialize the app with the extension
db.init_app(app)
# This class create for schema of database

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    with app.app_context():
        db.create_all()
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)

# For page routing
# @app.route("/products")
# def products():
#     return "<h1>This is product page</h1>"

# Login page route
@app.route("/login")
def login():
    return render_template("login.html")

# Show Tables
@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is show page"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    delete_Todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_Todo)
    db.session.commit()
    return redirect("/")

if __name__ == "main":
    app.run(debug=False, port=8000)