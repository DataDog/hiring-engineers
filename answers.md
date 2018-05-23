## Introduction
Hi, I'm Jordan Storms. For this challenge I used Linux Mint 18.3.

## Collecting Metrics

#### Adding a tag
In order to add a tag we need to customize the datadog.yaml file, located at etc/datadog-agent/datadog.yaml. Open the file with your editor of choice and add a tag as shown in the screenshot below:

<a href="https://www.flickr.com/photos/158412660@N04/42261444992/in/dateposted/" title="Gedit-tag"><img src="https://farm1.staticflickr.com/954/42261444992_7322386909_z.jpg" width="640" height="498" alt="Gedit-tag"></a>

After you save the file, exit the docker bash shell with ```exit```. Next we must reset the datadog agent, which is accomplished by restarting the docker container:
&nbsp;&nbsp;&nbsp;&nbsp;```docker container restart name-of-your-container```

After a few moments, the datadog dashboard will display your newly added tags in infrastructure -> host as shown below:

<a href="https://www.flickr.com/photos/158412660@N04/42261445672/in/dateposted/" title="Infrastructure-Tag"><img src="https://farm1.staticflickr.com/977/42261445672_f95721ea22_z.jpg" width="640" height="529" alt="Infrastructure-Tag"></a>

[A link to my dashboard]: https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=485640810
