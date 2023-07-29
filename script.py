import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim
import urllib.request
from flatten_json import flatten

geolocator = Nominatim(user_agent="email")

testAddress = "addressHere"

homeAddressLat = lat
homeAddressLon = lon

trips = []

def getCoords(address):
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return lat, lon

def getDriveDistance(lat, lon):
    with urllib.request.urlopen(f"https://router.project-osrm.org/route/v1/car/{homeAddressLon},{homeAddressLat};{lon},{lat}?overview=false") as url:
        route = json.load(url)
        flattened = flatten(route)
        distancem = flattened['routes_0_distance']
        distance = round(distancem/1000,2)
        return distance


def main():
    lat, lon = getCoords(testAddress)
    distance = getDriveDistance(lat, lon)
    print(str(distance) + "km to " + testAddress)
    

if __name__ == "__main__":
    main()

    