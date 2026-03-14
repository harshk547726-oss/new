import pickle
from pathlib import Path

import numpy as np


class DiseasePredictor:
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model_package = None

    def load(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. Run `python train_model.py` first."
            )
        with self.model_path.open("rb") as file:
            self.model_package = pickle.load(file)

    @property
    def symptom_order(self):
        return self.model_package["symptom_order"]

    def predict(self, symptom_values: dict):
        if self.model_package is None:
            self.load()

        feature_vector = [int(bool(symptom_values.get(symptom, 0))) for symptom in self.symptom_order]
        X = np.array([feature_vector])
        model = self.model_package["model"]
        label_encoder = self.model_package["label_encoder"]

        predicted_idx = model.predict(X)[0]
        disease = label_encoder.inverse_transform([predicted_idx])[0]

        if hasattr(model, "predict_proba"):
            confidence = float(np.max(model.predict_proba(X)))
        else:
            confidence = 0.75

        return {
            "disease": disease,
            "confidence": round(confidence * 100, 2),
            "vector": feature_vector,
        }
