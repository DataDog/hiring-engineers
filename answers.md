##Questions

###Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

* Bonus question: what is the agent?  

  The agent is a program called: ddagent. It's a program that runs on my computer and collects events and metrics from it to send to Datadog.

* Submit an event via the API.

  I used information from: http://docs.datadoghq.com/api/

  To create this test.rb program: 

```
require 'rubygems'
require 'dogapi'


api_key = '9f23006b40cf32e3af4d159b319f9a15'

dog = Dogapi::Client.new(api_key)

response = dog.emit_event(Dogapi::Event.new('Test message!', :msg_title => 'Test
 Title!'))

puts response
```


  I ran that program and it returned this result and posted an event:

```
202
{"status"=>"ok", "event"=>{"priority"=>"normal", "date_happened"=>1395713431, "handle"=>nil, "title"=>"Test Title!", "url"=>"https://app.datadoghq.com/event/jump_to?event_id=2205374623024400909", "text"=>"Test message!", "tags"=>[], "related_event_id"=>nil, "id"=>2205374623024400909}}
```


* Get an event to appear in your email inbox (the email address you signed up for the account with)

  I again used information from: http://docs.datadoghq.com/api/

  To create this test2.rb program to email the event info to me:


```
require 'rubygems'
require 'dogapi'
require 'mail'
require 'json'


api_key = '9f23006b40cf32e3af4d159b319f9a15'
app_key = '050fc7832721f75fb76f784863e3e7cc55097078'
event_id = '2205374623024400909'


dog = Dogapi::Client.new(api_key, app_key)

response = dog.get_event(event_id)

options = {
        :address => "smtp.gmail.com",
        :port => 587,
        :domain => 'your.host.name',
        :user_name => 'joseph.patrick.cabanilla@gmail.com',
        :password => '',
        :authentication => 'plain',
        :enable_starttls_auto => true  }


Mail.defaults do
  delivery_method :smtp, options
end


Mail.deliver do
       to 'joseph.patrick.cabanilla@gmail.com'
     from 'not_a_real_email@datadoghq.com'
  subject 'Event from DataDog: '+event_id
     body response
end
```

  Here's a screen shot of the email that was sent:
  http://i.imgur.com/sa5gCSP.png




###Level 2

* Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

  I used the information from these pages to create a test app using Ruby on Rails and SQLite3:
  http://ruby.railstutorial.org/chapters/a-demo-app
  http://guides.rubyonrails.org/
  http://www.rubydoc.info/github/DataDog/dogstatsd-ruby/master/frames
  http://docs.datadoghq.com/guides/dogstatsd/

  The web app is at:
  https://github.com/JosephPatrickCabanilla/DataDog-Ruby-on-Rails-Test-App


  I used this library to add dogstatsd to the web app and send metrics:
  https://github.com/DataDog/dogstatsd-ruby

  I added this to the web app:
```
my_statsd = Statsd.new 'localhost', 8125
my_statsd.increment 'page.views', :tags => ["support"]
```


* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

  I made a Ruby script called page_reloader.rb that runs Apache's benchmarking tool to send requests to my web app at 100 requests sending 10 at a time, repeating it X times:

```
require 'rubygems'

go_time = Time.now() + rand(10)
counter = 0

  if ARGV[0].nil?

  puts "Hey, you need to put in a number!"

  else 
    while counter.to_s < ARGV[0]

      if Time.now >= go_time

      2.times do puts "" end
      puts "+-----------------+"
      puts "|                 |"
      puts "|  It's go time!  |"
      puts "|                 |"
      puts "+-----------------+"
      2.times do puts "" end

      counter2 = rand(10)
 
      while counter2 > 0
        system("ab -n 100 -c 10 http://192.168.2.17:3000/")
        system("ab -n 100 -c 10 http://192.168.2.17:3000/users")
        system("ab -n 100 -c 10 http://192.168.2.17:3000/microposts")
        counter2 -= 1
      end

      go_time = Time.now() + rand(10)
      counter += 1
    end

  end

end
```


  Here's a link to the graph:
  http://i.imgur.com/14524xv.png


* Create a histogram to see the latency; also give us the link to the graph
  I used random to simulate latency:  

```
my_statsd = Statsd.new 'localhost', 8125
my_statsd.histogram 'page.latency', rand(100), :tags => ["support"]
```

  Here's a link to the graph:
  http://i.imgur.com/jRQzQie.png


* Bonus points for putting together more creative dashboards.

  Here's a fun dashboard that I made:
  http://i.imgur.com/WthOxsi.png


###Level 3

Using the same web app from level 2:

* tag your metrics with support (one tag for all metrics)

  I added this to the counters:
```  
my_statsd.increment 'page.views', :tags => ["support"]
```

  and this to the histogram:
```
my_statsd.histogram 'page.latency', rand(100), :tags => ["support"]
```

* tag your metrics per page (e.g. metrics generated on / can be tagged with page:home, /page1 with page:page1)

  I added this to the home page controller:
```
my_statsd.increment 'page.views', :tags => ["page:home"]
```

  I added this to the users page controller:
```
my_statsd.increment 'page.views', :tags => ["page:users"]
```

Added this to the microposts page controller:
```
my_statsd.increment 'page.views', :tags => ["page:microposts"]
```


* visualize the latency by page on a graph (using stacked areas, with one color per page)

  This was done using dashboards:  
  http://i.imgur.com/iTKhine.png


###Level 4

Same web app:

* count the overall number of page views using dogstatsd counters.

  I added this to the home page controller:
```
my_statsd.count 'page.overall_views', rand(100)
```

  I added this to the users page controller:
```
my_statsd.count 'page.overall_views', rand(100)
```

  I added this to the microposts page controller:
```
my_statsd.count 'page.overall_views', rand(100)
```

* count the number of page views, split by page (hint: use tags)

  I added tags to the 'page.overall_views' counter for home page :
```
my_statsd.count 'page.overall_views', rand(100), :tags => ["page:home"]
```

  I added tags to the 'page.overall_views' counter for users page:
```
my_statsd.count 'page.overall_views', rand(100), :tags => ["page:users"]
```

  I added tags to the 'page.overall_views' counter for microposts page:
```
my_statsd.count 'page.overall_views', rand(100), :tags => ["page:microposts"]
```

* visualize the results on a graph

  This was done using dashboards:
  http://i.imgur.com/S3SXPN2.png

* Bonus question: do you know why the graphs are very spiky?

  The graphs are spiky because the agent waits to gather metrics and then sends the metrics out at the specified interval.  My automated test also randomly generates views for the pages instead of the normal flow from one page to another which is normally generated as a user clicks through pages.





###Level 5

Let's switch to the agent.

* Write an agent check that samples a random value. Call this new metric: test.support.random
Here is a snippet that prints a random value in python:

```
import random
print(random.random())
```

  I used information from:
  http://docs.datadoghq.com/guides/agent_checks/ 
  http://docs.datadoghq.com/guides/basic_agent_usage/deb/


  I added this TestSupportRandom.yaml file to the /etc/dd-agent directory:

```
init_config:


instances:
  [{}]
```


  I made this TestSupportRandom.py file in the /etc/dd-agent/checks.d directory:

```
import random

class TestSupportRandom(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```


