from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def top_edited_pages(minutes=30, limit=10):
    since = datetime.utcnow() - timedelta(minutes=minutes)

    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$title", "edit_count": {"$sum": 1}}},
        {"$sort": {"edit_count": -1}},
        {"$limit": limit}
    ]

    return list(collection.aggregate(pipeline))

def edit_activity_per_user(minutes=30):
    since = datetime.utcnow() - timedelta(minutes=minutes)

    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$user", "edit_count": {"$sum": 1}}},
        {"$sort": {"edit_count": -1}},
        {"$limit": 20}
    ]

    return list(collection.aggregate(pipeline))

def bot_vs_human_edits(minutes=30):
    since = datetime.utcnow() - timedelta(minutes=minutes)

    pipeline = [
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$bot", "edit_count": {"$sum": 1}}},
        {"$project": {
            "actor_type": {
                "$cond": [{"$eq": ["$_id", True]}, "Bot", "Human"]
            }, 
            "edit_count": 1,
            "_id": 0
        }},   
    ]

    return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    print("Top Edited Pages")
    print(top_edited_pages())

    print("\nEdit Activity Per User:")
    print(edit_activity_per_user())

    print("\nBot vs Human Edits:")
    print(bot_vs_human_edits())

