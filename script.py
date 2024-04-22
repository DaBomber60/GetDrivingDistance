import json
import pandas as pd
from geopy.geocoders import Nominatim
import urllib.request
from flatten_json import flatten
import time
import csv

#This script calculates the total distance to all appointments in a given CSV file, and writes the results to a new CSV file with the address, distance, and client name for each appointment. It uses the Open Source Routing Machine API to calculate driving distances.

geolocator = Nominatim(user_agent="your_user_agent_here") #Nominatim likes you to use your email in case of overuse of the API

addressFile = "appointments.csv"

startAddress = "1 Fleet Street, London, UK" #Your address here

tripsFields = ['Address', 'Distance', 'Client Name']
tripsRows = []

def loadAddresses():
    addressdf = pd.read_csv(addressFile)
    return addressdf

    #print(addressdf.to_string())

def getCoords(address):
    #gets coordinates for given address
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return lat, lon

def getDriveDistance(lat, lon):
    #gets driving distance from start address to given lat/lon
    startAddressLat, startAddressLon = getCoords(startAddress)
    with urllib.request.urlopen(f"https://router.project-osrm.org/route/v1/car/{startAddressLon},{startAddressLat};{lon},{lat}?overview=false") as url:
        route = json.load(url)
        flattened = flatten(route)
        distancem = flattened['routes_0_distance']
        distance = round(distancem/1000,2)
        return distance

def main():
    #calculates total distance for all appointments
    totalDistance = 0
    addressdf = loadAddresses()
    for i in addressdf.index:
        lat, lon = getCoords(addressdf.at[addressdf.index[i],'address'])
        distance = getDriveDistance(lat, lon)
        totalDistance += distance
        tripsRows.append([str(addressdf.at[addressdf.index[i],'address']), str(distance), str(addressdf.at[addressdf.index[i],'client_name'])])
        print("Adding trip " + str(i+1), end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(". Done!")
    totalDistance = round(totalDistance,2)
    print("The total distance to all appointments is " + str(totalDistance) + "km, for a total rount trip distance of " + str(totalDistance*2) + "km!")
    with open('trips.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(tripsFields)
        write.writerows(tripsRows)

if __name__ == "__main__":
    main()
