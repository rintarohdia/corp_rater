from flask import Flask, request, render_template, jsonify,Response
import pandas as pd
import requests
import io

app = Flask(__name__)

@app.route('/post/', methods=['POST'])
def predict():
    data = request.files['file'] 
    response = requests.post('https://predict-rate.onrender.com/predict/',  files={'file': data})
    
    # レスポンスのCSVデータを読み込む
    csv_data = io.StringIO(response.text)
    result_df = pd.read_csv(csv_data)

    # 結果をレスポンスとして返す
    csv_string = result_df.to_csv(index=False)
    return Response(csv_string, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=predictions.csv'})

    return response.content

@app.route('/', methods=['GET'])
def upload():
    return render_template('App.vue')

if __name__ == '__main__':
    app.run(debug=True,port=5050)
