#This script is used to get all ids from a certain category for given coordinates

import json
import requests
import logging
import time
from logentries import LogentriesHandler
import logging
log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler('56926f61-286f-4224-9ff3-e23ebfa858f6'))
API_PLACES = "AIzaSyDHoS63IY3s5KczZujHBhhl70mrQLVo-QE"


types = []
coordinates = []
ids = []


business_types = open("input_data/types", "r")
poland_coordinates = open("input_data/poland_coordinates.txt", "r")

log.info("Starting to build the array of types")
for type in business_types:
    types.append(type)
log.info("Finished the array of types")

log.info("Starting to build the array of coordinates")
for coordinate in poland_coordinates:
    coordinates.append(coordinate)
log.info("Finished the array of coordinates")

#At this stage, each coordinate and type is pushed into array and we should start building the database of identifiers
#Make a call and get a response. Check if response is OK. If not, give reason.
def getMultipleIDS(coordinate,radius,api):
    request = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&key=%s" % (coordinate, radius, api))
    ids = []
    reply = json.loads(request.text.encode('ascii', 'ignore'))
    log.info("Found: " + str(len(reply['results'])) + "locations (not unique)")

    for each in range(0,len(reply['results'])-1):
        ids.append(reply['results'][each]['place_id'])

    #Return multiple IDS for that coordinate
    return ids

def aggregateIDS(locations):


    location_counter = 1

    for location in locations:
        #Save collective ids to file
        file = open('output_data/ids','a+')

        log.info("Location: " + str(location))
        retrieved = getMultipleIDS(location, "5000", API_PLACES)

        total_count = 0
        unique_count = 0
        for each in retrieved:
            total_count = total_count + 1
            if each not in ids:
                ids.append(each)
                file.write(str(each) + '\n')
                unique_count = unique_count + 1

        log.info("Total IDs found: " + str(total_count) + " out of which " + str(unique_count) + " were unique.")
        log.info("Number of IDS currently in the list: " + str(len(ids)) + " ... moving to next location")

        print(str(location_counter) + "/" + str(len(locations)))
        location_counter = location_counter + 1

        file.close()

aggregateIDS(coordinates)
