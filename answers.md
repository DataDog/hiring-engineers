Brian Carbonette
Support Engineer Challenge


Level 1

The agent is in charge of starting the Supervisor and making sure that the statsd, forwarder and collector are up and running.
Carbs          60768   0.0  0.0  2433432    872   ??  S     5:23PM   0:00.01 sh /Users/Carbs/.datadog-agent/bin/agent

I had to install the binary agent since I couldn't sudo or gain root access on my bluehost VPS web server.  
I also had to manually adjust 'minprocs' to a lower number than 200 since that was the max amount allowable on bluehost.
agent/packaging/datadog-agent-deb/supervisor.conf:minprocs = 100 
agent/packaging/datadog-agent-rpm/supervisor.conf:minprocs = 100
100 seemed to work fine.  The supervisor procs time out on me every hour though.
2013-10-20 22:10:37,343 INFO success: collector entered RUNNING state, process has stayed up for > than 2 seconds (startsecs)
2013-10-20 22:10:38,344 INFO success: dogstatsd entered RUNNING state, process has stayed up for > than 3 seconds (startsecs)
2013-10-20 22:10:38,345 INFO success: forwarder entered RUNNING state, process has stayed up for > than 3 seconds (startsecs)
2013-10-20 23:10:34,608 INFO stopped: collector (exit status 0)
2013-10-20 23:10:34,610 INFO stopped: forwarder (exit status 0)
2013-10-20 23:10:34,661 INFO stopped: dogstatsd (exit status 0)

Easy_Install with OSx agent worked great. No timeout issues on the Mac.

api.event_with_response(title, text, tags=tags) where including @briancarbs@gmail.com in the text will send an api triggered event to
my inbox.

Level 2

Link to ab page_views/sec on index.html
https://s3.amazonaws.com/dd-snapshots-prod/org_6571/2013-10-21/e66a9ca564935070244e02b65c73aacca2c968d7.png

Link to ab page_views/sec on about.html 
https://s3.amazonaws.com/dd-snapshots-prod/org_6571/2013-10-21/76050225075d0620050b2967293be12558d75a2e.png

(still need to do histogram)



Level 3

to tag support... statsd.increment('about.page_v', 10, tags=['support'])
support tag chart...

overlaid metrics using tag and host... statsd.increment('about.page_v, 10, tags=['about:about.html])
https://s3.amazonaws.com/dd-snapshots-prod/org_6571/2013-10-21/5b11c1b90eab25ca783ee521db603ec37a70a1af.png

(still need to visualize latency with diff colors)

Level 4

I implemented a .cgi python script that gets "onloaded" by javascript upon page loads to create a page view counter that
can be distinguished by tag.  Here's the .cgi code...

"#!/usr/bin/python"                                                                      //so cgi knows where to load python interp
print("Content-Type: text/plain\n\n")   

from statsd import statsd							      //import statsd and dogapi lib
from dogapi import dog_http_api as api              
api.api_key = 'a87f80079d0fccc4eded3f079f7b605e'				//set api keys for good measure
api.application_key = '576ef5c9e5d44b6e2f01e06420111666ec5a1007'
statsd.increment('home.page_v', 10)						//inc page view normalized to 1 view/sec 
print("It worked!")

Javascript that runs the cgi in each html (about.html/index.html) is triggered by <body onload="pageView()"> 

separate .cgi file for eeach page http://briancarbonette.com/dogstatsd-python/inc_pv.cgi

statsd.increment('home.page_v', 10, tags=['home:index.html'])

http://briancarbonette.com/dogstatsd-python/inc_pv_about.cgi
statsd.increment('about.page_v', 10, tags=['about:about.html'])

I think the graphs are spikey because we are using an average maybe an ewma_x() will smooth it out.

Level 5
(still need to do this)
