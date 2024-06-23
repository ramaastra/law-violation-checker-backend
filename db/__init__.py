from dotenv import dotenv_values
from urllib.parse import urlparse
import pandas as pd
import psycopg2


def get_connection():
    if dotenv_values()["DATABASE_URL"]:
        db_uri = urlparse(dotenv_values()["DATABASE_URL"])
        username = db_uri.username
        password = db_uri.password
        database = db_uri.path[1:]
        hostname = db_uri.hostname
        port = db_uri.port

        conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port,
        )
        return conn

    else:
        conn = psycopg2.connect(
            host="localhost",
            database="expert_system_fp",
            user=dotenv_values()["DB_USERNAME"],
            password=dotenv_values()["DB_PASSWORD"],
        )
        return conn


def init_db():
    try:
        conn = get_connection()
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

        print("> Creating seed data for labels...")
        for _, row in labels_seed.iterrows():
            cursor.execute(
                "INSERT INTO labels (title, description)" "VALUES (%s, %s)",
                (row["title"], row["description"]),
            )

        print("> Creating seed data for cases...")
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
