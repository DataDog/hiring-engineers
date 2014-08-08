# Answers

## Level 1

* Two separate ways of sending the event via email
1. Send using the flask-mail API (attempt can be found in mailTest.py)
2. Send using @ notifications (attempt can be found in eventTest.py)
* Bonus answer: The agent is a process that handles the collection of local events/metrics and sends them to Datadog

## Level 2

### Webapp and code used for Levels 2-5 can be found at https://github.com/handigarde/san-francisco-food-carts  

* A basic incrementer was added to each function handling page responses (statsd.increment('cart-api.requests')) for basic metrics handling
* A timed decorator was added to these functions in order to detect latency (@statsd.timed('cart-api.request_time'))
* Graphs for the metrics and latency can be found in the "Level 2" dashboard at https://app.datadoghq.com/dash/dash/26059
* For reference to metrics collected during the test, a screenshot has been placed in screenshots/Level_2_Graphs.png

## Level 3

* Tags were added to incrementers and timers to be able to differentiate between individual pages while maintaining ability to aggregate all metrics under one name (i.e. tags=['support','page:options'])
* Stacked latency graph can be found in the "Level 3" dashboard at https://app.datadoghq.com/dash/dash/26086
* For reference to metrics collected during the test, a screenshot has been placed in screenshots/Level_3_Graph.png

## Level 4

* Tags for incrementers were used for the Level 4 check, however rather than gathering the average, a sum was taken on the value to gather a total number of page views
* Page view counts can be found in the "Level 4" dashboard at https://app.datadoghq.com/dash/dash/26071
* For reference to metrics collected during the test, a screenshot has been placed in screenshots/Level_4_Graphs.png

## Level 5

* checks.d/randomCheck.py created for the check
* conf.d/randomCheck.yaml created for configuration