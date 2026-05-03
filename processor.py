from datetime import datetime
from pymongo import MongoClient, errors
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from local_queue import event_queue

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

seen_event_ids = set()

def transform_event(event):
    event_id = event.get("id")

    if not event_id:
        return None
    
    timestamp = event.get("timestamp")

    return {
        "event_id": event_id,
        "wiki": event.get("wiki"),
        "type": event.get("type"),
        "namespace": event.get("namespace"),
        "title": event.get("title"),
        "page_id": event.get("page_id"),
        "revision_id": event.get("revision_id"),
        "old_revision_id": event.get("old_revision_id"),
        "user": event.get("user"),
        "bot": event.get("bot"),
        "minor": event.get("minor"),
        "comment": event.get("comment"),
        "server_name": event.get("server_name"),
        "server_url": event.get("server_url"),
        "timestamp": datetime.fromtimestamp(timestamp) if timestamp else None,
        "raw_event": event,
        "ingested_at": datetime.utcnow()
    }

def process_events():
    print("Starting event processor...")

    while True:
        raw_event = event_queue.get()

        event_id = raw_event.get("id")

        if event_id in seen_event_ids:
            print(f"Duplicate event skipped: {event_id}")
            continue

        seen_event_ids.add(event_id)

        transformed_event = transform_event(raw_event)

        if not transformed_event:
            print("Invalid event skipped: Missing ID")
            continue
       
        try:
            collection.insert_one(transformed_event)
            print(f"Processed and stored event: {transformed_event['title']}")

        except errors.DuplicateKeyError:
            print(f"Duplicate in DB skipped: {event_id}")
            
        except Exception as e:
            print(f"Error storing event: {e}")

if __name__ == "__main__":
    process_events()