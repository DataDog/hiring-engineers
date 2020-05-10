![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/logousage_white.png "Title")

# Datadog Beginner's Guide

> This repository is a self-guided walkthrough that covers the main features of the Datadog product offering.


![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/overview.png "Title")


## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Walkthrough](#walkthrough)
    - [Datadog Console](#datadog-console)
    - [Collecting Metrics](#collecting-metrics)
    - [Visualizing Data](#visualizing-data)
    - [Monitoring Data](#monitoring-data)
    - [Collecting APM Data](#collecting-apm-data)
- [FAQ](#faq)
- [References](#references)



## Prerequisites

1. [Install Docker](https://docs.docker.com/get-docker/)

2. [Install Docker Compose](https://docs.docker.com/compose/install/) - If you are using Docker Desktop (MacOS or Windows)      Compose is already installed.

3. [Setup Datadog 14 Day Trial](https://www.datadoghq.com/)

4. Follow instructions to install the Docker integration

5. Take note of your Datadog API and APP key (Integrations > APIs in the console)
    - you'll need these keys for the various examples in this repo

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/apikey.png "title")




## Getting Started

- ```git clone``` this repository

- Update your ```DD_API_KEY``` in ```docker-compose.yaml```

- run ```docker-compose up```



## Walkthrough

### Datadog Console


#### You now have a Datadog agent running in a Docker container on your machine. Lets check it out on the Datadog [console](https://app.datadoghq.com/dashboard/lists).

- In the console select ```infrastructure``` > ```host map```

##### A host map visualize hosts together on one screen, with metrics made comprehensible via color and shape.

- Click on the host to see more information

- On the bottom left corner you will see tags associated with your host.
    - Host tags enable you to observe aggregate performance across a number of hosts
    - Host tags are defined with the ```DD_TAGS``` environment variable in the ```docker-compose.yaml```

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/tagsnew.png "title")

#### You can see that a postgres database container is running within the host

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/postgresnew.png "title")

- this is done by running the agent container as sidecar to postgres through the ```docker-compose.yaml```

```yaml
version: "2"
services:

  postgres:
    image: postgres:10-alpine
    environment:
        - POSTGRES_DB=postgres
        - POSTGRES_USER=postgres
        - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql


    ... Code ommited for clarity ...

  datadog:
    build:
      context: ./agent
      dockerfile: Dockerfile
    environment:
     - DD_APM_ENABLED=true
     - DD_APM_NON_LOCAL_TRAFFIC=true
     - DD_API_KEY=166778f02f524bf7e00573d19a7d5ae1
     - DD_TAGS="tag1:value1 tag2:value2 tag3:value3"
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /proc/:/host/proc/:ro
     - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
    labels:
      com.datadoghq.ad.check_names: '["postgres"]'
      com.datadoghq.ad.init_configs: '[{}]'
      com.datadoghq.ad.instances: '[{"host": "postgres","port":"5432","username":"datadog","password":"datadog"}]'

```


- The agent container connects to postgres container via [Docker-Compose Network](https://docs.docker.com/compose/networking/)


- Uses [Autodiscovery](https://docs.datadoghq.com/agent/docker/integrations/?tab=docker#configuration) via ```labels:```

```yaml
labels:
      com.datadoghq.ad.check_names: '["postgres"]'
      com.datadoghq.ad.init_configs: '[{}]'
      com.datadoghq.ad.instances: '[{"host": "postgres","port":"5432","username":"datadog","password":"datadog"}]'
```



- Complete the Postgres integration by
    - entering into the ```integrations``` menu

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/postgres1.png "text")

    - search ```postgres```

    - Scroll down and click

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/postgres2.png "text")

    (Ignore the configuration instructions since thats handled in the ```init.sql``` )

- Now ```dashboard > dashboard list ``` on the console should display ```Postgres-metrics``` as an option

[Postgres Metrics](https://p.datadoghq.com/sb/rzjjh1tim3wtvb6p-e07484dcaa4560f7856d5b5cb999bb6f) - link to dashboard

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/postgres4.png "text")

 ---

### Collecting Metrics


#### Along with the out-of-box agent checks (CPU,uptime,IO), Datadog allows users to write custom agent checks.

- Lets take a look at the example in this repo
    ```bash
    ├── agent
    │   ├── checks
    │   │   ├── custom_check.py
    │   ├── conf
    │   │   ├── custom_check.yaml
    │   ├── Dockerfile

    ```
    - custom checks are composed of a ```.py``` with the check logic and a ```yaml``` config file
        - custom_check.py

        ```python
        import random
        # the following try/except block will make the custom check compatible with any Agent version
        try:
        # first, try to import the base class from new versions of the Agent...
        except ImportError:
            # ...if the above failed, the check is running in Agent version < 6.6.0
            from checks import AgentCheck


        __version__ = "1.0.0"

        #Custom Check that sends a random value between 0 and 1000 for the metric 'my_metric'
        class MyMetricCheck(AgentCheck):
            def check(self, instance):
                self.gauge('my_metric', random.randint(0,1000), tags=['test_tag:bglin'])
        ```
        - custom_check.yaml

        ```yaml
        init_config:

            instances:
                - min_collection_interval: 45
        ```

    - these files go in specific directories on the agent container as shown in the ```Dockerfile```

        ```docker
        COPY ./conf/custom_check.yaml /etc/datadog-agent/conf.d/custom_check.yaml
        COPY ./checks/custom_check.py /etc/datadog-agent/checks.d/custom_check.py
        ```

 To change the collection interval of your check, use ```min_collection_interval``` in the configuration file. The default value is ```15``` which means the ```check``` method from your class is invoked with the same interval as the rest of the integrations on the Agent.

---

### Visualizing Data


#### You can build custom dashboards through the console using drag and drop features or you can programmatically create them through the [Datadog API](https://docs.datadoghq.com/api/v1/dashboards/). This repo has an example of creating a Timeboard via the API.

- open ```timeboard.py``` and update the ```api_key``` and ```app_key``` variables

```python
options = {
    'api_key': 'your_api_key_goes_here',
    'app_key': 'your_app_key_goes_here'
}
```

- within the ```dashboard``` directory run these commands:

    - ```docker build -t timeboard_example:latest . ```

    - ```docker run timeboard_example:latest```

-  ```dashboard > dashboard list ```  in the console now lists the new Timeboard

[Example Timeboard](https://p.datadoghq.com/sb/rzjjh1tim3wtvb6p-b93d4c22346e4bb3638cf99dbb853063) - - link to timeboard

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/timeboard.png "text")

   - the Example Timeboard consists of three visualizations
        - My Metric scoped over the docker host

        - My Metric applied with the rollup() function

        - docker.cpu.user with the anomalies() function

            - The anomaly function identifies when a metric is behaving differently then it has in the past. It takes into                   account trends, seasonal day-of-week, and time-of-day patterns. In the dashboard example, the anomaly graph                   identifies anomolies (in red) as changes in the metric that are two standard deviations away from the ordinary                 value.
     - You can change the timeframe of the board and send snapshot via email

     ![Recordit GIF](http://g.recordit.co/jqI6danbdT.gif)

     ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/newemail.png "text")

---

### Monitoring Data


####  Datadog gives you the ability to create monitors that actively check metrics, integration availability, network endpoints, and more.

- To create a monitor in Datadog, hover over **Monitors** in the main menu and click **New Monitor** in the sub-menu.

- The following monitor on My Metric sends:

    - A warning for values above 500
    - An alert for values above 800
    - A notification when there's no data for this metric in the last 10 minutes

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/monitor1.png "text")

- the monitor can be configured  to send the message to an email

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/monitor2.png "text")
![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/alert.png "text")


####  You can also schedule downtime to silence the alerts on your monitors

- To schedule downtime hover over **Monitors** in the main menu and click **Manage Downtime** in the sub-menu.
    - scheduled downtime on weekdays from 7PM to 9AM

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/downtime1.png "text")

    - scheduled downtime on weekends


    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/downtime2.png "text")

    - email notification for weekend downtime:

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/email1.png "text")

    - email notification for weekday downtime

    ![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/email2.png "text")

---

### Collecting APM Data

#### Datadog has an application monitoring solution that provides full-stack observability for modern applications.

-  The ```docker-compose.yaml``` in the beginning of this guide deploys a sample application instrumented with the APM            solution.

```yaml

... code ommited for clarity ...

flask:
    build:
      context: ./apm
      dockerfile: Dockerfile
    environment:
      - DD_AGENT_HOST=datadog
      - DD_TRACE_AGENT_PORT=8126
    ports:
      - "5050:5050"

  load-generator:
    build:
      context: ./load-generator
      dockerfile: Dockerfile

  datadog:
    build:
      context: ./agent
      dockerfile: Dockerfile
    environment:
     - DD_APM_ENABLED=true
     - DD_APM_NON_LOCAL_TRAFFIC=true
     - DD_API_KEY=166778f02f524bf7e00573d19a7d5ae1
     - DD_TAGS="tag1:value1 tag2:value2 tag3:value3"
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /proc/:/host/proc/:ro
     - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
    labels:
      com.datadoghq.ad.check_names: '["postgres"]'
      com.datadoghq.ad.init_configs: '[{}]'
      com.datadoghq.ad.instances: '[{"host": "postgres","port":"5432","username":"datadog","password":"datadog"}]'
```

- APM is enabled via the environment variable  ```DD_APM_ENABLED``` and allows tracing from other containers via ```DD_APM_NON_LOCAL_TRAFFIC```

- The ```flask``` service, is configured to submit traces to the agent container via ```DD_AGENT_HOST``` and  ```DD_TRACE_AGENT_PORT``` environment variables

- the sample application resides in the ```apm``` directory

    ```python
    from flask import Flask
    import logging
    import sys
    from ddtrace import patch_all

    patch_all()


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
    ```

 - the ```ddtrace``` module instruments all the application endpoints automatically via the ```patch_all()``` function


- the ```load-generator``` service uses [locustio](https://locust.io/) to generate traffic on the application

    ```python
    from locust import HttpLocust, TaskSet, task, between

    class UserBehaviour(TaskSet):

        @task(4)
        def index(self):
            self.client.get('/')

        @task(2)
        def apm_endpoint(self):
            self.client.get('/api/apm')

        @task(1)
        def trace_endpoint(self):
            self.client.get('/api/trace')

    class WebsiteUser(HttpLocust):
        task_set = UserBehaviour
        wait_time = between(5, 9)
    ```

[Example Custom APM Dashboard](https://p.datadoghq.com/sb/rzjjh1tim3wtvb6p-6bbf5e190686293e502578155990064c) - link to dashboard

![alt text](https://github.com/bruno-lin/hiring-engineers/blob/solutions-engineer/images/apm.png "Title")

> See the FAQ on the differences between a service and a resource


---


## FAQ
> In this section you will find the answers to the questions asked throughout the exercise.

### Collecting Metrics
- **Can you change the collection interval without modifying the Python check file?**

    - To change the collection interval of your check, use ```min_collection_interval``` in the configuration file. The             default value is ```15``` which means the ```check``` method from your class is invoked with the same interval as the         rest of the integrations on the Agent.

### Visualizing Data
- **What is the anomaly graph displaying?**

    - The anomaly function identifies when a metric is behaving differently then it has in the past. It takes into account           trends, seasonal day-of-week, and time-of-day patterns. In the dashboard example, the anomaly graph identifies anomolies       (in red) as changes in the metric that are two standard deviations away from the ordinary value.

### Collecting APM Data
- **What is the difference between a Service and a Resource?**
    - A **service** is the overarching term for software that delivers content. For example, in a microservices architecture,      there exists smaller services connected to each other such as an API, database and web page. Each microservice is              contained and serves a single purpose.

    - A **resource** describes the data that a service makes available. For example,
     in an API service, the resources are the different data that the API makes available via its endpoints.


### Final Question
- **Is there anything creative you would use Datadog for?**
    - A lot of companies today are exploring the implementation of chatbots to handle certain aspects of their       business. Chatbots have many use cases from internal(employee facing) to external (customer facing). For example, a chatbot could be deployed internally within a company to handle common human resource inquiries or process request such as an expense form. A chatbot could also be used externally to handle customer service.

    Deploying a chatbot is an iterative development process. Developers need to refine and manage the training data as the chatbot interacts with inputs in order to maximize success. Utilizing the Datadog platform, I could see this process being streamlined. Developers would be able to track performance in real time and make parameter changes accordingly. Along with monitoring the chatbot performance, you can also collect data on user behavior which has great value for a business.



## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)



---
