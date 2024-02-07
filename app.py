from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Define Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Route for homepage
@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# Route for adding new todo
@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# Route for marking todo as complete
@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
