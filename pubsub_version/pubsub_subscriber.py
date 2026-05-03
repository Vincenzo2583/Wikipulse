import json
from google.cloud import pubsub_v1

PROJECT_ID = "your-gcp-project-id"
TOPIC_ID = "wikipedia-edits-sub"
SUBSCRIPTION_ID = "your-subscription-id"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message):
    event = json.loads(message.data.decode("utf-8"))
    
    print("Received event")
    print(event)

    message.ack()

if __name__ == "__main__":
    streaming_pull_future = subscriber.subscribe(
        subscription_path, 
        callback=callback
    )
    print(f"Listening for messages on {subscription_path}...")
    
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("Stopped listening for messages.")