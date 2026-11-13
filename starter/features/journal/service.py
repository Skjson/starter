"""Чтение журнала и транзакции для оценки по паре студент и предмет."""

from db import connect_db
from features import positive_id
from features.groups.repo import get_group
from features.students.repo import get_student
from features.subjects.repo import get_subject, list_subjects
from . import repo


def get_journal(group_id):
    positive_id(group_id, "Группа")
    con = connect_db()
    try:
        with con:
            # Все части матрицы читаются из одного состояния БД.
            con.execute("BEGIN")
            group = get_group(con, group_id)
            if group is None:
                raise LookupError("Группа не найдена.")
            return {
                "group": group,
                "students": repo.list_students(con, group_id),
                "subjects": list_subjects(con),
                "grades": repo.list_grades(con, group_id),
            }
    finally:
        con.close()


def require_grade_parents(con, student_id, subject_id):
    if get_student(con, student_id) is None:
        raise LookupError("Студент не найден.")
    if get_subject(con, subject_id) is None:
        raise LookupError("Предмет не найден.")


def save_grade(student_id, subject_id, mark):
    positive_id(student_id, "Студент")
    positive_id(subject_id, "Предмет")
    if type(mark) is not int or mark not in (2, 3, 4, 5):
        raise ValueError("Оценка должна быть целым числом от 2 до 5.")
    con = connect_db()
    try:
        with con:
            # Получаем право записи до SELECT, чтобы два сохранения не выбрали INSERT одновременно.
            con.execute("BEGIN IMMEDIATE")
            require_grade_parents(con, student_id, subject_id)
            if repo.get_grade(con, student_id, subject_id) is None:
                repo.insert_grade(con, student_id, subject_id, mark)
            else:
                repo.update_grade(con, student_id, subject_id, mark)
            return repo.get_grade(con, student_id, subject_id)
    finally:
        con.close()


def delete_grade(student_id, subject_id):
    positive_id(student_id, "Студент")
    positive_id(subject_id, "Предмет")
    con = connect_db()
    try:
        with con:
            con.execute("BEGIN IMMEDIATE")
            require_grade_parents(con, student_id, subject_id)
            repo.delete_grade(con, student_id, subject_id)
    finally:
        con.close()
