Technical Challenge for Solutions Engineer Position at Datadog
Nate Perkins
Recruiter: Avery Johnson

# Datadog Solutions-Engineer Technical Challenge
## Or:  How To Break Things, Fix Them, And Have Fun Doing It
###### By Nate Perkins

Coding is hard.  I mean, it can be really hard.  I've often spent a full hour (probably more accurate to say hours) staring at a computer screen with my head in my hands saying "This *should* work.  What is wrong with *me*?"  I check the code, line by line, check with a debugger to find not even it knows what I've done to ruin my code.  The logic *has* to be right.  If the logic isn't right, I fear I don't even understand the problem I'm working on.  I'll spend an hour diving into dry API's, reading endless questions and responses on Stack Overflow, check to see if W3 schools can tell me why this block of code isn't compiling or my console is filling with dreaded red error-text, taunting me, telling me "You are not the coder you thought yourself to be."  It tells me "walk away, give up."  It tells me "you won't get hired anywhere if you can't fix this simple issue."  The problem hangs in the air over me, shrouding my belief in my future in this career.  It's a crisis of confidence, but I'm not so easily defeated.  I check my code again, line by line.

Inevitably, I discover I've missed a semicolon, or I had an "r" where there should have been an "R," or I have otherwise fat-fingered something important, or a mis-placed curly bracket has brought a vital variable out of the proper scope, or I've somehow managed to try to run two different versions of Java in the same project by messing around with the integrated terminal in Spring STS, severely angering the JVM to the point of breaking it.  Given a million years and as many dollars, I don't think I could reproduce that last error.

"Whew," I think after I find the slip-up, "I *am* as smart as I think I am.  I've got this."  I get to go back to believing I am a competent junior programmer, and that maybe all I need is new glasses or a more readable theme for my IDE.  Then I code until everything is broken again, and repeat the process until everything works.

So recently, the whole reason I'm here, the fine people of Datadog are considering me for a position, and this is a technical challenge to get up and running with Datadog, showing my work as cleary and with as much verbos-ity as I can.

"Awesome," I thought after I got off of the phone screen, "when do I get to start breaking things?"

### Reasearch and Preparation
     
Being relatively new to coding (having graduated a bootcamp in May), I'm always trying to approach each project I attempt in a new way.  I think one of my largest problems as a new coder currently is feeling rushed.  If I'm reading through documentation, and the thing I've just read will solve the problem I'm working on, I'm back to coding before you can say "you should always read the full documentation."  I feel rushed to prove myself, so I don't read what I don't need.  I'm fighting that instinct here and from now on, because I think it's a bad habit that ultimately results in more beating my head against a desk, and I sincerely want to be one of those *boring* guys who always asks "did you read the documentation first?"

I'm not familiar with most of the technologies I'll be using here, and so would like to take some time to dive into some of the cool things I learned along the way.

   #### Vagrant: A Very Brief Overview

**Introduction and Information** : https://www.vagrantup.com/intro/index.html
**Documentation** : https://www.vagrantup.com/docs/
    

Vagrant's stated goal is to 'Say goodbye to "works on my machine" bugs.'  It is a child of the Hashicorp company, which also makes Terraform.

Vagrant just wants code to run on any machine without OS specific and versioning problems.  Vagrant works by creating a consistent work environment inside of a container platform like VirtualBox, while the Vagrantfile keeps a hold of consistency through environment variables across platforms, versions, machine-quirks, etcetera.  It differs from some other VM technologies in it's usage of containers, as containers are faster and more lightweight than traditional VM's.

NPM installs and other package manager installs are highly discouraged, as many of them will be missing dependencies or will include outdated Vagrant versions.

Make sure you've installed Vagrant and the recommended container software from their respective sites, then use `vagrant init`, and then `vagrant up` at the command line to get started.

Run `vagrant` at the command line for help to be displayed, along with a list of commands.  Append `-h` to any command for further information.

**From** Quora.com- What's the difference between a VM, Docker and Vagrant?:  https://www.quora.com/Whats-the-difference-between-a-VM-Docker-and-Vagrant

**From** YouTube user LearnCode.academy (10 minutes-ish on how to get Vagrant going and working with an nginx web server): https://www.youtube.com/watch?v=PmOMc4zfCSw

**From** YouTube user Traversy Media (45 minutes for a very clear, deeper dive into Vagrant.  It uses a different tech stack [LAMP] than this project, but is still worth a look because it goes through what a vagrant file should have in it): https://www.youtube.com/watch?v=vBreXjkizgo

**From** Vagrant Cloud (a list of vagrant boxes for download with fully configured vagrantfiles for different tech stacks and working environments): https://app.vagrantup.com/boxes/search

