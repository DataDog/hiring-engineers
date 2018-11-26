import requests
from datetime import datetime, date, time
import time as t
import json
with open('2018_11.json') as json_file:
    json_data = json.load(json_file)

myit = iter(json_data)

for item in json_data:
	
	#print (item['text'])
	#"2013-12-30 23:00:00 +0000",
	secs = datetime.strptime(item['created_at'][0:19], "%Y-%m-%d %H:%M:%S").strftime('%s')
	splitItem = item['text'].split(' ')
	#print("Length:"+ str(len(splitItem)) )
	if len(splitItem) >= 6:
		ww = splitItem[2]
		#print( secs)
		metricWW = '{"metric":"WW Usage kWh","points":[['+secs+','+ww+']],"type":"gauge","interval":20,"host":"raspberrypi","tags":["environment:test"]}'
		#print(metricWW)
		hz = splitItem[5]
		#print(hz)
		metricHZ = '{"metric":"HZ Usage kWh","points":[['+secs+','+hz+']],"type":"gauge","interval":20,"host":"raspberrypi","tags":["environment:test"]}'
		#print(metricHZ)
		series = '{"series":['+metricWW+','+metricHZ+']}'
		print(series)
		response = requests.post(
		url="https://api.datadoghq.eu/api/v1/series",
		params={
				 "api_key": "d3086d9ee6433b3af5e47a2eb5485abf",
		},
		headers={
			 "Content-Type": "application/json",
		},
		#data=json.dumps(series)
		data=series
		)
		print('Response HTTP Status Code: {status_code}'.format(
			 status_code=response.status_code))
		print('Response HTTP Response Body: {content}'.format(
			 content=response.content))
		t.sleep(0.5)