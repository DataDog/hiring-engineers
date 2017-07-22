Steven Wang's Answer

# Level 1 - Collecting your Data

+ Screenshot of tags in Host Map :

    Following picture shows the Host Map after I installed Datadog agent on my local host. Tags have been added via UI and Agent Config file.
    ![image](https://user-images.githubusercontent.com/8587006/28491447-1ecbe354-6f35-11e7-9c43-233710acb87f.png)

+ Bonus :

    The Agent is a client software that are ruuning on the target hosts and collecting statistics. It collects events and metrics, including CPU , memory, network status and even severs connections, request/sec, etc. All collected data would be organised and then sent to *Datadog SaaS*. After login personal account, we can check the gathered data graphically. 

    DataDog Agent mainly have four components, which are implemented in Python and running as seperated process in the system.
    + Collector (agent.py)
        
        It checks the integration environment of running hosts, and gather standard performance statistics, like CPU and memory
    + DogStatsD (dogstatsd.py)

        This is the StatsD server, which is running at background. It is collecting the customised metrics

    + Forwarder (ddagent.py)

        *Forwarder* takes responsibility to push the data coming from *Collector* & *DogStatsD* to a queue, which will be sent to *Datadoghq.com*
    
    + SupervisorD

        It is running in a separated process and is used to monitor all collecting and forwarding procedure above.

+ Agent Check :
  + Customer Agent Check Script

    Following pic shows customer agent check Python script.
    ![check](https://user-images.githubusercontent.com/8587006/28492654-9f45a8e8-6f4a-11e7-8802-bf277a3478d5.JPG)

  + Config file

    Following shows YAML config file for test.support.random

    ![image](https://user-images.githubusercontent.com/8587006/28491906-668aafe8-6f3c-11e7-8188-5a2a8c9afc02.png)
# Level 2 - Visualizing your Data
+ screenshot of database and customer random metrics : 
    
    Following pic illustrates the database and random metrics status
    ![database random](https://user-images.githubusercontent.com/8587006/28491959-258ffc72-6f3d-11e7-9267-0c6c2e800d1b.JPG)
    
+ Bonus : 
    
    The timeboards show all graphs scoped to the same time. All the showed graphs will be displayed in a grid-like structure. In such way, users can do troubleshooting and correlation easily. In addition, a TimeBoard graphic can be shared individually. A screenboard is used to illustrated higher level of monitoring. It has more customised options. Lots of widgets can be operated by drag-and-drop to anywhere you like, and displayed in a different time frame. We can even add notes or call-outs. Moreover, live ScreenBoards can be easily shared as read-only with others, whereas TimeBoards cannot.

+ Screenshot snapshot of 'test.support.random' graph :
    
    I receive the email immediately after snapshot sent with @notification
    ![test random value above 0 9](https://user-images.githubusercontent.com/8587006/28491913-86ecbd9e-6f3c-11e7-9ca3-96a06f82919a.jpg)

# Level 3 - Alerting on your Data
+ Screenshot of Monitor Email Alert:

    ![multiple aler above 0 9](https://user-images.githubusercontent.com/8587006/28492058-f91cdab4-6f3e-11e7-86a8-e2c64476976b.jpg)
+ Bonus:

    Make it a multi-alert by host
    ![multiple alert](https://user-images.githubusercontent.com/8587006/28491983-9d9bf2de-6f3d-11e7-87b8-244b04ab305f.JPG)

+ Bonus:

    A scheduled downtime for this monitor that silences it from 7pm to 9am daily
    ![schedule](https://user-images.githubusercontent.com/8587006/28492019-4acb19e4-6f3e-11e7-86b3-d15a27259553.JPG)

    And I also received an email about the scheduled downtime.
    ![schdule2](https://user-images.githubusercontent.com/8587006/28492045-ca4398c2-6f3e-11e7-8bf0-735506316840.JPG)




