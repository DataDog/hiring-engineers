# Logan Morales - Technical Exercise

## Prerequisites - Setup the environment

To set up my environment, I chose to utulize Virtualbox to spin up an Ubuntu Virtual Machine. The benefit of using a virtual machine over a native system, in my opinion, is the convenience of what I like to call... 'Nuking it'. 

![alt text](https://media.giphy.com/media/YA6dmVW0gfIw8/giphy.gif "Logo Title Text 1")

If something goes wrong, or I make a few config changes that don't play nice with other services, I have the luxury of nuking it and starting fresh within just a few moments. While working with new technologies (and even with familiar ones) it is very comforting to have this fail safe in place - it makes me feel safe to know nothing I do is affecting my core machine and I am working in a complete sandbox. 

After getting my VM up and running, I created a trial account with Datadog and started sniffing around. I added my Ubuntu integration, used the install script to get my system connected and within a few moments, began to see metrics from my VM coming in.
![alt text](https://i.imgur.com/FEdqXWr.png "Logo Title Text 1")

## Collecting Metrics

### Tags... Oh tags.
Following alongside the [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/) I was able to locate the `datadog.yaml` config file inside of `/etc/datadog-agent` and make a few changes:

- `sudo nano datadog.yaml`
- Uncomment out the 'tags' section
- Change to:
```tags:
	- name:logan
	- applying_for:solutions_engineer
```


