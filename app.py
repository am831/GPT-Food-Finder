from flask import Flask, jsonify, request
import requests
import os
from urllib.parse import quote
import json
import openai
from flask_cors import CORS
from typing import Any
import time

app = Flask(__name__)
CORS(app)

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
messages = []
openai_api_key = os.environ.get("OPENAI_API")
YELP_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
YELP_SEARCH_LIMIT = 20
headers = {'Authorization': 'Bearer {}'.format(yelp_api_key),'accept': 'application/json'}

@app.route('/', methods=['POST', 'GET'])
def init():
    location = request.get_json()
    if location is None:
        return jsonify(error='Invalid JSON'), 400
    latitude, longitude = location.get('latitude'), location.get('longitude')
    response = jsonify(success=True)
    response.headers.add("Access-Control-Allow-Origin", "*")
    data, extra_info = get_restaurant_info(latitude, longitude)
    data_string = json.dumps(data)
    messages.append({"role": "user", "content": "Here is data about restaurants in JSON format. Use this data to answer my questions. " + data_string})
    messages.append({"role": "user", "content": "Here is extra info about restaurants in JSON format. Use this data to answer my questions. " + extra_info})
    return jsonify(messages)

"""
@app.route('/location', methods=['POST', 'GET'])
def _get_user_location():
    location = request.get_json()
    if location is None:
        return jsonify(error='Invalid JSON'), 400
    latitude, longitude = location.get('latitude'), location.get('longitude')
    response = jsonify(success=True)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print("check", latitude, longitude)
    return latitude, longitude
"""

def _request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
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
    data = {} # name and cuisine type
    extra = {} # address and rating
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
        entry2 = {"name": name, "location" : location, "rating" : rating, "coordinates" : coords2}
        data[id] = entry
        extra[id] = entry2
    data_json = json.dumps(data)
    extra_json = json.dumps(extra)
    return data_json, extra_json

@app.route("/messages/", methods=["POST", "GET"])
async def message_sent():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify(error="Invalid JSON"), 400
        user_message = data.get("text")
        messages.append({"role": "user", "content": user_message})
        response = await _send_chat_request()
        messages.append({"role": "assistant", "content": response})
        message_dto = {
            "date": int(time.time() * 1000),
            "text": response['choices'][0]['message']['content'],
            "sender": "bot",
        }
        return jsonify(message_dto)


async def _send_chat_request():
    '''
    Helper function that handles the chat request to the OpenAI API.
    '''
    response = ""
    openai.api_key = openai_api_key
    try:
        response: Any = await openai.ChatCompletion.acreate(
            model= "gpt-3.5-turbo",
            messages= messages,
        )
    except Exception as exception:
        raise OpenAIServiceError (
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
    app.run(debug=True)
