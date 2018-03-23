Your answers to the questions go here.

## Collecting Metrics

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/195rm1" title="Host Map Screen showing tags"><img src="https://farm1.staticflickr.com/795/39158435810_f96b2bf0ef_b.jpg" width="656" height="593" alt="Wyatt-DD-01"></a>


Bonus Question Can you change the collection interval without modifying the Python check file you created?
  I added the parameter min_collection_interval: 45  to the init section of my my_metric.yaml file.  So I would say yes.


## Visualising Data

Bonus Question: What is the Anomaly graph displaying?

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/Lm6b90" title="Anomaly-Graph"><img src="https://farm1.staticflickr.com/813/40258707614_a5d9d91ff6_z.jpg" width="609" height="210" alt="Anomaly-Graph"></a>

The parts of this CPU graph coloured RED are showing that for this basic anomaly profile the value is outside of the norm.  In this case given the parameters I used ('1e-3', direction='above') any spikes above the value of 1e-3 will be highlighted as outside of the norm.


## Monitoring Data

Bonus Question:  Set Monitoring Schedule Downtime

The following 2 graphics in combination show that the downtime is configured for the intervals as specified in the question, namely:
weekdays blackout from 7:00pm thru 9:00am the following morning

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/9XXn3C" title="downtime1"><img src="https://farm1.staticflickr.com/803/39158730080_6de7b7f512_z.jpg" width="640" height="164" alt="downtime1"></a>

and over the weekend from 7:00pm Friday evening thru 9:00am Monday morning

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/73v2i6" title="downtime2"><img src="https://farm1.staticflickr.com/805/40074407335_b2da7ab705_z.jpg" width="640" height="151" alt="downtime2"></a>

Here are screenshots of the email notifications sent at the start:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/NFU6bY" title="downtime-email1"><img src="https://farm1.staticflickr.com/794/40074537625_322f7fefc6_z.jpg" width="640" height="481" alt="downtime-email1"></a>

and end:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/uk1by4" title="downtime-email2"><img src="https://farm5.staticflickr.com/4783/40074538275_92b6a43804_z.jpg" width="640" height="462" alt="downtime-email2"></a>

of the midweek downtime.



