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


