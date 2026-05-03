import json
import time
import requests
import sseclient

from config import WIKIPEDIA_STREAM_URL
from local_queue import event_queue

def ingest_events():
    print("Connecting to Wikipedia stream...")

    while True:
        try:
            response = requests.get(
                    WIKIPEDIA_STREAM_URL, 
                    stream=True, 
                    headers={'Accept': 'text/event-stream'},
                    timeout=60
            )
            client = sseclient.SSEClient(response)

            for event in client.events():
                if event.event == 'message':
                    try:
                        event_data = json.loads(event.data)
                        
                        if "id" in event_data and "timestamp" in event_data:
                            event_queue.put(event_data)

                            print(
                                f"Ingested: {event_data.get('title')} | "
                                f"User: {event_data.get('user')}"
                            )
                    except json.JSONDecodeError:
                        print("Failed: Invalid JSON data received.")

        except Exception as e:
            print(f"Ingestion error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    ingest_events()