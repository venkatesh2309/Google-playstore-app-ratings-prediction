import pickle
import config


## Read the model
model=pickle.load(open(config.trained_model,'rb')) 


"""
This function will take the  decoded input featues 
featues and  returns the prediction for ratings
"""
def predictor(obj):
    prediction=model.predict(obj)
    return prediction


    
    