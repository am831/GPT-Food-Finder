from flask import Flask, jsonify, request
import requests
from geopy.geocoders import Nominatim
import os
from urllib.parse import quote
import json
import openai
from flask_cors import CORS

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
openai_api_key = os.environ.get("OPENAI_API")
coords = "37.7749,-122.4194"
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
    location = request.get_json()
    if location is None:
        return jsonify(error='Invalid JSON'), 400
    latitude, longitude = location.get('latitude'), location.get('longitude')
    response = jsonify(success=True)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

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
    latitude, longitude = coords.split(',')
    url_params = {
    'term': "food",
    'latitude': latitude,
    'longitude': longitude,
    'limit': YELP_SEARCH_LIMIT,
    'radius': 25 
    }
    json_data = _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)
    print(json_data)
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

# def _add_role_n_message(role, message):
#     messages.append({"role": role, "content": message})

def _get_distance(rest_loc, user_loc):
    # TODO call maps api to get distance
    return 1

@app.route('/chat')
def chatbot():
    #TODO: Keeping track of user's content/response into messages
    # Create a list to store all the messages for context
    data, extra_info = get_restaurant_info()
    data_string = json.dumps(data)
    messages = [
            {"role": "user", "content": "Here is data about restaurants in JSON format. Use this data to answer my questions. " + data_string}, 
            {"role": "user", "content": "Here is extra info about restaurants in JSON format. Use this data to answer my questions. " + extra_info}, 
            {"role": "user", "content": "Show me restaurant with ice cream"}
            ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        # max_tokens = 1024, # this is the maximum number of tokens that can be used to provide a response.
    )
    chat_message = response['choices'][0]['message']['content']
    print(f"Bot: {chat_message}")
    messages.append({"role": "assistant", "content": chat_message})
    messages.append({"role": "user", "content": "What is the full address of the restaurant?"})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        # max_tokens = 1024, # this is the maximum number of tokens that can be used to provide a response.
    )
    chat_message = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": chat_message})
    return messages[2:]

if __name__ == '__main__':
    app.run(debug=True)
