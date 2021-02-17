import numpy as np
from flask import Flask, request, jsonify,render_template, url_for
import pickle
import config
import utils as ut
import pandas as pd
import model_prediction as mt


app=Flask(__name__)  ## create a flask app
##model=pickle.load(open(config.trained_model,'rb')) ## Read the model

@app.route('/') ## Root page/home page
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST': 
        application_name=request.form['application_name']
        Category=request.form['Category']
        Type=request.form['Type']
        Size_Label=request.form['Size_Label']
        ContentRating=request.form['ContentRating']
        Lastupdated_year=request.form['Lastupdated_year']
        Install_Labels=request.form['Install_Labels']
        Price_Label=request.form['Price_Label']
        obj=pd.DataFrame(ut.decode_features(Category,Type,Size_Label,ContentRating,Lastupdated_year,Install_Labels,Price_Label))
        output=mt.predictor(obj)
        out=np.round(output,1)
        ##print(obj)
        return render_template('index.html',prediction_text="The Ratings for the Application {}".format(float(out)))## .format(output)
    
        
        
if __name__ == '__main__':
    app.run(debug=True)
    

