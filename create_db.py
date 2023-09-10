"""Flaskアプリケーションのデータベースを初期化(作成)"""
from app import app, db

with app.app_context():
    db.create_all()
