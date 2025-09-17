import os
from flask import Flask
from flask_migrate import Migrate
from .models import db  # importa tus modelos

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    Migrate(app, db)
    return app

app = create_app()
