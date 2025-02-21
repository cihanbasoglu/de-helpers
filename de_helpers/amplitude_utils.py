import json
import requests
import csv
from .date_utils import convert_to_epoch_ms

AMPLITUDE_URL = "https://api2.amplitude.com/attribution"

def send_amplitude_event(api_key, event):
    """Send an event to Amplitude."""
    payload = {
        "api_key": api_key,
        "event": json.dumps(event)
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(AMPLITUDE_URL, data=payload, headers=headers)
    if response.status_code == 200:
        print("Event sent successfully.")
    else:
        print(f"Failed to send event. Status: {response.status_code}, User ID: {event.get('user_properties', {}).get('user_id')}")

def send_amplitude_events_from_csv(csv_file_path, api_key, user_id_column, gaid_column=None, idfv_column=None,
                                   time_column="Event Time", campaign_column="Campaign", adset_column="Adset",
                                   ad_column="Ad", media_source_column="Media Source", install_time_column="Install Time"):
    """Send multiple events to Amplitude from a CSV file."""
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        events = []
        
        for row in reader:
            event_time = convert_to_epoch_ms(row.get(time_column, ""))
            platform = row.get("Platform", "").strip().lower()
            device_id = row.get(gaid_column if platform == "android" else idfv_column, "").strip()
            if not device_id or device_id == "00000000-0000-0000-0000-000000000000":
                print(f"Skipping event with invalid device_id: {device_id}")
                continue
            
            event = {
                "adid": device_id if platform == "android" else None,
                "idfv": device_id if platform == "ios" else None,
                "event_type": "[CUSTOM] Install",
                "platform": platform,
                "time": event_time,
                "event_properties": {
                    "campaign": row.get(campaign_column, ""),
                    "adset": row.get(adset_column, ""),
                    "ad": row.get(ad_column, ""),
                    "[CUSTOM] Media Source": row.get(media_source_column, ""),
                },
                "user_properties": {
                    "campaign": row.get(campaign_column, ""),
                    "adset": row.get(adset_column, ""),
                    "ad": row.get(ad_column, ""),
                    "media_source": row.get(media_source_column, ""),
                    "install_time": row.get(install_time_column, 0),
                    "user_id": row.get(user_id_column, "")
                },
            }
            events.append(event)
        
        for event in events:
            send_amplitude_event(api_key, event)