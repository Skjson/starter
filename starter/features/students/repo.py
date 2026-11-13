"""SQL для списка, редактирования и удаления студентов."""

STUDENT_COLUMNS = """
    SELECT s.id, s.name, s.group_id, g.name AS group_name, s.email,
           (SELECT COUNT(*) FROM grades AS gr WHERE gr.student_id = s.id) AS grade_count
    FROM students AS s
    JOIN groups AS g ON g.id = s.group_id
"""


def list_students(con, group_id=None):
    query = STUDENT_COLUMNS
    params = ()
    if group_id is not None:
        query += " WHERE s.group_id = ?"
        params = (group_id,)
    rows = con.execute(query + " ORDER BY s.name, s.id", params)
    return [dict(row) for row in rows]


def get_student(con, record_id):
    row = con.execute(STUDENT_COLUMNS + " WHERE s.id = ?", (record_id,)).fetchone()
    return dict(row) if row is not None else None


def insert_student(con, name, group_id, email):
    cursor = con.execute(
        "INSERT INTO students (name, group_id, email) VALUES (?, ?, ?)",
        (name, group_id, email),
    )
    return cursor.lastrowid


def update_student(con, name, group_id, email, record_id):
    con.execute(
        "UPDATE students SET name = ?, group_id = ?, email = ? WHERE id = ?",
        (name, group_id, email, record_id),
    )


def delete_grades(con, student_id):
    con.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))


def delete_student(con, student_id):
    con.execute("DELETE FROM students WHERE id = ?", (student_id,))
