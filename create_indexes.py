from pymongo import MongoClient, ascending, descending
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def create_indexes():
    collection.create_index("event_id", unique=True)
    collection.create_index([("timestamp", descending)])
    collection.create_index([("user", ascending)])
    collection.create_index([("title", ascending)])
    collection.create_index([("bot", ascending)])
    collection.create_index([("wiki",ascending), ("timestamp", descending)])

    print("Indexes created successfully.")

if __name__ == "__main__":
    create_indexes()