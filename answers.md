## Introduction
Hi, I'm Jordan Storms. For this challenge I used Linux Mint 18.3 (an Ubuntu derivative) and docker. I followed these instructions for setting up my environment: 
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)


## Collecting Metrics

#### Adding a tag
In order to add a tag we need to customize the datadog.yaml file. Since we are using docker and version 6 of the Datadog Agent in this example, the file will be located at etc/datadog-agent/datadog.yaml inside the docker container.

To open and edit the file with gedit:
```sudo gedit /etc/datadog-agent/datadog.yaml```

<a href="https://www.flickr.com/photos/158412660@N04/40499437960/in/dateposted/" title="Tags-text-editor"><img src="https://farm1.staticflickr.com/970/40499437960_2a79383464_z.jpg" width="640" height="351" alt="Tags-text-editor"></a>

<a href="https://www.flickr.com/photos/158412660@N04/28432878508/in/dateposted/" title="Host-tags"><img src="https://farm1.staticflickr.com/959/28432878508_76a0058106_z.jpg" width="640" height="631" alt="Host-tags"></a>
