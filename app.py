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
    loc = ip_response.json()["loc"]
    city = ip_response.json()["city"]

    return jsonify({"ip": user_ip}, {"Coords": loc}, {"city": city})
  

if __name__ == '__main__':
    app.run()