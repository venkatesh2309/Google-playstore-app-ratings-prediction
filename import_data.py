from pymongo import MongoClient
import urllib
import pandas as pd


def read_datafrom_mongo(project='Project1',Collection='googleplaystoredata'):
    password = urllib.parse.quote_plus('password@123')
    ## Creating a client object
    client=MongoClient('mongodb+srv://analytics:' + password + '@mongodb01-k4zak.mongodb.net/test?retryWrites=true&w=majority')
    ## read the database
    db=client[project]
    ## read the collection/table
    collectiondata=db[Collection]
    ## read all the data
    read_df=collectiondata.find()
    ## converting to dataframe
    df=pd.json_normalize(read_df)
    return df