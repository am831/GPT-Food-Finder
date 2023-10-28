from flask import Flask, jsonify
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/test')
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/location')
def get_user_location():
    ip_response = requests.get("https://ipinfo.io")
    user_ip = ip_response.json()["ip"]
    geolocator = Nominatim(user_agent="https://query-csv.streamlit.app/")
    location = geolocator.geocode(user_ip)
    return jsonify({"City:": location}, {"ip": user_ip})

if __name__ == '__main__':
    app.run()