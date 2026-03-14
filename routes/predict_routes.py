import json

from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user, login_required

from model import Prediction, db
from utils.disease_info import get_disease_info

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict")
@login_required
def predict_page():
    symptom_order = current_app.predictor.symptom_order
    return render_template("predict.html", symptom_order=symptom_order)


@predict_bp.route("/predict", methods=["POST"])
@login_required
def predict_submit():
    payload = request.get_json(silent=True) or {}
    symptoms = payload.get("symptoms", {})
    result = current_app.predictor.predict(symptoms)

    record = Prediction(
        user_id=current_user.id,
        symptoms=json.dumps(symptoms),
        predicted_disease=result["disease"],
        confidence=result["confidence"],
    )
    db.session.add(record)
    db.session.commit()

    disease_info = get_disease_info(result["disease"])
    response = {**result, **disease_info, "record_id": record.id}
    return jsonify(response)


@predict_bp.route("/result/<int:record_id>")
@login_required
def result_page(record_id: int):
    record = Prediction.query.filter_by(id=record_id, user_id=current_user.id).first_or_404()
    details = get_disease_info(record.predicted_disease)
    return render_template("result.html", record=record, details=details)
