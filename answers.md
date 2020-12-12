Section I: Collecting Metrics

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
https://s3.console.aws.amazon.com/s3/object/la-psql-zebra?region=us-east-1&prefix=host_tags.PNG

I choose to install PostgreSQL and installed the Datadog integration for Postgres. This can be verified in Section II by viewing my dashboard. 

Bonus Question Can you change the collection interval without modifying the Python check file you created? 
Yes, I modified conf.d/my_metric.yaml to include - min_collection_interval: 45. 

Section II: Visualizing Data
