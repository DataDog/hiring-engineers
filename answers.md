
Level 1

-what is the agent?
An agents job is to  collect events and metrics from your host to datadog. 
-Event Submited via api:
https://app.datadoghq.com/event/event?id=413417324575025951
http://imgur.com/mliiWBr
-Event sent via email:
http://imgur.com/K4GcRzn

Level 2 & 3 & 4

I used datadog-metrics - Node.js API client in app.js. Tsung load test saved to config.xml.
Dashboard link: https://app.datadoghq.com/dash/100146/page-views?live=true&page=0&is_auto=false&from_ts=1456429561340&to_ts=1456433161340&tile_size=m
screenshot - Histogram: http://imgur.com/cZxqKU0
screenshot - Pageviews: http://imgur.com/3aL2UsX
screenshot - Latency: http://imgur.com/ek5vqWW
screenshot - Dashboard: http://imgur.com/U2d2LUo
-do you know why the graphs are very spiky?
Each spike represents a large group of users. Each dip is a lower amount of users. The number of users generated in the load test is is a random amount of users. 

Level 5
Its saved in random.py and random.yaml
screenshot: http://imgur.com/SZ16i2P
link: https://app.datadoghq.com/dash/102101/random-number-sample?live=true&page=0&is_auto=false&from_ts=1456431089050&to_ts=1456434689050&tile_size=m


