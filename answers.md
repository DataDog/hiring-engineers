Level 1

- I signed up for Datadog, getting an agent on Windows 7

- I submitted an event via the shell API

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Did you hear the news today?",
      "text": "Oh boy! @kgi.perez",
      "priority": "normal",
      "tags": ["environment:test"],
      "alert_type": "info"
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=9775a026f1ca7d1c6c5af9d94d9595a4'

- I included @kgi.perez in the text field, to get notified by email

Level 2

- I set up a simple webapp using the framework web.py, and I instrumented my code with statsd
	
- I used locust.io to run a simple load test, here's the code I used to get the different metrics:

class hello:
	dt = time.time()
	def GET(self, name):
		if not name:
			name = 'home'
		statsd.increment('web.page_views', tags = ["support", "page:" + name])
		dt2 = time.time()
		statsd.histogram('query.time', dt2 - hello.dt, tags = ["support", "page:" + name])
		hello.dt = dt2
		return 'Hello, ' + name + '!'
		
Level 3

- I used this to stack the page views per page:

	{
      "q": "avg:web.page_views{page:home}"
    },
    {
      "q": "avg:web.page_views{page:new}"
    }

- I am providing a link to the embed graph:
https://app.datadoghq.com/graph/embed?token=a09d2bd18bc6f3e58fce1bd02cee8d85be9d2cabcb6d1f62e67e897f4e2773b4&height=300&width=600&legend=false
	
Level 4

- I used this to compute the total amount of page views

	cumsum(avg:web.page_views{page:home})
		
Level 5

- This is the code for the agent check:

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
		
- I am providing a link to the embed graph:
https://app.datadoghq.com/graph/embed?token=a36825d369ebe2659d48a4ed3c185b4a3d59ffcdb2e19d0c5e78ef0fead0984f&height=300&width=600&legend=false

	

