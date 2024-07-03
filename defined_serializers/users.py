from pydantic import BaseModel

class UserCreation(BaseModel):
    username : str
    password : str
    email: str
    address : str
    mobile_no : int

class UserLogin(BaseModel):
    username: str
    password : str