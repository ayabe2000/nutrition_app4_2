"""このモジュールはユーザー、パスワード、フードエントリー、フード、日別の栄養素のテーブルを含む"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class User(db.Model, UserMixin):
    """ユーザ情報を格納するテーブル。Flask-LoginのUserMixinを継承しており、ユーザ認証に関する機能を提供"""
    __tablename__ = 'user'  # テーブル名をuserとして指定

    # データベースのカラム定義
    id = db.Column(db.Integer, primary_key=True)  # idという名前のカラム
    username = db.Column(db.String(100), unique=True,nullable=False)  # ユーザー名を保存するカラム

    # ユーザーのパスワードハッシュを保存するカラム
    password_hash = db.Column(db.String(128), nullable=False)
    daily_nutrients = db.relationship(
        'DailyNutrient', back_populates='user', lazy='dynamic')
    food_entries = db.relationship('FoodEntry', backref='user', lazy='dynamic')
    # レコードが作成された日時と更新された日時を保存するためのカラム。
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)  # ユーザーが削除されたかどうかを示すブール値

    def set_password(self, password):
        """ユーザーのパスワードをハッシュ化して保存"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ハッシュ化されたパスワードをチェックするためのメソッド"""
        return check_password_hash(self.password_hash, password)

# pylint: disable=too-few-public-methods


class FoodEntry(db.Model):
    """食品エントリ情報を格納するテーブル"""
    __tablename__ = 'food_entry'

# 各属性はデータベースのカラム定義
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_name = db.Column(db.String(255), nullable=False)
    grams = db.Column(db.Float, nullable=False, default=0.0)
    protein = db.Column(db.Float, nullable=False, default=0)
    fat = db.Column(db.Float, nullable=False, default=0)
    cholesterol = db.Column(db.Float, nullable=False, default=0)
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    energy_kcal = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    food_id = db.Column(db.Integer, db.ForeignKey(
        'food.id'))  # foodテーブルとの関連を示す外部キー。
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow)  # レコードが作成された日時
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )  # レコードが作成された日時
    # このエントリーが削除されているかどうかのフラグ。
    is_deleted = db.Column(db.Boolean, default=False)

    # FoodEntryオブジェクトを文字列として表現する際のフォーマットを定義
    def __repr__(self):  # __repr__は、Pythonオブジェクトを文字列として表現する際に使用される特殊メソッド

        return f"<FoodEntry {self.food_name}>"
    

class Food(db.Model):
    """各食品の情報を格納するカラムを定義し食品情報をデータベース内で効果的に管理"""
    __tablename__ = 'food'  # テーブル名を指定
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # name: 食品の名前を格納するカラム
    protein_per_100g= db.Column(db.Float)  # 1gあたりのタンパク質の量を格納するカラム
    carbs_per_100g = db.Column(db.Float)  # 炭水化物
    fat_per_100g = db.Column(db.Float)  # 脂質
    cholesterol_per_100g = db.Column(db.Float)  # コレステロール
    energy_kcal_100g = db.Column(db.Float)  # エネルギー
    variant = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    is_deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    

# pylint: disable=too-few-public-methods
class DailyNutrient(db.Model):
    """日別栄養素情報を格納するテーブル"""
    __tablename__ = 'daily_nutrient'
    __table_args__ = (db.UniqueConstraint(
        'date', 'user_id'), {'extend_existing': True})

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_protein = db.Column(db.Float)
    total_carbs = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    user = db.relationship('User', back_populates='daily_nutrients')
    date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
