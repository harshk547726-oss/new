# Disease Prediction System (Flask + MySQL + ML)

Production-ready full-stack web app for symptom-based disease prediction.

## Features
- User registration/login (Flask-Login, hashed passwords)
- Forgot password via reset token flow
- Dashboard with prediction trend charts (Chart.js)
- Symptom search + AJAX prediction flow
- Prediction result insights (description, precautions, medications, doctor suggestion)
- Contact form stored in DB
- Prediction history and profile management
- Admin dashboard for aggregate analytics
- Dark mode toggle
- Model training pipeline compares Random Forest, Decision Tree, Naive Bayes

## Project Structure
```
project/
  app.py
  config.py
  model.py
  train_model.py
  requirements.txt
  database_schema.sql
  dataset/disease_symptoms.csv
  models/
  routes/
  utils/
  static/
    css/style.css
    js/app.js
    js/predict.js
  templates/
```

## Setup
1. Create virtualenv and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create MySQL database:
```sql
CREATE DATABASE disease_prediction;
```

3. Configure DB connection:
```bash
export DATABASE_URL="mysql+pymysql://<user>:<password>@localhost:3306/disease_prediction"
export SECRET_KEY="<your-secret>"
```

4. Train model:
```bash
python train_model.py
```

5. Run app:
```bash
python app.py
```

6. Open in browser:
`http://127.0.0.1:5000`

## Deployment Notes (Render/Heroku)
- Set environment vars: `DATABASE_URL`, `SECRET_KEY`, `MODEL_PATH`.
- Add Procfile:
```bash
web: gunicorn app:application
```
- Ensure model is trained in build/release phase (or committed model artifact).

## Helpful Commands
- Train model: `python train_model.py`
- Start server: `python app.py`
- Initialize DB tables: `flask --app app:create_app init-db`
