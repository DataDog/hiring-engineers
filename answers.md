Your answers to the questions go here.

Level 1
------
- Sign up for Datadog, get the agent reporting metrics from your local machine.
ANSWER: I signed up for Datadog. Instead of using my local machine, a macbook pro, I decided to use my VPS running Ubuntu 10.04. I thought that using an actual server, serving up some of my portfolio pieces, "http://wizardsandspaceships.com" and "http://thenewpolice.com," as well as my portfolio site itself at "http://portfolio47.com" was a better choice for obvious reasons.

- Bonus question: what is the agent?
ANSWER: "The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data." copied and pasted from: "http://docs.datadoghq.com/guides/basic_agent_usage/"

- Submit an event via the API.
ANSWER: I did this using irb:
Copied and Pasted:

	irb(main):001:0> require 'dogapi'
	=> true
	irb(main):002:0> api_key = "a5b9f13e690ce1693b2c23f928450c87"
	=> "a5b9f13e690ce1693b2c23f928450c87"
	irb(main):003:0> dog = Dogapi::Client.new(api_key)
	=> #<Dogapi::Client:0xa17c6cc @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @datadog_host="https://app.datadoghq.com", @host="thenewpolice.com", @device=nil, @metric_svc=#<Dogapi::V1::MetricService:0xa17c49c @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @event_svc=#<Dogapi::V1::EventService:0xa17c460 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @tag_svc=#<Dogapi::V1::TagService:0xa17c424 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @comment_svc=#<Dogapi::V1::CommentService:0xa17c3d4 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @search_svc=#<Dogapi::V1::SearchService:0xa17c398 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @dash_service=#<Dogapi::V1::DashService:0xa17c35c @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @alert_svc=#<Dogapi::V1::AlertService:0xa17c320 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @user_svc=#<Dogapi::V1::UserService:0xa17c2e4 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @snapshot_svc=#<Dogapi::V1::SnapshotService:0xa17c294 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @screenboard_svc=#<Dogapi::V1::ScreenboardService:0xa17c258 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @legacy_event_svc=#<Dogapi::EventService:0xa17c1f4 @api_key="https://app.datadoghq.com", @host="https://app.datadoghq.com">>
	irb(main):004:0> dog.emit_event(Dogapi::Event.new('Testing done, FTW'), :host => "my_host")
	=> ["202", {"status"=>"ok", "event"=>{"priority"=>"normal", "date_happened"=>1391045539, "handle"=>nil, "title"=>"", "url"=>"https://app.datadoghq.com/event/jump_to?event_id=2127060304289814517", "text"=>"Testing done, FTW", "tags"=>[], "related_event_id"=>nil, "id"=>2127060304289814517}}]

- Get an event to appear in your email inbox (the email address you signed up for the account with)
ANSWER: I did this using irb:
Screenshot of email: http://thenewpolice.com/data_dog_event_in_inbox.png

Copied and Pasted:

	irb(main):001:0> require 'dogapi'
	=> true
	irb(main):002:0> api_key = 'a5b9f13e690ce1693b2c23f928450c87'
	=> "a5b9f13e690ce1693b2c23f928450c87"
	irb(main):003:0> dog = Dogapi::Client.new(api_key)
	=> #<Dogapi::Client:0xa409520 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @datadog_host="https://app.datadoghq.com", @host="thenewpolice.com", @device=nil, @metric_svc=#<Dogapi::V1::MetricService:0xa40928c @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @event_svc=#<Dogapi::V1::EventService:0xa409250 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @tag_svc=#<Dogapi::V1::TagService:0xa4091ec @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @comment_svc=#<Dogapi::V1::CommentService:0xa4090fc @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @search_svc=#<Dogapi::V1::SearchService:0xa4090c0 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @dash_service=#<Dogapi::V1::DashService:0xa40905c @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @alert_svc=#<Dogapi::V1::AlertService:0xa408fbc @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @user_svc=#<Dogapi::V1::UserService:0xa408f30 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @snapshot_svc=#<Dogapi::V1::SnapshotService:0xa408ee0 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @screenboard_svc=#<Dogapi::V1::ScreenboardService:0xa408e54 @api_key="a5b9f13e690ce1693b2c23f928450c87", @application_key=nil, @api_host="https://app.datadoghq.com", @silent=true>, @legacy_event_svc=#<Dogapi::EventService:0xa408dc8 @api_key="https://app.datadoghq.com", @host="https://app.datadoghq.com">>
	irb(main):014:0> dog.emit_event(Dogapi::Event.new('@rdias23@gmail.com msg_text', :msg_title => 'Title'))
	=> ["202", {"status"=>"ok", "event"=>{"priority"=>"normal", "date_happened"=>1391049861, "handle"=>nil, "title"=>"Title", "url"=>"https://app.datadoghq.com/event/jump_to?event_id=2127132817447565547", "text"=>"@rdias23@gmail.com msg_text", "tags"=>[], "related_event_id"=>nil, "id"=>2127132817447565547}}]

