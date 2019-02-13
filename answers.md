# DataDog Coding Assignment

## Step One - Setting Up The Environment

First I signed up for Datadog, and then used the integration tool to install and set up the Agent on my Mac OSX. 

## Step Two - Collecting Metrics

For the first metric I had to go into the datadog.yaml file and uncomment the tags in order to set up a custom tag for my server.

![tag](/Setting_tags_in_config.png)

I then checked the [host map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) to see if the new tag had updated.

![host](/Host_map_with_custom_tags.png)

You can see that the new tag "role:server" is included in the Tags section.

The next step is setting up a database and integrating it into the Datadog Agent. I created a database in Postgres with the name "aleks". Then I created a user called "datadog" and created an empty table called "DATADOG" so that there would be something to measure.

```sql
CREATE TABLE DATADOG(
   ID INT PRIMARY KEY      NOT NULL,
   NAME           TEXT     NOT NULL
);
```
Now I had to update the settings in my postgres.yaml file (I left out the password in the image).

![postgres](/postgres.yaml_file.png)

This created a [metrics page](https://app.datadoghq.com/dash/integration/17/postgres---metrics?tile_size=m&page=0&is_auto=false&from_ts=1550019120000&to_ts=1550022720000&live=true) for Postgres.

![postgres metric](/postgres_metrics.png)

We can see it works! I've connected to the database to make sure it's accurately measuring it.

The next metric that we want to display is our custom metric that will periodically show a number between 0 and 1,000 every 45 seconds. For this we'll need to create a custom agent check, which we'll call "my_metric". The first step to that is to create a `my_metric.py` file in the `checks.d` directory and then a `my_metric.yaml` file in the `conf.d` directory.

 ![my_metric python](/my_metric.py_file.png "Our my_metric python file")

 This is our python file which creates an Agent check, and imports randint which will generate our random number.

  ![my_metric yaml](/my_metric.yaml_file.png "Our my_metric yaml file")

  This is our yaml file which specifies we want to run our check every 45 seconds.

  ## Step Three - Visualizing Our Metric

  Now we want to visualize our custom my_metric check. To do this we'll use the Datadog API to create timeboards. I've included the script inside the `api_call.rb` file. It creates three timeboards. I used the API documentation to figure out what my graph hashes should look like, and also used the dotenv gem to store the API and app keys in an `.env` file in order to not expose my keys when I upload this to github.

![my_metric timeboards](/timeboards.png "The three timeboards that were created")

From the top left corner going across, they are:
* A timeseries graph that measures rows fetched from my database with an anomaly function applied
* A timeseries graph scoped to my host that shows the random number that's generated every 45 seconds
* A query value board showing the sum of the random numbers generated within the last hour

Here's a [link](https://app.datadoghq.com/dashboard/yjh-4qi-cc2/mymetricapi?tile_size=m&page=0&is_auto=false&from_ts=1550018880000&to_ts=1550022480000&live=true) to said dashboard.

Using the `option/alt + ]` shortcut we can change the graph to show only the last 5 minutes of activity.

![5 minute time span](/five_minutes.png)

In order to take a snapshot we click on the camera icon above one of our boards and use the "@" notation to send it to ourselves.

![5 minute snapshot](/five_minute_snapshot.png)

## Step Four - Creating A Monitor For Our Metric

In order to set up a monitor we can go into the "Monitors" side tab and click on "New Monitor" where we can specify when we want our monitor to trigger.

First we'll set our monitor to be a threshold monitor since we want it to trigger once it goes past a certain threshold. Then we have to set it to detect changes in "my_metric" and set the scope to our host.

![monitor step one](/monitor_scope.png)

Now we set up our thresholds for our alerts.

![monitor step two](/threshold_settings.png)

Finally we create our message and make sure it's sending the alert to us.

![monitor step three](/alert_message.png)

After waiting for a little bit we get our first warning email.

![warning email](/warning_email.png)

It looks like we went past our warning threshold which we set to be 500.

We can also schedule downtimes for these emails by using the "Manage Downtime" feature in our "Monitors" sidebar. 

We'll set up two scheduled downtimes, one to silence the alerts after work hours during the week and another for the weekends.

![weekday downtime](/weekday_downtime.png)

Now we'll set up the weekend downtime.

![weekend downtime](/weekend_downtime.png)

This is what a downtime email looks like:

![weekend downtime email](/weekend_email.png)

## Step Five - Collection APM Data

The first step to setting up the APM was to change the config file to enable APM.

![apm config](/config_apm_setting.png)

Next we have to make a simple app which will be tracked. For this I used Sinatra since the setup is quite easy. After installing the sinatra gem and the ddtrace gem I just had to configure the trace so that it knows it's Sinatra and then configure the routes. You can see this app in the `apm.rb` file. Unfortunately I came upon a "Client Error: Not Found" when I ran this little app. After much troubleshooting it seemed like the trace-agent wasn't working. For whatever reason, manually starting the trace-agent from `/opt/datadog-agent/embedded/bin/trace-agent` fixed this problem and I was able to get the APM working. 

We can now click on the APM sidebar and go through the [information](https://app.datadoghq.com/apm/service/sinatra/sinatra.request?end=1550022777581&env=none&paused=false&start=1550019177581) our tracer is giving us. 

![services graphs](/service_graphs.png)

![resources info](/resources_info.png)

We can see that difference between services and resources is that a service is the way our app is run, and in this case it's through Sinatra, while the resources graph represents the endpoints for our app, it's all the data that's being exchanged.

Here is a map of all of our services.

![service map](/service_map.png)

Finally we modified our simple app to also include a logger, which will print out a message when the sinatra app starts.

![logger working](/logger_working.png)

## Final Question

Something I've always been curious about is the accuracy of various weather prediction sources. I'm not sure how available that kind of data is but I imagine DataDog would be a great platform to have multiple alerts and ways to sort information from various weather forecast websites. Having it all in one place would possibly give you the best prediction of the weather for the upcoming day/week. You'd also be able to see outliers quite easily.
