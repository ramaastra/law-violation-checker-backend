from db import get_connection


class label:
    def get_detail(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, description FROM labels WHERE id=%s;", [id])
        detail = cursor.fetchone()
        cursor.close()
        conn.close()

        return detail
