Your answers to the questions go here.
Kristyn Bryan

## Questions

### Level 1

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the agent reporting metrics from your local machine.
![Ruby Email Example](/images/metrics.png)

* Bonus question: what is the agent?
The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data.

The Agent has three main parts: the collector, dogstatsd, and the forwarder.

The collector runs checks on the current machine for whatever integrations you have and it will capture system metrics like memory and CPU.
Dogstatsd is a statsd backend server you can send custom metrics to from an application.
The forwarder retrieves data from both dogstatsd and the collector and then queues it up to be sent to Datadog.

* Submit an event via the API.
Step 1: Create and API Key
In order to do this, sign up for an API key through your Datadog dashboard. Navigate to the page by clicking on `Integrations` on the left-hand navigation bar and then `APIs`.
![Ruby Email Example](/images/left_nav.png)

Click on `Create API Key`.
![Ruby Email Example](/images/create_api.png)

Step 2: Install the dogapi-rb gem (if using Ruby)
Go to [https://github.com/DataDog/dogapi-rb] and follow the instructions to install the Ruby client for DataDog's API.
![Ruby Email Example](/images/gem_install_dogapi.png)

Step 3: Create a Ruby file, customize, and run it
Once dogapi-rb is installed, create a Ruby file and use the sample code that is given to you in the dogapi-rb documentation. You will insert your custom API key here and update the message. Run your Ruby file.
![Ruby Email Example](/images/run_ruby_file.png)

Your your event will be submitted and will appear in your Datadog dashboard.
![Ruby Email Example](/images/sending_events.png)

* Get an event to appear in your email inbox (the email address you signed up for the account with)
Customize the Ruby event file that you created to include the email address of where you would like to send the event notification in the message field. Be sure to use and `@` before the email address.
![Ruby Email Example](/images/email_ruby.png)

Run your ruby file and your event and email will be submitted.
![Ruby Email Example](/images/email_response.png)

### Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
* Create a histogram to see the latency; also give us the link to the graph
* Bonus points for putting together more creative dashboards.

### Level 3

Using the same web app from level 2:
* tag your metrics with `support` (one tag for all metrics)
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)
* visualize the latency by page on a graph (using stacked areas, with one color per `page`)

### Level 4

Same web app:
* count the overall number of page views using dogstatsd counters.
* count the number of page views, split by page (hint: use tags)
* visualize the results on a graph
* Bonus question: do you know why the graphs are very spiky?

### Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`
* Visualize this new metric on Datadog, send us the link.

Here is a snippet that prints a random value in python:

```python
import random
print(random.random())
```

## Instructions
If you have a question, create an issue in this repository.

To submit your answers:

1. Fork this repo.
2. Answer the questions in `answers.md`
3. Commit as much code as you need to support your answers. At a minimum, for level 5.
4. Submit a pull request.
5. Don't forget to include links to your dashboard(s), even better links *and* screenshots.

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
