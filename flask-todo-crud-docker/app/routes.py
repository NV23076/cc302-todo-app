from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime, date
from . import db
from .models import Todo

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        priority = request.form.get("priority", "medium")
        due_date_str = request.form.get("due_date")

        if task:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
            todo = Todo(
                task=task,
                description=description,
                priority=priority,
                due_date=due_date
            )
            db.session.add(todo)
            db.session.commit()

        return redirect(url_for("main.index"))

    # Get query parameters for search, filter, sort
    q = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    sort_by = request.args.get('sort', 'created_at')

    query = Todo.query

    # Search
    if q:
        query = query.filter(
            db.or_(
                Todo.task.ilike(f'%{q}%'),
                Todo.description.ilike(f'%{q}%')
            )
        )

    # Filters
    if status_filter:
        query = query.filter(Todo.status == status_filter)
    if priority_filter:
        query = query.filter(Todo.priority == priority_filter)

    # Sorting
    if sort_by == 'due_date':
        query = query.order_by(Todo.due_date.asc())
    elif sort_by == 'priority':
        # Custom priority order: high, medium, low
        query = query.order_by(
            db.case(
                (Todo.priority == 'high', 1),
                (Todo.priority == 'medium', 2),
                (Todo.priority == 'low', 3)
            )
        )
    else:  # created_at
        query = query.order_by(Todo.created_at.desc())

    todos = query.all()
    today = date.today().isoformat()
    return render_template("index.html", todos=todos, today=today, q=q, status_filter=status_filter, priority_filter=priority_filter, sort_by=sort_by)

@main.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    new_task = request.form.get("task")
    if new_task:
        todo.task = new_task
        todo.description = request.form.get("description")
        todo.priority = request.form.get("priority", "medium")
        due_date_str = request.form.get("due_date")
        todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        todo.updated_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/toggle/<int:id>")
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.status = 'completed' if todo.status == 'pending' else 'pending'
    todo.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("main.index"))

# API endpoints for AJAX if needed
@main.route("/api/todos", methods=["GET"])
def api_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@main.route("/api/todos/<int:id>", methods=["PUT"])
def api_update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    if 'task' in data:
        todo.task = data['task']
    if 'description' in data:
        todo.description = data['description']
    if 'priority' in data:
        todo.priority = data['priority']
    if 'due_date' in data:
        todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None
    if 'status' in data:
        todo.status = data['status']
    todo.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(todo.to_dict())
