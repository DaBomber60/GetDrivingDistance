import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="email")

testAddress = "addressHere"

def getCoords(address):
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return lat, lon

def main():
    lat, lon = getCoords(testAddress)
    print (lat)
    print (lon)
    

if __name__ == "__main__":
    main()

    