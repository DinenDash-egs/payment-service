from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client["payments"]
transactions_collection = db["transactions"]

@app.post("/transaction")
async def create_transaction(transaction: dict):
    result = transactions_collection.insert_one(transaction)
    return {"id": str(result.inserted_id)}
