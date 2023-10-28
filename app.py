from flask import Flask, jsonify, request
import requests
from geopy.geocoders import Nominatim
import os
from urllib.parse import quote

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
YELP_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
YELP_SEARCH_LIMIT = 20
headers = {'Authorization': 'Bearer {}'.format(yelp_api_key),'accept': 'application/json'}

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/models/location', methods=['GET'])
def _get_user_location():
    if request.method == "GET":
        location = request.args.get("location")
      
    return location.latitude, location.longitude
    

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
def search():
    coords = _get_user_location()
    latitude, longitude = coords.split(',')
    url_params = {
    'term': "food",
    'latitude': latitude,
    'longitude': longitude,
    'limit': YELP_SEARCH_LIMIT,
    'radius': 25 
     }
    return _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)

if __name__ == '__main__':
    app.run(debug=True)
