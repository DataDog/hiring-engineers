## Collecting Metrics:
The tags were added by updating the tags attribute in the yaml file located at `/etc/datadog-agent/datadog.yaml`:
![Updated tags](/images/update_tags.png "Update tags image")

Verified that the tags were changed on the application:
![Verified tags](/images/verify_tags.png "Post tag verification")

Installed  MongoDB and the datadog integration for MongoDB is already installed into the agent as noted [here](https://docs.datadoghq.com/integrations/mongo/?tab=standalone). I was able to verify that the integration worked by running a check:
![Verified mongo](/images/verify_mongo.png "Post mongo verification")

Created a custom agent check named my_metric that submitted a random value between 0 and 1000 and changed the collection interval to 45 seconds by updating the `/etc/datadog-agent/config.d/my_metric.yaml` file to add the time interval attribute:
![Verified custom agent](/images/verify_custom_metric.png "Post mongo verification")

## Visualizing Data:


## Monitoring Data


## Collecting APM Data:


## Final Question: