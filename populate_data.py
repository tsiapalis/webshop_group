import os
import django
import json
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshop.settings")
django.setup()

from core_app.models import Candle

JSON_FILE_PATH = "candles_data.json"

def populateData(candles_data):
    for candle_data in candles_data:
        category_mapping = {
            "Scented": "SC",
            "Pillar": "PI",
            "Decrotive": "DE",
            "Twisted": "TW",
            "Tapper": "TA"
        }
        category = category_mapping.get(candle_data["category"], "TA")
        created_at = candle_data.get("created_at") or datetime.now()
        updated_at = candle_data.get("updated_at") or datetime.now()

        # Create or update a Candle instance
        candle = Candle(
            title=candle_data["title"],
            description=candle_data["description"],
            price=candle_data["price"],
            burn_time=candle_data["burn_time"],
            material=candle_data["material"],
            in_stock=candle_data["in_stock"],
            created_at=candle_data["created_at"],
            updated_at=candle_data["updated_at"],
            category=category,
            image=candle_data["image"] if candle_data["image"] else None,
        )

        candle.save()
        print(f"Saved {candle}")

if __name__=="__main__":
    print("Starting population script...")
    
    print("Loading JSON data...")
    print()
    try:
        with open(JSON_FILE_PATH, "r") as json_file:
            candles_data = json.load(json_file)
        
            populateData(candles_data)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {JSON_FILE_PATH}.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")