Level 2
-------
- Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.
ANSWER: I decided to use my "Wizards and Spaceships" (Rails) application at http://wizardsandspaceships.com for this. I put the dogstatsd gem ( gem "dogstatsd-ruby", "~> 1.2.0" ) in the Gemfile and did a bundle install, then I put "require 'statsd'" at the top of the "home controller" in my application. Then, inside the "def landing" method of the "home controller" I put the following:
	statsd = Statsd.new('localhost', 8125)
        statsd.increment('web.landing_page_views')

Then I ran the apache benchmark tool a couple times with a command like so:
	ab -n 9999 -c 100 http://wizardsandspaceships.com/

- While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!
ANSWER: Here is a link to the graph that I was able to get from the now available metric, "web.landing_page_views": https://app.datadoghq.com/graph/embed?token=c231b15eb56dca98a331d16f7fd79c251c646a522744d10cc333c51a777b3b6a&height=300&width=600

--> Here is a link to a screenshot: http://thenewpolice.com/web_landing_page_views.png

- Create a histogram to see the latency; also give us the link to the graph.
If we take latency to be the time it takes a given network packet to travel from source to destination and back, I know this can't be the best way to measure this, but it's better than nothing... I used the histogram option for a "file.upload.size" metric by adding "statsd.histogram('file.upload.size', 1234)" to the landing method of the "home controller", then I pulled up a graph for the "file.upload.size.count" metric. Here's the link to the graph: https://app.datadoghq.com/graph/embed?token=97109ff2d4ebb3be7fb460e364d109b7560a4a9f8fc0c6072ea935f5f4538536&height=300&width=600

And, here's a screenshot: http://thenewpolice.com/histogram_latency.png

- Bonus points for putting together more creative dashboards.

Level 3
-------
Using the same web app from level 2
- Tag your metrics with support (one tag for all metrics)
I did two things here, and I'm not sure which was being asked for... (1) Under "Infrastructure" I selected the "inspect" button for my server, and then I clicked "Edit User Tags" and I added a tag called "support". (2) I added a ":tags => ['support']" to the "statsd.increment" and "statsd.histogram" line in my "def landing" page method on the "home controller".

- Tag your metrics per page (e.g. metrics generated on "/" can be tagged with "page:home", "page1" with "page:page1")

I tagged the metrics for the landing page of my application, which is at http://wizardsandspaceships.com/ , with "page:landing", and I tagged the metrics for the index page of my application, which is at http://wizardsandspaceships.com/home/index , with "page:index".

- Visualize the latency by page on a graph (using stacked areas, with one color per "page")

I created a graph with this JSON:

{
  "requests": [
    {
      "q": "avg:file.upload.size.count{page:index}, avg:file.upload.size.count{page:landing}"
    }
  ],
  "events": []
}

Here is a link for the graph: https://app.datadoghq.com/graph/embed?token=fa9cdcd4e107e2bca618965a959bc110d84dd9cfd73f6b76f4cc774fe7efa35a&height=300&width=600


Level 4
-------
Same web app
- Count the overall number of page views using dogstatsd counters.

I'm already incrementing a counter for the landing page, and a counter for the index page, like so:
statsd.increment('web.landing_page_views', :tags => ['support', 'page:landing'])
AND
statsd.increment('web.index_page_views', :tags => ['support', 'page:index'])

I'm not sure if you're asking me for a specific number, or how I would get that number.

- Count the number of page views, split by page (hint: use tags)
The counter for landing page views and the counter for index page views are using different tags, 'page:index' and 'page:landing' respectively, but I called the counters different names, 'web.landing_page_views' and 'web.index_page_views', so I don't think it's neccessary to make reference to the tags in the JSON for the graph.

- Visualize the results on a graph

I edited the JSON for my "index page" hit count graph so the JSON was this:

{
  "requests": [
    { 
      "q": "avg:web.index_page_views{*}, avg:web.landing_page_views{*}"
    }
  ],
  "events": []
}

Then I renamed the graph to: "Stacked Series: Landing Page and Index Page"

Here is a screenshot of the graph ( Note: I had to do a zoom-in. ): http://thenewpolice.com/Stacked_Series_Index_and_Landing.png

- Bonus question: do you know why the graphs are very spiky?

Level 5
------
Let's switch to the agent
- Write an agent check that samples a random value. Call this new metric: "test.support.random"

I don't think I can do this in a reasonable amount of time... From what I gather, the agent check needs to be written in Python. I know ruby, but not python, sadly... (I do have an interest in learning python.)

Here is a snippet that prints a random value in python:
import random
print(random.random())

