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

    def create(title, description):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO labels (title, description)"
            "VALUES (%s, %s) RETURNING id, title, description",
            (title, description),
        )
        label = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return label


class case:
    def get_all(request, page, items_per_page):
        page = int(page)
        items_per_page = int(items_per_page)

        if not page:
            page = 1
        if not items_per_page:
            items_per_page = 10

        next_url = None
        prev_url = None
        offset = (page - 1) * items_per_page

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(id) FROM cases;")
        count = cursor.fetchone()[0]
        print(count)

        cursor.execute(
            "SELECT * FROM cases LIMIT %s OFFSET %s", [items_per_page, offset]
        )
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        labels = format_tuples(("id", "text", "label", "created_at"), data)
        if count - page * items_per_page > 0:
            next_url = f"{request.base_url}?page={page+1}&limit={items_per_page}"
        if page - 1 > 0:
            prev_url = f"{request.base_url}?page={page-1}&limit={items_per_page}"

        return {
            "labels": labels,
            "pagination": {"next": next_url, "prev": prev_url, "total": count},
        }

    def create(text, label):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM labels WHERE id=%s;", [label])
        is_label_exist = cursor.fetchone()

        if not is_label_exist:
            return False

        cursor.execute(
            "INSERT INTO cases (text, label)"
            "VALUES (%s, %s) RETURNING id, text, label, created_at",
            (text, label),
        )
        case = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return case
