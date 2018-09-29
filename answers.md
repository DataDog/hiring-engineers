

## The Solutions


### Solution 1 

I use the following config file for my Macbook Pro agent. [Datadog config](./opt/datadog-agent/etc/datadog.yaml)

Here is a view of my Macbook Pro with tags.

<img src="./images/host_map.jpeg" width="700" height="500" alt="Host Map">


### Solution 2

I added a custom metric "girish.random" to display a random number between 0 and 1000. The customer metric files are [random_num.py](./opt/datadog-agent/etc/checks.d/random_num.py) and [random_num.yaml](./opt/datadog-agent/etc/checks.d/random_num.yaml).

Here is a view of my custom metric dashboard. 