#### Datadog

**Introduction and Dcumentation**:  https://docs.datadoghq.com/

While none of this information will be new to the hiring team, this is my first introduction to working with the Datadog platform and that is truly the meat of this assignment.  I'll remain brief to avoid glossing your eyes over with stuff you already know.

Datadog is a metrics platform for measuring performance across any stack or infrastructure, at any scale.  With 200+ intergrations, you'd be hard pressed not to find your favorite stack, host, and services fully integrated.  Don't see your favorite?  Datadog is probably working on it right now.

In researching Datadog versus another metrics platform called Splunk I find that Datadog outperforms it in several ways, remaining more cost effective by scale than Splunk (Splunk's steep monthly price of $225 and limited free version versus Datadog's annual $15/host/month and robust free plan), and is generally understood by the folks at financesonline.com to score higher while also retaining a small lead in customer satisfaction.  In other words, Datadog doesn't price you out, they allow costs to follow the scale of the architecture it is being laid over.  The argument could be made that Splunk could be more cost effective at larger scales, but Datadog seems to want in at the ground floor of up and coming companies that are doing exciting things, to create and maintain that relationship early to become integral to the day to day monitoring of their platform.

Datadog has a focus on being usable for everyone.  The eggheads love it for it's sophistication in custom metrics, and hobbyists can plug and play after watching a few videos.  It retains an incredible amount of customization without becoming too complex for a beginner to get running quickly, and doesn't box in devs who really want to rev the engine and see what is underneath.

"Awesome," I'm thinking, "before I get to breaking and fixing this thing I have to learn some Python."

   #### Python

 Whoa.  Python is cool.  I mean, Python is really cool.  Python makes me feel kind of sweaty and excited to write code.  I come from a Java background,  so I thought a good place to start would be asking google "python java differences?"  Then I went over to W3 schools to get a deeper dive into basic syntax, structure, and highlights of the language.  Lastly I looked into naming and style conventions in Python to try to be certain I don't end up looking like a Java writer dressed as a Python writer.  Don't get me wrong, Java is a robust language and even holds some significant advantages over Python, especially in Java's usage of JIT (just in time) compiling, and syntactically is a language that forces clarity (if sacrificiing readability in some situations) in it's strict rules for method signatures and static typing.  I like Java.  It's great.  It does what I ask it to about half the time, and what more could you ask for?  I'm starting to *love* Python, though.  I'll get into why a little later, and I'm going to apologize ahead of time for not being brief.  Python is, as I've said already, really cool.

 **From** (a short blog from Active State about key differences and similarities between Python and Java):  https://www.activestate.com/blog/python-vs-java-duck-typing-parsing-whitespace-and-other-cool-differences/

 **From** (W3 schools tutuorial documentation on Python): https://www.w3schools.com/python/default.asp

 **From** (Python Software Foundation: a quick style guide for reference while writing code): https://www.python.org/dev/peps/pep-0008/

 I found the general theme to be that Python retains many of the things I like about Java and gets rid of much of what I don't like about Java, with few exceptions.  (Almost) everything is still an object in Python, and the import statements look extremely familiar.  Speaking of imports, Python and Java make extensive use of libraries both in the box and from third parties.  This was always what I thought was the greatest strength of Java, and I'm happy to see Python using a similar library structure to import useful tools into your code.

 Now for the cooler part.  How are Java and Python different?  The first thing that jumped out at me is semi-colons are dead, and thank God; who needs 'em?  To complete a line of code and tell Python you want it to execute, hit the return button.  With Python, there's no more finding that you just spent an hour thinking you were a below average coder and a Real Horrible Person over a missing or extra semi-colon.  Java uses strict and statically typed variables.  This forces clarity in what a variable is, but casting types can quickly begin to fill up line after line of code.  Don't even get me started on working with the BigDecimal class in Java.  For instance, if you have a counter variable that you need to return as a string, the Java looks something like:

```java
int counter = 0;

// do something with the counter

// the counter variable can use an implicit or explicit cast to an Integer boxed-type, and then explicitly cast to a String object from there

//implicit cast to Integer boxed-type
String counterString = String.valueOf(counter);

//explicit cast to Integer first if you need to do something else with the boxed-type Integer, then cast that to a String object
Integer counterToCast = new Integer(counter);
String counterString = counterToCast.ToString();
```

The Python code for this is significantly more concise.  Being dynamically but strongly typed on compilation allows less variables and less explicit casting:

```python
counter = 0

# Do something with the counter

str(counter)
```

