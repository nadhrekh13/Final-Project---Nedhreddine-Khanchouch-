from settings import DATABASE_URI, SECRET_KEY

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "completed": self.completed}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.as_dict() for task in tasks]), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.as_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = Task.query.get_or_404(task_id)
    task.title = data['title']
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.as_dict()), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)