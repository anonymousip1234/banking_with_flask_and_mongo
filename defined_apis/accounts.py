from flask import jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from pydantic import ValidationError
from app import app
from config import *
from defined_databases.mongo import user_collection,account_collection
from defined_serializers.accounts import AccountCreation,ViewAccounts
from utils.parsing import parse_request

@app.route(CREATE_ACCOUNT,methods=[POST])
@jwt_required()
def create_account():
    parsed_data,errors = parse_request(request=request,schema=AccountCreation)
    if errors:
        return errors
    
    account_no=parsed_data.account_no

    existing_account = account_collection.find_one({"account_no" : account_no})

    if existing_account:
        return jsonify({"message" : "account already exists"}),400
    
    username=get_jwt_identity()

    user=user_collection.find_one({"username" : username})

    bank_name=parsed_data.bank_name
    
    balance=parsed_data.balance



    account_dict={}
    account_dict["user"] = user
    account_dict["bank_name"] = bank_name
    account_dict["account_no"] = account_no
    account_dict["balance"] = balance
    
    account = account_collection.insert_one(account_dict)

    return jsonify({"message" : f"your banking account is succesfully initiated with amount rs {balance}"}),200
    

@app.route(VIEW_ACCOUNTS,methods=[GET])
@jwt_required()
def view_account_list():
    username = get_jwt_identity()

    user = user_collection.find_one({"username" : username})

    accounts = account_collection.find({"user" : user})
    try:
        serialized_accounts_list = [ViewAccounts(**account).model_dump() for account in accounts]
    except ValidationError as e:
        return jsonify({"errors" : e}),400


    return jsonify({"accounts" : serialized_accounts_list}),201