Python also requires significantly less code to declare functions/methods, let's look at a function that takes an int and casts to String, then returns the String.  The method in Java would go something like:

```java
public static String castIntToString(int numberToCast){
  String caster = String.valueOf(numberToCast);
  return caster;
}

String numString = castIntToString(counter)
 ```

 Did you notice I missed the final semi-colon in this code block?  Neither did I at first.  This wouldn't even *compile*.  Ask me again how I feel about semi-colons.  While we're on that ask me how I feel about counting curly braces to find out why my variables are all out of scope.  If you really want to see me get red in the face, ask me how I feel about every Object in the Java Library that deals with dates and times, and then ask me if the third-party joda time library solves those problems.  Ask any Java person about time libraries, and they're likely to blow a gasket.  Anyways, in Python, method and variable declarations are much simpler.  This function even will accept non-integer objects and cast them to a string:

```python
counter = 0

# Do something with the counter


def cast_to_string(obj_to_cast):
  return str(obj_to_cast)


cast_to_string(counter)
```

   Python is, and I know I've said it three or more separate times, *really cool*.  Syntactically significant whitespace and tabs?  Code blocks based on indentation instead of easy-to-lose brackets? A robust dyamically typed language with some of the advantages of static typing at runtime?  These are all great things, but there is a double-edged sword to Python that I think really becomes a hidden strength. If the dev writing the Python code isn't descriptive, it becomes gibberish with very few clues to aid anyone who is reading their code.  Python forces you to write more elegantly *because* it does so much work for you.  Java forces clarity at the expense of readability, whereas Python forces the programmer to be clear.  Variables in Python must be more descriptive to maintain readability, while the syntactically significant white spaces for code blocks force a naturally readable flow.  I can't say enough about Python at the moment.  I feel like the first cave man to discover fire.  I can feel my code becoming more descriptive and readable.  I'm thinking more deeply about how to be descriptive with naming variables and functions, and how to write code that's partially/mostly readable to someone who has never even coded in their life.  I imagine my code being simple and pretty and good and Python-y, and I'm trying not to run off and re-code every Java project on my GitHub into Python, because I've got to learn a little about the Flask framework before using it with Datadog.

   #### Flask

**From**:  http://flask.pocoo.org/docs/1.0/installation/#installation
**From**:  http://flask.pocoo.org/docs/1.0/quickstart/
**Full Documentation**: http://flask.pocoo.org/docs/1.0/

My experience with frameworks is mostly with using Spring Boot with Java as a back-end framework using a ReST architecture, and using Angular as a front-end framwork to create SPA's that interact via HTTP requests to do CRUD functions with a MySQL database underneath the back-end.  To get a deeper look at the architecture I'm most familiar with check out these two repos on my github page:
Back-end for the Cincinnati DIY Writer's site I built:  https://github.com/darthnater007/CDW-Web
The front-end for the same project:  https://github.com/darthnater007/CDW-ng

Flask is a self-described "micro-framework," but doesn't sacrifice features to remain lightweight and user-friendly.  Everything I'm able to do in the occasionally clunky, heavyweight Spring Framework for HTTP requests, business logic, database connectivity, and more is available in Flask.  Flask also offers a routing feature for displaying content that is reminiscent of an Angular project generated with routing features built in.

Some other noteworthy features of the Flask Framework include a debugging mode,

Flask stands on the shoulders of and relies on Werkzeug (stadard Python interface between applications and servers), Jinja (a template language for rendering), ItsDangerous (for securely signing data), and Click (for building command line interfaces).  These all come together under the Flask framework.  Just import the flask module to your app, and add Python!

Alright, that should cover most of the technologies I learned to get this project moving.  Let's get started!

Yes, it's finally time to break things, fix them, and have fun doing it.

### Setting Up An Environment With Vagrant and Running The Datadog Agent

**Attempt one:** 

I downloaded Vagrant's latest stable release from https://www.vagrantup.com/downloads.html and then VirtualBox from https://www.virtualbox.org/wiki/Downloads .  Then I downloaded Docker for Mac to my machine.

To test that Vagrant was working correctly, I ran `vagrant init hashicorp/trusty32` at the terminal, and watched a vagrantfile appear in the folder.  Everything seemed good, so I ran `vagrant up`, and within a minute I was running Ubuntu 12-something, with the VM automatically appearing in the VirtualBox GUI.  Awesome.  I ran `vagrant ssh`, and my terminal was inside the VM.  Easy.

Wait.  I'm *inside* the VM, where docker doesn't exist yet, where nothing is installed.  Docker is on *my* computer.  Okay.  It was only a test and I'm running the wrong version of Ubuntu anyways.

