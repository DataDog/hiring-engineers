Datadog Solutions Engineer Challenge
Owen Cummings

Q: Collecting Metrics

Added tags in the Agent and recieved the tags from Host Map as below.
![My image](https://i.imgur.com/C5X5Lo0.png)
![My image](https://i.imgur.com/N1Dwx6d.png)


MongoDB was already installed on my machine, so I ran this in the mongo shell to activate it on the host device. Notified of integration success the Datadog WebApp.
![My image](https://i.imgur.com/QmeFfm7.png)


Created the two following files at the required locations.
![My image](https://i.imgur.com/omdHdKG.png)
![My image](https://i.imgur.com/9MaDW6X.png)



Q: Visualizing Data

I used the API .py file in this repository to generate the following dashboard. I could find no documentation on the anomaly function and I assume that it isn't working. I read something about using anomalies in monitors but decided not to pursue it since it seemed off-task. The MongoDB metric is there, it's just a low value. Here is the code I used to make the API request.

'''

from datadog import initialize, api

options = {
    'api_key': 'aaf2a348158cadcc3879184d80500418',
    'app_key': '759aa880aeb746f779317e7de7431157207a9b37'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*} by {host}"},
            {"q": "mongodb.network.numrequestsps{*}.anomaly()"},
            {"q": "my_metric{*}.rollup(avg, 300)"}
        ],
    "viz": "timeseries"
    },
    "title": "Metrics"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

'''

![My image](https://i.imgur.com/2Vjup6U.png)



Q: Monitoring Data

I set the following alert/downtime conditions and recieved the appropriate emails.

![My image](https://i.imgur.com/cM1kZk8.png)
![My image](https://i.imgur.com/5sJd7Zw.png)
![My image](https://i.imgur.com/yFrL8nl.png)
![My image](https://i.imgur.com/qySnFnI.png)
![My image](https://i.imgur.com/PNboapl.png)
![My image](https://i.imgur.com/TAzufzm.png)




Q: Collecting APM Data

I ran into some issues with this. I'm pretty sure my implementation is correct: I installed dd-trace and tried doing both dd-trace run python file.py AND putting in the middleware, separately like suggested. I ran into some errors with the Flask dependencies and fixed those up. I ran the file again and it appeared to work. File is in this repo. 

![My image](https://i.imgur.com/wer0W2X.png)

But nothing was showing up as being traced in the DD web app. I discovered that I needed to set apm_enabled: yes in the agent's config file, so I did that. However I ran into an issue where the agent would not restart, giving me the following error, even when I restarted my machine.

![My image](https://i.imgur.com/l5my8sx.png)

This error seemed pretty ambiguous to me, and I couldn't find any way to resolve it. I felt like the way I did everything was fine. It is sad that I couldn't manage to find the solution to this, but it seemed beyond the scope of the exercise. Here is the code I used, with commented middleware for the other approach.

'''
from flask import Flask
#import blinker as _
import logging
import sys

#from ddtrace import tracer
#from ddtrace.contrib.flask import TraceMiddleware

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

#traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run()


'''

Conventionally, services refer to 'actions' - allowing certain operations or functions on data. Resources refer to 'nouns' - allowing the accessing and defining of certain data types or configurations.



Q: Datadog Uses

What's nice about Datadog is that it's great for monitoring and modeling any type of large system. Partnering with an ISP to see how much open networks can make a difference or see how we can improve routing would be a cool, though involved, project.





Sources:
I mostly referenced the following documentation.

http://pypi.datadoghq.com/trace/docs/#
https://docs.datadoghq.com/guides/monitors/
https://docs.datadoghq.com/guides/tagging/
https://docs.datadoghq.com/guides/agent_checks/
https://docs.datadoghq.com/graphing/#rollup-to-aggregate-over-time
