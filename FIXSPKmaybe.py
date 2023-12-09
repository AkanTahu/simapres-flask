from flask import Flask  , render_template,request,make_response,jsonify,url_for,redirect,Response
import numpy as np
import pandas as pd
import operator
import requests
from pyDecision.algorithm import edas_method
import json
from flask_cors import CORS

# Connect to the MySQL database



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}}) 

@app.route("/test" , methods=['GET'])
def testing():
    return "hello"

@app.route("/post-rank" , methods=['POST'])
def postRank():
    data = request.json['api_datas']
    print(data)
    
    df = pd.DataFrame(data)
    namamhs = df["nama"]
    idmhs = df["id"]
    nimmhs = df["nim"]
    prodimhs = df["prodi"]
    jurusanmhs = df["jurusan"]
    tahunMasukmhs = df["tahunMasuk"]
    # ipkmhs = df["ipk"]
    # alphamhs = df["alpha"]

    columns_of_interest = ['ipk', 'alpha', 'sertifikat']
    dataset = df[columns_of_interest].values
    
    criterion_type = ['max', 'min', 'max']

    weights = [0.25, 0.40, 0.20]

    rank = edas_method(dataset, criterion_type, weights,graph = False, verbose = False)

    hasil = []
    
    for i in range(0, rank.shape[0]):
        hasil.append({
            "mhsId":int(idmhs[i]),
            "namamahas":namamhs[i],
            "nimmahas":nimmhs[i],
            "jurusanmahas":jurusanmhs[i],
            "prodimahas":prodimhs[i],    
            "alternative":'a' + str(i+1),
            "score":round(rank[i], 4)
        })

    sorted_list = sorted(hasil, key=lambda x: x['score'], reverse=True)
   

    send_data = json.dumps(sorted_list)
    
    return send_data

if __name__ == "__main__":
    app.run()
        
    
