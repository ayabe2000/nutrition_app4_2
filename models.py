"""このモジュールはユーザー、パスワード、フードエントリー、フード、日別の栄養素のテーブルを含む"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from extensions import db


db = SQLAlchemy()


class User(db.Model, UserMixin):
    """ユーザ情報を格納するテーブル。Flask-LoginのUserMixinを継承しており、ユーザ認証に関する機能を提供"""

    __tablename__ = "user"  # テーブル名をuserとして指定

    # データベースのカラム定義
    id = db.Column(db.Integer, primary_key=True)  # idという名前のカラム
    username = db.Column(db.String(100), unique=True, nullable=False)  # ユーザー名を保存するカラム

    # ユーザーのパスワードハッシュを保存するカラム
    password_hash = db.Column(db.String(128), nullable=False)
    daily_nutrients = db.relationship(
        "DailyNutrient", back_populates="user", lazy="dynamic"
    )
    food_entries = db.relationship("FoodEntry", backref="user", lazy="dynamic")
    # レコードが作成された日時と更新された日時を保存するためのカラム。
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
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

    __tablename__ = "food_entry"

    # 各属性はデータベースのカラム定義
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    food_name = db.Column(db.String(255), nullable=False)
    grams = db.Column(db.Float, nullable=False, default=0.0)
    protein = db.Column(db.Float, nullable=False, default=0)
    fat = db.Column(db.Float, nullable=False, default=0)
    cholesterol = db.Column(db.Float, nullable=False, default=0)
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    energy_kcal = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"))  # foodテーブルとの関連を示す外部キー。
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # レコードが作成された日時
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # レコードが作成された日時
    # このエントリーが削除されているかどうかのフラグ。
    is_deleted = db.Column(db.Boolean, default=False)

    # FoodEntryオブジェクトを文字列として表現する際のフォーマットを定義
    def __repr__(self):  # __repr__は、Pythonオブジェクトを文字列として表現する際に使用される特殊メソッド
        return f"<FoodEntry {self.food_name}>"


class Food(db.Model):
    """各食品の情報を格納するカラムを定義し食品情報をデータベース内で効果的に管理"""

    __tablename__ = "food"  # テーブル名を指定
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # name: 食品の名前を格納するカラム
    protein_per_100g = db.Column(db.Float)  # 1gあたりのタンパク質の量を格納するカラム
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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


# pylint: disable=too-few-public-methods
class DailyNutrient(db.Model):
    """日別栄養素情報を格納するテーブル"""

    __tablename__ = "daily_nutrient"
    __table_args__ = (db.UniqueConstraint("date", "user_id"), {"extend_existing": True})

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_protein = db.Column(db.Float)
    total_carbs = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    user = db.relationship("User", back_populates="daily_nutrients")
    date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_deleted = db.Column(db.Boolean, default=False)


def get_food_by_name(food_name):
    """名前を使って食品情報を取得する"""

    food = Food.query.filter_by(name=food_name).first()

    if food:
        return food
    else:
        return None
def get_nutrition_data(user_id, date):
    daily_nutrient = DailyNutrient.query.filter_by(user_id=user_id, date=date).first()

    if daily_nutrient:
        return {
            "total_protein":daily_nutrient.total_protein,
            "total_carbs":daily_nutrient.total_carbs,
            "total_fat":daily_nutrient.total_fat,
            "total_energy_kcal":daily_nutrient.total_energy_kcal,
            "total_cholesterol":daily_nutrient.total_cholesterol,

        }
    else:
        return None


def create_new_food_entry(food, food_name, grams, user_id, selected_date):
    """新しい食品エントリの作成と追加"""
   
    food = get_food_by_name(food_name) 


    food = get_food_by_name(food_name)  # この関数はfoodオブジェクトを取得するための実際の関数名であるべきです


    if not food or food.protein_per_100g is None:
        
        return
    

    print(f"Protein per 100g: {food.protein_per_100g}")
    print(f"Carbs per 100g: {food.carbs_per_100g}")
    print(f"Fat per 100g: {food.fat_per_100g}")
    print(f"Cholesterol per 100g: {food.cholesterol_per_100g}")
    print(f"Energy per 100g: {food.energy_kcal_100g}")

    
    
    protein_per_serving = (food.protein_per_100g * grams) / 100
    carbs_per_serving = (food.carbs_per_100g * grams) / 100
    fat_per_serving = (food.fat_per_100g * grams) / 100
    cholesterol_per_serving = (food.cholesterol_per_100g * grams) / 100
    energy_per_serving = (food.energy_kcal_100g * grams) / 100


    print(f"Protein per serving: {protein_per_serving}")
    print(f"Carbs per serving: {carbs_per_serving}")
    print(f"Fat per serving: {fat_per_serving}")
    print(f"Cholesterol per serving: {cholesterol_per_serving}")
    print(f"Energy per serving: {energy_per_serving}")


    protein = food.protein_per_100g * (grams / 100)
    carbohydrates = food.carbs_per_100g * (grams / 100)
    fat = food.fat_per_100g * (grams / 100)
    cholesterol = food.cholesterol_per_100g * (grams / 100)
    energy_kcal = food.energy_kcal_100g * (grams / 100)



    return FoodEntry(
        user_id=user_id,
        food_name=food_name,
        grams=grams,

        protein=protein_per_serving, 
        carbohydrates=carbs_per_serving, 
        fat=fat_per_serving,
        cholesterol=cholesterol_per_serving, 
        energy_kcal=energy_per_serving, 
        date=selected_date,
    )


  
     