I deleted my Vagrantfile and associated metadata within the project, and opted for a clean start.

**Attempt two-threeish:**

I found a box called ubuntu/xenial64 on the Vagrant cloud that is running Ubuntu v16.04.  This is a better start.  So I run `vagrant init ubuntu/xenial64`, and my correctly versioned vagrantfile appears.  I run `vagrant up`, and boom.  Here we are.  My VM is running at the right version, and everything looks great.

![Vagrant Up: Nothing Installed](/images/vagrant_up_one.png)

I run `vagrant destroy` to spin down the VM, because now I need to go about making sure that my Vagrantfile includes provisioning to install Docker for Linux, and then the Datadog Docker Agent.  This is proving more challenging than I thought, as the shell command to install Docker, then fetch the Datadog Agent Image is not easy to find online.

Knowing that I will need to create an account with Datadog to recieve my API key anyways, I've decided to move ahead with that until I can find the proper shell commands, and I have a feeling these will be included in the setup.  This turned out to be a good instinct, as the  shell script to install the dockerized datadog agent was included directly after completing registration.  The correct script was:

```
docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=de9e4eb74662bf570392b15046b76e43 datadog/agent:latest
```

All I had to do was provide Docker to the vagrantfile, using `config.vm.provider "docker"` inside the Vagrantfile, then boot it up and run the agent installation command, and this happened:

![First Agent Reporting](/images/first_agent_reporting.png)

Awesome!  I have the Datadog Agent running inside of my containerized Ubuntu VM, and it's reporting.  The Agent still is not installing itself during boot, which bothers me, so I'll be working to provision that shell command to run automatically.  I re-organized my Vagrantfile.  I type `exit` in the terminal to get back into my local machine, and then type `vagrant reload`, and...  I broke it again.  No worries.  I'm getting a syntax error, and I don't understand vagrantfiles well enough to know what it specifically means.  I'm going to try downloading an extension for VS Code that will give me syntax notes on vagrant.  

I downloaded an extension called Vagrantfile Support by user Marca Stazi.  It's not showing me any errors, although the syntax highlighting has improved the readability of the code.

The shell script is not compiling.  The agent is installed on my local machine.  Not the VM.  Oops.

**Attempt four-ish, five-ish:**

Okay.  I slept on it, and when I woke up this morning I got it done in about twenty minutes.  My vagrantfile is now provisioning Docker, and then using an inline script to pull the docker image and configure the agent.  The meat of my Vagrantfile looks like this:

```
Vagrant.configure("2") do |config|

config.vm.box = "ubuntu/xenial64"

config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

config.vm.provider "virtualbox" do |vb|
# Display the VirtualBox GUI when booting the machine
     vb.gui = true
     vb.name = "Nate Ubuntu VM"
# Customize the amount of memory on the VM:
     vb.memory = "1024"
end

#provide docker to the VM
config.vm.provision "docker" do |d|
end

#provision a shell script to mount the agent image
config.vm.provision "shell" do |s|
     s.inline = "docker pull datadog/agent" 
     s.inline = "docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v                       /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=de9e4eb74662bf570392b15046b76e43 datadog/agent:latest"
end
```

   I have a feeling that there may be a way to provision docker and run the shell script in the same block, or mount the image using `d.build_image` just beneath `config.vm.provision "docker`, but it's working currently so I'm not going to touch it for now, or maybe ever again.  I have now sucessfully spun up a vagrant VM running Ubunu v16.04, installed Docker through provisioning, and then provisioned the Datadog Agent using a shell script.  That's awesome.  A week ago if someone had asked me to do that, I would have stared blankly into their eyes and said "You're out of you mind.  That's rocket science."  All it took was some good old fashioned beating my head into the desk, some self-doubt, and reading.  This is what coding is all about to me.  That moment when you finally figure something out is worth it.  It's the same feeling as trying to record a complex guitar part, and the fingering stretches beyond your limits, moving faster than you can keep up with, the melody escapes you and you can't even remember what key you're in.  It doesn't matter if it takes twenty takes as long as you get it.  

   Then I realized the VM was not recognizing the `datadog-agent`command, so I ran the `DD_API_KEY=de9e4eb74662bf570392b15046b76e43 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"` to install again.  The site had mentioned that I should be prompted for a password after running this command, but I was not prompted and I'm unsure why.  I don't have permission to access the datadog.yaml file, and cannot run the GUI.  I have a feeling it has to do with the App key I generated from the datadog site, but I'm unsure of how to use it or where to put it. (update: it had nothing to do with the app-key)

