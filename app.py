from flask import Flask, jsonify
import requests
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)

with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        os.environ[key] = value

# Get the API key from the environment variable
yelp_api_key = os.environ.get("YELP_API")
headers = {'Authorization': 'Bearer {}'.format(yelp_api_key),'accept': 'application/json'}

@app.route('/test')
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/location')
def get_user_location():
    ip_response = requests.get("https://ipinfo.io")
    
    user_ip = ip_response.json()["ip"]
    loc = ip_response.json()["loc"]
    city = ip_response.json()["city"]

    return jsonify({"ip": user_ip}, {"Coords": loc}, {"city": city})
  

@app.route('/business/<business_id_or_alias>')
def get_by_id(business_id_or_alias):
    """ Getting business details from id or alias
    Arg:
        business_id_or_alias(str): The business alias (i.e. yelp-san-francisco) or
                ID (i.e. 4kMBvIEWPxWkWKFN__8SxQ.
    
    """
    business_path = f'https://api.yelp.com/v3/businesses/{business_id_or_alias}'
    business_response = requests.get(business_path, headers=headers)
    return business_response.json()

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