from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, List
import requests
import os
import json
import openai
import time
import uuid

app = FastAPI()

# Enable CORS to allow cross-origin requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_env(file_path='.env'):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print(f"{file_path} not found. Make sure the .env file exists.")

load_env()
yelp_api_key = os.environ.get("YELP_API")
openai_api_key = os.environ.get("OPENAI_API")
openai.api_key = openai_api_key
YELP_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
YELP_SEARCH_LIMIT = 20

class Location(BaseModel):
    latitude: float
    longitude: float

class UserMessage(BaseModel):
    text: str

messages = []

def _request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = f"{host}{path}"
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    print(f'Querying {url} ...')
    response = requests.get(url, headers=headers, params=url_params)
    return response.json()

def get_restaurant_info(latitude, longitude):
    url_params = {
        'term': "food",
        'latitude': latitude,
        'longitude': longitude,
        'limit': YELP_SEARCH_LIMIT,
        'radius': 25
    }
    json_data = _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)
    restaurants = json_data["businesses"]
    data = {}  # name and cuisine type
    extra = {}  # address and rating
    for restaurant in restaurants:
        entry = {}
        entry2 = {}
        name = restaurant["name"]
        categories = restaurant["categories"]
        category_aliases = [category["title"] for category in categories]
        id = restaurant["id"]
        coords2 = restaurant["coordinates"]
        location = restaurant["location"]
        rating = restaurant["rating"]
        entry = {"name": name, "categories": category_aliases}
        entry2 = {"name": name, "location": location, "rating": rating, "coordinates": coords2}
        data[id] = entry
        extra[id] = entry2
    data_json = json.dumps(data)
    extra_json = json.dumps(extra)
    return data_json, extra_json

@app.post("/")
def init(location: Location):
    latitude, longitude = location.latitude, location.longitude
    data, extra_info = get_restaurant_info(latitude, longitude)
    data_string = json.dumps(data)
    messages.append({"role": "user", "content": "Here is data about restaurants in JSON format. Use this data to answer my questions. " + data_string})
    messages.append({"role": "user", "content": "Here is extra info about restaurants in JSON format. Use this data to answer my questions. " + extra_info})
    return {"success": True}

@app.post("/messages/")
def message_sent(data: UserMessage):
    user_message = data.text
    messages.append({"role": "user", "content": user_message})
    response = _send_chat_request()
    messages.append({"role": "assistant", "content": response})
    unique_id = abs(hash(uuid.uuid4()))
    message_dto = {
        "id": unique_id,
        "date": int(time.time() * 1000),
        "text": response['choices'][0]['message']['content'],
        "sender": "bot",
    }
    return message_dto

def _send_chat_request():
    '''
    Helper function that handles the chat request to the OpenAI API.
    '''
    response = ""
    try:
        response: Any = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    except Exception as exception:
        raise OpenAIServiceError(
            f"OpenAI service failed to complete the chat: {exception}"
        ) from exception
    return response

class OpenAIServiceError(Exception):
    """
    Custom exception for OpenAI service errors.
    """

    def __init__(self, message):
        super().__init__(message)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)