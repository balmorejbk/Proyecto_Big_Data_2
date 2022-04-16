from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import json
import numpy as np
import math
from ModelPrediction import ModelPredicition 

app = Flask(__name__)
CORS(app)

@app.route('/api/test/headers',methods=['POST'])
def headers():
    # Get headers for payload
    headers = ['times_pregnant', 'glucose', 'blood_pressure', 'skin_fold_thick', 'serum_insuling', 'mass_index', 'diabetes_pedigree', 'age']

    payload = request.json['data']
    #prediction = model.predict([[np.array(data['exp'])]])
    #output = prediction[0]
    values = [float(i) for i in payload.split(',')]
    
    input_variables = pd.DataFrame([values],
                                columns=headers, 
                                dtype=float,
                                index=['input'])
    sr = pd.Series([19.5, 16.8, 22.78, 20.124, 18.1002]) 
    #return input_variables.to_json(orient='records')
    return input_variables.to_json(orient='records')


     

@app.route('/api/anomalydetection/load',methods=['POST'])
def load():  
    modelPredicition = ModelPredicition()
    modelPredicition.loadModel('models/isolation_forest.pickle')
    print('leido pikle')
    return "leido"

@app.route('/api/anomalydetection/predict',methods=['POST'])
def predict():  
    now = datetime.now()
    today = date.today()

    datos = {'DataObserved': now, 'H' : 2, 'V': 2, 'C' : 0.1}

    client = request.json
    product =request.json
    payload = request.json
    price =  request.json

    #leo la matriz para poder predecir
    print(client)
    print(product)
    print(price)
    print(payload)

    data = pd.json_normalize(client, product, price, payload)
    #calculo
    modelPredicition = ModelPredicition()
    model = modelPredicition['models/isolation_forest.pickle']
    dfResultados = modelPredicition.predict(model, data)
    
    return Response(dfResultados.to_json(orient='records'), mimetype='application/json')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug = True)