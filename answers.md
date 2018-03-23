Your answers to the questions go here.

## Collecting Metrics

<a title="Wyatt: Datadog Host Screen Showing Tags">
<img src="https://www.flickr.com/gp/157063551@N05/80895e"></a>

Bonus Question Can you change the collection interval without modifying the Python check file you created?
  I added the parameter min_collection_interval: 45  to the init section of my my_metric.yaml file.  So I would say yes.
  
Bonus Question: What is the Anomaly graph displaying?
  The anomaly graph shows the normal bounds for a value on the graph as defined in my custom script:
  'basic', '48', direction='above'
  so then it is a basic anomally line that would highight if the value of the plotted point was above the value of 48 +/- a small  
  tolerance
  

