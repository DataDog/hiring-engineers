Finally the last piece of the Datadog puzzle is something that really sets the offering apart from anything else on the market: Application Performance Monitoring or APM


# Application Performance Monitoring

Datadog's APM offering is extremely robust and I'll only scratch the surface here. APM allows you to set up traces within your codebase to monitor the performance of your code in production with all of the visualizations, anomoly detection algorithms and alerting capabilities we've already discussed so far.

You can use any application you'd like for this as long as you know the language it was written in and have a way of starting the application yourself. For the purposes of this demo, let's take a very small `Flask` application with three routes that just returns a 200 with every request. You can [get the code here](./app.py).


You can find [the dashboard I created](https://app.datadoghq.com/dashboard/qgp-qjj-7ap?from_ts=1587139760095&live=true&to_ts=1587143360095) here.
