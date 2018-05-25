## Introduction
Hi, I'm Jordan Storms. For this challenge I used Linux Mint 18.3.

## Collecting Metrics

#### Adding a tag
In order to add a tag we need to customize the datadog.yaml file, located at etc/datadog-agent/datadog.yaml. Open the file with your editor of choice and add a tag as shown in the screenshot below:

<a href="https://www.flickr.com/photos/158412660@N04/42261444992/in/dateposted/" title="Gedit-tag"><img src="https://farm1.staticflickr.com/954/42261444992_7322386909_z.jpg" width="640" height="498" alt="Gedit-tag"></a>

Once this is saved, restart the datadog agent for the changes to update: ```sudo service datadog-agent restart```

After a few moments, the datadog dashboard will display your newly added tags in infrastructure -> host as shown below:

<a href="https://www.flickr.com/photos/158412660@N04/42261445672/in/dateposted/" title="Infrastructure-Tag"><img src="https://farm1.staticflickr.com/977/42261445672_f95721ea22_z.jpg" width="640" height="529" alt="Infrastructure-Tag"></a>

[A link to my dashboard host map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=485640810)

#### Linking with MongoDB
With MongoDB installed on the machine, adding the datadog integration is outlined [here](https://docs.datadoghq.com/integrations/mongo/). *Note: while following these instructions you may need to create the conf.yaml file in /etc/datadog-agent/conf.d/mongo.d*. The file should look like this once completed: 

<a href="https://www.flickr.com/photos/158412660@N04/40505072750/in/dateposted/" title="mongo-conf"><img src="https://farm1.staticflickr.com/962/40505072750_b42b888a6d_z.jpg" width="640" height="498" alt="mongo-conf"></a>

Once this file is saved, restart the datadog-agent again: ```sudo service datadog-agent restart```. Like before, after a few minutes the dashboard should refresh and your MongoDB metrics should be viewable: 

<a href="https://www.flickr.com/photos/158412660@N04/40505109150/in/dateposted/" title="mongo-dash"><img src="https://farm1.staticflickr.com/957/40505109150_33a10bd436_z.jpg" width="640" height="454" alt="mongo-dash"></a>

My dashboard with MongoDB metrics can be found [here](https://app.datadoghq.com/dash/host/485640810?live=true&page=0&from_ts=1527109051020&to_ts=1527123451020&is_auto=false&tile_size=m)

#### Creating a custom check
To create a custom check we need to add a python script in /etc/datadog/checks.d and a config (yaml) file in /etc/datadog/conf.d. In this example I used mycheck.py and mycheck.yaml which is included in the code folder in this branch. 

<a href="https://www.flickr.com/photos/158412660@N04/40521358110/in/photostream/" title="mycheck"><img src="https://farm1.staticflickr.com/962/40521358110_31b3113fbe_z.jpg" width="640" height="199" alt="mycheck"></a>

To only send the metric at an interval of 45 seconds without altering the python file, simply add: ```min_collection_interval: 45``` to the instances section of the config file as shown above (**bonus question**).

After some time the changes will show in the dashboard and the metric can be viewed by going to infrastructure -> host as shown here:

<a href="https://www.flickr.com/photos/158412660@N04/40521356690/in/dateposted/" title="my-metric-host"><img src="https://farm1.staticflickr.com/882/40521356690_02f63bc67a_z.jpg" width="584" height="640" alt="my-metric-host"></a>

Clicking on the ((no-namespace) dashboard) link brings you [here](https://app.datadoghq.com/dash/integration/custom?live=true&tpl_var_scope=host%3Ajordans-pc&page=0&is_auto=false&from_ts=1527185954883&to_ts=1527189554883&tile_size=m):
<a href="https://www.flickr.com/photos/158412660@N04/40521357180/in/dateposted/" title="my_metric"><img src="https://farm1.staticflickr.com/968/40521357180_72b63db753_z.jpg" width="640" height="323" alt="my_metric"></a>

## Visualizing Data

Before moving forward, I had to request an app api key for access to datadog api  and install the datadog python package. The python script I created can be found in the code folder of this branch. The resulting timeboard is shown below and can be found [here](https://app.datadoghq.com/dash/820253/jordans-timeboard?live=false&page=0&is_auto=false&from_ts=1527200945943&to_ts=1527201245943&tile_size=m&fullscreen=false).

<a href="https://www.flickr.com/photos/158412660@N04/28459451498/in/dateposted/" title="my-timeboard"><img src="https://farm1.staticflickr.com/966/28459451498_5900a3d672_z.jpg" width="614" height="640" alt="my-timeboard"></a>

To take a snap shot click the camera icon as shown below:

<a href="https://www.flickr.com/photos/158412660@N04/28459451498/in/dateposted/" title="my-timeboard"><img src="https://farm1.staticflickr.com/966/28459451498_5900a3d672_z.jpg" width="614" height="640" alt="my-timeboard"></a>

Finally annotate as shown below:

<a href="https://www.flickr.com/photos/158412660@N04/28459451308/in/dateposted/" title="tag-timeboard"><img src="https://farm1.staticflickr.com/971/28459451308_85390d7a3d.jpg" width="481" height="304" alt="tag-timeboard"></a>

#### Bonus Question
The anomaly function is designed to show if a metric is falling outside a defined threshold of standard deviations within a defined window of time. This is important to see when a metric is behaving differently. In my example, I use basic detection with a standard deviation of 2, but the available connections of my metric are steady.


## Monitoring Data
Since I used the api to create a timeboard, I wanted to use the UI to create the monitor.

A new monitor can be created by going to the manage monitor page and clicking on New Monitor. You can then fill in the approriate information to create your monitor as shown below and the monitor can be found [here](https://app.datadoghq.com/monitors/5040024)

<a href="https://www.flickr.com/photos/158412660@N04/42345774181/in/dateposted/" title="monitor1"><img src="https://farm2.staticflickr.com/1721/42345774181_1087485bd4.jpg" width="456" height="500" alt="monitor1"></a>
<a href="https://www.flickr.com/photos/158412660@N04/41443611265/in/photostream/" title="monitor2"><img src="https://farm1.staticflickr.com/882/41443611265_4ab20cf7a0.jpg" width="456" height="500" alt="monitor2"></a>

The resulting notification I received via email is:

<a href="https://www.flickr.com/photos/158412660@N04/41443611395/in/dateposted/" title="warning"><img src="https://farm2.staticflickr.com/1746/41443611395_8ba4be95ce.jpg" width="491" height="500" alt="warning"></a>

####Bonus Question
Muting the monitor over night or weekend is accomplished in the manage downtime tab: 

<a href="https://www.flickr.com/photos/158412660@N04/41443611115/in/dateposted/" title="downtime-dash"><img src="https://farm1.staticflickr.com/874/41443611115_6701bb3324.jpg" width="500" height="166" alt="downtime-dash"></a>

Simply fill in the appropriate information for a daily mute from 7PM to 9AM:

<a href="https://www.flickr.com/photos/158412660@N04/42345773911/in/dateposted/" title="daily-mute"><img src="https://farm1.staticflickr.com/897/42345773911_02f529f865.jpg" width="456" height="500" alt="daily-mute"></a>

And for muting over the weekend:

<a href="https://www.flickr.com/photos/158412660@N04/42345774061/in/dateposted/" title="weekend-muting"><img src="https://farm2.staticflickr.com/1756/42345774061_1bfe8b30c8.jpg" width="456" height="500" alt="weekend-muting"></a>

Once these are set an email notification will be sent:

<a href="https://www.flickr.com/photos/158412660@N04/41443611025/in/dateposted/" title="downtime-email"><img src="https://farm2.staticflickr.com/1733/41443611025_6142441023.jpg" width="500" height="322" alt="downtime-email"></a>

## Collecting APM Data:
The flask app that I modified can be found in this repositories code folder. Rather than using the ddtrace-run approach, I manually inserted the Middleware into the application. In a separate terminal I ran the following commands to start the flask server:

&nbsp;&nbsp;&nbsp;&nbsp; ```export FLASK_APP=apm_flask.py```
&nbsp;&nbsp;&nbsp;&nbsp; ```flask run```

Within a few moments, the Dashboard UI updated the APM tab to show the traces.

<a href="https://www.flickr.com/photos/158412660@N04/28473998728/in/dateposted/" title="my_service"><img src="https://farm2.staticflickr.com/1730/28473998728_c7b6583349.jpg" width="500" height="414" alt="my_service"></a>

I then added to my dashboard I created earlier using the UI:

<a href="https://www.flickr.com/photos/158412660@N04/41445051175/in/dateposted/" title="timeboard-with-apm"><img src="https://farm1.staticflickr.com/886/41445051175_422fb29b3c.jpg" width="500" height="414" alt="timeboard-with-apm"></a>

#### Bonus Question
A service is a part of the whole application. A Ruby on Rails api contains many processes and components, and would be considered a service. When setting up my middleware, I set my service by: ```service='my_service'```.

A resource can best be explained using Ruby on Rails routes. A resource is simply a query to a single route.


## Final Question
First, this was a great challenge for a client facing position. It provided perspective of how a client would interact with Datadog's robust service.

As for a creative way to use datadog... I would definitely like to see it used on timing traffic lights and how it affects traffic. Out here in NJ some highways have lights that are timed horribly that waste gas and creates excess emissions. It would also be interesting to be able to monitor public transportation in correlation with the traffic light timing.



