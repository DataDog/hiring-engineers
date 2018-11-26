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

I added a Agent check that submits metric from my real home automation system (HAB).
* Temp_outside Temperature outside my house, direction North 

The additional metrics are added by a rule in my HAB once a day<br>
* HZ_usage-kWh the consumption of gas for heating in kWh
* WW_Usage_kWh the consumption of gas for warm water in kWh



#My comments

I liked the structure of the datadog.conf file. All default values have been entered and
umcommented like <br>```# enable_gohai: true```



