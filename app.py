from flask import Flask, request, Response
from flask_cors import CORS
from db import init_db
from model import train_knn, predict_case
from controller import label as label_controller
from controller import case as case_controller

app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return "Server connected"


@app.route("/init-db")
def init():
    if init_db():
        return "Database initialized successfully"
    else:
        return "Database initialization error"


@app.route("/model/train", methods=["POST"])
def train():
    if request.method == "POST":
        try:
            train_knn()
            return "KNN model created successfully"
        except:
            return "Model training failed"


@app.route("/model/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        request_body = request.get_json()
        text = request_body.get("text")

        if not text:
            return "Field 'text' is required", 400

        label, description, probability = predict_case(text)
        return {
            "text": text,
            "prediction": {
                "label": label,
                "description": description,
                "probability": probability,
            },
        }


@app.route("/labels", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        labels = label_controller.get_all()
        return labels
    elif request.method == "POST":
        request_body = request.get_json()
        title = request_body.get("title")
        description = request_body.get("description")

        if not title or not description:
            return "Field 'title' and 'description' are required", 400

        id, title, description = label_controller.create(title, description)
        return {"id": id, "title": title, "description": description}


@app.route("/cases")
def handle_request():
    if request.method == "GET":
        cases = case_controller.get_all()
        return cases


if __name__ == "__main__":
    app.run(debug=True)
