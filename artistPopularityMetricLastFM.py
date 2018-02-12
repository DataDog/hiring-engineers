import json 
import requests

from datetime import datetime,timedelta
from datadog import initialize, api

# initialize datadog api connection parameters
options = {
    'api_key' : 'd81b4c03c052be98c0b368cf8606ba68',
    'app_key' : '122313caaf83fb325fa1aa0482f2ab9d9d3e6125'
}
initialize(**options)

# send metrics to Datadog
def ddPost(mymetric,myvalue,mytags,ts):
    api.Metric.send(metric=mymetric, points=(ts/1000, myvalue), tags=mytags)

# get current epoch timestamp
def getEpoch():
    end_time = datetime.now()
    end_time = end_time - timedelta(seconds=end_time.second,microseconds=end_time.microsecond)
    tdelta = timedelta(seconds=60)
    start_time = end_time - tdelta
    start_epoch = int(start_time.strftime('%s')) * 1000
    end_epoch = int(end_time.strftime('%s')) * 1000
    return(start_epoch, end_epoch)

# Datadog API key
API_KEY = "0108d1afcd40db5dbe8e71f528c18c58"

# last.fm API 
api_root = "http://ws.audioscrobbler.com/2.0/"
api_artist_getInfo = "?method=artist.getinfo"
api_format = "&format=json"
api_key = "&api_key=" + API_KEY

artists = [
	'Anderson%20.Paak',
	'Bill%20Evans',
	'Bruno%20Mars',
	'Cyhi%20the%20Prynce',
	'Jay-Z',
	'John%20Coltrane',
	'Kanye%20West',
	'Kendrick%20Lamar',
	'Miles%20Davis',
	'Nina%20Simone',
	'Thelonious%20Monk'
]

# loop through list of artists
for a in artists:
	# build web API URL per artist
	url = api_root + api_artist_getInfo + api_key + api_format + '&artist=' + a
	#print (url)

	r = requests.get(url) 
	try:
		r.raise_for_status()
	except requests.exceptions.HTTPError as e:
		# status was non-200
		print ("Error: " + str(e))
		break

	data = json.loads(r.content)

	if data is not None:

		# get artist's name
		artist_name = data['artist']['name']
		print ("artist name: " + artist_name)

		# get artist's playcount
		artist_playcount = data['artist']['stats']['playcount']
		print ("playcount: " + artist_playcount)

		# get artist's listeners count:
		artist_listeners = data['artist']['stats']['listeners']
		print ("listeners: " + artist_listeners)

		# send data to Datadog

		# get current epoch timestamp
		interval = getEpoch()
		start_time = interval[0]
		end_time = interval[1]

		# tag metric with artist's name 
		ddtags = "artist:" + artist_name

		ddmetric="hvd.listeners"
		ddPost(ddmetric, artist_listeners, ddtags, start_time)

		ddmetric="hvd.playcount"
		ddPost(ddmetric, artist_playcount, ddtags, start_time)
	else:
		print ("Warning: data object is empty, not sending metrics to Datadog")
