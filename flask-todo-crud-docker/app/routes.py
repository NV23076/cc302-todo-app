from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date

main = Blueprint("main", __name__)

todos = []

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        due_date = request.form.get("due_date")

        if task:
            todos.append({
                "task": task,
                "completed": False,
                "due_date": due_date
            })

        return redirect(url_for("main.index"))

    today = date.today().isoformat()
    return render_template("index.html", todos=todos, today=today)

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
