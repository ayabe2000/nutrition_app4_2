from models import Food  # データベースとFoodモデルをインポート
from app import app,db

with app.app_context():

    # SQLAlchemyを使用して全ての食品データを取得
    foods = Food.query.all()

    for food in foods:
        # 栄養素の値を正しいものに修正
        food.protein_per_100g = food.protein_per_100g * 100 if food.protein_per_100g <= 1 else food.protein_per_100g
        food.carbs_per_100g = food.carbs_per_100g * 100 if food.carbs_per_100g <= 1 else food.carbs_per_100g
        food.fat_per_100g = food.fat_per_100g * 100 if food.fat_per_100g <= 1 else food.fat_per_100g
        food.cholesterol_per_100g = food.cholesterol_per_100g * 100 if food.cholesterol_per_100g <= 1 else food.cholesterol_per_100g
        food.energy_kcal_100g = food.energy_kcal_100g * 100 if food.energy_kcal_100g <= 1 else food.energy_kcal_100g

        db.session.commit()

        foods = Food.query.all()
        for food in foods:
            print(f"Food ID: {food.id}, Protein: {food.protein_per_100g}, Carbs: {food.carbs_per_100g}, Fat: {food.fat_per_100g}, Cholesterol: {food.cholesterol_per_100g}, Energy: {food.energy_kcal_100g}")


        