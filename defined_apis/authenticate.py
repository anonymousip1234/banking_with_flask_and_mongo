from flask import request,jsonify
from app import app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
from config import *
from defined_databases.mongo import user_collection
from defined_serializers.users import UserCreation,UserLogin
from utils.parsing import parse_request



@app.route('/',methods=[POST])
def home():
    return jsonify({"Message" : "this is the home page"})

@app.route(REGISTER,methods=[POST])
def register():
    
    parsed_data,errors = parse_request(request=request,schema=UserCreation)
    if errors:
        return errors
        # return jsonify({"message" : "please provide all the necessary details"}),400
    username = parsed_data.username
    password = parsed_data.password

    if not username or not password:
        return jsonify({"message" : "Please Provide username or password"}),400
    
    
    existing_user = user_collection.find_one({"username" : username})

    if existing_user:
        return jsonify({"message" : "username is already taken"}),400
    
    hashed_password = generate_password_hash(password)

    user_id = user_collection.insert_one({"username" : username,"password": hashed_password}).inserted_id

    return jsonify({"message" : "User created succesfully","user_id" : str(user_id)}),200


@app.route(LOGIN,methods = [POST])
def login():

    parsed_data,errors = parse_request(request=request,schema=UserLogin)
    if errors:
        return errors
    username = parsed_data.username
    password = parsed_data.password
    

    if not username or not password:
        return jsonify({"message" : "Missing username or password"}),400
    
    user = user_collection.find_one({"username" : username})

    password = check_password_hash(user["password"],password)

    if not user or not password:
        return jsonify({"message" : "invalid username or password"}),400
    
    access_token = create_access_token(identity=username)

    return jsonify({"message" : "You are logged in succesfully","access_token" : access_token})