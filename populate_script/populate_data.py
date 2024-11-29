import os
import sys
import django
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webshop.settings")
django.setup()

from core_app.models import Candle

JSON_FILE_PATH = "populate_script/candles_data.json"
DEFAULT_IMAGE_PATH = "populate_script/candle_images/Stearin candle Polka countdown.jpg"

def validate_image_path(image_path):
    if image_path and os.path.isfile(image_path):
        return image_path
    print(f"Warning: Image file not found for path '{image_path}'. Using placeholder image.")
    return DEFAULT_IMAGE_PATH

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
        image_path = validate_image_path(candle_data.get("image"))

        # Create or update a Candle instance
        candle = Candle(
            title=candle_data["title"],
            description=candle_data["description"],
            price=candle_data["price"],
            burn_time=candle_data["burn_time"],
            material=candle_data["material"],
            in_stock=candle_data["in_stock"],
            created_at=created_at,
            updated_at=updated_at,
            category=category,
            image=image_path,
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