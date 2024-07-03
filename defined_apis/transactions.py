from flask import jsonify,request
import json
from bson import json_util
from pydantic import ValidationError
from flask_jwt_extended import get_jwt_identity,jwt_required
from pymongo import ReturnDocument
from app import app
from config import *
from defined_serializers.transactions import CreateTransaction,ViewTransaction
from defined_databases.mongo import account_collection,transaction_history_collection,user_collection
from utils.parsing import parse_request
from utils.transactions import create_transaction_history


@app.route(CREATE_TRANSACTION,methods=[POST])
@jwt_required()
def create_transaction():
    parsed_data,errors = parse_request(request,schema=CreateTransaction)
    if errors:
        return errors
    if not parsed_data.withdraw and not parsed_data.deposit:
        return jsonify({"message" : "please select an option deposit or withdraw"})
    username=get_jwt_identity()
    account_no=parsed_data.account_no
    if parsed_data.deposit:
        amount = parsed_data.deposit
        balance= account_collection.find_one({"account_no" : account_no})["balance"]
        account = account_collection.find_one_and_update(
            {"account_no" : account_no},
            {"$set" : {
                "balance" : balance + amount
            }},
            return_document=ReturnDocument.AFTER

        )
        
        remaining_balance = account["balance"]
        transaction_history = create_transaction_history(
            username=username,
            account_no=account_no,
            deposit=amount,
            remaining_balance=remaining_balance
        )
            
        return jsonify({"message" : f"your amount has been deposited successfully,remaining balance is {remaining_balance}"})
    if parsed_data.withdraw:
        amount = parsed_data.withdraw
        balance = account_collection.find_one({"account_no" : account_no})["balance"]
        if amount > balance:
            return jsonify({"message" : "insufficient balance!"})
        account = account_collection.find_one_and_update(
            {"account_no" : account_no},
            {"$set" : {
                "balance" : balance - amount
            }},
            return_document=ReturnDocument.AFTER
        )
        remaining_balance = account["balance"]
        transaction_history = create_transaction_history(
            username=username,
            account_no=account_no,
            withdraw=amount,
            remaining_balance=remaining_balance
        )

        return jsonify({"message" : f"amount has been withdrawn successfully,remaining balance {remaining_balance}"})


@app.route(VIEW_TRANSACTION,methods=[GET])
@jwt_required()
def view_transaction_history():
    username = get_jwt_identity()
    account_no = request.get_json()['account_no']
    user = user_collection.find_one({"username":username})
    account = account_collection.find_one({"account_no" : account_no})

    if not account_no or not user:
        return jsonify({"message" : "Insufficient Data"}),400
    
    transaction_history_list_cursor = transaction_history_collection.find({"user" : user,"account" : account})

    transaction_history_list = json.loads(json_util.dumps(transaction_history_list_cursor))
    try:
        serialized_transaction_history = [ViewTransaction(**transaction_history).model_dump() for transaction_history in transaction_history_list]
    except ValidationError as e:
        return jsonify({"errors" : e}),400


    return jsonify({"history" : serialized_transaction_history}),201
