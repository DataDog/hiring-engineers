Your answers to the questions go here.


Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:

![add_tags](https://user-images.githubusercontent.com/38845846/51808195-8fabce80-2245-11e9-8d31-d6f26b07f1f3.png)

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.



-Bonus Question Can you change the collection interval without modifying the Python check file you created?

The collection interval is updated in the /config.d/custom_random.yaml file, rather than the /checks.d/custom.randon.py file.



Visualizing Data:

Timeboard snapshot:

![screen shot 2019-01-28 at 11 33 07 am](https://user-images.githubusercontent.com/38845846/51861256-9e9b8b00-22f0-11e9-91ae-c1c4dd945699.png)




Monitoring Data:
New Alert Monitor screenshots:

![screen shot 2019-01-28 at 11 28 06 am](https://user-images.githubusercontent.com/38845846/51861025-056c7480-22f0-11e9-8228-fdf22e57455b.png)

![screen shot 2019-01-28 at 11 26 00 am](https://user-images.githubusercontent.com/38845846/51861054-1b7a3500-22f0-11e9-987d-327dc9c37108.png)


Downtime for scheduled alert:
![screen shot 2019-01-28 at 11 27 45 am](https://user-images.githubusercontent.com/38845846/51861015-feddfd00-22ef-11e9-809b-53d78e7150f0.png)

![screen shot 2019-01-28 at 11 25 43 am](https://user-images.githubusercontent.com/38845846/51861037-0ef5dc80-22f0-11e9-9ad3-77efb7b0a65c.png)

