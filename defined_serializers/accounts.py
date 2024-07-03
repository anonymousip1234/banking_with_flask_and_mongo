from pydantic import BaseModel

class AccountCreation(BaseModel):
    bank_name:str
    account_no:str
    balance:int

class ViewAccounts(BaseModel):
    account_no:str
    balance:int