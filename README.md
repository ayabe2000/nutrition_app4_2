# Nutrition App

このプロジェクトは栄養素情報を管理するためのアプリケーションです。

## 動作環境

このプロジェクトを実行するためには以下の環境が必要です：

- Python 3.10.12
- Flask 2.3.3
- Werkzeug 2.3.7

## インストールとセットアップ

プロジェクトのセットアップ手順を詳細に説明します。以下は一般的な手順の例です。

1. プロジェクトのクローン

   ```bash
   git clone https://github.com/ayabe2000/nutrition_app4
   cd nutrition_app4

2,仮想環境の作成とアクティベーション

    python -m venv venv
    source venv/bin/activate

3,依存ライブラリのインストール

    pip install -r requirements.txt

4,データベースのセットアップ

    flask db init
    flask db migrate
    flask db upgrade

5,サーバーの起動

    flask run

## DBの栄養素情報の登録方法

このプロジェクトでは、栄養素情報をデータベースに登録するために以下の手順を使用します。栄養素情報は通常、Excelファイルから取り込むことが一般的です。

1. Excelファイルの準備:
   
   - 栄養素情報を含むExcelファイルを用意します。
   - Excelファイルのカラムには、必要な栄養素情報（食品名、カロリー、たんぱく質、脂質、炭水化物）が含まれている必要があります。

2. データの取り込み:

   - プロジェクトのルートディレクトリに移動し、仮想環境をアクティベートします。

     source venv/bin/activate


   - 以下のコマンドを使用して、Excelファイルからデータをデータベースに取り込みます。ファイル名やパスは実際のファイルに合わせて変更してください。

     flask import-nutrition-data /mnt/c/Users/user/Downloads/food_data.xlsx

   - データの取り込みが完了すると、栄養素情報がデータベースに登録されます。

これで、Excelファイルから栄養素情報をデータベースに効率的に登録できます。

 