"""このモジュールはデータをインポートに関連する関数を含む"""

import pandas as pd
import logging
from app import db, create_app
from models import Food

logging.basicConfig(filename='import_food.log', level=logging.INFO)

def convert_to_float(value):
    """
    引数として受け取った値を浮動小数点数(float)に変換します。変換できない場合は0.0を返します。

    Args:
        value (int, float, str): 変換する値。整数、浮動小数点数、または数値を含む文字列が想定されます。

    Returns:
        float: 変換後の浮動小数点数。変換できない場合は0.0。
    """
    try:
        if isinstance(value, (int, float)):
            return float(value)
        return float(value.replace(',', ''))
    except ValueError:
        return 0.0


def process_row(row):
    """Excelのデータを処理するコード"""
    # 食品名
    food_name = row['食品名']
    # エネルギー（kcal）
    energy_val = convert_to_float(row['エネルギー（kcal）'])
    # たんぱく質
    protein_val = convert_to_float(row['たんぱく質'])
    # 脂質
    fat_val = convert_to_float(row['脂質'])
    # コレステロール
    cholesterol_val = convert_to_float(row['コレステロール'])
    # 炭水化物
    carbohydrates_val = convert_to_float(row['炭水化物'])

    if not Food.query.filter_by(name=food_name).first():
        new_food = Food(
            name=food_name,
            protein_per_100g=protein_val,
            carbs_per_100g=carbohydrates_val,
            fat_per_100g=fat_val, 
            cholesterol_per_100g=cholesterol_val, 
            energy_kcal_100g=energy_val  
        )
        db.session.add(new_food)
        db.session.commit()
        logging.info(f"Added food: {food_name}")


def import_food_data_from_excel(excel_path):
    """
    Excelファイルから食品データをインポートしてデータベースに追加。

    Args:
        excel_path (str): インポートするExcelファイルのパス。

    Returns:
        None
    """

    app = create_app()
    error_rows = []
    index = 0

    with app.app_context():
        try:
            data = pd.read_excel(excel_path, header=0)
            error_rows = []

            for index, row in data.iterrows():
                try:
                    process_row(row)
                except pd.errors.ParserError as parser_error:
                    logging.error(
                        f"An error occurred while processing the data: {parser_error}")  # 2. ログを出力
                except KeyError as key_error:
                    logging.error(f"Error at row {index + 1}: {key_error}")  # 2. ログを出力
                    error_rows.append(index + 1)

            db.session.commit()
        

        except ValueError as value_error:
            logging.error(f"An error occurred while reading the Excel data: {value_error}")  # 2. ログを出力




if __name__ == '__main__':
    app_instance = create_app()
    with app_instance.app_context():
        import_food_data_from_excel("/mnt/c/Users/user/Downloads/food_data.xlsx")
