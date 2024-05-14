from pydantic import BaseModel
from typing import List, Optional

class Account(BaseModel):
    email: str
    account_id: str
    account_name: str
    app_secret_token: str
    website: Optional[str] = None

class Destination(BaseModel):
    url: str
    http_method: str
    headers: dict

from fastapi import FastAPI, HTTPException, Depends
from typing import List

app = FastAPI()

accounts = []
destinations = {}

@app.get("/")
def index():
    return "hello world"

# Account CRUD Operations
@app.post("/accounts/")
def create_account(account: Account):
    accounts.append(account)
    return account

@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    for account in accounts:
        if account.account_id == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")

# Destination CRUD Operations
@app.post("/accounts/{account_id}/destinations/")
def create_destination(account_id: str, destination: Destination):
    if account_id not in destinations:
        destinations[account_id] = []
    destinations[account_id].append(destination)
    return destination

@app.get("/accounts/{account_id}/destinations/")
def get_destinations(account_id: str):
    if account_id not in destinations:
        raise HTTPException(status_code=404, detail="Account not found")
    return destinations[account_id]

@app.post("/server/incoming_data")
def receive_data(account_id: str, data: dict, app_secret_token: str):
    if account_id not in destinations:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Validate app secret token
    account = None
    for acc in accounts:
        if acc.account_id == account_id and acc.app_secret_token == app_secret_token:
            account = acc
            break
    if not account:
        raise HTTPException(status_code=401, detail="Unauthenticated")

    for destination in destinations[account_id]:
        pass
    
    return {"message": "Data sent to destinations successfully"}
