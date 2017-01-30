If you'd like to apply as a devops evangelist at [Datadog](http://datadog.com) you are in the right spot. Here is the more formal [job description](http://jobs.datadoghq.com/apply/s2J6Da/DevOps-Evangelist.html).

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

# The Challenge

Don't forget to read the **References**.

## Questions

### Level 1

done * Sign up for Datadog, get the agent reporting metrics from your local machine.
done * Bonus question: what is the agent?
done * Submit an event via the API.
* Get an event to appear in your email inbox (the email address you signed up for the account with)

### Level 2

done * Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built, and instrument your code with dogstatsd. This will create **metrics**.
done * While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
done * Create a histogram to see the latency; also give us the link to the graph
done * Bonus points for putting together more creative dashboards.

### Level 3

Using the same web app from level 2:
done * tag your metrics with `support` (one tag for all metrics)
done * tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)
done * visualize the latency by page on a graph (using stacked areas, with one color per `page`)

### Level 4

Same web app:
done * count the overall number of page views using dogstatsd counters.
done * count the number of page views, split by page (hint: use tags)
done * visualize the results on a graph
done * Bonus question: do you know why the graphs are very spiky?
 
### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Post a screenshot of the `test.support.random` metric

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```

### Level 6

Now sum up your whole experience in a writeup in markdown.

## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit your code for question #4.
4. Submit a pull request.
5. Don't forget to include links to your dashboard(s)

## References

### How to get started with Datadog

* [Datadog overview](http://docs.datadoghq.com/overview/)
* [Guide to graphing in Datadog](http://docs.datadoghq.com/graphing/)

### The Datadog API and clients

* [API docs](http://docs.datadoghq.com/api)
* [Guide to the Agent](http://docs.datadoghq.com/guides/basic_agent_usage/)
* [Libraries](http://docs.datadoghq.com/libraries/)
* [Guide to Metrics](http://docs.datadoghq.com/guides/metrics/)

### Extending the Agent

* [Writing an agent check](http://docs.datadoghq.com/guides/agent_checks/)

### Tools you may need

Load testing
* [ab](https://httpd.apache.org/docs/2.2/programs/ab.html)
* [tsung](http://tsung.erlang-projects.org/user_manual.html#htoc2)
