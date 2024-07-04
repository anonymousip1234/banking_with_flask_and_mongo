from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os



load_dotenv()

app=Flask(__name__)

jwt=JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

from defined_apis import *


if __name__== "__main__":
    app.run(debug=True)