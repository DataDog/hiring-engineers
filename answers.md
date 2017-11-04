# Solutions Engineer Technical Challenge:

## Collecting Metrics

    1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

        datadog.conf:

            tags: region: east, env:prod, role:database, database:primary, name:practice

        Host Map page: 

            <img width="1373" alt="screen shot 2017-11-02 at 10 06 22 pm" src="https://user-images.githubusercontent.com/22550176/32390708-df8aa4ce-c0a5-11e7-9d8d-8c105e2b7fe7.png">

    2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

        postgres.yaml: 

            init.config:

            instances:
              - host: localhost
                port: 5432
                username: datadog
                password: a

        Datadog integration:

            <img width="1073" alt="screen shot 2017-11-02 at 11 57 30 pm" src="https://user-images.githubusercontent.com/22550176/32400541-f6cbbd4e-c0d7-11e7-9475-89e6560c85fc.png">

            <img width="1002" alt="screen shot 2017-11-03 at 11 47 49 am" src="https://user-images.githubusercontent.com/22550176/32400551-055beabe-c0d8-11e7-9628-a14fa2da2af7.png">

    3.Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

       checks.d/check.py:

            from checks import AgentCheck
            import random

            class RandomCheck(AgentCheck):
                def check(self, instance):
                    rand = random.randint(0, 1001)
                    self.gauge('my_metric', rand)

        conf.d/check.yaml:

            init_config:

            instances:
                [{}]

    4. Change your check's collection interval so that it only submits the metric once every 45 seconds./Bonus Question: Can you change the collection interval without modifying the Python check file you created?

        conf.d/check.yaml:

            init_config:
                min_collection_interval: 45

            instances:
                [{}]

## Visualizing Data

    1. Utilize the Datadog API to create a Timeboard that contains:

        a. Your custom metric scoped over your host.

        <img width="979" alt="screen shot 2017-11-03 at 12 01 01 pm" src="https://user-images.githubusercontent.com/22550176/32400664-7058002c-c0d9-11e7-998d-6bcd9f42538c.png">

        b. Any metric from the Integration on your Database with the anomaly function applied.

        <img width="979" alt="screen shot 2017-11-03 at 11 59 26 am" src="https://user-images.githubusercontent.com/22550176/32400673-91995f06-c0d9-11e7-9c15-98b286dc9301.png">

        c. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

        <img width="980" alt="screen shot 2017-11-03 at 11 54 10 am" src="https://user-images.githubusercontent.com/22550176/32400683-af7cfbd6-c0d9-11e7-8167-b9a7370ab402.png">

        Timeboard:

        <img width="1209" alt="screen shot 2017-11-03 at 12 02 30 pm" src="https://user-images.githubusercontent.com/22550176/32400711-044a6eaa-c0da-11e7-9bb7-38d7fdf90d42.png">

    2. Once this is created, access the Dashboard from your Dashboard List in the UI:

        a. Set the Timeboard's timeframe to the past 5 minutes

        <img width="1204" alt="screen shot 2017-11-03 at 12 26 22 pm" src="https://user-images.githubusercontent.com/22550176/32400733-47cb5554-c0da-11e7-917e-28406a89e921.png">

        b. Take a snapshot of this graph and use the @ notation to send it to yourself.

        <img width="571" alt="screen shot 2017-11-03 at 12 36 26 pm" src="https://user-images.githubusercontent.com/22550176/32400757-96166ba4-c0da-11e7-818b-c3af0892db85.png">

        <img width="569" alt="screen shot 2017-11-03 at 12 34 52 pm" src="https://user-images.githubusercontent.com/22550176/32400762-9f3d0b2a-c0da-11e7-8ace-f34a67909c85.png">

        <img width="572" alt="screen shot 2017-11-03 at 12 35 58 pm" src="https://user-images.githubusercontent.com/22550176/32400765-a580560e-c0da-11e7-8333-9a642bbb501d.png">

        Bonus Question: What is the Anomaly Graph Displaying?

        The Anomaly Graph highlights data that falls a specified number of standard deviations above or below the value expected at a point in time, given the recent behavior of the data. In the case of my graph, data points inside the gray locus fall within two standard deviations of the expected value at that time, while the red locus describes data points that fall outside of that range. 

## Monitoring Data

    1. Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it's above the following values over the past 5 minutes:
        
        a. Warning threshold of 500

        b. Alerting threshold of 800

        c. And also ensure that it will notify you if there is No Data for this query over the past 10m.

        <img width="1170" alt="screen shot 2017-11-03 at 10 12 19 pm" src="https://user-images.githubusercontent.com/22550176/32401419-2463c6c8-c0e4-11e7-920b-2d4071d1429f.png">

        <img width="1167" alt="screen shot 2017-11-03 at 1 06 13 pm" src="https://user-images.githubusercontent.com/22550176/32401085-e950fca4-c0de-11e7-97e6-d8479e33f81a.png">

    2. Please configure the monitor’s message so that it will:

        a. Send you an email whenever the monitor triggers.

        b. Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

        c. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

        <img width="1190" alt="screen shot 2017-11-03 at 10 14 14 pm" src="https://user-images.githubusercontent.com/22550176/32401429-6ce3459a-c0e4-11e7-8a03-15b8cceb224b.png">

        d. When this monitor sends you an email notification, take a screenshot of the email that it sends you.

        <img width="814" alt="screen shot 2017-11-03 at 1 25 17 pm" src="https://user-images.githubusercontent.com/22550176/32401036-66268862-c0de-11e7-991a-9e88decee25d.png">

    Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

        a. One that silences it from 7pm to 9am daily on M-F 

        <img width="688" alt="screen shot 2017-11-03 at 10 05 08 pm" src="https://user-images.githubusercontent.com/22550176/32401369-42d05302-c0e3-11e7-9007-3eb1aa697707.png">

        b. And one that silences it all day on Sat-Sun. 

        <img width="689" alt="screen shot 2017-11-03 at 10 05 45 pm" src="https://user-images.githubusercontent.com/22550176/32401373-55d7237c-c0e3-11e7-8f70-8985388af1fd.png">

        c. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

        <img width="812" alt="screen shot 2017-11-03 at 9 39 55 pm" src="https://user-images.githubusercontent.com/22550176/32401137-abe7b76c-c0df-11e7-9e49-7dca52ea0a14.png">

## Collecting APM Data

    1. Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

    link: https://p.datadoghq.com/sb/949c6719c-85b88adf09 
    
    <img width="1210" alt="screen shot 2017-11-03 at 9 59 47 pm" src="https://user-images.githubusercontent.com/22550176/32401318-82f06450-c0e2-11e7-9f77-4b44990f4975.png">

    Bonus Question: What is the difference between a Service and a Resource?

    A Service is a group of processes that work together to perform a specific function. A Resource is a query that calls upon a Service in order to get something from it. 

## Final Question

