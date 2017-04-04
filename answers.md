Your answers to the questions go here.
Level 1 - Collecting your Data
	* Agent reporting metrics from your local maching: See "Screen Shot - local matching metrics.png"

	* What is the Agent?
	Agent is a datadog program/softwar which can be installed on any system or app.  It will monitor and collect metrics and events from that system or app.

	* Add tags: See "Screen Shot - host tags.png"

	* Intall database: See "Screen Shot - Database dashboard.png"

	* Custom Agent Check: See "Screen Shot - Custom Agent Check.png"

Level 2 - Visualizing your Data
	* Clone database dashboard and add Agent Check metrics: "Screen Shot - Custom Agent Check.png"

	* What is the difference between a timeboard and a screenboard?
	All the graphs on timeboard are synchronized on the same time and they are sorted in a grid-like fashion.  
	Screenboard provides more flexibility.  Graphs can have different time frame and can be palced anywhere on the page.  Text and pictures can be added to screenboard as well.  
	Graphs on timeboard can be shared individuly but ScreenBoard can be shared as a whole.

	* Draw a box around a section that shows it going above 0.90 on test.support.random graph: See "Screen Shot - Custom Agent Check.png"

Level 3 - Alerting on your Data
	* Set up a monitor: See "Screen Shot - monitor email"

	* Make it a multi-alert: See Manage Monitors at https://app.datadoghq.com/monitors#manage

	* Give it a descriptive monitor and message: See "Screen Shot - monitor email"
	
	* Downtime: See downtime setup at this link https://app.datadoghq.com/monitors#downtime
		- downtime is setup for daily from 7pm to 9am.  it was setup after 7pm today so the email will be sent tomorrow.
