## Read the file
from pymongo import MongoClient
import pandas as pd
import urllib

def Insertion(Dbname=None,collectionName=None,path=None):
    password = urllib.parse.quote_plus('password@123')
    ## Creating a client object
    client=MongoClient('mongodb+srv://analytics:' + password + '@mongodb01-k4zak.mongodb.net/test?retryWrites=true&w=majority')
    ## username: analytics
    DB=client[Dbname]
    collection=DB[collectionName]
    ## read the file
    df=pd.read_csv(path)
    data=df.to_dict('records')
    collection.insert_many(data,ordered=False)


if __name__ == "__main__":
    Insertion(Dbname="Project1",collectionName="googleplaystoredata",path='googleplaystore.csv')
    



