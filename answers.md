Submission for support engineer at Datadog <br> 
Date: 08/14/2014 <br> 
From: Dara Mao <br>
Email: dara.mao@gmail.com 

## Questions and My answers:

### Level 1
===
* <strong>Sign up for Datadog, get the agent reporting metrics from your local machine.<br>Answer:</strong> I have set up the agent reporting metrics for my local machine: `host:Daras-MacBook-Air-2.local`

* <strong>Bonus question: what is the agent? <br> Answer: </strong> The agent is a piece of software that collects events and metrics on the users hosts for monitoring and managing performance data.

* <strong>Submit an event via the API.<br> Answer: </strong> 
 To submit an event via the API, my code:

	 require 'dogapi'
	 
	 api_key = 'DATADOG_API_KEY' 
	 dog = Dogapi::Client.new(api_key)
	 
	 response = dog.emit_event(Dogapi::Event.new('Level 1 question 3', :msg_title => 'Support Engineer Dara Mao')) 

* <strong>Get an event to appear in your email inbox (the email address you signed up for the account with)<br> Answer: </strong> By adding @dara.mao@gmail.com in the event body. 
 My code:

	 require 'dogapi'
	 
	 api_key = 'DATADOG_API_KEY' 
	 dog = Dogapi::Client.new(api_key)
	 
	 response = dog.emit_event(Dogapi::Event.new('Level 1 question 4 to @dara.mao@gmail.com', :msg_title => 'Support Engineer Dara Mao'))
