Your answers to the questions go here.

# Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

	<a href="https://www.flickr.com/photos/138504719@N03/22983167964/in/dateposted-public/" title="metrics_joe-pc">
	<img src="https://farm1.staticflickr.com/586/22983167964_efc97e20a5_b.jpg" width="512" height="239" alt="metrics_joe-pc"></a>
* Bonus question: what is the agent?
	* The Agent is a piece of software that collects systems data and application data from the host machine. It then sends this data to the Datadog servers, from which the user can visualize one or any combination of the acquired metrics via dashboards and monitors.
* Submit an event via the API.
  	
        from datadog import initialize, api

        options = {
            'api_key': '92747aca1506808b4fc4a4eb331f8461',
            'app_key':'e5bb287ca4fdd7b4d6676b89bc6b9cedf613c810'
        }
	
        initialize(**options)
	
  		title = "Create Event Test"
    	text = 'This event was submitted via the datadog API @kimjo3900@gmail.com'
    	tags = ['test', 'joe-pc']
	
    	api.Event.create(title=title, text=text, tags=tags)
* Get an event to appear in your email inbox (the email address you signed up for the account with)

	<a href="https://www.flickr.com/photos/138504719@N03/23528946651/in/dateposted-public/" title="Event">
	<img src="https://farm6.staticflickr.com/5793/23528946651_fe726d4aaa_b.jpg" width="512" height="239" alt="Event"></a>

# Level 2

* Take a simple web app ([in any of our supported languages](http://docs.datadoghq.com/libraries/)) that you've already built and instrument your code with dogstatsd. This will create **metrics**.
	
    	def main():
        	start = time()
        	r = requests.get('http://192.168.1.67:8080')
        	latency = time() - start
        	statsd.increment('page.views.home')
        	statsd.histogram('latency.home', latency)
* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
* Create a histogram to see the latency; also give us the link to the graph
	* [link to the dashboard](https://app.datadoghq.com/dash/84646/level-2?live=false&page=0&is_auto=false&from_ts=1449406812950&to_ts=1449407147367&tile_size=m)

	<a href="https://www.flickr.com/photos/138504719@N03/23243199149/in/dateposted-public/" title="level2">
	<img src="https://farm6.staticflickr.com/5800/23243199149_573b3529a6_b.jpg" width="512" height="239" alt="level2"></a>

# Level 3

Using the same web app from level 2:

* tag your metrics with `support` (one tag for all metrics)
* tag your metrics per page (e.g. metrics generated on `/` can be tagged with `page:home`, `/page1` with  `page:page1`)

		@app.route('/')
		def main():
		    start = time()
		    r = requests.get('http://192.168.1.67:5000')
		    latency = time() - start
		    statsd.increment('page.views', tags=['support', 'page:home'])
		    statsd.histogram('latency.home', latency, tags=['support', 'page:home'])

		@app.route('/showSignUp')
		def showSignUp():
		    start = time()
		    r = requests.get('http://192.168.1.67:5000/showSignUp')
		    latency = time() - start
		    statsd.increment('page.views', tags=['support', 'page:SignUp'])
		    statsd.histogram('latency.SignUp', latency, tags=['support', 'page:SignUp'])
		
		@app.route('/showSignIn')
		def showSignIn():
		    start = time()
		    r = requests.get('http://192.168.1.67:5000/showSignIn')
		    latency = time() - start
		    statsd.increment('page.views', tags=['support', 'page:SignIn'])
		    statsd.histogram('latency.SignIn', latency, tags=['support', 'page:SignIn'])
* visualize the latency by page on a graph (using stacked areas, with one color per `page`)
	* [link to the dashboard](https://app.datadoghq.com/dash/85371/level-3?live=false&page=0&is_auto=false&from_ts=1449570206474&to_ts=1449570782745&tile_size=m)

	<a href="https://www.flickr.com/photos/138504719@N03/23245740969/in/dateposted-public/" title="level3">
	<img src="https://farm1.staticflickr.com/654/23245740969_23309690b6_b.jpg" width="512" height="239" alt="level3"></a>

# Level 4

Same web app:

* count the overall number of page views using dogstatsd counters.
* count the number of page views, split by page (hint: use tags)
* visualize the results on a graph
	* [link to the dashboard](https://app.datadoghq.com/dash/85661/level-4?live=false&page=0&is_auto=false&from_ts=1449569578841&to_ts=1449569959514&tile_size=m)

	<a href="https://www.flickr.com/photos/138504719@N03/23587583426/in/dateposted-public/" title="level4">
	<img src="https://farm6.staticflickr.com/5726/23587583426_af2bbb3b3b_b.jpg" width="512" height="239" alt="level4"></a>
* Bonus question: do you know why the graphs are very spiky?
	* The spikes in the graph are largely determined by the current condition of the network. At any given instant, the network may be more or less congested with traffic, which affects page load times. Also, DogStatsD aggregates data over a default interval of ten seconds before sending metric data to the server. Increasing the flush interval to 60 seconds would help "smooth out" the graph.

# Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: `test.support.random`

		from checks import AgentCheck  
		import random

		class RandomCheck(AgentCheck):  
  			def check(self, instance):
				r_value = random.random()
    			self.gauge('test.support.random', r_value)
* Visualize this new metric on Datadog, send us the link.
	* [link to the dashboard](https://app.datadoghq.com/dash/85697/level-5?live=false&page=0&is_auto=false&from_ts=1449588586107&to_ts=1449588894009&tile_size=m)

	<a href="https://www.flickr.com/photos/138504719@N03/23585034226/in/dateposted-public/" title="Level5">
	<img src="https://farm1.staticflickr.com/677/23585034226_911f00c1a3_b.jpg" width="512" height="239" alt="Level5"></a>