from flask import Flask, jsonify
import requests
from geopy.geocoders import Nominatim
import os
from urllib.parse import quote

app = Flask(__name__)

# Get the API key from the environment variable
yelp_api_key = os.environ.get("YELP_API")
YELP_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
YELP_SEARCH_LIMIT = 3
headers = {'Authorization': 'Bearer {}'.format(yelp_api_key),'accept': 'application/json'}

@app.route('/test')
def hello_world():
    return jsonify({"message": "Hello, World!"})

def _get_user_location():
    ip_response = requests.get("https://ipinfo.io")
    loc = ip_response.json()["loc"]
    return loc

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
    'radius': 25 # TODO : get from user
     }
    return _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)


if __name__ == '__main__':
    app.run(debug=True)