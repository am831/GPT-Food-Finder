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
    city = ip_response.json()["city"]
    return loc, city

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
    coords, city = _get_user_location()
    url_params = {
    'term': "dinner",
    'location': coords.replace(' ', '+'),
    'limit': YELP_SEARCH_LIMIT
    }
    return _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)

# @app.route('/business/search/<phone>')
# def get_business_location(phone):
#     """ Getting business location from phone number
#         could have multiple location returned 
#     Arg:
#         phone(str): It must start with + and include the country code, like +14159083801.
#     """
#     # headers = {'Authorization': 'Bearer {}'.format(MY_API_KEY),'accept': 'application/json'}
#     business_path = 'https://api.yelp.com/v3/businesses/search/phone'
#     business_response = requests.get(business_path, headers=headers)
#     return business_response.json()
if __name__ == '__main__':
    app.run(debug=True)