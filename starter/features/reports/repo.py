"""Три SQL-отчёта электронного журнала."""

def group_report(con):
    cursor = con.execute(
        """
        SELECT g.id, g.name, COUNT(DISTINCT s.id) AS student_count,
               COUNT(gr.id) AS grade_count, ROUND(AVG(gr.mark), 2) AS average_mark
        FROM groups AS g
        LEFT JOIN students AS s ON s.group_id = g.id
        LEFT JOIN grades AS gr ON gr.student_id = s.id
        GROUP BY g.id, g.name
        ORDER BY g.name, g.id
        """
    )
    return [dict(row) for row in cursor.fetchall()]


def no_grades_report(con):
    cursor = con.execute(
        """
        SELECT s.id, s.name, g.name AS group_name
        FROM students AS s
        JOIN groups AS g ON g.id = s.group_id
        LEFT JOIN grades AS gr ON gr.student_id = s.id
        GROUP BY s.id, s.name, g.name
        HAVING COUNT(gr.id) = 0
        ORDER BY g.name, s.name, s.id
        """
    )
    return [dict(row) for row in cursor.fetchall()]


def failing_report(con):
    cursor = con.execute(
        """
        SELECT s.id, s.name, g.name AS group_name
        FROM students AS s
        JOIN groups AS g ON g.id = s.group_id
        JOIN grades AS gr ON gr.student_id = s.id
        GROUP BY s.id, s.name, g.name
        HAVING MIN(gr.mark) = 2
        ORDER BY g.name, s.name, s.id
        """
    )
    return [dict(row) for row in cursor.fetchall()]
