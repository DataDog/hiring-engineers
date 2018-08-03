Answers to Solution Engineering by Fernando Cremer (cremerfc@gmail.com)

## Collecting Metrics

Adding tags to configuration file and showing them in host map:

* Here is my Datadog.yaml

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/Datadogyaml.jpg" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/Datadogyaml.jpg"  alt="_DSC4652"></a>

* Here is my Host Map showing the tags for the host Unbuntu-Xenial

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/HostMapTags.png" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/HostMapTags.png"  alt="_DSC4652"></a>

* Screenshot showing mySQL metrics on host after installing mySQL and configuring the integration

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/hostwmysql.png" title="DataDogYamlTags">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/hostwmysql.png"  alt="_DSC4652"></a>

* Python file to create custom check to send my_metric a random value between of 0 and 1000:
[Python file to create custom check](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/myCustomCheck.py)

* Tried to configure in the Python file to force it only sending the metric every 45 seconds. Was not able to properly determine the last time the metric ran. Found a couple of examples online but would not work. Thinking that checks are called every 15 - 20 seconds, I could check the last time it ran, find how long ago that was, and sleep for whatever time until we reach 45 seconds. Here is a screenshot of what I tried to do:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/customcheck_w_sleep.png" title="Custom Check w Sleep">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/customcheck_w_sleep.png"  alt="customcheck_w_sleep"></a>


And the error received:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/error_python_script.png" title="Error When Trying to Figure out Last Collection Time">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/error_python_script.png"  alt="error_python_script"></a>

So ended up setting the min_collection_interval in the YAML file for the custom check which can be seen here:

[Yaml file for custom check](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/myCustomCheck.yaml)

## Visualizing Data:

* Python file used to create Timeboard:

[Python file to create timeboard](https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/create_timeboard.py)

* Here is a screenshot:

<a href="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/TimeboardAPI.png" title="Timeboard created by API">
<img src="https://github.com/cremerfc/hiring-engineers/blob/solutions-engineer/TimeboardAPI.png"  alt="TimeboardAPI"></a>




