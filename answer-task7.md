Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

TASK #7: Display your custom metric scoped over your host.

ANSWER #7:

Brief Explanation:
The host agent that has been integrated with the custom metric quite immediately after the restart in Task 6.
I can correlate this metric easily among other metrics in the hostmap to help pinpointing some related issues with that host.
I created 1 timeboard dashboard with 3 main widgets for the custom metric.
- Widget1: host map to show the host map
- Widget2: query (answer-task7-pic2.png) to display the last metric from the custom script
- Widget3: historical graph (answer-task7-pic3.png) to display the historical graph of the metric

Steps:
- Go to Host Map and look for new my metric on the Host (answer-task7-pic1.png)
- Build a new timeboard and display 3 widgets for my metric
- Dashboard widgets can be seen here: answer-task7-json1.txt

Snapshots:
- answer-task7-pic1.png
- answer-task7-pic2.png
- answer-task7-pic3.png

Scripts:
- answer-task7-json1.txt

Reference:
https://docs.datadoghq.com/getting_started/#dashboards
