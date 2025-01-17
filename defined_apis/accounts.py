#Imported all the necessary modules and functions
from flask import jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from pydantic import ValidationError
from app import app
from config import *
from defined_databases.mongo import user_collection,account_collection
from defined_serializers.accounts import AccountCreation,ViewAccounts
from utils.parsing import parse_request,serialize_data_lists


#Api for creating an account
@app.route(CREATE_ACCOUNT,methods=[POST])
@jwt_required()
def create_account():
    #function for data validation
    parsed_data,errors = parse_request(request=request,schema=AccountCreation)
    if errors:
        return errors,400
    
    account_no=parsed_data.account_no

    existing_account = account_collection.find_one({"account_no" : account_no})
    
    #non existent account error checking
    if existing_account:
        return jsonify({"message" : "account already exists"}),400
    
    username=get_jwt_identity()

    user=user_collection.find_one({"username" : username})

    bank_name=parsed_data.bank_name
    
    balance=parsed_data.balance


    #creation of the dictionary which will be inserted in mongo
    account_dict={}
    account_dict["user"] = user
    account_dict["bank_name"] = bank_name
    account_dict["account_no"] = account_no
    account_dict["balance"] = balance
    
    account = account_collection.insert_one(account_dict)

    return jsonify({"message" : f"your banking account is succesfully initiated with amount rs {balance}"}),201
    
#Api for viewing accounts specific to an existing,logged in user
@app.route(VIEW_ACCOUNTS,methods=[GET])
@jwt_required()
def view_account_list():
    username = get_jwt_identity()

    user = user_collection.find_one({"username" : username})

    accounts = account_collection.find({"user" : user})
    #serialization function for validating list of data using list comprehension
    data_list,status = serialize_data_lists(data_list=accounts,schema=ViewAccounts)
    return data_list,status


#Api to view all the accounts,normal user wont have authorization to use this api
@app.route(VIEW_ALL_ACCOUNTS,methods=[GET])
@jwt_required()
def view_all_accounts():
    accounts = account_collection.find()
    #same function as the above api
    data_list,status = serialize_data_lists(data_list=accounts,schema=ViewAccounts)
    return data_list,status


