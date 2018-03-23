Your answers to the questions go here.

## Collecting Metrics

[datadog.yaml file with tags set](datadog.yaml)



<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/195rm1" title="Host Map Screen showing tags"><img src="https://farm1.staticflickr.com/795/39158435810_f96b2bf0ef_b.jpg" width="656" height="593" alt="Wyatt-DD-01"></a>


[MySQL Config file with tags set](conf.yaml.mysql)

[my_metric python source](my_metric.py)

[my_metric Config file](my_metric.yaml)

Bonus Question Can you change the collection interval without modifying the Python check file you created?
  I added the parameter min_collection_interval: 45  to the init section of my my_metric.yaml file.  So I would say yes.


## Visualising Data

[timeboard creation script](timeboard2.py)

Here is a screenshot showing the timeboard resulting from this script (modified as per later in the exercise to include my APM graph)

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/W4J89F" title="InfraandAPM"><img src="https://farm5.staticflickr.com/4782/27097852958_3e4ff2a8ca_z.jpg" width="640" height="297" alt="InfraandAPM"></a>

5 minute "My_Metric" timeboard - sent via email using the @ tag:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/610501" title="My_Metric_5min_timeboard"><img src="https://farm1.staticflickr.com/813/39159109980_055eb8335a_z.jpg" width="640" height="570" alt="My_Metric_5min_timeboard"></a>


Bonus Question: What is the Anomaly graph displaying?

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/Lm6b90" title="Anomaly-Graph"><img src="https://farm1.staticflickr.com/813/40258707614_a5d9d91ff6_z.jpg" width="609" height="210" alt="Anomaly-Graph"></a>

The parts of this CPU graph coloured RED are showing that for this basic anomaly profile the value is outside of the norm.  In this case given the parameters I used ('1e-3', direction='above') any spikes above the value of 1e-3 will be highlighted as outside of the norm.


## Monitoring Data

Alert Conditions as defined in the exercise:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/Xqik83" title="alert_conditions"><img src="https://farm1.staticflickr.com/786/26096620287_50d27f78dc_z.jpg" width="640" height="333" alt="alert_conditions"></a>

Alert Message Configuration:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/PZ0Qv4" title="Alert-Email-Config"><img src="https://farm1.staticflickr.com/810/40078163785_80ace841ac_z.jpg" width="640" height="297" alt="Alert-Email-Config"></a>


and an email that has resulted from the configuration:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/V688i6" title="AlertingEmail"><img src="https://farm1.staticflickr.com/808/39162932020_a14a2fc673_z.jpg" width="640" height="548" alt="AlertingEmail"></a>


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


## Collecting APM Data

[instrumented flask file](myFlask.py)

Bonus Question: What is the difference between a Service and a Resource?
A service is a collection of processes that contribute to the same application.  For example a dynamic website may have UI (web html) and data (database) services.

Resources on the other hand represent actions on those services.  Extending the example above the web UI service will have resource actions performed on it that are represented by URLs or handlers through the client side app.  Data service resources will include things like queries.

Here is a screenshot showing a mixuture of Infrastructure and APM Data:

<a data-flickr-embed="true" data-header="true"  href="https://www.flickr.com/gp/157063551@N05/W4J89F" title="InfraandAPM"><img src="https://farm5.staticflickr.com/4782/27097852958_3e4ff2a8ca_z.jpg" width="640" height="297" alt="InfraandAPM"></a>

## Imaginative Ways of Using DataDog?

A few ideas spring to mind:
- as a parent I actually insist on my kids sharing their location with me at all times from their mobile phone.  I made it a condition of my paying their bill and it is purely a safety thing.  To get to see where they are I need to log in to my iphone and enquire the appropriate app, but a more generic way would be to use Google Maps.

Using Datadog it would be possible to raise an alert if they are not where they should be (e.g. at school) at a particular time.  Furthermore it would also be possible to raise an alert if for whatever reason their location was not being shared.

- another idea is to try and elimate some of those wasted trips to the local retail park later in the evening.  I could write a simple website that you could search for your local retail park to return a list of retailers with shops there.  In turn then it would trawl those retailers websites to find the opening and closing times of those stores at that location and return a traffic light status by retailer as to when the stores are still open - Green for open, Red for closed and Amber for closing within the hour.
-  we could extend this idea to use the APIs for travel websites to check the RAG status for the local roads to see if the trip to the retail park is going to be smooth or not, or similarly local train, bus and tram services
