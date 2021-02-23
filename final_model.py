## Import the libraries
import re
import pandas as pd
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import import_data as im
import mlflow
import mlflow.sklearn
import config
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score,mean_absolute_error
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
    
## load the data
def load_data():
    dataset=im.read_datafrom_mongo()
    return dataset
    



## Data preprocessing
def preprocessing():
    loaded_data=load_data()
    loaded_data.rename(columns={'Last Updated': 'Lastupdated','Content Rating':'ContentRating','Current Ver': 'CurrentVer','Android Ver': 'AndroidVer'},inplace=True)
    loaded_data=loaded_data.drop(['_id','App','CurrentVer','AndroidVer'],axis=1)
    
    ## split the data for lastupdated feature
    df1=pd.DataFrame(loaded_data.Lastupdated.str.split(",",1).tolist(),columns=['Lastupdated_date','Lastupdated_year']) ## 1= no of splits
    df_final=pd.concat([loaded_data,df1],axis=1)
    
     ## Removing white spaces
    df_final['Lastupdated_year']=df_final['Lastupdated_year'].apply(lambda x: str(x).strip())
    
    ## dropping the irrelvant data
    df_final.drop(df_final.index[10471],inplace=True)
    
    ##ContentRating feature
    ## We can conmbine few labels as those labels are similar
    content_map={'Everyone':'Everyone','Everyone 10+':'Everyone 10+','Teen':'Teen','Mature 17+':'Adults','Adults only 18+':'Adults','Unrated':'Adults'}
    df_final['ContentRating']=df_final['ContentRating'].map(content_map)
    
    ## Price feature
    ## Lets remove the $ symbol
    df_final['Price'] = df_final.Price.apply(lambda x: re.sub('\$','',str(x)) if pd.notna(x) else x)
    df_final['Price']=df_final['Price'].astype(float)
    ## round the float values
    df_final['Price']=round(df_final['Price'])
    ## Price
    df_final['Price_label']= pd.cut(x=df_final['Price'],bins=[-1,0,100,1000],labels=['Free','1$ to 100$','101$ or above'])
    ##PS: the first value will be always be the next value of what you mentioned
    
    
    ## Installs feature
    ## lets remove + and , and try to convert into an integer/float
    df_final['Installs']=df_final.Installs.apply(lambda x: re.sub('\+','',str(x)) if pd.notna(x) else x)
    df_final['Installs']=df_final.Installs.apply(lambda x: re.sub('\,','',str(x)) if pd.notna(x) else x)
    df_final['Installs']=df_final['Installs'].astype(int)
    ## installs
    df_final['install_Labels']= pd.cut(x=df_final['Installs'],bins=[-1,1000,1000000,10000000,1000000000],labels=['Zero - Thousand','Morethan Thousand - 1Million','Morethan 1Million - 10Million','Morethan 10Million'])
    ##PS: the first value will be always be the next value of what you mentioned
    
    ##Cateory feature
    ## We can able to cover 90% of the data with the Top20 categories.
    Top_Category_20=df_final.Category.value_counts()[:20].index
    df_final['Category']=np.where(df_final['Category'].isin(Top_Category_20),df_final['Category'],'Others')
    
    ## Size feature
    ## Filtering the values which has kbytes to a list
    k_indices = df_final['Size'].loc[df_final['Size'].str.contains('k')].index.tolist()
    df_final['Size']=df_final.Size.str.replace('M','')
    
    ##Converting those values into Mbytes 
    Converter=pd.DataFrame(df_final.loc[k_indices,'Size'].str.replace('k','')).astype(float).apply(lambda x: x/1024)
    Converter=round(Converter,3)## Taken first 3 decimals
    df_final.loc[k_indices,'Size']=Converter
    
    ##Binnig
    df_final.loc[df_final['Size'] == 'Varies with device','Size'] = 99999
    df_final.Size=df_final.Size.astype(float)
    df_final['Size_label']= pd.cut(x=df_final['Size'],bins=[-1,1,10,9999,99999],labels=['0 to 1MB','1 to 10MB','More then 10MB','Varies to device'])
    
    ## Lets drop the unwanted feature
    df_final=df_final.drop(['Size','Installs','Price','Lastupdated','Lastupdated_date','Genres','Reviews'],axis=1)
    return df_final



## Encode the data
def encode_data():
    ## read the the file
    with open(config.factors_codes) as file:
        factors_codes=json.load(file)
    df_final=preprocessing()
    df_final['Category']=df_final['Category'].map(factors_codes['Category_L'])
    df_final['Type']=df_final['Type'].map(factors_codes['Type'])
    df_final['ContentRating']=df_final['ContentRating'].map(factors_codes['ContentRating'])
    df_final['Lastupdated_year']=df_final['Lastupdated_year'].map(factors_codes['LastUpdated_year'])
    df_final['install_Labels']=df_final['install_Labels'].map(factors_codes['Install_Labels'])
    df_final['Price_label']=df_final['Price_label'].map(factors_codes['Price_Label'])
    df_final['Size_label']=df_final['Size_label'].map(factors_codes['Size_Label'])
    return df_final



## Missing value imputation
def missing_imputation():
    df_final=encode_data()
    ## lets fill with max value for Type Feature
    df_final['Type']=df_final['Type'].fillna(1)
    ## lets use knnimputer for Rating feature
    from sklearn.impute import KNNImputer
    imputer=KNNImputer()
    x=imputer.fit_transform(df_final)
    df_final=pd.DataFrame(x,columns=df_final.columns)
    df_final.Rating=round(df_final.Rating,1)
    return df_final

## function for metrics
def model_metrics(actual,predicted):
    ##R_square=r2_score(actual,predicted)
    mse_error=mean_squared_error(actual,predicted)
    mae_error=mean_absolute_error(actual,predicted)
    return mse_error,mae_error


if __name__ == '__main__':
    data_df=missing_imputation()
    x=data_df.drop('Rating',axis=1)
    y=data_df['Rating']
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
    n_estimators= int(sys.argv[1]) if len(sys.argv) > 1 else 50
    min_samples_split= int(sys.argv[2]) if len(sys.argv) > 2 else 2
    criterion= str(sys.argv[3]) if len(sys.argv) > 3 else 'mae'
    with mlflow.start_run():
        random_regressor = RandomForestRegressor(n_estimators=n_estimators,min_samples_split=min_samples_split,criterion=criterion)
        random_regressor.fit(x_train, y_train)
        y_pred = random_regressor.predict(x_test)
        (mse,mae)=model_metrics(y_test,y_pred)
        
        print("Random_regressor (n_estimators=%d , min_samples_split=%d , criterion=%s):" % (n_estimators,min_samples_split,criterion))
        print("mse:%s"  % mse)
        print("mae:%s"  % mae)
        
        
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("criterion",criterion)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(random_regressor, "model")
        
    
  


    
    
    
    
    
    
    
    
    
    
    
    
    



