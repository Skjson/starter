"""Правила справочника предметов и управление транзакциями."""

import sqlite3
from db import connect_db
from . import repo


def list_subjects():
    con = connect_db()
    try:
        return repo.list_subjects(con)
    finally:
        con.close()


def save_subject(name, record_id=None):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Введите название.")
    name = name.strip()
    con = connect_db()
    try:
        with con:
            con.execute("BEGIN IMMEDIATE")
            if record_id is None:
                record_id = repo.insert_subject(con, name)
            else:
                if repo.get_subject(con, record_id) is None:
                    raise LookupError("Предмет не найден.")
                repo.update_subject(con, name, record_id)
            return repo.get_subject(con, record_id)
    except sqlite3.IntegrityError as error:
        raise ValueError("Такое название уже существует.") from error
    finally:
        con.close()


def delete_subject(record_id):
    con = connect_db()
    try:
        with con:
            con.execute("BEGIN IMMEDIATE")
            if repo.get_subject(con, record_id) is None:
                raise LookupError("Предмет не найден.")
            repo.delete_subject(con, record_id)
    except sqlite3.IntegrityError as error:
        raise ValueError("По предмету есть оценки. Сначала удалите их в журнале.") from error
    finally:
        con.close()