Running `sudo chmod -R a+rwx /path/to/folder` into the terminal allowed me access into the agent folders and files.  Trying to run the GUI gave me an error that I would have to set an appropriate port in the .yaml file.  Tried setting port to "5002" with no success.  I believe it isn't going to work because the Datadog Docs say "For security reasons, the GUI can only be accessed from the local network interface (localhost/127.0.0.1), so you must be on the same host that the Agent is running to use it. In other words, you can’t run the Agent on a VM or a container and access it from the host machine."

Here's a picture from the Datadog dashboard showing my beautiful green hexagonal machine quietly and calmly running and reporting in:

![My VM Reporting] (images/vm_host_reporting.png)

Alright, that's been broken several times and then mostly fixed.  I accidentally have a datadog-agent running somewhere on my machine and I don't know where, but I've got one running inside the VM and that's what counts. It isn't perfect but might get me through the rest of this exercise.  What's next?

### Collecting Metrics

**My Host**
I added a tag called "example_tag" to the ubuntu/xenial host via the add tags button on the popup box that shows after clicking on the host.

![My Host and Tags] (/images/host_and_tags.png)

**Install MySQL to my VM**
To begin, I ran `sudo apt-get update`, then `sudo apt-get install mysql-server`.  I set the root password to 1234.

From here I followed the instructions on the datadog integration page for MySQL.
I was unable to complete the full integration into my system due to permissions errors, and finding answers is coming slowly.  I'm able to log into the root user, but root does not seem to have any permissions, and even when running commands signed in as the root user with the proper password, I'm given another error message that states user vagrant@localhost does not have permissions.   The last error I got was that the world-writable config file at /etc/mysql/my.cnf is ignored.  I tried to make the file read only, as suggested at https://github.com/cytopia/devilbox/issues/212, but permission to change permissions was denied.  The problem may be the environment, and I'm not sure I know enough about the environment to fix it as is, and I'm worried about crashing the entire box if I continue messing around with permissions.  I'm going to push ahead in hopes I can answer the other questions without this integration returning data to the agent, as I'm unable to create a datadog user.  Here is a picture showing a manual install of the MySQL integration from my Datadog Account:

![MySQL Integration] (/images/mysql_installed.png)

