Part 1

Signed up with the email mbabineau@gmail.com

The agent is the utility that does the communication back to DataDog's servers. There seem to be 2 different parts that do the communication. There is a collector that waits for data and there is the forwardard that sends the data. Then there is the stats server that allows custom configuration of metrics that are sent the DataDog. 

I submitted an api using the following code.

from dogapi import dog_http_api as api

api.api_key='673c9ffe6dXXXXXXXXXXXXXXXXXXa'
api.application_key='a63b95ef42b4bXXXXXXXXXXXXXXXe88b5cfd212a'

title = "ALERT!"
text = "Here is a description of the broken server connection"
tags = ["myDataServer", "application:web"]

api.event_with_response(title,text,tags=tags)


Level 2

1. Implemented simple hello world web app using webpy. 

2. Used ab to create lots of page loads - here is the screen shot -  https://app.datadoghq.com/dash/dash/32280?from_ts=1416171044522&to_ts=1416171525000&tile_size=m

3. my histogram collects its data from a database.query.time.avg metric - https://app.datadoghq.com/dash/dash/32280?from_ts=1416171044522&to_ts=1416171525000&tile_size=m

4. coming back after finishing the other stuff.

5. ''

Level 3

I implented 2 pages and graphed their latency in a stacked graph with 2 different colors - https://app.datadoghq.com/dash/dash/32280?from_ts=1416252192909&to_ts=1416252855636&tile_size=m

Level 4

1. 615 page views total
2. https://app.datadoghq.com/dash/dash/32280?from_ts=1416252192909&to_ts=1416252855636&tile_size=m
3. https://app.datadoghq.com/graph/embed?from_ts=1416169540298&to_ts=1416255940298&token=d4343b66bfa9cdc77aa0894147f26b0c4f8c66ebe7416dd32fb86bcebc913c5e&height=300&width=600&legend=true&tile_size=m&live=true
4. My guess as to their spikeyness is not running ab all day long. If this was real site with a pretty constant flow of traffic it would be much more predictable. 

Level 5
