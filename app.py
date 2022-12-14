import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import pickle
import flask
from flask import request,redirect, url_for, request, render_template


# creating instance of the class
app = flask.Flask(__name__, template_folder='templates')

# to tell flask what url should trigger the function index()


@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/form2')
def form2():
    return flask.render_template('form2.html')


# prediction function
# Memprediksi input dari form user
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(
        open("./model.pkl", "rb"))  # load the model
    # predict the values using loded model
    result = loaded_model.predict(to_predict)
    return result


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        Alcohol = request.form['alc']
        Malic_Acid = request.form['mal']

        to_predict_list = list(map(int, [Alcohol, Malic_Acid]))
        result = ValuePredictor(to_predict_list)

        if int(result) == 0:
            prediction = 'Wine dengan rasa manis, tidak terlalu pedas dan tidak terlalu asam'
        elif int(result) == 1:
            prediction = 'Wine dengan rasa manis, sedikit lebih pedas, dan tidak terlalu asam'
        elif int(result) == 2:
            prediction = 'Wine dengan rasa asam yang lebih kuat'

        return render_template("result.html", prediction=prediction)


if __name__ == "__main__":
    app.debug=True
    app.run (host='0.0.0.0', port=5000)  # use debug = False for jupyter notebook