TASK #8:
Display any metric from the Integration on your Database with the anomaly function applied.
Bonus Question: What is the Anomaly graph displaying?

ANSWER #8:

Brief Explanation:
Anomaly graph is very useful to identify metrics outside the norm. It is displayed based on the width gap of the standard graph. By default, the width factor is 2, if Datadog detects graph that’s wider than 2, it will be considered as anomaly behavior. 
I think anomaly can represent to know the uncommon. The use case for anomaly doesn’t always mean bad, example: if I have a burst of my sales revenue out of the norm; that could be one of the best thing that can happen.
 
The graph below is showing some anomaly out of the standard line in blue.
I can trace when the anomaly occurred based on the timestamp and I might be able to correlate this anomaly with other metrics that happen on the same time line.

Steps:
- On the timeboard dashboard, at one time series widget
- Go to function > Algorithms > Anonmalies to display anomaly graph (answer-task8-pic1.png)
- Change the time period of the graph and start seeing the anomaly (answer-task8-pic2.png)

 Snaptshots:
 - answer-task8-pic1.png
 - answer-task8-pic2.png

Json script:
{
  "viz": "timeseries",
  "requests": [
    {
      "q": "anomalies(avg:mysql.net.connections{host:sg-db-01}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "aggregator": "avg",
      "conditional_formats": []
    },
    {
      "q": "anomalies(avg:mysql.performance.com_load{host:sg-db-01}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ],
  "autoscale": true
}
 
Reference:
https://docs.datadoghq.com/graphing/functions/algorithms/#anomalies
