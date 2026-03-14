import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/disease_prediction"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = 604800
    MODEL_PATH = os.getenv("MODEL_PATH", "models/best_disease_model.pkl")
    MAIL_SENDER = os.getenv("MAIL_SENDER", "noreply@diseasepredictor.local")
