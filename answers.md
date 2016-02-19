Your answers to the questions go here.

Level 1:

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

level 2:
```
statsd = Statsd.new()
```

```
def histogram_create_user
  <!-- For some reason when the program forgets what statsd is when running this block -->
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

level 3 and 4:
```
statsd = Statsd.new()
```

```
def histogram_create_user
  <!-- For some reason when the program forgets what statsd is when running these blocks -->
  statsd = Statsd.new()
  start_time = Time.now
  results = User.create(username: 'test_user');
  duration = Time.now - start_time
  statsd.histogram('database.create_user.time', duration, :tags => ['support', 'page:sign_up'])
end
```

```
def histogram_find_user
  <!-- For some reason when the program forgets what statsd is when running these blocks -->
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

level 5:

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