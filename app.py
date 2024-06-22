from flask import Flask
from db import init_db
from controller import label as label_controller

app = Flask(__name__)


@app.route("/")
def root():
    return "Server connected"


@app.route("/init-db")
def init():
    if init_db():
        return "Database initialized successfully"
    else:
        return "Database initialization error"


@app.route("/labels")
def get_all():
    labels = label_controller.get_all()
    return labels


if __name__ == "__main__":
    app.run(debug=True)
