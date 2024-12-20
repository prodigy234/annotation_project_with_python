from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kajolagbenga@localhost/annotation_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)

class Annotation(db.Model):
    __tablename__ = 'annotations'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    annotation_data = db.Column(db.JSON, nullable=False)

# API to create a task (add image URL)
@app.route('/create-task', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(image_url=data['image_url'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task_id": new_task.id}), 201

# API to fetch all tasks (images)
@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "image_url": task.image_url} for task in tasks])

# API to save annotations
@app.route('/save-annotation', methods=['POST'])
def save_annotation():
    data = request.json
    new_annotation = Annotation(task_id=data['task_id'], annotation_data=data['annotation_data'])
    db.session.add(new_annotation)
    db.session.commit()
    return jsonify({"message": "Annotation saved successfully"}), 201

# Annotation UI (HTML Page)
@app.route('/')
def index():
    return render_template('index.html')  # Loads the annotation UI

if __name__ == '__main__':
    app.run(debug=True)
