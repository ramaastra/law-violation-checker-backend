from db import get_connection


def format_tuples(keys, list_of_tuples):
    list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    return list_of_dict


class label:
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM labels")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        labels = format_tuples(("id", "title", "description"), data)
        return labels

    def get_detail(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, description FROM labels WHERE id=%s;", [id])
        detail = cursor.fetchone()
        cursor.close()
        conn.close()

        return detail


class case:
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        labels = format_tuples(("id", "text", "label", "created_at"), data)
        return labels