**Creating a Custom Agent Check** (used a tutorial from https://datadog.github.io/summit-training-session/handson/customagentcheck/)

Step one is to create a configuration file for the custom check in /etc/datadog-agent/conf.d. I created a file called my_metric.yaml, then wrote the following inside it:  (I decided to set the min_interval_collection to 45 from here, as the default is 15 seconds)
```
init_config:

instances:
-min_collection_interval: 45`

The next step is to create the python file that has instructions for the check.  In checks.d, I created a file called my_metric.py and wrote the following:

`from checks import AgentCheck
class MyMetric(AgentCheck):
def check(self, instance):
self.guage ('my_metric', random.randint(0,1000))
```

To test the check, I ran `datadog-agent check my_metric`, which showed an error in my yaml file.  There was some metadata nonsense at the top of the file.  I deleted that, and now running a metric check shows the error at line four.  I believe it's the hyphen, and I also think wrapping the who min_collection line in `[{}]` will do the trick so I'm going to delete and add, then run the check again.  This didn't work, so I'll delete the minimum interval and the init_config: and run again.  As far as I can tell, the page https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6 says all I need in the yaml file is `instances: [{}]`, so I'll match that exactly and re-run.
Awesome.  A new error, which is progress.  It says Global name random is not recognized, so my thought is I may be missing an import in my .py file.  Boom.  I believe my custom check is now working, and will try to verify this on the site:

![Custom Metric Found] (/images/my_metric_found.png)

Great,  I've installed an integration that I can try to get up and running if I figure out my permissions errors with mysql, created a custom metric, and the Datadog site has access to it.  
To end this section, I'll be trying to adjust the metric to report every 45 seconds instead of the default 15 second interval.  I went back into my yaml and am trying to find where the min_collection_interval goes.  This configuration appears to work:

```
min_collection_interval: 45

instances: [{}]
```

This returns a successful check from the command-line, so I'm crossing my fingers here because I think I've got it right.  I'm not sure why init_config: is not working, but theoretically my metric is now sending a random number between 0 and 1000 on an approximately 45 second interval.

### Visualising Data
 **Seeing my_metric in Action**
 Okay, so now I'm going to create a Timeboard that observes this metric reporting data from my ubuntu/xenial host.  I'm unable to show metrics from my database integration, as I was unable to resolve permissions errors, and don't think I will be able to on the Ubuntu system that I'm not as familiar with as OSX.  I had the same issues installing MySql Server to my machine, and was barely able to fix it on a familiar OS.  Then I'm going to display my custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.  Here's the screenshot from my dashboard:

 ![My First Timeboard] (/images/timeboard1.png)

The code for the metric over host graph is:
 ```
 {
   "requests": [
     {
       "q": "avg:my_metric{host:ubuntu-xenial}",
       "type": "line",
       "style": {
         "palette": "dog_classic",
         "type": "solid",
         "width": "normal"
       },
       "conditional_formats": [],
       "aggregator": "avg"
     }
   ],
   "viz": "timeseries",
   "autoscale": true,
   "yaxis": {
     "max": "1000",
     "min": "0"
   },
   "status": "done"
 }
 ```

 The code for the rollup function graph looks like:

 ```
 {
   "requests": [
     {
       "q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)",
       "type": "line",
       "style": {
         "palette": "dog_classic",
         "type": "solid",
         "width": "normal"
       },
       "conditional_formats": [],
       "aggregator": "sum"
     },
     {
       "q": "avg:my_metric{host:ubuntu-xenial}",
       "type": "line",
       "style": {
         "palette": "dog_classic",
         "type": "solid",
         "width": "normal"
       }
     }
   ],
   "viz": "query_value",
   "autoscale": true,
   "status": "done",
   "yaxis": {
     "max": "1000"
   }
 }
 ```
 The next step in this assignment is to set the Timeboard's frame to five minutes, take a snapshot, and send it to myself with @ notation.  I set the rollup function to a time period of 5 minutes and sent a snapshot to myself, and it showed up instantly in my inbox!

 ![Snapshot email] (/images/snapshot_email.png) 

 Alright.  Cool.  I got through this section without breaking anything else!  I'm unable to answer the bonus question because I couldn't get my database integration to listen to me, and don't have an anomoly graph to refer to.  Now to work with monitoring in Datadog.

### Monitoring Data

 **Creating Monitors**
 Okay, so first I'm going to take my metric, and create a monitor that will warn at a threshold of 500, Alert at a threshold of 800, or notification if there's no data for 10 minutes.  This monitor is going to be configured to send me an email whenever it is triggered, have different messages for Warning, Alert, and No Data.  The email notification should also include the metric value that cause the monitor to trigger and the host ip when the monitor triggers an alert state.


 This was pretty easy, just navigate to the Monitor section on teh Datadog platform, and create a new one!  It's pretty straightforward from there, just fill out the boxes, and make sure your message is using the right message template variables.  Here's a screen shot showing my monitor before saving and creating it.  I've also been at this for a while, so I added a funny subject line to the email.  It's the little things in life.  Anyways, here is what the monitor creation looks like inside Datadog:

 ![Creating a Monitor] (/images/create_monitor.png)

 Now I just click save, and wait for my monitor to be triggered!  Boom!  Near instantaneously my computer notifies me I have a new message from datadog alerts, and here is my email:

 ![Alert] (/images/alert.png)

 **Scheduling Downtime**
 Okay, the last step is to get this monitor not to bother me if I'm outside of the office,  I navigated to Monitors, and then "Manage Downtime."  This is another relatively simple operation.  Fill out the boxes, double check your downtime, and submit.  I created two downtaimes for this monitor, one for weekends and one for weekdays.  The weekend downtime is scheduled to start on Saturday at 9AM and last for two days (the time before 9AM should be covered by the downtime scheduled on Fridays, and then from there last until Monday at 9AM).  This should cover downtime.  Here is a screenshot of the downtime creatiion window on Datadog.com:

 ![Down Time Editor] (/images/downtime.png)

 This covers some basic information on Monitors in Datadog, and I got through this one without breaking anything!!

 Next, we'll look at APM Data in Datadog, and how to get your own apps reporting data to the agent.

### Collecting APM Data

**Attempt one**
Okay, here we go.  I'm not sure if I actually have Python or an interpreter installed on the machine, so I can check that by running `python -v` in the command line.  This tells me my VM has the packages for Python 3.  I ran an install script, `sudo apt-get update; sudo apt-get install python3`, and everything is up to date.

Installation instructions for Python on this OS can be found at http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/.

Now to install Flask to the VM so I can get this Flask App going.  The first step is to make sure that virtualenv is installed on your machine.  I've read that it is bundled with Python 3+, so theoretically I already have it.  On the command line I typed `virtualenv`, and was told that it is not currently installed, so I run `sudo apt-get install python-virtualenv`.  So virtualenv installs, and is supposed to help make certain that a virtual environment remains consistent for the project you are working on.  The next step is to creat a project folder for the app, and get the virtual environment running on it.  So I created a folder called DD_APM_app, and I'll be working from there to get the app up and running.  Then I thought better of that approach.  Having the app running outside of my VM seems bound to cause issues, so I went to read up some more on it.

Reading has convinced me that I will be able to gather data from the application outside of my VM, because I'll be installing another Datadog Agent in it or I can utilize the agent I accidentally installed on my local machine, if I can find it.  The Agent running in my VM currently shouldn't need access to the app, or at least I think so.  Now I think the issue will be that I'm running a Flask App on my local machine, and I probably will need to install Python (unless OSX already has it installed, and I need to make sure that virtualenv is running on my computer.)  Let's figure it out!

**Attempt two**

Okay, I'm going to start this time by getting the application up and running.  I brought up a new terminal for my local machine, and found that it is running Python 2.7.10.  I'm going to update Python to the latest version.  To do this I went to https://www.python.org/downloads/ and clicked download.  Easy.

Now I'll be following the directions to install Flask on my machine.  I've already created a directory for the app to go in (DD_APM_app), and the next step is to run `python3 -m venv venv` inside the app's directory.  This adds a venv folder to the project.  The next step is to activate the environment by running `. venv/bin/activate`.  Now virtualenv is running, and I run `pip install Flask` to install.  Alright, I think it's installed in the environment, where (with any luck) I can now copy/paste the app code for this challenge, and get it running.  I put the code into the app.py file, and we're back to that critical moment of "This *should* work."

To run the app, simply tell flask what to run.  In this case, the command is `export FLASK_APP=app.py`.  Next, tell flask to run with `flask run`.  The terminal outputs that the app is running at http://127.0.0.1:5000/.  So I navigate there in my browser and...

![Flask App Running] (/images/flask_app_works)

Okay.  The app is up and running, and looking through the code it appears to be a simple application with three routes that specify an entry pointto the application, an apm endpoint, and a trace endpoint.  So my Flask app is up and running.  What's next?

I found instructions for tracing Python applications at https://docs.datadoghq.com/tracing/setup/python/.  The first step is to install the Datadog Agent.  I run `DD_API_KEY=de9e4eb74662bf570392b15046b76e43 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"` from my app's directory on the mac terminal, and the agent is installed.  The next step is to install ddtrace using the `pip install ddtrace`.  This returned an error.  Permissions again.  I tried running `sudo pip install ddtrace`, and that was successful.

Now, if all goes well, running `ddtrace-run python app.py` from the project directory should instrument the application.  Hmmm.  I'm not sure if it's working, so I'm going to switch over to my dashboards on the Datadog site, and see if anything new is coming through.  By going to the Nathan's Imac host, I was able to see that the apm is not currently functioning.  I think it may be disabled in the datadog.yaml file.  I navigated to that on my local machine and uncommented `apm_config` and `enabled: true`.  Now I wait a few minutes and see if that fixed the problem.

**Attempt three-ish**

Okay, it looks like the apm is set up, but no metrics have started coming in yet.  My python file is not importing flask properly, and I think this may be due to having created the file outside of the venv environment.  My host has also disappeared from the hostmap on the site, and I feel it may have to do with trying to change the datadog.yaml file to enable apm.  I'm not sure how to fix this, but I'm going to try deleting the python file I have and creating a new one from inside the environment.  This has not helped.  I'm going to try running the program with `pythron3 app.py` instead of flask run, as a user at https://stackoverflow.com/questions/37508020/no-module-named-flask-in-virtualenv-although-installed suggested.  I still don't believe this solves the importing issue, but the app is running again.  I have stopped and re-started the agent, hoping that this error would go away after changing the datadog.yaml file to enable apm, though it doesn't seem to have had an effect.

I have been at it for about two hours now, and I can't seem to find a reference to this error that is being reported from the host page.

Datadog's apm integration is reporting:
Instance #initialization[ERROR]:{"Core Check Loader":"Could not configure check APM Agent: APM agent disabled through main configuration file","JMX Check Loader":"check is not a jmx check, or unable to determine if it's so","Python Check Loader":"No module named apm"}

I have changed the datadog.yaml file to enable the apm reporting, and stopped and restarted the agent several times in hopes that it would re-evaluate these variable upon starting again.  Everything I've read says that this should get rid of this error.  The last thing I can think of is that the agent that is running inside the environment is simply unable to see the datadog.yaml file from where it is currently sitting, so I'm going to try stopping the current agent, then installing a new one from outside the environment.  If this does not resolve the issue, I'll sleep on it and come back tomorrow.

The Datadog Agent has crashed on my system, and will not open.  The bone icon in my tray gives me the rainbow death wheel and has been doing so for about twenty minutes now.

I'm going to attempt a restart of my computer, crossing my fingers that I'm able to save the information currently on my VM.  Restarting ran the agent, and I was able to finally open the GUI for the agent.  I edited the yaml file from there, and am now awaiting to see if my app is reporting properly.  I also noticed that I hadn't installed the python integration yet on the site (I could have sworn I did that--oops), so I have installed that.

It took some doing, but I'm down to my final error before I think it has to work.  I cannot get python, inside of my venv virtual environment, to accept the flask import.

AH!  I think I've figured it out from this site: https://docs.python.org/3/library/venv.html.  For whatever reason, the environment doesn't create itself with access to the system site packages, which is conveniently where flask is stored.  I'm not sure why this is the case.  It seems counter intuitive to tell the environment you plan to use things you have downloaded.  I went into the pyvenv.cfg and changed false to true on the include site packages option.  Let's see if this was the problem all along!

Negative.  I'll try again if I have any new ideas, but as of now I'm tapped out.

Unfortunately, I was unable to get the ddtrace program to integrate successfully with my application.  I've racked my brain as to why, and cannot come up with anything to resolve the issue.  As a last resort, I tried moving app.py to within the venv folder so that it would be fully within the environment.  This had no effect.  Unfortunately, I'm at the end of my knowledge, and won't be able to complete this portion of the exercise.  Any feedback as to where I went wrong would be greatly appreciated, because it makes no sense to me.  In a work setting, I'm sure I'd be going to someone that understands this environment better and saying "I cannot figure this out.  Here's the steps I've taken, and I'm lost and fear anything I do from here on out will further break it."  It's frustrating, because I hate giving up, but I'm at the end of my knowledge here.  I will probably give it some further consideration, and if I come up with a novel approach I'll be sure to commit and push these changes to my forked repo on github.


### Going Outside The Box With Datadog

 Datadog has been used for more than simply measuring metrics, including working with the NYC Subway System and more.  I've been asked to think outside of the box about how Datadog could be used, and I think that this tech could be utilized by ad agencies to test the effectiveness of marketing campaigns.
 Let's say you are a Marketing person, and you're using two different campaigns on the same product, and you're looking for a way to aggregate data about which campaign is driving more traffic to the site, app, etc.  You even want to know how it's faring on the east versus west coasts to gauage the campaigns effectiveness by region or city.  If both campaigns point to the same host site but have two different servers that are accessed by a different domain (one for the first campaign, and the other for the second), I could imagine that each servers hit rates could be summed to show the advertiser which campaign is getting greater hits.  A third server could even indicate traffic that isn't being driven by the campaigns.  If these metrics can also include an accurate server location (for instance, when someone types the url in Austin the server shows a hit in Austin instead of Timbuktoo), someone could theoretically set up a dashboard showing real-time statistics on the success of one campaign over the other spread out across any number of regions or cities in the world.  Further research on this would include how to gather demographic data from users that make a hit so that these can be graphed to show success by demographic by campaign as well as total stats.  I'm certain tools that do this exist currently, though I think the level of customization available to the Datadog platform may be worth exploring in the Marketing realm.

### Closing Remarks

 So, here we are.  At the end of this assignment.  I've learned a handful of new-to-me technologies at a basic level (Vagrant, VirtualBox, Docker, Datadog, Python, Flask, Virtualenv, Pip), gotten a deeper delve into the Ubuntu system that I'm unfamiliar with, and come to understand a great deal more about running dev environments and programs from the command line.  I think I've performed well, given how over my head I was at the beginning of this assignment, and was only unable to configure a MySQL integration installed on an unfamiliar OS with permissions errors I don't understand, and an apm integration that failed (I think) based on a bizarre but common error that seems specific to the Virtualenv platform.  I'm truly bummed out by this.  I don't like giving up on anything, but in light of the fact that it's 1:30AM on a Sunday and I began at around 1:00PM Saturday.
 Regardless, this assignment has been eye-opening, the biggest learning experience I've had since attending coding bootcamp, and mostly fun (minus a few moments of heavy doubt) and I've taken a liking to the Datadog platform and found a deep interest I didn't know  I had in performance monitoring.
 I've done (most) of it, and I believe that I've proved myself to be mostly competent, a tenacious and eager learner who takes a ton of pride in his work, someone who does not give up easily, and a pretty decent writer to boot.  We have reached the end of this assignment, and I have fixed more things than I've broken and learned more than I thought possible over the past few days.  This, I think, is a win in any programmers book.
 Thank you again for your consideration, and thank you for reading my submission.  I'm eagerly looking forward to hearing back from the team at Datadog!
