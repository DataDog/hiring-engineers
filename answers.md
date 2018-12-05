Your answers to the questions go here.

Collection Metrics:
The collection interverval is changed in the config file of the custom agent (mycheck.yaml)

Visualizing Data:
Anomoly graph is displaying the standard deviation from the norm for documents inserted per second. 
The bounds for the deviation is set to 2 and the type is basic. 
The Basic type uses simple lagging rolling quantile computation to determine the range of expected values, b
The bounds of 2 will flag anything that is 2 times or more the normal deviation. 

Monitoring Data:
See screen shots

Collection APM Data:
A "Service" is the name of a set of processes that work together to provide a feature set.
These services are defined by the user when instrumenting their application with Datadog. 

A "Resourc" is a particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ? The Tracing backend can track thousands (not millions or billions) of unique resources per service, so resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources.
These resources can be found after clicking on a particular service. 

Bonus Questions:
I would use Datadog to monitor the locations of people who view a particular instagram page so that we can tell which pages pull the most internation views.

Link to HostMap: https://app.datadoghq.com/dash/1010026/my-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1543894200000&to_ts=1543980600000&live=true

Link to Timeboard: https://app.datadoghq.com/dash/1010026/my-timeboard?tile_size=m&page=0&is_auto=false&from_ts=1543894200000&to_ts=1543980600000&live=true
