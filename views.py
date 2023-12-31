"""FlaskやDjangoといったPythonのウェブフレームワークにおいて、ウェブアプリケーションの"ビュー"層を定義"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user
from forms import LoginForm, RegistrationForm, FoodEntryForm, EditGramsForm
from models import (
    User,
    FoodEntry,
    Food,
    DailyNutrient,
    db,
    get_food_by_name,
    create_new_food_entry,
)
from utils import get_available_foods
from models import create_new_food_entry


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    """indexのルート関数"""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login_page"))


@main_blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    """roginのルート関数"""
    login_form = LoginForm()
    register_form = RegistrationForm()

    if request.method == "POST":
        if "submit_login" in request.form:
            if login_form.validate_on_submit():
                user = User.query.filter_by(username=login_form.username.data).first()
                if user:
                    if user and user.check_password(login_form.password.data):
                        login_user(user)
                        return redirect(url_for("main.dashboard"))
        elif "submit_register" in request.form:
            if register_form.validate_on_submit():
                existing_user = User.query.filter_by(
                    username=register_form.new_username.data
                ).first()
                if existing_user:
                    return render_template(
                        "login.html",
                        login_form=login_form,
                        register_form=register_form,
                        message="Username already exists.",
                    )

                new_user = User(username=register_form.new_username.data)
                new_user.set_password(register_form.new_password.data)

                db.session.add(new_user)
                db.session.commit()

                login_user(new_user)
                return redirect(url_for("main.dashboard"))
    return render_template(
        "login.html", login_form=login_form, register_form=register_form
    )


@main_blueprint.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """フォームデータの取得と処理"""
    form = FoodEntryForm()
    available_foods = get_available_foods()
    nutrients_data_today = None
    selected_date = form.date.data

    form.name.choices = [(food, food) for food in available_foods]

    if form.validate_on_submit() and current_user.is_authenticated:
        selected_date = form.date.data
        nutrients_data_today = handle_form_submission(form)

    all_entries = FoodEntry.query.order_by(FoodEntry.date.desc()).all()
    nutrients_data = compute_nutrients(all_entries)
    entries = group_entries_by_date(all_entries)

    available_foods = get_available_foods()
    form.name.choices = available_foods

    return render_template(
        "dashboard.html",
        form=form,
        nutrients_data_today=nutrients_data_today,
        nutrients_data=nutrients_data,
        entries=entries,
        available_foods=available_foods,
        selected_date=selected_date,
    )


def handle_form_submission(form):
    """食品データベースから食品の取得"""
    food_name = form.name.data
    print("food_name:", food_name)
    grams = form.grams.data
    selected_date = form.date.data

    food = Food.query.filter(Food.name == food_name).first()
    print("food:", food)

    if food:
        user_id = current_user.id
        selected_date = form.date.data
        new_entry = create_new_food_entry(
            food, food_name, grams, user_id, selected_date
        )

        db.session.add(new_entry)
        db.session.commit()

        today = datetime.utcnow().date()
        nutrients_data_today = get_nutrients_data_today(today)

        update_daily_nutrient(user_id, nutrients_data_today, selected_date)

        return nutrients_data_today

    return {"error": "Food not found in the database"}


def get_nutrients_data_today(today):
    """今日の栄養データの計算"""
    end_of_today = today + timedelta(days=1) - timedelta(seconds=1)
    today_entries = FoodEntry.query.filter(
        FoodEntry.date.between(today, end_of_today)
    ).all()
    return compute_nutrients(today_entries)


def update_daily_nutrient(user_id, nutrients_data_today, selected_date):
    """デイリーナットリエントの作成/更新"""
    daily_nutrient = DailyNutrient.query.filter_by(
        user_id=user_id, date=selected_date
    ).first()
    if not daily_nutrient:
        daily_nutrient = DailyNutrient(date=selected_date, user_id=user_id)
        db.session.add(daily_nutrient)

    daily_nutrient.total_protein = nutrients_data_today["Protein"]
    daily_nutrient.total_carbs = nutrients_data_today["Carbohydrates"]
    daily_nutrient.total_fat = nutrients_data_today["Fat"]

    db.session.commit()


def compute_nutrients(entries, debug_mode=False):
    """全エントリーの取得と栄養データの計算"""
    nutrients_data = {
        "Protein": 0,
        "Carbohydrates": 0,
        "Fat": 0,
        "Cholesterol": 0,
        "Energy_kcal": 0,
    }

    for entry in entries:
        if isinstance(entry, FoodEntry):
            entry_dict = {
                "protein": entry.protein,
                "carbohydrates": entry.carbohydrates,
                "fat": entry.fat,
                "cholesterol": entry.cholesterol,
                "energy_kcal": entry.energy_kcal,
            }
            required_keys = [
                "protein",
                "carbohydrates",
                "fat",
                "cholesterol",
                "energy_kcal",
            ]
        elif isinstance(entry, dict):
            entry_dict = entry
            required_keys = [
                "protein",
                "carbohydrates",
                "fat",
                "cholesterol",
                "energy_kcal",
            ]
        else:
            raise ValueError("Invalid entry format detected.")

        if not all(key in entry_dict for key in required_keys):
            raise ValueError("Invalid entry format detected.")

        if debug_mode:
            print("Entry:", entry_dict)

        nutrients_data["Protein"] += entry_dict["protein"]
        nutrients_data["Carbohydrates"] += entry_dict["carbohydrates"]
        nutrients_data["Fat"] += entry_dict["fat"]
        nutrients_data["Cholesterol"] += entry_dict["cholesterol"]
        nutrients_data["Energy_kcal"] += entry_dict["energy_kcal"]

    if debug_mode:
        print("Nutrients Data:", nutrients_data)

    return nutrients_data


def group_entries_by_date(all_entries):
    """グループ化されたエントリーの作成"""
    grouped_entries = {}
    for entry in all_entries:
        date_str = entry.date.strftime("%Y-%m-%d")
        if date_str not in grouped_entries:
            if len(grouped_entries) >= 10:  # 10日分のデータのみ保持
                oldest_entry_key = list(grouped_entries.keys())[0]  # 最も古いエントリのキーを取得
                grouped_entries.pop(oldest_entry_key)  # 最も古いエントリを削除
            grouped_entries[date_str] = {
                "kcal": 0,
                "protein": 0,
                "fat": 0,
                "cholesterol": 0,
                "carbs": 0,
                "foods": [],
            }

        grouped_entries[date_str]["kcal"] += entry.energy_kcal
        grouped_entries[date_str]["protein"] += entry.protein
        grouped_entries[date_str]["fat"] += entry.fat
        grouped_entries[date_str]["cholesterol"] += entry.cholesterol
        grouped_entries[date_str]["carbs"] += entry.carbohydrates
        grouped_entries[date_str]["foods"].append(entry)

    entries = []
    for date_str, data in grouped_entries.items():
        entries.append(
            {
                "date": date_str,
                "kcal": f"{data['kcal']} kcal",
                "protein": f"{data['protein']} g",
                "fat": f"{data['fat']} g",
                "cholesterol": f"{data['cholesterol']} mg",
                "carbs": f"{data['carbs']} g",
                "foods": data["foods"],
            }
        )
    return entries


@main_blueprint.route("/edit_food/<int:id>", methods=["GET", "POST"])
def edit_food(id):
    """食品エントリの編集"""
    entry = FoodEntry.query.get(id)
    form = EditGramsForm()
    print("Entry:", entry)

    if request.method == "POST":
        new_grams = request.form.get("grams")
        if new_grams:
            entry.grams = new_grams
            db.session.commit()
            return redirect(url_for("main.dashboard"))
        else:
            error_message = "新しいグラム数を入力してください"
    else:
        error_message = ""

    print("Entry object before render_template:", entry)
    return render_template(
        "edit_food.html", entry=entry, error_message=error_message, form=form
    )


@main_blueprint.route("/delete_food/<int:id>", methods=["POST"])
def delete_food(id):
    """食品エントリの削除"""
    entry = FoodEntry.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("エントリが正常に削除されました", "success")
    else:
        flash("エントリが見つかりません", "error")
    return redirect(url_for("main.dashboard"))
