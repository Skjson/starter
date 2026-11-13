"""SQL для матрицы журнала и итоговых оценок."""

def list_students(con, group_id):
    rows = con.execute(
        "SELECT id, name FROM students WHERE group_id = ? ORDER BY name, id",
        (group_id,),
    )
    return [dict(row) for row in rows]


def list_grades(con, group_id):
    rows = con.execute(
        """
        SELECT gr.id, gr.student_id, gr.subject_id, gr.mark
        FROM grades AS gr
        JOIN students AS s ON s.id = gr.student_id
        WHERE s.group_id = ?
        ORDER BY gr.student_id, gr.subject_id
        """,
        (group_id,),
    )
    return [dict(row) for row in rows]


def get_grade(con, student_id, subject_id):
    row = con.execute(
        "SELECT id, student_id, subject_id, mark FROM grades WHERE student_id = ? AND subject_id = ?",
        (student_id, subject_id),
    ).fetchone()
    return dict(row) if row is not None else None


def insert_grade(con, student_id, subject_id, mark):
    con.execute(
        "INSERT INTO grades (student_id, subject_id, mark) VALUES (?, ?, ?)",
        (student_id, subject_id, mark),
    )


def update_grade(con, student_id, subject_id, mark):
    con.execute(
        "UPDATE grades SET mark = ? WHERE student_id = ? AND subject_id = ?",
        (mark, student_id, subject_id),
    )


def delete_grade(con, student_id, subject_id):
    con.execute(
        "DELETE FROM grades WHERE student_id = ? AND subject_id = ?",
        (student_id, subject_id),
    )
