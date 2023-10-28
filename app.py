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

@app.route('/models/location', methods=['GET', 'POST'])
def _get_user_location():
    if request.method == "GET":
        location = request.args.get("latitude", "longitude")
        print("check", location)
    return location

def get_user_location():
    ip_response = requests.get("https://ipinfo.io")
    loc = ip_response.json()["loc"]
    print("check", loc)
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
    coords = get_user_location()
    latitude, longitude = coords.split(',')
    url_params = {
    'term': "food",
    'latitude': latitude,
    'longitude': longitude,
    'limit': YELP_SEARCH_LIMIT,
    'radius': 25 
    }
    return _request(YELP_HOST, SEARCH_PATH, yelp_api_key, url_params)

def chatbot():
  # Create a list to store all the messages for context
  messages = []

  # Keep repeating the following
  while True:
    # Prompt user for input
    message = input("User: ")
    # Exit program if user inputs "quit"
    if message.lower() == "quit":
        break

    # Add each new message to the list
    messages.append({"role": "user", "content": message})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    # Print the response and add it to the messages list
    chat_message = response['choices'][0]['message']['content']
    print(f"Bot: {chat_message}")
    messages.append({"role": "assistant", "content": chat_message})

if __name__ == '__main__':
    app.run(debug=True)
