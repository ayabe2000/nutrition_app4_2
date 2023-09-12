from sqlalchemy import create_engine, text

# テストデータの名前
food_name_to_delete = "テスト食品"

# データベースに接続
engine = create_engine("sqlite:///nutrition_app4.db")
connection = engine.connect()

# テストデータを削除するためのSQL削除クエリを作成
delete_query = text("DELETE FROM food WHERE name = :food_name")

# テストデータを削除
connection.execute(delete_query, {"food_name": food_name_to_delete})

# データベース接続を閉じる
connection.close()
