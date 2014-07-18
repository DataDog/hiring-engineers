# Level 1

## Question 1: Sign Up for Data Dog and Install the Agent

My dashboard for my local machine is at: https://app.datadoghq.com/dash/host/4879890?live=true&from_ts=1405698620859&to_ts=1405702220859&tile_size=m

My events are at: https://app.datadoghq.com/event/stream?show_private=true&per_page=30&aggregate_up=true&display_timeline=true&from_ts=1405101600000&live=true&to_ts=1405706400000&incident=true&codemirror_editor=true&bucket_size=10800000

I installed the agent using the provided shell command.

## Bonus Question: What is the agent?

I looked at the install shell script and followed what it was doing to install the agent. I saw a line that mentioned installing the agent from: https://github.com/DataDog/dd-agent/ . I looked at that and saw it was a big python application. From the shell script, I saw the line where the script was testing if the agent was running properly. The way it tested was by submitting a curl to http://localhost:17123 so I assumed the agent is a combination of python scripts that report to some local running web application written in python cause I saw the shell script also install Tornado which I think is a python web server.

## Question 2: Submitting the Event via the API

I created a ruby script to submit an event via teh DataDog ruby gem using the sample script from the API documentation as a template. The script is in this repository as post_event.rb.

## Question 3: Get an Event to Appear in Email

I wasn't sure how to trigger an event to notify me via email however I did find the Alert feature. I figured that if I created an alert, those would notify me of events. I created an alert using the sample ruby script from the API documentation and sort of figured that if I lowered the threshold to > 1 byte and made it an alert of 5 minutes, that would always trigger and then data dog would email me. However, so far, this has yet to happen. Not quite sure how the Alert/Notification feature of datadog is suppose to work. The script is in this repository as create_alert.rb