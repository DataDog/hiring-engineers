## Introduction
Hi, I'm Jordan Storms. For this challenge I used Linux Mint 18.3.

## Collecting Metrics

#### Adding a tag
In order to add a tag we need to customize the datadog.yaml file, located at etc/datadog-agent/datadog.yaml. Open the file with your editor of choice and add a tag as shown in the screenshot below:

<a href="https://www.flickr.com/photos/158412660@N04/40499437960/in/dateposted/" title="Tags-text-editor"><img src="https://farm1.staticflickr.com/970/40499437960_2a79383464_z.jpg" width="640" height="351" alt="Tags-text-editor"></a>

After you save the file, exit the docker bash shell with ```exit```. Next we must reset the datadog agent, which is accomplished by restarting the docker container:
&nbsp;&nbsp;&nbsp;&nbsp;```docker container restart name-of-your-container```

After a few moments, the datadog dashboard will display your newly added tags in infrastructure -> host as shown below:

<a href="https://www.flickr.com/photos/158412660@N04/28432878508/in/dateposted/" title="Host-tags"><img src="https://farm1.staticflickr.com/959/28432878508_76a0058106_z.jpg" width="640" height="631" alt="Host-tags"></a>
