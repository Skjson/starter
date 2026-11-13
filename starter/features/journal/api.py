"""HTTP и JSON журнала оценок."""

from flask import request
from . import bp, service


@bp.get("/api/journal")
def get_items():
    return service.get_journal(request.args.get("group_id", type=int))


@bp.post("/api/journal/grades")
def save_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Ожидается JSON-объект.")
    item = service.save_grade(data.get("student_id"), data.get("subject_id"), data.get("mark"))
    return {"item": item}, 200


@bp.delete("/api/journal/grades/<int:student_id>/<int:subject_id>")
def delete_item(student_id, subject_id):
    service.delete_grade(student_id, subject_id)
    return "", 204
