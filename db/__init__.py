from dotenv import dotenv_values
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="expert_system_fp",
    user=dotenv_values()["DB_USERNAME"],
    password=dotenv_values()["DB_PASSWORD"],
)


def init_db():
    try:
        cursor = conn.cursor()

        cases_seed = pd.read_csv("./db/seeds/cases.csv")
        labels_seed = pd.read_csv("./db/seeds/labels.csv")

        cursor.execute("DROP TABLE IF EXISTS labels CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS cases;")

        cursor.execute(
            "CREATE TABLE labels (id serial PRIMARY KEY,"
            "title VARCHAR(50) NOT NULL,"
            "description TEXT NOT NULL);"
        )

        cursor.execute(
            "CREATE TABLE cases (id serial PRIMARY KEY,"
            "text TEXT NOT NULL,"
            "label INTEGER REFERENCES labels(id) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
        )

        for _, row in labels_seed.iterrows():
            cursor.execute(
                "INSERT INTO labels (title, description)" "VALUES (%s, %s)",
                (row["title"], row["description"]),
            )

        for _, row in cases_seed.iterrows():
            cursor.execute(
                "INSERT INTO cases (text, label)" "VALUES (%s, %s)",
                (row["text"], row["label"]),
            )

        conn.commit()

        cursor.close()
        conn.close()

        return True

    except:
        return False
