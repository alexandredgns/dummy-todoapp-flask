from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://postgres:{os.environ['DB_KEY']}@localhost:5432/dummy-todoapp")

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id}, {self.description}>"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    new_description = request.get_json()['description']
    new_todo = Todo(description=new_description)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({
        'description': new_todo.description
    })

