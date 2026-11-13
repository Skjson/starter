"""Проверка данных студента, перевод и атомарное удаление."""

import re
from db import connect_db
from features import positive_id
from features.groups.repo import get_group
from . import repo


def clean_values(name, group_id, email):
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 50:
        raise ValueError("Введите имя длиной от 1 до 50 символов.")
    group_id = positive_id(group_id, "Группа")
    if email is not None and not isinstance(email, str):
        raise ValueError("Введите корректный email.")
    email = email.strip() if email else None
    if email and not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", email):
        raise ValueError("Введите корректный email.")
    return name.strip(), group_id, email or None


def list_students(group_id=None, q=""):
    if group_id is not None:
        positive_id(group_id, "Группа")
    con = connect_db()
    try:
        items = repo.list_students(con, group_id)
    finally:
        con.close()
    query = q.strip().lower()
    return [item for item in items if query in item["name"].lower()] if query else items


def save_student(name, group_id, email, record_id=None):
    name, group_id, email = clean_values(name, group_id, email)
    if record_id is not None:
        positive_id(record_id, "Студент")
    con = connect_db()
    try:
        with con:
            con.execute("BEGIN IMMEDIATE")
            if get_group(con, group_id) is None:
                raise ValueError("Выбранная группа не существует.")
            if record_id is None:
                record_id = repo.insert_student(con, name, group_id, email)
            else:
                if repo.get_student(con, record_id) is None:
                    raise LookupError("Студент не найден.")
                repo.update_student(con, name, group_id, email, record_id)
            return repo.get_student(con, record_id)
    finally:
        con.close()


def delete_student(student_id, simulate_error=False):
    positive_id(student_id, "Студент")
    con = connect_db()
    try:
        with con:
            con.execute("BEGIN IMMEDIATE")
            if repo.get_student(con, student_id) is None:
                raise LookupError("Студент не найден.")
            repo.delete_grades(con, student_id)
            if simulate_error:
                raise RuntimeError("Учебная ошибка после удаления оценок.")
            repo.delete_student(con, student_id)
    finally:
        con.close()
