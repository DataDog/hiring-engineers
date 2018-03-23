Your answers to the questions go here.

## Collecting Metrics

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/195rm1" title="Host Map Screen showing tags"><img src="https://farm1.staticflickr.com/795/39158435810_f96b2bf0ef_b.jpg" width="656" height="593" alt="Wyatt-DD-01"></a>


Bonus Question Can you change the collection interval without modifying the Python check file you created?
  I added the parameter min_collection_interval: 45  to the init section of my my_metric.yaml file.  So I would say yes.
  
Bonus Question: What is the Anomaly graph displaying?
  The anomaly graph shows the normal bounds for a value on the graph as defined in my custom script:
  'basic', '48', direction='above'
  so then it is a basic anomally line that would highight if the value of the plotted point was above the value of 48 +/- a small  
  tolerance
  

