import json
from google.cloud import pubsub_v1

PROJECT_ID = "your-gcp-project-id"
TOPIC_ID = "wikipedia-edits"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_event(event):
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    print(f"Published message ID: {message_id}")

if __name__ == "__main__":
    sample_event = {
        "id": 1,
        "title": "Sample Wikipedia Page",
        "user": "SampleUser",
        "bot": False
    }
    
    publish_event(sample_event)
