import preprocess
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from controller import label as label_controller


def preprocess_data(text):
    clean_text = str.lower(text)
    clean_text = preprocess.remove_newlines(clean_text)
    clean_text = preprocess.remove_unicodes(clean_text)
    clean_text = preprocess.replace_colloquials(clean_text)
    clean_text = preprocess.remove_stopwords(clean_text)
    clean_text = preprocess.remove_non_alphanums(clean_text)
    clean_text = preprocess.remove_twitter_placeholders(clean_text)
    clean_text = preprocess.remove_extra_spaces(clean_text)

    return clean_text.strip()


def train_knn(data):
    texts = data.get("text")
    labels = data.get("label")

    tfidf_vectorizer = TfidfVectorizer()
    tdm = tfidf_vectorizer.fit_transform(texts)

    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(tdm, labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

    print("\n> Creating KNN model.")

    k_values = [k for k in range(1, 6)]
    scores = []

    for k in k_values:
        print(f"  > Searching best value of k (current k={k})...")
        knn = KNeighborsClassifier(n_neighbors=k, metric="euclidean")
        score = cross_val_score(knn, X, y, cv=3)
        scores.append(np.mean(score))

    best_index = np.argmax(scores)
    best_k = k_values[best_index]

    knn = KNeighborsClassifier(n_neighbors=best_k, metric="euclidean")
    knn.fit(X_train, y_train)

    print(f"\n> KNN model created with k={best_k}.")

    y_pred = knn.predict(X_test)
    print("\n", classification_report(y_test, y_pred))

    joblib.dump(knn, "./model/trained_models/knn.pkl")
    joblib.dump(tfidf_vectorizer, "./model/trained_models/vectorizer.pkl")

    print("\n> Model saved in model/trained_models/knn.pkl")
    print("> Vectorizer saved in model/trained_models/vectorizer.pkl")


def predict_case(text):
    model = joblib.load("./model/trained_models/knn.pkl")
    vectorizer = joblib.load("./model/trained_models/vectorizer.pkl")

    text = preprocess_data(text)
    x = vectorizer.transform([text])
    pred = model.predict_proba(x)[0]
    y_index = np.argmax(pred)

    label, description = label_controller.get_detail(y_index.item() + 1)
    probability = pred[y_index] * 100

    return (label, description, probability)
