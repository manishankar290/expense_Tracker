from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["expense_tracker"]

trips_collection = db["trips"]
expenses_collection = db["expenses"]