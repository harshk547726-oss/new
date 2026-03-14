import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

DATASET_PATH = Path("dataset/disease_symptoms.csv")
MODEL_OUTPUT_PATH = Path("models/best_disease_model.pkl")


def train_and_save_model():
    df = pd.read_csv(DATASET_PATH)
    symptom_order = [column for column in df.columns if column != "disease"]
    X = df[symptom_order]
    y = df["disease"]

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    candidates = {
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "decision_tree": DecisionTreeClassifier(random_state=42),
        "naive_bayes": GaussianNB(),
    }

    best_name = None
    best_model = None
    best_score = -1

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))
        print(f"{name}: {score:.4f}")
        if score > best_score:
            best_name = name
            best_model = model
            best_score = score

    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_OUTPUT_PATH.open("wb") as file:
        pickle.dump(
            {
                "model": best_model,
                "label_encoder": encoder,
                "symptom_order": symptom_order,
                "best_model_name": best_name,
                "accuracy": best_score,
            },
            file,
        )

    print(f"Best model: {best_name} (accuracy={best_score:.4f})")
    print(f"Saved model to: {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    train_and_save_model()
