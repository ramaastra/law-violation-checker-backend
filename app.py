from db import init_db, get_connection
from model import train_knn, predict_case

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


test_text = [
    "Kamu orangnya baik banget!",
    "Kamu orangnya BANGSAT banget!",
    "mati aja lo sana",
    "pemerintah ngentot",
    "Babi den",
    "Bupati orang bodoh",
]

print("======================================================\n")
for text in test_text:
    label, desc, proba = predict_case(text)
    print(text)
    print("> Label:", label)
    print("> Description:", desc)
    print("> Probability:", proba)
    print("\n======================================================\n")
