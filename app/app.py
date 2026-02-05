import json
from flask import Flask, jsonify, request

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# Helper function to read tasks from the JSON file
def read_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
    return tasks

# Helper function to write tasks to the JSON file
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = read_tasks()
    return jsonify(tasks)

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        'id': len(read_tasks()) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    tasks = read_tasks()
    tasks.append(new_task)
    write_tasks(tasks)
    return jsonify({"message": "Task created!"}), 201

# Route to get a task by ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == id), None)
    if task:
        return jsonify(task)
    return jsonify({"message": "Task not found!"}), 404

# Route to update a task by ID
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == id), None)
    
    if task:
        task['title'] = data['title']
        task['description'] = data.get('description', task['description'])
        task['completed'] = data['completed']
        write_tasks(tasks)
        return jsonify({"message": "Task updated!"})
    
    return jsonify({"message": "Task not found!"}), 404

# Route to delete a task by ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == id), None)
    
    if task:
        tasks.remove(task)
        write_tasks(tasks)
        return jsonify({"message": "Task deleted!"})
    
    return jsonify({"message": "Task not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
