"""Выбор отчёта и чтение данных."""

from db import connect_db
from . import repo

REPORTS = {
    "groups": repo.group_report,
    "no_grades": repo.no_grades_report,
    "failing": repo.failing_report,
}


def get_report(kind):
    report = REPORTS.get(kind)
    if report is None:
        raise ValueError("Неизвестный вид отчёта.")
    con = connect_db()
    try:
        return report(con)
    finally:
        con.close()
