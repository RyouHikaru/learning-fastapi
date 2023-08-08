from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://<mongodb-username>:<mongodb-password>@cluster0.qmkainu.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.todo_db

collection_name = db["todo_collection"]
