from app import app, db
from datetime import datetime
from flask import render_template, request, jsonify
from app.models import ToDoItem


@app.route("/", methods=["GET"])
def home():
    todoitems = db.session.query(ToDoItem).all()
    return render_template("index.html", todoitems=todoitems)


@app.route("/submit", methods=["POST"])
def submit():
    global_todoitem_object = ToDoItem()

    title = request.form["title"]
    description = request.form["description"]
    due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d")

    todoitem = ToDoItem(title=title, description=description, due_date=due_date)
    db.session.add(todoitem)
    db.session.commit()
    global_todoitem_object = todoitem

    response = f"""

    <tr>
        <td>{title}</td>
        <td>{description}</>
        <td>{due_date.date()}</>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_todoitem_object.todoitem_id}">
                Edit Item
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_todoitem_object.todoitem_id}"
                class="btn btn-danger">
                Delete
            </button>
        </td>
    </tr>
    """

    return response


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_todoitem(id):
    todoitem = ToDoItem.query.get(id)
    db.session.delete(todoitem)
    db.session.commit()

    return ""


@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    todoitem = ToDoItem.query.get(id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-todoitem-row/{id}">
    <td><input name="title" value="{todoitem.title}"/></td>
    <td><input name="description" value="{todoitem.description}"/></td>
    <td><input type="date" name="due_date" value="{todoitem.due_date.date()}"/></td>
    <td>
        <button class="btn btn-primary" hx-get="/get-todoitem-row/{id}">
            Cancel
        </button>
        <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
            Save
        </button>
    </td>
    </tr>
    """
    return response


@app.route("/get-todoitem-row/<int:id>", methods=["GET"])
def get_todoitem_row(id):
    todoitem = ToDoItem.query.get(id)

    response = f"""
    <tr>
        <td>{todoitem.title}</td>
        <td>{todoitem.description}</td>
        <td>{todoitem.due_date.date()}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Item
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-danger">
                Delete
            </button>
        </td>
    </tr>
    """

    return response


@app.route("/update/<int:id>", methods=["PUT"])
def update_todoitem(id):
    db.session.query(ToDoItem).filter(ToDoItem.todoitem_id == id).update(
        {
            "title": request.form["title"],
            "description": request.form["description"],
            "due_date": datetime.strptime(request.form["due_date"], "%Y-%m-%d"),
        }
    )
    db.session.commit()

    title = request.form["title"]
    description = request.form["description"]
    due_date = request.form["due_date"]

    response = f"""
    <tr>
        <td>{title}</td>
        <td>{description}</td>
        <td>{due_date}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Item
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-danger">
                    Delete
            </button>
        </td>
    </tr>
    """

    return response
