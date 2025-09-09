import os
from pathlib import Path

basedir = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + str(basedir / "app.db")
    )