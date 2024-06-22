from db import init_db, get_connection
from model import train_knn

if init_db():
    print("Database initialized.")
else:
    print("Something was wrong in database initialization.")

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT text, label FROM cases;")
data = cursor.fetchall()

cases = {"text": [], "label": []}
for text, label in data:
    cases["text"].append(text)
    cases["label"].append(label)

train_knn(cases)


cursor.close()
conn.close()
