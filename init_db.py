

from app import create_app, db
from models import Food

app = create_app()
app.app_context().push()

foods = [
    {"name": "こむぎ", "protein_per_100g": 10.6, "carbs_per_100g": 72.2, "fat_per_100g": 10.6, "cholesterol_per_100g": 1, "energy_kcal_100g": 337},
    {"name": "食パン", "protein_per_100g": 9.3, "carbs_per_100g": 46.7, "fat_per_100g": 4.4, "cholesterol_per_100g": 1, "energy_kcal_100g": 264},
    {"name": "うどん", "protein_per_100g": 6.1, "carbs_per_100g": 56, "fat_per_100g": 0.8, "cholesterol_per_100g": 1, "energy_kcal_100g": 270},
    {"name": "こめ", "protein_per_100g": 6.8, "carbs_per_100g": 74.3, "fat_per_100g": 2.7, "cholesterol_per_100g": 1, "energy_kcal_100g": 353},
    {"name": "いも", "protein_per_100g": 1.9, "carbs_per_100g": 14.7, "fat_per_100g": 0.4, "cholesterol_per_100g": 1, "energy_kcal_100g": 35},
    {"name": "あずき", "protein_per_100g": 20.3, "carbs_per_100g": 6.6, "fat_per_100g": 0.2, "cholesterol_per_100g": 1, "energy_kcal_100g": 339},
    {"name": "オクラ", "protein_per_100g": 2.1, "carbs_per_100g": 6.6, "fat_per_100g": 0.2, "cholesterol_per_100g": 1, "energy_kcal_100g": 30},
    {"name": "かぶ", "protein_per_100g": 2.3, "carbs_per_100g": 3.9, "fat_per_100g": 0.2, "cholesterol_per_100g": 1, "energy_kcal_100g": 30},
]

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        for food_data in foods:
            existing_food = Food.query.filter_by(name=food_data['name']).first()
            if existing_food is None:
                food = Food(**food_data)
                db.session.add(food)
            else:
                print(f"Food item '{food_data['name']}' already exists in the database.")
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while inserting the data: {e}")

