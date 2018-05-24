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
To create a custom check we need to add a python script in /etc/datadog/checks.d and a config (yaml) file in /etc/datadog/conf.d. In this example I used mycheck.py and mycheck.yaml which is included in the code folder in this repository. 

<a href="https://www.flickr.com/photos/158412660@N04/40521358110/in/photostream/" title="mycheck"><img src="https://farm1.staticflickr.com/962/40521358110_31b3113fbe_z.jpg" width="640" height="199" alt="mycheck"></a>

To only send the metric at an interval of 45 seconds without altering the python file, simply add: ```min_collection_interval: 45``` to the instances section of the config file as shown above.

After some time the changes will show in the dashboard and the metric can be viewed by going to infrastructure -> host as shown here:

<a href="https://www.flickr.com/photos/158412660@N04/40521356690/in/dateposted/" title="my-metric-host"><img src="https://farm1.staticflickr.com/882/40521356690_02f63bc67a_z.jpg" width="584" height="640" alt="my-metric-host"></a>

Clicking on the ((no-namespace) dashboard) link brings you [here](https://app.datadoghq.com/dash/integration/custom?live=true&tpl_var_scope=host%3Ajordans-pc&page=0&is_auto=false&from_ts=1527185954883&to_ts=1527189554883&tile_size=m):
<a href="https://www.flickr.com/photos/158412660@N04/40521357180/in/dateposted/" title="my_metric"><img src="https://farm1.staticflickr.com/968/40521357180_72b63db753_z.jpg" width="640" height="323" alt="my_metric"></a>

