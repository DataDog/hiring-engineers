TASK #9:    
Display your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

ANSWER #9:

Brief Explanation:
Roll up function is used for aggregating / summarizing data points within 1 time period e.g: hourly, daily. There are 4 roll up summary:
-	Minimum: to display only the lowest data point
-	Maximum: to display only the highest data point
-	Average: to display the average calculation of total data points divided by number of data points that got collected during that period.
-	Sum: to display the total amount of data from each data point.

Steps:
- Create time series widget and change the function to roll up with 3600 seconds (1 hour)

Snapshots:
- answer-task9-pic1.png
- answer-task9-pic2.png

{
  "viz": "timeseries",
  "requests": [
    {
      "q": "avg:my_metric{*}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "aggregator": "avg",
      "conditional_formats": []
    }
  ],
  "autoscale": true
}

References:
https://docs.datadoghq.com/graphing/functions/rollup/
