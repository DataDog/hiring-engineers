TASK #5: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

ANSWER #5:

Brief Explanation:
This is a simple random number generator between 0 and 1000 with python script that will be collected by the agent. 
The use case is limitless. I can use it for collecting non-default metric that produced by the script.
There are different kind of metric type such as Gauge and Rate, this will differentiate how the metric gets collected. Gauge will be collected as the current metric shows up from the script. Rate is used for collecting the delta between collection intervals.
I’m using Gauge in this script because I want to get the current random number.
Rate can be used if the number if increasing, so I want to get the rate to know how much it gets increased for each collection.

Steps:
- Created python script

Snapshots:
- answer-task5-pic1.png

Ref:
https://datadog.github.io/summit-training-session/handson/customagentcheck/
