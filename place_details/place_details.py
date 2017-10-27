import json
import requests
import logging
import time
from logentries import LogentriesHandler
import logging
from place import *
log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler('56926f61-286f-4224-9ff3-e23ebfa858f6'))
API_PLACES = "AIzaSyDHoS63IY3s5KczZujHBhhl70mrQLVo-QE"



def getDetails(id, api):
    request = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" % (id.rstrip(), api))
    reply = json.loads(request.text.encode('ascii', 'ignore'))
    print reply
    return reply

def createPlace(details):
    new_place = Place()

    if details['result']['place_id']:
        new_place.set_place_id(details['result']['place_id'])

    if details['result']['types']:
        new_place.set_types(details['result']['types'])

    if details['result']['geometry']['location']:
        new_place.set_location(str(details['result']['geometry']['location']['lat']) + "," + str(details['result']['geometry']['location']['lng']))

    print(new_place.location)

ids = open("output_data/test_ids", "r")

for each in ids:
    createPlace(getDetails(each, API_PLACES))
