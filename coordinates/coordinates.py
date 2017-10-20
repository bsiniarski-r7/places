import shapely.geometry
import pyproj
import json
import requests
from geopy.distance import vincenty
import logging
import time
from logentries import LogentriesHandler
import logging


log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler('56926f61-286f-4224-9ff3-e23ebfa858f6'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_PLACES = "AIzaSyDHoS63IY3s5KczZujHBhhl70mrQLVo-QE"
API_GEOCODING = "AIzaSyDOlH5P4SiOy7FqVqqNxu03KIWWm4ucRJM"

#Make a call and get a response. Check if response is OK. If not, give reason.
def getResponse(lat,lng,api):
    request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s" % (lat, lng, api))

    reply = json.loads(request.text.encode('ascii', 'ignore'))
    return reply


#Find out what country it is.
def getCountry(reply):
    country_found = False

    if len(reply['results']) >0:
        #1. Find how many field are there in address_components
        number_fields = len(reply['results'][0]['address_components'])
        #2. Iterate over all fields
        for i in range(0,number_fields):
            #3. Search for country field
            if 'country' in reply['results'][0]['address_components'][i]['types']:
                country_found = True
                return reply['results'][0]['address_components'][i]['short_name']

        #4. Make sure the country was found. If not, log.
        if country_found == False:
            logger.info('Country not found')

#Check if country found is within wanted borders
def isCountry(country_searched, country_found):
    if country_searched == country_found:
        return True
    else:
        return False

def createGrid():
    # Set up projections
    p_ll = pyproj.Proj(init='epsg:4326')
    p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

    # Create corners of rectangle to be transformed to a grid
    nw = shapely.geometry.Point((49.151536, 15.192732))
    se = shapely.geometry.Point((54.944651, 23.795426))

    #Stepsize 100000 = 64km (77 map points)
    #Stepsize 10000 = 6.4km (6,630 map points)
    #Stepsize 7812.5 = 5km (10,873 map)
    #Stepsize 1562.5 = 1km (268,863 map points)


    stepsize = 7812.5 # 5 km grid step size

    # Project corners to target projection
    s = pyproj.transform(p_ll, p_mt, nw.x, nw.y) # Transform NW point to 3857
    e = pyproj.transform(p_ll, p_mt, se.x, se.y) # .. same for SE

    # Iterate over 2D area
    gridpoints = []
    x = s[0]
    while x < e[0]:
        y = s[1]
        while y < e[1]:
            p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
            gridpoints.append(p)
            #print(len(gridpoints))
            y += stepsize
        x += stepsize

    return gridpoints

###### MAIN ######

file = open('poland_coordinates.txt','w')
coordinates = createGrid()

for i in range(0,len(coordinates)-1):
    data = getResponse(coordinates[i].x, coordinates[i].y,API_GEOCODING)


    while (data['status'] == 'OVER_QUERY_LIMIT'):
        logger.info('Quota exceeded, going to sleep for an hour')
        time.sleep(3600)
        logger.info('Waking up. Checking if quota is renewed')
        data = getResponse(coordinates[i].x, coordinates[i].y,API_GEOCODING)
        print(i)


    if isCountry('PL', getCountry(data)) == True:
        file.write(str(coordinates[i].x) + ',' + str(coordinates[i].y) + '\n')
        log.info(str(i)+"/"+str(len(coordinates)-1))

    #Make sure we don't go over 2500 quota
    time.sleep(10)

file.close()
