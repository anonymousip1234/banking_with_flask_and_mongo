from pydantic import BaseModel
from typing import Optional
from .users import UserCreation
from .accounts import AccountCreation

class CreateTransaction(BaseModel):
    account_no:str
    deposit:Optional[int]=None
    withdraw:Optional[int]=None

class TransacrtionHistory(BaseModel):
    user:Optional[UserCreation]=None
    account:Optional[AccountCreation]=None
    withdraw:Optional[int]=None
    deposit:Optional[int]=None
    remaining_balance:int


class ViewTransaction(BaseModel):
    withdraw:Optional[int] = None
    deposit:Optional[int] = None
    remaining_balance:int
    

class TransactionRequest(BaseModel):
    account_no : str
