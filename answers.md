Your answers to the questions go here.

DataDog Dashboard:

Link: [My Dashboard](https://app.datadoghq.com/dash/100189/pageviews?live=true&page=0&is_auto=false&from_ts=1455904962326&to_ts=1455908562326&tile_size=m&fullscreen=false)

![dd-dashboard](/imgs/dd_dashboard.png)

**Level 1**:

Language: Node.js

![dd-email](/imgs/dd_email.png)

```
var dataDog = require('dogapi');
var nodemailer = require('nodemailer');

var options = {
  api_key: "0676cc82c8b37aadc3b0014028e87f98",
  app_key: "fcf990aa197aaa558d4e93acbccd75263d4db2ec"
};

dataDog.initialize(options);

var transporter = nodemailer.createTransport();

var title = "1st test event";
var text = "this is a test to see if it worked";

dataDog.event.create(title, text, function(err, results) {
  if (err) {
    console.log(err);
  };
  var mailOptions = {
    from: 'test@datadog.com',
    to: 'alex.schofield816@gmail.com',
    subject: results.event.title,
    text: results.event.text
  };
  transporter.sendMail(mailOptions, function(error, info){
    if(error){
      console.log(error);
    }
    console.log(info);
  });
  console.log(results);
});
```

**Level 2, 3, & 4**:

Language: Ruby

Project Used: 

[Liverpool FC Forum](https://peaceful-gorge-7113.herokuapp.com/)

[Github Repo](https://github.com/alschofield/LiverpoolForum)

![login-page-views](/imgs/login_page_views.png)

![avg-db-time](/imgs/avg_db_time.png)

Part 2:

```
statsd = Statsd.new()
```

```
def histogram_create_user
  <!-- For some reason the program forgets what statsd is when running this block -->
  statsd = Statsd.new()
  start_time = Time.now
  results = User.create();
  duration = Time.now - start_time
  statsd.histogram('database.create_user.time', duration)
end
```

```
get('/sign_up') do
  statsd.increment('page.views')
  histogram_create_user()
  erb :signup_form
end
```

Part 3 and 4:

Language: Ruby

![db-time-by-page](/imgs/db_time_by_page.png)

![views-by-page](/imgs/views_by_page.png)

```
statsd = Statsd.new()
```

```
def histogram_create_user
  <!-- For some reason the program forgets what statsd is when running these blocks -->
  statsd = Statsd.new()
  start_time = Time.now
  results = User.create(username: 'test_user');
  duration = Time.now - start_time
  statsd.histogram('database.create_user.time', duration, :tags => ['support', 'page:sign_up'])
end
```

```
def histogram_find_user
  <!-- For some reason the program forgets what statsd is when running these blocks -->
  statsd = Statsd.new()
  start_time = Time.now
  results = User.find_by({username: 'test_user'});
  duration = Time.now - start_time
  statsd.histogram('database.fins_user.time', duration, :tags => ['support', 'page:login'])
end
```

```
get('/') do
  statsd.increment('page.views', :tags => ['support', 'page:login'])
  histogram_find_user()
  erb :login_form
end
```

```
get('/sign_up') do
  statsd.increment('page.views', :tags => ['support', 'page:sign_up'])
  histogram_create_user()
  erb :signup_form
end
```

**level 5**:

Language: Python

![dd-agent-check](/imgs/dd_agent_check.png)

```
init_config:

instances:
    [{}]
```

```
from checks import AgentCheck
import random
class TestCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())
```

*Files for level 1 and 5 are in their respective folders*
