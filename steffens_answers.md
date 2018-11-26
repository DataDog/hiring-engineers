# Steffen's answers

Hi<br>
my name is Steffen and I enjoyed runnning through this exercise. I was already
looking into some monitoring or visualization for my home automation system.<br>

# Environment
I have attached my home automation instance on a raspberry. There is no
binding for my Openhab installation, so I also tried to use home assistant
to transmit Smart Home information. In addition I added some data feeds via APIs<br>

## Collecting metrics
The screenshots show the hostmap after installing the agent to my Raspberry.
Hass means homeassitant, which is default naming by home assistance, not very clever in German language :-)
So, I changed the tag to \#homeassistant.

![ScreenShot](https://github.com/mod42/hiring-engineers/raw/master/screenshots/hostmap_details.png)

I added a Agent check that submits metric from my real home automation system (HAB). <br>
*	Temp_outside Temperature outside my house, direction North 

The additional metrics are added by a rule in my HAB once a day<br>
* HZ_usage-kWh the consumption of gas for heating in kWh<br>
* WW_Usage_kWh the consumption of gas for warm water in kWh<br>

Attached code and config is [house.py](src/house.py) and [house.yaml](src/house.yaml).

![Alt text](screenshots/openhab.png?raw=true "Openhab")

<b>Bonus question:</b> Is there another way to change the collection interval? <br>
 I was able to change the interval in the yaml.

## Visualizing Data

I used Paw on my Mac to execute the API call, please find the exported curl command here <br>
[Visualizing Data.sh](src/Visualizing_Data.sh)

My Timeboard (Past week)

 ![Alt text](screenshots/dashboard.png?raw=true "Dashboard")

The snapshot feature with the easy @ function is really great idea to quickly
save, send/inform others. Screenshots are a way more tideous. 

 ![Alt text](screenshots/snapshot.png?raw=true "Dashboard")


# Bonus Question: What is the Anomaly graph displaying?<br>

I assume the Anomaly graph displace diviation from a band of expected values.
For my warm water heating, this would mean a high usage of energy. I had that in
the past, but without automatic chekcing. I found that one of the valve was broken,
whene the consumption rose by 50%, after a specific date. With this detector I would 
be alarmed earlier.

# Monitoring Data



# My comments

I liked the structure of the datadog.conf file. All default values have been entered and
umcommented like <br>```# enable_gohai: true```



