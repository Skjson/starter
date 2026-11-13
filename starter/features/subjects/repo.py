"""SQL справочника предметов."""

def list_subjects(con):
    rows = con.execute("SELECT id, name FROM subjects ORDER BY name, id")
    return [dict(row) for row in rows]


def get_subject(con, record_id):
    row = con.execute("SELECT id, name FROM subjects WHERE id = ?", (record_id,)).fetchone()
    return dict(row) if row is not None else None


def insert_subject(con, name):
    return con.execute("INSERT INTO subjects (name) VALUES (?)", (name,)).lastrowid


def update_subject(con, name, record_id):
    con.execute("UPDATE subjects SET name = ? WHERE id = ?", (name, record_id))


def delete_subject(con, record_id):
    con.execute("DELETE FROM subjects WHERE id = ?", (record_id,))
