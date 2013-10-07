# The Challenge

## Questions
1. Sign up for Datadog, get the agent reporting metrics from your local machine. Bonus question- what is the agent?

2. Submit an event via the API. 

3. Get an event to appear in your email inbox (the email address you signed up for the account with)

4. Technical Challenge: 
  * Take a simple web app ([in any language](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd.
  * While running a load test for a few minutes, visualize page views per second. Send us the link to this graph!
  * Create a histogram to see the latency; also give us the link to the graph
  * Bonus points for putting together more creative dashboards.

If you need a tool to load-test your web app you can use tools like:
* [ab](https://httpd.apache.org/docs/2.2/programs/ab.html)
* [tsung](http://tsung.erlang-projects.org/user_manual.html#htoc2)

## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit your code for question #3.
4. Submit a pull request.

# References:
* [API docs](http://docs.datadoghq.com/api)
* [Guide to the Agent](http://docs.datadoghq.com/guides/basic_agent_usage/)
* [Libraries](http://docs.datadoghq.com/libraries/)
* [Guide to Metrics](http://docs.datadoghq.com/guides/metrics/)
