from flask import Flask, jsonify, request
import requests
from geopy.geocoders import Nominatim
import os
from urllib.parse import quote
import json
import openai

app = Flask(__name__)

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
headers = {'Authorization': 'Bearer {}'.format(yelp_api_key),'accept': 'application/json'}

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/models/location', methods=['POST', 'GET'])
def _get_user_location():
    if request.method == "POST":
        location = request.get_json()
        print("check1", location)
        return location
    elif request.method == "GET":
        location = request.args.get('latitude', 'longitude')
        print("check2", location)
        return location
    return {"message": "Hello, World!"}

def _request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

@app.route('/business/<business_id_or_alias>')
def get_by_id(business_id_or_alias):
    """ Getting business details from id or alias
    Arg:
        business_id_or_alias(str): The business alias (i.e. yelp-san-francisco) or
                ID (i.e. 4kMBvIEWPxWkWKFN__8SxQ.

    """
    # headers = {'Authorization': 'Bearer {}'.format(MY_API_KEY),'accept': 'application/json'}
    business_path = f'https://api.yelp.com/v3/businesses/{business_id_or_alias}'
    business_response = requests.get(business_path, headers=headers)
    return business_response.json()

@app.route('/search')
def get_restaurant_info():
    location = _get_user_location()
    print("locaiton", location)
    coords = "37.7749,-122.4194"
    latitude, longitude = coords.split(',')
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
        location = restaurant["location"]
        rating = restaurant["rating"]
        entry = {"name": name, "categories": category_aliases}
        entry2 = {"location" : location, "rating" : rating}
        data[id] = entry
        extra[id] = entry2
    data_json = json.dumps(data)
    extra_json = json.dumps(extra)
    return data_json, extra_json

# def _add_role_n_message(role, message):
#     messages.append({"role": role, "content": message})

@app.route('/chat')
def chatbot():
    #TODO: Keeping track of user's content/response into messages
    # Create a list to store all the messages for context
    messages = [
            {"role": "user", "content": "What is the nearest Indian restaurant?"},
            {"role": "user", "content": "Show me restaurant with vegan option"}
            ]
    while True:
        # user_response = message.content
        # # Exit program if user inputs "quit"
        # if user_response == "quit":
        #     break

        # messages.append({"role": "user", "content": user_response})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            # max_tokens = 1024, # this is the maximum number of tokens that can be used to provide a response.
        )
        chat_message = response['choices'][0]['message']['content']
        print(f"Bot: {chat_message}")
        messages.append({"role": "user", "content": chat_message})

        ''' Example of chat completion object 
        {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-3.5-turbo-0613",
            "choices": [{
                "index": 0,
                "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }
        '''

if __name__ == '__main__':
    app.run(debug=True)
