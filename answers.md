# Collecting Metrics:
* **Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**
    
    _Documentation I referred to get started with tags. https://docs.datadoghq.com/getting_started/tagging/_    
    The steps below were used to add a tag to the Agent config file.
    1. [Methods for assigning Tags](http://google.com) states "The Agent configuration file (datadog.yaml) is used to set host tags which apply to all metrics, traces, and logs forwarded by the Datadog Agent." Based on this information, I went ahead and modified the datadog.yaml file which can be accessed using `vi ~/.datadog-agent/datadog.yaml`. 
    2. In datadog.yaml I added a tag of `project:hiring_engineers`. I used this host tag to filter by a common app/project
    3. The following screenshot displays the Host Map within Datadog filtering by the project tag set above.
    ![Image of host map](./img/host_map.png)   

    

* **Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**
    
    _The following steps show how we can install the respective Datadog integration for MongoDB Atlas._

    1. In [MongoDB Atlas](https://docs.atlas.mongodb.com/getting-started/), create an account start a project, and create a cluster.
    2. Back inside of Datadog, click on the *Integrations > Integrations* tab found in the left hand navigation menu.
    ![Image of integrations tab](./img/integrations_tab.png)
    3. In the Integrations tab, search for _MongoDB_ and click install.
    ![Image of MongoDB Atlas Install](./img/mongodb_install.png)
    4. Next, visit the *Configuration* tab of the MongoDB integration modal and follow the steps provided. 
    5. Jump back into MongoDB Atlas and verify that datadog is configured. Your integrations tab should display the following.
    ![Image of MongoDB Atlas](./img/mongodbatlas_configured.png)

* **Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

    _Documentation I referred to get started creating a Custom Agent Check can be found **[here](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#should-you-write-an-agent-check-or-an-integration)**._ 

    1. To get started writing a custom Agent check, create a new directory as a child of conf.d (ex: custom_agent_check.d)
    2. In the newly created directory, create a YAML file (ex: custom_agent_check.yaml)
    3. Change to the datadog agent root and jump into the checks.d directory.
    4. In the checks.d directory, create a check file (ex: custom_agent_check.py) with the following code snippet.
    ```python
    import random
    # the following try/except block will make the custom check compatible with any Agent version
    try:
        # first, try to import the base class from new versions of the Agent...
        from datadog_checks.base import AgentCheck
    except ImportError:
        # ...if the above failed, the check is running in Agent version < 6.6.0
        from checks import AgentCheck

    # content of the special variable __version__ will be shown in the Agent status page
    __version__ = "1.0.0"

    class My_Metric(AgentCheck):
        def check(self, instance):
            self.gauge('my_metric', random.randrange(0,1000), tags=['custom_agent_check:test_check'])
    ```

    To verify the check with macOS:
    1. Stop the agent using ```launchctl stop com.datadoghq.agent```
    2. Start the agent back up using ```launchctl start com.datadoghq.agent```
    3. Run ```datadog-agent status```. You should see the following results
    ![Image of custom agent](./img/custom_agent_check.png)

* **Change your check's collection interval so that it only submits the metric once every 45 seconds.**
    
    * Modify the YAML file created in your Custom Agent check folder located in the conf.d directory. Include the following snippet
    ```yaml
        init_config:

        instances:
            - min_collection_interval: 45 
    ```
* **Bonus Question Can you change the collection interval without modifying the Python check file you created?**

    According to the Datadog documentation on "Writing a Custom Check", the collection interval can be set at the configuration level (YAML file) opposed to the Python script provided.

# Visualizing Data

**Utilize the Datadog API to create a Timeboard that contains:**

 **1. Your custom metric scoped over your host.**

 **2. Any metric from the Integration on your Database with the anomaly function applied.**

 **3. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket**

* For more information on creating a Timeboard using the Datadog API, please see the documentation attached [here](https://docs.datadoghq.com/dashboards/guide/timeboard-api-doc/?tab=python)

    The steps listed below detail my implementation to complete the tasks listed above.
    
    First, lets set up our Timeboard. I created a python script (shown below). This code creates a Dashboard named Visualize Data Exercise and creates widgets that allow us to do the following
     - View the custom metric created in the collecting metrics section.
     - View the normalized CPU kernel space for mongodb processes.
     - View a rollup of our custom metric that summed up all the points over a 1 hour time span into a single bucket. the rollup function allows us to perform time aggregation.

     ```Python
    from datadog import initialize, api

    options = {
        'api_key': '<API_KEY>',
        'app_key': '<APP_KEY>'
    }

    initialize(**options)

    title = 'Visualize Data Exercise'

    widgets= [
    {
        "definition":{
            "type":"timeseries",
            "requests": [
                {
                    "q":"avg:my_metric{*}"
                }
            ],
            "title":"Average of my_metric"
        }
    },
    {
        "definition":{
            "type":"timeseries",
            "requests":[
                {

                    "q":"anomalies(mongodb.atlas.system.cpu.mongoprocess.norm.kernel,'basic',2)"
                }
            ],
            "title":"Anomalies Function"
        }
    },
    {
        "definition":{
            "type":"timeseries",
            "requests":[
                {
                    "q":"avg:my_metric{*}.rollup(sum,3600)"
                }
            ],
            "title":"Metric Rollup"
        }
    }]


    layout_type = 'ordered'
    description = 'A dashboard using the DataDog API'
    is_read_only = False
    notify_list = ['shawnppitts@gmail.com']


    api.Dashboard.create(title=title,
                        widgets=widgets,
                        layout_type=layout_type,
                        description=description,
                        is_read_only=is_read_only,
                        notify_list=notify_list)
    ```

    


         

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
![Image of dashboard](./img/dashboard.png)
* **Bonus Question**: What is the Anomaly graph displaying?

    The anomoly function detects when a metric is behaving differently than it has in the past. More documentation on anomoly monitoring [here](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms).