from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

jwt=JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

from defined_apis.authenticate import register,login,home
from defined_apis.accounts import create_account,view_account_list
from defined_apis.transactions import create_transaction,view_transaction_history


if __name__== "__main__":
    app.run(debug=True)