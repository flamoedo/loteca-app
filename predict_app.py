import pandas as pd
import numpy as np
import json
from sklearn.externals import joblib
from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)

model = joblib.load('model.joblib') 

df = pd.read_csv("BRA.csv")

vocab = df['Home'].sort_values().unique()

word2idx = {word: i for i, word in enumerate(vocab)}

def create_app():    
    return app

def word2vector(word):
    m = np.zeros(len(word2idx))
    m[word2idx.get(word)] = 1
    return m


def prepare(H,A):
    vec = [word2vector(H), word2vector(A)]
    return np.array(vec).reshape(np.array(vec).shape[1]*2)


@app.route('/list', methods=['GET'])
def team_list():
    teams = vocab.tolist()
    d = {}
    for i in range(len(teams)):
        d[i]=teams[i]
    # d['teams'] = teams    
    return json.dumps(d)


@app.route('/pred', methods=['GET'])
def prediction():
    # data = request.get_json(force=True)
    H = request.args.get('H')
    A = request.args.get('A')
    p = model.predict([prepare(H,A)])
    if p < 0:
        return jsonify(H + ' Vence com ' + str(round(abs(p[0]),3)) + ' gols de diferença ')# + str(prepare(H,A)))
    else:
        return jsonify(A + ' Vence com ' + str(round(abs(p[0]),3)) + ' gols de diferença ')# + str(prepare(H,A)))


