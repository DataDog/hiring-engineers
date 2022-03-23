## Collecting Metrics
Can you change the collection interval without modifying the Python check file you created?
> Yes, an interval can be changed by updating the instance description in the `.yaml` file:
```
init_config:

instances:
    - min_collection_interval: 45
```

## Visualizing Data
What is the anomaly graph displaying?
> The anomaly graph is identifies when a particular metric is behaving differently that expected based on historical data. The algorithm is able to pick up what would be considered normal behavior, identifying seasonal trends/patterns, and this is able to highlight when a particular metric value falls outside of that normal behavior. In the partifulcar graph that I have setup in my dashboard, the anomalies are highlighted when the metric datapoint lands 2 deviations away from the normal behavior.
