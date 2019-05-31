TASK #6: 
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?

ANSWER #6:

Brief Explanation:
At first, I added time wait to the python script to generate the random number within 45 seconds
Then I realized, I can simply change the default minimum collection interval is 15 seconds in the YAML file. This is configurable for each instance of application integration with the Datadog agent. 
I also found another way to change the interval by editing the individual Metric metadata under Datadog Web UI Menu: Metrics > Summary and find “my_metric” metrics (answer-task6-pic3.png)

Steps:
- Create python script /etc/datadog-agent/check.d/my_metric.py (answer-task6-pic1.png)
- Create yaml script /etc/datadog-agent/conf.d/my_metric.yaml as follows:
    init config:
    instances:
      [{}]
- Change the YAML file with min collection interval 45 (answer-task6-pic2.png)

 Snapshots:
 - answer-task6-pic1.png
 - answer-task6-pic2.png
 - answer-task6-pic3.png 
 
 Reference:
 https://docs.datadoghq.com/developers/metrics/custom_metrics/
