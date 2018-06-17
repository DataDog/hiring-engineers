# Logan Morales - Technical Exercise

## Prerequisites - Setup the environment

To set up my environment, I chose to utulize Virtualbox to spin up an Ubuntu Virtual Machine. The benefit of using a virtual machine over a native system, in my opinion, is the convenience of what I like to call... 'Nuking it'. 

![alt text](https://media.giphy.com/media/YA6dmVW0gfIw8/giphy.gif "Logo Title Text 1")

If something goes wrong, or I make a few config changes that don't play nice with other services, I have the luxury of nuking it and starting fresh within just a few moments. While working with new technologies (and even with familiar ones) it is very comforting to have this fail safe in place - it makes me feel safe to know nothing I do is affecting my core machine and I am working in a complete sandbox. 

After getting my VM up and running, I created a trial account with Datadog and started sniffing around. I added my Ubuntu integration, used the install script to get my system connected and within a few moments, began to see metrics from my VM coming in.
![alt text](https://i.imgur.com/FEdqXWr.png "Logo Title Text 1")

## Collecting Metrics

### Tags... Oh tags.
![alt text](https://media.giphy.com/media/3o6Ei0fWOw1iQ79d0A/giphy.gif)

Following alongside the [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) I was able to locate the `datadog.yaml` config file inside of `/etc/datadog-agent` and make a few changes:

- `sudo nano datadog.yaml`
- Uncomment out the 'tags' section
- Change to:
```
tags:
	- name:logan
	- applying_for:solutions_engineer
```

My configuration file looks like this:

![alt text](https://i.imgur.com/2im4SJj.png "Logo Title Text 1")

I restarted the datadog- agent using 
`sudo service datadog-agent restart` 
so that the agent would read the updated config file and my tags populated inside of Datadog's interface within a few minutes:

![alt text](https://i.imgur.com/XqA2WIu.png)

### Lets get that database going!

I was first introduced into databases during my time at General Assembly where we learned PostgreSQL. Recently, I have been working with MySQL quite a lot and I'm going to use this for my database integration. 

I took the following steps to get this going:
	
1. `sudo apt-get update` to update the package index
2. `sudo apt-get install mysql-server` to install MySQL
3. Follow the [Datadog documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) for installing the MySQL integration:
	- I created a user for the datadog agent with rights to the MySQL Server using the commands:

	```
	sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '$password'
	sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
	```

	- I also opted to receive full metrics catalog by using the following command provided in the docs:

	```
	sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
	sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
	```

	- Moving on! Next I edited the MySQL config file for datadog inside of `/etc/datadog-agent/conf.d/mysql.d/` to connect MySQL to my agent. I created a working copy of the example file 
	(`conf.yaml.example`) using `cp conf.yaml.example ./conf.yaml` and un-commented out the lines corresponding to the documentation provided by Datadog:

	```
	init_config:

	instances:
	  	server: localhost
    	user: datadog
    	pass: $password 
    	tags:
        	optional_tag1
        	optional_tag2
    	options:
        	replication: 0
        	galera_cluster: 1
	```

   Here is a screenshot of my configuration file (`/etc/datadog-agent/conf.d/mysql.d/conf.yaml`):
	
   ![alt text](https://i.imgur.com/ViXlih0.png)

   - I then restarted my agent - `sudo service datadog-agent restart` and ran a check command `sudo datadog-agent check mysql | more` . I appended `| more` so that I could scroll through the results. 

   Here is a screenshot of the check command results:

   ![alt text](https://i.imgur.com/gLBcC2A.png)

   And here is Datadog web interface reporting the metrics from my MySQL integration:

   ![alt text](https://i.imgur.com/AsY1xUt.png)

### Custom Agent reporting metrics with random integer between 1 and 1000.

To understand the process of doing this, I spent a lot of time reading over the [documentation](https://docs.datadoghq.com/developers/agent_checks/) provided by Datadog. Following along with the documentation, here are the steps that I took:

1. `cd /etc/datadog-agent/conf.d/` getting into the directory for the .yaml file.
2. `sudo touch my_metric.yaml` creating a new config file, sudo rights required.
3. `sudo nano my_metric.yaml` to edit the file and filled with:

	```
	# barebones configuration boilerplate
	
	init_config: 	

	instances:
    	[{}]
	```

   Here is a screenshot of my configuration file:

   ![alt text](https://i.imgur.com/FIiMzNX.png)

4. `cd /etc/datadog-agent/checks.d/` getting into the directory for the python script.
5. `sudo touch my_metric.py` must be the same name as the .yaml created in step 2, sudo rights required.
6. `sudo nano my_metric.py` to edit the file and filled with:
	
	```
	from checks import AgentCheck	# Required, inherits from AgentCheck
	import random					# import random number package

	class CustomCheck(AgentCheck):  # define class CustomCheck
		def check(self, instance):
			self.gauge('my_metric', random.randint(0,1000))
	```

   Here is a screenshot of my python file:

   ![alt text](https://i.imgur.com/MDVntv8.png)

7. my_metric Inbound!

   ![alt text](https://media.giphy.com/media/tG6ZDOfW5Xeo/giphy.gif)

   Screenshot of my_metric on Datadog

   ![alt text](https://i.imgur.com/DvsDEob.png)

### 45 Second Collection Interval

To change the collection interval of my_metric, I simply followed the same documentation mentioned above. I modified the file 'my_metric.yaml' to add `min_collection_interval: 45` under `init_config`. The file contents looks like this:

```
init_config: 	
	
instances:
    - username: <$username>
    - password: <$password>
    - min_collection_interval: 45
```

And here is a screenshot my of 'my_metric.yaml' file:

![alt_text](https://i.imgur.com/Dp4HJcG.png?1)

Here is a screenshot of the metric on a 45 second interval from Datadog:

![alt_text](https://i.imgur.com/1E4KIro.png)

### BONUS!!

Changing the collection interval seems to be a key feature of adding a custom metric. I changed the interval using the 'my_metric.yaml' file and did not need to touch my python file

## Visualizing Data

To accomplish this task, I carefully ready the [documentation](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard) on using the API to create a new Timeboard. 

Lets begin!

![alt_text](https://media.giphy.com/media/WZ4M8M2VbauEo/giphy.gif)

1. Get the API and Application Key - It's easy to do:
	- Hover over 'Integrations' from the sidebar and select 'APIs'.
	- An API key is generated by default and resides at the top of the page under the section 'API Keys'.
	- Generate an Application Key - Just below the API Key section - and give it a name.

2.  Test out the API using Postman!
	- Before getting to the final product, I generated some test timeboards using Postman to iron out the bugs that were sure to come 👀
	- I made a test timeboard called 'Hi there' that I pulled from a file on Datadogs [documentation](https://help.datadoghq.com/hc/en-us/articles/115002182863-Using-Postman-With-Datadog-APIs) on using Postman with Datadog. Below is a screenshot of the timeboard in Datadog:

	![alt_text](https://i.imgur.com/bxLPTZI.png)

	- Next, I created a timeboard with my custom metric scoped over my host. Here is my script and a screenshot of the timeboard in Datadog:

	![alt_text](https://i.imgur.com/TLee4CM.png)

	```
	{
      "graphs" : [{
          "title": "Metric over Host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard1",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

	- Moving on! Then, I made a another timeboard with anomoly information on my MySQL database integration. This was a bit more difficult because I didnt initially know how to connect the MySQL integration. After navigating to the 'Integrations' page and Selected 'MySQL', I navigated right to 'Metrics' and found some usuful information I can look for. I combined this with the anomoly function found in Datadogs [documentation](https://docs.datadoghq.com/graphing/miscellaneous/functions/#anomalies) Below is my script and a screenshot of the timeboard in Datadog.

	![alt_text](https://i.imgur.com/rhhTRL6.png)

	```
	{
      "graphs" : [{
          "title": "MySQL Anomoly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard2-1",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

	- Next! To make the 'custom metric with the rollup function applied to sum up all the points for the past hour into one bucket'... I used the [rollup function in Datadog docs](https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup) to assist me on this one. Below is my script and a screenshot of the timeboard in Datadog.

	![alt_text][Imgur](https://i.imgur.com/fP0ygb5.png)

	```
	{
      "graphs" : [{
          "title": "Fruit Rollups 🍭",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's timeboard3",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
	```

3. After getting all of my individual timeboards together I put them together into one... GIANT... TIMEBOARD! Script and Datadog screenshot below:

![alt_text](https://i.imgur.com/0PRUgce.png)

```
{
      "graphs" : [{
          "title": "Fruit Rollups 🍭",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "MySQL Anomoly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.net.connections{*}, 'basic', 2)"}
              ]
          },
          "viz": "timeseries"
      },{
          "title": "Custom Metric over Host",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "timeseries"
      }],
      "title" : "Logan's Custom Ultimate Timeboard",
      "description" : "Made by Logan Morales",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }
```




