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

@app.route('/models/location', methods=['GET', 'POST'])
def _get_user_location():
    if request.method == "GET":
        location = request.args.get("latitude", "longitude")
        print("check", location)
    return location

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

def get_restaurant_info():
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


if __name__ == '__main__':
    app.run(debug=True)
