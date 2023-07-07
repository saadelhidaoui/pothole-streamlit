from flask import Flask, jsonify, request
import csv
import pandas as pd
import json
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="http")

# POST request to store data in detections.csv
@app.route('/add_detections', methods=['POST'])
def add_detections():
    image = 'image'
    lat = request.form['lat']
    lon = request.form['lon']
    nb_potholes = request.form['nb_potholes']
    #date = request.form['date']
    coord = f"{lat}, {lon}"
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    city = address["city"]
    region = address["state"]
    country = address["country"]
    date = ""

    with open('/home/SaadEL00/potholes/detections.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image,lat, lon, nb_potholes,date, city, region, country])

    return jsonify({'message': 'Data added successfully!'})

# GET request to retrieve all data from detections.csv
@app.route('/get_detections', methods=['GET'])
def get_detections():
    data = []
    with open('/home/SaadEL00/potholes/detections.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    json_data = json.dumps(data, indent=4)
    return json_data

if __name__ == '__main__':
    app.run(port = 8800)