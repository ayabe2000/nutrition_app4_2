from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/nutrition_app4/nutrition_app4.db'  # 実際のデータベースURIに変更する
db = SQLAlchemy(app)
