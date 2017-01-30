Level 1: 
a. Sign up for Datadog, get the agent reporting metrics from your local machine. 

I used this command to install the agent on my local system:

bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/setup_agent.sh)"

b. What is the Agent?
The Agent is Datadog software that runs on your hosts. It collects events and metrics and sends them to Datadog to encapsulate all the data and provide a meaningful narrative about your monitoring and performance data.

c. Submit an event via the API
I created a ruby test file and ran it in the terminal. The file contained this code(I ommitted my API Key):
	require 'rubygems'
	require 'dogapi'

	api_key=''
	app_key=''

	dog = Dogapi::Client.new(api_key, app_key)

	dog = Dogapi::Client.new(api_key)

	dog.emit_event(Dogapi::Event.new('msg_text', :msg_title => 'Title'))
When you run this file, you will see the event in your event stream on your dashboard. 

d. Get an event to appear in your email inbox
In the ruby file, change the last line to this(or whichever email you sign up with and run it. :
dog.emit_event(Dogapi::Event.new('Event submitted via API @remykartzman@gmail.com', :msg_title => 'Email Event'))

You will receive an email in your inbox that says "A Datadog event mentioned you."
Link to Image: 
[Imgur](http://i.imgur.com/wk4O9Bk.png)

Level 2: 

A. Take a web app and instrument your code with dogstatsd to create metrics. 
I'm choosing to use my rails stack overflow clone to implement some of the statsd instruments. First I have to go ahead and install the dogstatsd-ruby gem. Then, after opening up the file structure and add the gem to my gemfile to ensure the most recent version gets applied when I run a bundle install. In alignment with the Datadog docs, I require 'statsd' in my application.rb file and create a global variable called STATSD to initialize a new instance of Statsd. I will use this variable in some of my controllers to track page views when some of my routes get hit.Since it is primarily a question and answer site it seems reasonable to use some of Datadogs counters to track page views on both of those routes. In both my question and answer controllers I added a method called render_page(in accordance with the docs) that I will use on some of the actions I want to track. In this case I call the render_page method in my create method that should run when a new answer is created to a question. Additionally, in my Questions Controller I added the render_page method that I used to check whenever the form for a new question is rendered. That way I can compare later how frequently users are creating questions against how often users answer questions. This seems like an interesting metric to keep track of. After checking the metrics in my Datadog account for web.page_views I can confirm that the page incrementers are in fact working. 

Here is the corresponding code: 

application.rb:
require 'statsd'

STATSD = Statsd.new

app/controllers/questions_controller.rb: 
  def render_page()
    STATSD.increment('web.page_views', :tags => ['page:questions'])

  end

   def create
    render_page()
    start_time = Time.now
      if current_user == nil
         flash[:notice] = GlobalConstants::LOGIN_ERROR
          redirect_to new_question_path
      else
        @question = Question.create(question_params)
        if @question.save
        duration = Time.now - start_time
        STATSD.histogram('database.query.time', duration)
        params[:question][:user_id] = current_user.id
        redirect_to questions_path
      end
    end

  end

Apache Load Test: Questions Page Views/Sec
	in a ruby file 'loadapachetest.rb':
	exec 'ab -c 10 -n 300 http://127.0.0.1:3000/questions'
	exec 'ab -c 110 -n 130 http://127.0.0.1:3000/questions/new

[Imgur](http://i.imgur.com/sx76pL8.png)


Web Page Views over page:questions
[Imgur](http://i.imgur.com/a6voC28.png)

Latency Histogram: 
[Imgur](http://i.imgur.com/wk4O9Bk.png)

Average Database query time overlayed with page views for Answers and Questions: 
[Imgur](http://i.imgur.com/PQSXzBP.png)

Level 3:
Using the same web app from level 2

A. Tag metrics with support and page: 
Code: 


  def render_page()
    STATSD.increment('web.page_views', :tags => ['page:questions', 'support'])

  end

  def render_page()
  	STATSD.increment('web.page_views', :tags => ['page:answers', 'support'])
  end 

Graph with support tags: 
[Imgur](http://i.imgur.com/XDTpuu3.png)

Visualize latency by page:
[Imgur](http://i.imgur.com/XDTpuu3.png)

These are also saved as graphs to my dashboard 
Links to Dashboard here: 

https://app.datadoghq.com/dash/48486/remys-macbook-dashboard?live=true&from_ts=1430426667741&to_ts=1430430267741&tile_size=m

Graph depicting overall page views using dogstatsd counters:
[Imgur](http://i.imgur.com/AnxyiOK.png)

Graph depicting page views broken down by page:
[Imgur](http://i.imgur.com/lqGVsN8.png)

Why are the graphs spiky?

It seems that the page view graphs are spiky due to the way dogstatsd aggregates the counter data. Because of the way the x-axis(time) increments, a small number of page views over a longer period of time appears on the graph as a spike, however if the time was broken down to smaller increments the graph would be much smoother. 

Level 5: 
A. Write an agent check that samples a random value. call this new metric: test.support.random. 
B. Visualize this new metric on Datadog


For the agent check, I modified my original HelloCheck from the DataDog Docs to be: 

*in a file called: agent/checks.d/hello.py

from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())


* in the yaml file located at : agent/conf.d/hello.yaml

init_config:

instances:
    [{}]


In addition to inheriting from AgentCheck I add the line to import random so that I can I call the random method to return a random value

I alter the check method and use self.gauge. I pass gauge the metric I want to send('test.support.random') and as the second parameter call random.random()

Links:

Visualize writing an agent check:
[Imgur](http://i.imgur.com/cZCWeB7.png)


Link to My Dashboard:

https://app.datadoghq.com/dash/48486/remys-macbook-dashboard?live=true&from_ts=1430943025106&to_ts=1430946625106&tile_size=m

Link to My Event Stream:

https://app.datadoghq.com/event/stream?tags_execution=and&show_private=true&per_page=30&aggregate_up=true&display_timeline=true&from_ts=1430946240000&is_zoomed=true&to_ts=1430946480000&incident=true&codemirror_editor=true&bucket_size=4000






