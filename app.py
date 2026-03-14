from flask import Flask
from flask_login import LoginManager

from config import Config
from model import User, db
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.predict_routes import predict_bp
from utils.predictor import DiseasePredictor


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.predictor = DiseasePredictor(app.config["MODEL_PATH"])
    app.predictor.load()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(predict_bp)

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        print("Database initialized")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
