# Starting Off

Let's start off with a view of our host:

![enter image description here](https://s15.postimg.cc/h4p29ma97/dd_host_page.png)

We added tags via two methods, first was via the agent config file in etc/datadog-agent/datadog.yaml:

![enter image description here](https://s15.postimg.cc/543m8l5bv/agent_config_file.png)

We can also add them via the infrastructure list in the main datadog UI:

![enter image description here](https://s15.postimg.cc/mu5att63v/infrastructure_list_tags.png)



# Collecting Metrics
Let's install mysql on our virtual host and collect some sample metrics. We skip the installation details of mysql and focus on the Datadog aspects. Adding an integration is fairly straightforward and the Datadog interface helps guide us through it. Navigate to the integration list from the Datadog main page:

![enter image description here](https://s15.postimg.cc/ghq5jwq63/integrations.png)

Next let's filter the search to find mysql:

![enter image description here](https://s15.postimg.cc/vdooro1mj/search_filter.png)

In this case, the integration is already installed, but if we click on the icon we get some helpful instructions:

![enter image description here](https://s15.postimg.cc/7zgpfwrgr/instructions.png)

Following these through, we end up creating *conf.d/mysql.yaml*
![enter image description here](https://s15.postimg.cc/80qn91qmz/mysql.png)

It's fairly bare-bones as you can see. After this we restart the agent. To actually collect some dummy metrics, we create an agent check. There's two parts to this:

A check module. This is a py file in etc/datadog-agent/checks.d:
In this case, we are calling this metric *my_metric*
![we call it randomcheck.py as we're simply generating a random int between 0-1000](https://s15.postimg.cc/56nhvu93v/check_py.png)

A configuration file. This is a yaml file in etc/datadog-agent/conf.d:
![enter image description here](https://s15.postimg.cc/cnwpaqlor/check_yaml.png)

It's important to for the module and the configuration file (the py file and the yaml file) have the same name. In this case, both are `randomcheck`

In the configuration file we set the minimum collection interval to 45 seconds. All handy instructions for creating an agent check can be found at: https://docs.datadoghq.com/developers/agent_checks/

Once we follow this process, we see our metric show up within the Datadog metrics explorer:
![enter image description here](https://s15.postimg.cc/pj9ab4g0b/metrics_explorer.png)

# Visualizing Data
Let's take the metric we just created and do some visualizations with it. We create three different graphs:

**Simple time series:**
![enter image description here](https://s15.postimg.cc/mdool3kl7/time_series.png)

**Time series with Anomaly function applied:**
![enter image description here](https://s15.postimg.cc/7hq5dq6ob/anomalies.png)
The anomaly function is an algorithmic feature and can detect when a metric is behaving differently from what it has in the past. The function can take into account both trends and seasonal patterns by changing the detection algorithm (in this case we have selected *basic*) . Since our metric is randomly generated there is no seasonality to be expected. More information about the anomaly function can be found here: https://docs.datadoghq.com/monitors/monitor_types/anomaly/

**Our metric summed up by hour:**
![enter image description here](https://s15.postimg.cc/vmquvi3uj/sum_bins.png)

Note we can conveniently annotate graphs and share it with team members for easy collaboration:
![enter image description here](https://s15.postimg.cc/yw5a1w7cr/annotation.png)
You'll get an email notification of this:
![enter image description here](https://s15.postimg.cc/y7wfiniu3/email_notify.png)

# Monitoring Data

Metric monitors can help warn and alert us when our metrics are behaving in a certain way. A monitor is easy to setup. From the timeboard, click the gear icon of any graph and select Create Monitor:

![enter image description here](https://s15.postimg.cc/gkemkfth7/monitor_setup.png)

The tool will help guide you through the monitor creation:
![enter image description here](https://s15.postimg.cc/wveqgyo17/monitor_setup_2.png)

You can read more about creating monitors here: https://docs.datadoghq.com/monitors/
You will see the monitor send in email alerts once it's working:
![enter image description here](https://s15.postimg.cc/mzdnh17vv/alert_email.png)

We can also schedule downtimes for our monitors so that they do not notify us at certain times:

This is a downtime from 7PM - 9PM daily:
![enter image description here](https://s15.postimg.cc/8hgg92j5n/downtime1.png)

This is a downtime for every Sat-Sun (for the whole weekend):
![enter image description here](https://s15.postimg.cc/mnw74h9i3/downtime2.png)

You'll get notified by email once a downtime has been scheduled for a monitor:
![enter image description here](https://s15.postimg.cc/5alwprbnv/downtime_email.png)

# Collecting APM Data
Let's use Datadog's APM solution to instrument a sample app. The application we use will be the following flask app:

    from flask import Flask
    import logging
    import sys
    
    # Have flask use stdout as the logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)
    c = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c.setFormatter(formatter)
    main_logger.addHandler(c)
    
    app = Flask(__name__)
    
    @app.route('/')
    def api_entry():
        return 'Entrypoint to the Application'
    
    @app.route('/api/apm')
    def apm_endpoint():
        return 'Getting APM Started'
    
    @app.route('/api/trace')
    def trace_endpoint():
        return 'Posting Traces'
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5050')

Let's save the above as *my_app.py*

Setting up the tracing is fairly straightforward. We install ddtrace:

    pip install ddtrace

Next we run

    ddtrace-run python my_app.py
You'll see flask reports that it is running:
![enter image description here](https://s15.postimg.cc/owsr4r7kb/flask_running.png)

Let's visit this in our browser and try out some of the tracing:

![enter image description here](https://s15.postimg.cc/4cnx6czjv/dd3.png)

![enter image description here](https://s15.postimg.cc/jy58qclsr/dd4.png)

![enter image description here](https://s15.postimg.cc/vahu85x2j/dd5.png)

You'll see these appear in the APM section of the Datadog main UI as well:

![enter image description here](https://s15.postimg.cc/k4ixt253v/trace_search.png)

Note these are sortable by both the 'Service' and 'Resource'. A "Service" is the name of a set of processes that work together to provide a feature set. By default Datadog has detected the service as flask in this case. However, it is possible to define your own service names, for example:

![enter image description here](https://help.datadoghq.com/hc/en-us/article_attachments/115001888563/Custom_Service.png)

A "Resource" is a particular query to a service. For a web application, this might be a URL path. For example, the `/apm` and `/trace` paths we defined in our flask app are counted as resources. Resources can be though of as "belonging" to a Service. This article provides additional details: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-

Of course we can add APM metrics to an existing dashboard (alongside infrastructure metrics):
![enter image description here](https://s15.postimg.cc/yjw9e6igr/apm_metrics.png)

Here it is along with infrastructure metrics in the same timeboard:
![enter image description here](https://s15.postimg.cc/o9tuf783f/full_timeboard.png)


# Creative uses of Datadog - Greenhouses

Generally speaking, a greenhouse is a very intricate environment. There's all kinds of factors; from the lighting, air temperature, air humidity, vapor pressure, and even soil moisture. While these may not be factors if growing your everyday carrots and potatoes, scientists would surely benefit 

Luckily the wealth of meaningful factors also means a wealth of things to monitor, consider the following setup:

 - Sensors can be installed to monitor a variety of enviromental factors and report them to Datadog
 - Tags can be used in meaningful ways to organize your data. For example, certain greenhouse are meant to have a different local climate (rain forest vs. Mediterranean)
 - Dashboards can provide meaningful information on a greenhouse based off the sensor readings of environmental factors
 - Downtime for monitors can be scheduled in meaningful ways. One may not want sensitive equipment reporting on environmental factors when there are people in the greenhouse tending to plants or performing general maintenance

There's a lot of functionality within Datadog out of the box that can be extended to such real-world scenarios.

 
# Resources

Below are some of the graphs that were created for this exercise:

<iframe src="https://app.datadoghq.com/graph/embed?token=f0e941c5de016a7db90b5047b606fb22bae895f540a031210ba37c0ad05d517c&height=300&width=600&legend=true" width="600" height="300" frameborder="0"></iframe>

<iframe src="https://app.datadoghq.com/graph/embed?token=9c49af336eed936ab2823f9795f8a89331338789bc2a8172c0f589bf91ef6a1a&height=300&width=600&legend=true" width="600" height="300" frameborder="0"></iframe>

<iframe src="https://app.datadoghq.com/graph/embed?token=58178ec49e94718145581797410498e10c54c0ae17f4fb4f139c6407a0d94879&height=300&width=600&legend=true" width="600" height="300" frameborder="0"></iframe>

<iframe src="https://app.datadoghq.com/graph/embed?token=bb7615a7dc95a05be1aa3c6b2d7bdae2e704e196dadde0f77d06fa21e02db86e&height=300&width=600&legend=true" width="600" height="300" frameborder="0"></iframe>
