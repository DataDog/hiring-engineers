#3 #I used stackoverflow.com for help with this 
from checks import AgentCheck
import random

class HTTPCheck(AgentCheck):
    def check(self, instance):
        if 'url' not in instance:
            return
        self.count("my_metric", random.randint(0,1000))

#4 #I used stackoverflow.com for help with this 

from checks import AgentCheck
import random
import sched, time
s = sched.scheduler(time.time, time.sleep)

class HTTPCheck(AgentCheck):
    def check(self, instance):
        if 'url' not in instance:
            return
        self.count("my_metric", random.randint(0,1000))
        s.enter(45, 1, AgentCheck, (sc,))

s.enter(45, 1, AgentCheck, (s,))
s.run()

#Visualizing Data 

#1 - Your custom metric scoped over your host. I utilizied what I read
#on the Datadog Docs 

from datadog import initialize, api

options = {
    'api_key': '724921d3eadbe519e5f103efdb6052d5',
    'app_key': '724921d3eadbe519e5f103efdb6052d5'
}

initialize(**options)

title = "Jason Timeboard"
description = "Timeboard for DD Exercise"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only,
                     my_metric= my_metric)
                    #inclusion of my_metric

#2 Any metric from the Integration on your Database with the anomaly function applied.

from datadog import initialize, api

options = {
    'api_key': '724921d3eadbe519e5f103efdb6052d5',
    'app_key': '724921d3eadbe519e5f103efdb6052d5'
}

initialize(**options)

title = "Jason Timeboard"
description = "Timeboard for DD Exercise"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only,
                     my_metric= my_metric)
#for this one I'm not sure where to include the Anomaly function





