import requests
import json


########## function doc ##########

def reverseGeo(address, APIKey='AIzaSyARjslgIhWFOwKTo3lKbl2zXt5_kwAHC-4'):

	BASE_URL = 'https://maps.googleapis.com/maps/api'
	GEOCODE_API_URL = BASE_URL + '/geocode/json?'

	r = requests.get(GEOCODE_API_URL + '&address=' + address)

	if(r.status_code == 200):
		json_result = r.json()
		return json_result['results'][0]['geometry']['location']

	else:
		print 'something wrong with input'
		return {}
	

###################################


########## function doc ###########
## 
def getPlaceAPI(loc, APIKey='AIzaSyARjslgIhWFOwKTo3lKbl2zXt5_kwAHC-4'):

	lat = loc['lat']
	lon = loc['lng']

	BASE_URL = 'https://maps.googleapis.com/maps/api'
	PLACE_URL = BASE_URL + '/place'
	NEARBY_SEARCH_API_URL = PLACE_URL + '/nearbysearch/json?'
	RADAR_SEARCH_API_URL = PLACE_URL + '/radarsearch/json?'
	DETAIL_API_URL = PLACE_URL + '/details/json?'

	rankby = 'distance'
	types = 'food'
	radius = '1000'

	print [str(lat), str(lon)]

	r = requests.get(RADAR_SEARCH_API_URL ## the searching type ## 
					+ 'location=' + str(lat) + ',' + str(lon) 
					+ '&radius=' + radius
					+ '&type=' + types
					+ '&key=' + APIKey)

	print r.status_code

	if(r.status_code == 200):

		json_result = r.json()['results']
		json_result_list = []

		print len(json_result)

		for place in json_result:

			place_lat = place['geometry']['location']['lat']
			place_lon = place['geometry']['location']['lng']
			place_id = place['id']
			place_placeID = place['place_id']
			#place_name = place['name']

			temp = {
					'lat' : place_lat,
					'lon' : place_lon,
					'id' : place_id,
					'place_id' : place_placeID,
					#'name' : place_name
					}

			## find the detailed information ##
			json_result_list.append(temp)

		return json_result_list

	else:
		print 'something wrong with input'
		return {}

###################################

########## function doc ###########
## 

def getPlaceDetail(places, APIKey='AIzaSyARjslgIhWFOwKTo3lKbl2zXt5_kwAHC-4'):

	BASE_URL = 'https://maps.googleapis.com/maps/api'
	PLACE_URL = BASE_URL + '/place'
	DETAIL_API_URL = PLACE_URL + '/details/json?'

	for i in range(len(places)):

		place_id = places[i]['place_id']
		r = requests.get(DETAIL_API_URL ## the searching type ## 
					+ '&placeid=' + place_id
					+ '&key=' + APIKey)
		json_result = r.json()['result']

		places[i]['address'] = json_result['formatted_address']
		places[i]['name'] = json_result['name']

		if('website' in json_result):
			places[i]['website'] = json_result['website']
		else:
			places[i]['website'] = ''

		if('url' in json_result):
			places[i]['url'] = json_result['url']
		else:
			places[i]['url'] = ''

		if('icon' in json_result):
			places[i]['icon'] = json_result['icon']
		else:
			places[i]['icon'] = ''

	return places

def writeInJSON(resJSON, outfileName):
	with open(outfileName, 'w') as outfile:
	    json.dump(resJSON, outfile, indent=4, sort_keys=True)
	print 'finished writing'

###################################



res = reverseGeo('Green Street, Urbana, IL, USA')
print res

res2 = getPlaceAPI(res)
res3 = getPlaceDetail(res2)
print "finished gathering information from Google"

writeInJSON(res3, 'data.txt')

#print res2


