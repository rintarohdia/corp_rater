from flask import Flask, request,jsonify, Response

import joblib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import numpy as np
import pandas as pd
import io
import csv
import json

app = Flask(__name__)

# 保存された正規化モデルを読み込む
scaler = joblib.load('scaler.pkl')

# 保存されたPCAモデルを読み込む
pca_model = joblib.load('pca_model100.pkl')

model = lgb.Booster(model_file='lgbmodel')

@app.route('/predict/', methods=['POST'])
def predict():
    file = request.files['file']
    # ファイルを処理するコードをここに追加する
    if not file:
        return jsonify({'error': 'ファイルが存在しません'})

    # CSVデータを読み込む
    csv_data = io.StringIO(file.stream.read().decode("utf-16"))
    df = pd.read_csv(csv_data, sep='\t', encoding='utf-16')
    df = df.applymap(lambda x: str(x).replace(',', ''))  # カンマを削除

    df=df.drop(["Mark","Company name"],axis=1)

    
    df=df.replace("n.a.",np.float32(0.0))
    df=df.replace(",","")

    df=df.astype("float32")


    
    # データを正規化する
    standalized_df = pd.DataFrame(scaler.transform(df),columns=df.columns)

    

    # データをPCAモデルに適用して、次元を削減する
    pca_data = pca_model.transform(standalized_df)
    pca_df = pd.DataFrame(pca_data)


    # モデルを使用して予測を行う
    predictions = model.predict(pca_df.values)

    # 予測値をcsvに変換
    output = io.StringIO()
    np.savetxt(output, predictions, delimiter=',', fmt='%.2f')
    csv_string = output.getvalue()

    response = Response(csv_string, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="predictions.csv")
    return response


if __name__ == '__main__':
    app.run(debug=True,port=5000)