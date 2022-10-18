from app import db


class ToDoItem(db.Model):
    todoitem_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    due_date = db.Column(db.DateTime, nullable=False)
