from pydantic import ValidationError
from flask import jsonify
from defined_databases.mongo import user_collection,account_collection,transaction_history_collection
from defined_serializers.transactions import TransacrtionHistory



def create_transaction_history(username,account_no,remaining_balance,withdraw=None,deposit=None,):
    transaction_history_dict={}
    user = user_collection.find_one({"username" : username})
    account = account_collection.find_one({"account_no" : account_no})
    transaction_history_dict["user"] = user
    transaction_history_dict["account"] = account
    transaction_history_dict["remaining_balance"] = remaining_balance
    transaction_history_dict["withdraw"] = withdraw if withdraw else None
    transaction_history_dict["deposit"] = deposit if deposit else None


    transaction_history = transaction_history_collection.insert_one(transaction_history_dict)

    return transaction_history,None
