from flask import Flask,jsonify,request
import pandas as pd
import sqlite3 as sql
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json
import requests
from configuration import DATABASE_PATH

app = Flask(__name__)
connect = sql.connect(DATABASE_PATH)

database_table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'",connect)
data_rating = pd.read_sql_query("SELECT * from pages_myrating",connect)
pivoted_data=data_rating.pivot_table(index='places_id',columns='user_id',values='rating').fillna(0)
features= csr_matrix(pivoted_data.values)
model = NearestNeighbors(metric='cosine',algorithm='brute')
model.fit(features)

@app.route('/recommend',methods=["POST","GET"])
def hello_world():
    users = request.form.get("user_id")
    user_id = int(users)
    distances,indices = model.kneighbors(pivoted_data.iloc[user_id,:].values.reshape(1,-1),n_neighbors=5)
    recommended_items = set()
    for i in range(0,len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:\n'.format(pivoted_data.index[user_id]))
        else:
            print('{0}: {1}, with distance of {2}:'.format(i, pivoted_data.index[indices.flatten()[i]],distances.flatten()[i]))
            recommended_items.add(pivoted_data.index[indices.flatten()[i]])
    items = tuple(recommended_items)
    recommended = '{}'.format(items)
    return jsonify(recommended)


if __name__=='__main__':
    app.run(debug=True)