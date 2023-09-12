import unittest
from generate_graph import fetch_data
from sqlalchemy import create_engine,text


class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # テストデータをデータベースに挿入
        engine = create_engine("sqlite:///nutrition_app4.db")
        connection = engine.connect()
        
        # テストデータの情報
        food_name = "新しいテスト食品"  # 名前を一意のものに変更
        protein_per_100g = 10.0
        carbs_per_100g = 20.0
        fat_per_100g = 5.0
        cholesterol_per_100g = 0.0
        energy_kcal_100g = 150.0
        date = "2023-09-11"  # テストデータを追加する日付

        # SQLクエリを作成
        insert_query = text("""
            INSERT INTO food (name, protein_per_100g, carbs_per_100g, fat_per_100g, cholesterol_per_100g, energy_kcal_100g, date)
            VALUES (:food_name, :protein_per_100g, :carbs_per_100g, :fat_per_100g, :cholesterol_per_100g, :energy_kcal_100g, :date)
        """)

        # データを挿入
        connection.execute(insert_query, {
            "food_name": food_name,
            "protein_per_100g": protein_per_100g,
            "carbs_per_100g": carbs_per_100g,
            "fat_per_100g": fat_per_100g,
            "cholesterol_per_100g": cholesterol_per_100g,
            "energy_kcal_100g": energy_kcal_100g,
            "date": date
        })

        connection.close()

    def test_fetch_data(self):
        dates, protein, energy, fat, cholesterol, carbohydrates = fetch_data()
        
        # 期待されるデータのタイプを検証します
        self.assertIsInstance(dates, list)
        self.assertIsInstance(protein, list)
        self.assertIsInstance(energy, list)
        self.assertIsInstance(fat, list)
        self.assertIsInstance(cholesterol, list)
        self.assertIsInstance(carbohydrates, list)
        
        # リストが空でないことを検証します（データが正常にフェッチされた場合）
        self.assertTrue(dates)
        self.assertTrue(protein)
        self.assertTrue(energy)
        self.assertTrue(fat)
        self.assertTrue(cholesterol)
        self.assertTrue(carbohydrates)



if __name__ == '__main__':
    unittest.main()
