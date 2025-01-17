#All the required settings and the collections to be used in the project to connect flask with mongo db
#Using pymongo,flask_pymongo as the orm tool
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI=os.getenv('MONGO_URI')
DATABASE=os.getenv('FLASK_DATABASE')

client=MongoClient(MONGO_URI)

db=client[DATABASE]

user_collection=db['users']
account_collection=db["accounts"]
transaction_history_collection=db['transaction_history']
