"""HTTP и JSON раздела студентов."""

from flask import request
from . import bp, service


@bp.get("/api/students")
def get_items():
    group_id = request.args.get("group_id", type=int)
    if group_id is None and "group_id" in request.args:
        raise ValueError("Группа: укажите положительный целый ID.")
    return {"items": service.list_students(group_id, request.args.get("q", ""))}


@bp.post("/api/students")
@bp.post("/api/students/<int:record_id>")
def save_item(record_id=None):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Ожидается JSON-объект.")
    item = service.save_student(data.get("name"), data.get("group_id"), data.get("email"), record_id)
    return {"item": item}, 201 if record_id is None else 200


@bp.delete("/api/students/<int:record_id>")
def delete_item(record_id):
    service.delete_student(record_id)
    return "", 204
