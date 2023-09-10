"""Flaskアプリケーションの初期設定とデータベースの設定"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////root/nutrition_app4/nutrition_app4.db"
db = SQLAlchemy(app)
