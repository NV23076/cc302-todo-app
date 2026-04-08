from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date

main = Blueprint("main", __name__)

todos = []

@main.route("/", methods=["GET", "POST"])
def index():

    # ADD TASK
    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")

        if task:
            todos.append({
                "task": task,
                "description": description,
                "priority": priority,
                "completed": False,
                "due_date": due_date
            })

        return redirect(url_for("main.index"))

    # SEARCH
    query = request.args.get("q")

    filtered_todos = todos

    if query:
        filtered_todos = [
            t for t in todos
            if query.lower() in t["task"].lower()
            or (t.get("description") and query.lower() in t["description"].lower())
        ]

    # SORT
    sort = request.args.get("sort")

    if sort == "due":
        filtered_todos = sorted(
            filtered_todos,
            key=lambda x: x["due_date"] if x["due_date"] else "9999-99-99"
        )

    today = date.today().isoformat()

    return render_template(
        "index.html",
        todos=filtered_todos,
        today=today
    )


@main.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for("main.index"))


@main.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    if 0 <= index < len(todos):
        new_task = request.form.get("task")
        if new_task:
            todos[index]["task"] = new_task
    return redirect(url_for("main.index"))


@main.route("/toggle/<int:index>")
def toggle(index):
    if 0 <= index < len(todos):
        todos[index]["completed"] = not todos[index]["completed"]
    return redirect(url_for("main.index"))