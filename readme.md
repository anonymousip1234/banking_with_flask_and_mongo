This is a flask project with mongodb.

The main objective of this project is to work with mongo db using python,establish security,error
handling and some advanced python functionalities.

In the root there is app.py which is the main flask application which runs an WSGI server.

Necessary modules,functions and settings are imported in it which are essential to run with the main application,such as database settings,jwt settings,and api functions.

All the apis lie in the defined_apis folder,which contains file such as authentication,transactions and accounts which are responsible to take care of their respective functionalities.

All the schemas are inside defined_serializer folder,which are necessary to validate request and responses and other managements.

Defined_databases contain mongo settings and the collections which are to be used.

Utils folder contain all the necessary functions which are responsible for parsing and data validation and other things,this functions are imported and used in the created apis.

we have .env file for environment variables,and .gitignore for git management,essentially the files or folders which are to be ignored by git.

config.py file holds all the strings which are used in the api,later it can be used to save other variables too.


To run this project make sure to install all the requirements from requirements.txt,and 
flask run -h {host} -p {port} command to run the server.Also make sure to install mongo and start a server.

There are many comments in all over the code sections to make the project more readable and understandable.

I am also leaving thunderclient collections for api testing,to make the testing process more efficient.