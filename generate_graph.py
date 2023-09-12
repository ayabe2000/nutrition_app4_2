"""データベースにデータを追加し、そのデータを取得してグラフ化し、そのグラフをHTMLファイルに埋め込む"""
from sqlalchemy import create_engine, text
from flask import current_app as app

import matplotlib.pyplot as plt
import base64
from datetime import datetime, timedelta

foods = [
    {
        "name": "こむぎ",
        "protein_per_100g": 10.6,
        "carbs_per_100g": 72.2,
        "fat_per_100g": 10.6,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 337,
        "date": "2023-09-12"
    },
    {
        "name": "食パン",
        "protein_per_100g": 9.3,
        "carbs_per_100g": 46.7,
        "fat_per_100g": 4.4,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 264,
    },
    {
        "name": "うどん",
        "protein_per_100g": 6.1,
        "carbs_per_100g": 56,
        "fat_per_100g": 0.8,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 270,
    },
    {
        "name": "こめ",
        "protein_per_100g": 6.8,
        "carbs_per_100g": 74.3,
        "fat_per_100g": 2.7,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 353,
    },
    {
        "name": "いも",
        "protein_per_100g": 1.9,
        "carbs_per_100g": 14.7,
        "fat_per_100g": 0.4,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 35,
    },
    {
        "name": "あずき",
        "protein_per_100g": 20.3,
        "carbs_per_100g": 6.6,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 339,
    },
    {
        "name": "オクラ",
        "protein_per_100g": 2.1,
        "carbs_per_100g": 6.6,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 30,
    },
    {
        "name": "かぶ",
        "protein_per_100g": 2.3,
        "carbs_per_100g": 3.9,
        "fat_per_100g": 0.2,
        "cholesterol_per_100g": 1,
        "energy_kcal_100g": 30,
    }

]



def add_foods_to_db():
    engine = create_engine("sqlite:////root/nutrition_app4/nutrition_app4.db")
    connection = engine.connect()

    for food in foods:
        connection.execute(
            text("""
                INSERT INTO food (name,protein_per_100g, carbs_per_100g,cholesterol_per_100g,energy_kcal_100g,date)
                 VALUES (:name, :protein_per_100g, :carbs_per_100g, :fat_per_100g, :cholesterol_per_100g, :energy_kcal_100g, :date)
                 """),
                 **food
        )
    connection.close()

def fetch_data():
    """データベースから日付ごとの栄養素摂取量を取得"""
    engine = create_engine("sqlite:////root/nutrition_app4/nutrition_app4.db")
    

    connection = datetime.now()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=9)
    connection = engine.connect()
    result = connection.execute(
        text("SELECT date, SUM(protein_per_100g) as protein, SUM(energy_kcal_100g) as energy, SUM(fat_per_100g) as fat, SUM(cholesterol_per_100g) as cholesterol, SUM(carbs_per_100g) as carbohydrates FROM food WHERE date IS NOT NULL AND date BETWEEN :start_date AND :end_date GROUP BY date"),
        {'start_date': start_date.strftime('%Y-%m-%d'), 'end_date': end_date.strftime('%Y-%m-%d')}
    )
    

    dates = []
    protein = []
    energy = []
    fat = []
    cholesterol = []
    carbohydrates = []

    for row in result:

        date_str = row[0]
        if date_str:
            dates.append(datetime.strptime(date_str, '%Y-%m-%d'))     
        else:
            dates.append(None)


        protein.append(row[1])
        energy.append(row[2])
        fat.append(row[3])
        cholesterol.append(row[4]) 
        carbohydrates.append(row[5])  

    connection.close()




    return dates, protein, energy, fat, cholesterol, carbohydrates





def generate_graph(dates, protein, energy, fat, cholesterol, carbohydrates):
    """fetch_data関数から取得したデータを用いて栄養素摂取量の時間経過による変化を示すグラフを作成"""
    plt.figure()
    plt.plot(dates, protein, label="Protein (g)")
    plt.plot(dates, energy, label="Energy (kcal)")
    plt.plot(dates, fat, label="Fat (g)")
    plt.plot(dates, cholesterol, label="Cholesterol (mg)")
    plt.plot(dates, carbohydrates, label="Carbohydrates (g)")

    plt.title("Nutrient Intake Over Time")
    plt.xlabel("Date")
    plt.ylabel("Intake")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig("nutrient_intake.png")

    plt.show()


def get_base64_encoded_image(image_path):
    """画像をBase64でエンコードしHTMLに埋め込む"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def create_html(encoded_image):
    """Base64でエンコードされた画像データを用いて、HTMLファイルを作成し、画像を埋め込む"""
    html_str = f"""
    <html>
    <body>
    <img src="data:image/png;base64,{encoded_image}" alt="Nutrient Intake Graph">
    </body>
    </html>
    """

    with open("dashboard.html", "w") as html_file:
        html_file.write(html_str)


# main関数
def main():
    """fetch_data, generate_graph, get_base64_encoded_image,create_html関数を順番に呼び出し、プロセスを実行"""
    add_foods_to_db()
    dates, protein, energy, fat, cholesterol, carbohydrates = fetch_data()
    generate_graph(dates, protein, energy, fat, cholesterol, carbohydrates)

    encoded_image = get_base64_encoded_image("nutrient_intake.png")
    create_html(encoded_image)


if __name__ == "__main__":
    main()
