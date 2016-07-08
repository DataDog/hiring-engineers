# Vincent Colavin's really cool answers.

I've added my custom check to vincents_check.py.

[Here is the link to my dashboard](https://app.datadoghq.com/dash/158974/postgres---overview-cloned)

And here is what my dashboard looks like:

<img src="http://i.imgur.com/vXqn8Xf.png">

Here are my answers and screenshots:

## Level 1
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  <img src="http://i.imgur.com/inhJtSA.png">
- What is the Agent?
  - The Agent is the (open source!) Datadog software that runs on the client's server. Its main responsibility is sending metrics to Datadog, which then does its analytics magic. It supports custom metrics.

## Level 2
- What is the difference between a timeboard and a screenboard?
  - The graphs on a timeboard are all synchronized by time. Timeboard graphs are laid out on a grid. The graphs can be shared individually.
  - Screenboards can include graphs, but also other widgets. Their layout can be customized. They can be shared as a whole.
- Take a snapshot of your test.support.random graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

  <img src="http://i.imgur.com/eAR6LPt.png">

## Level 3
- Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

  <img src="http://i.imgur.com/DW6In00.png">
- Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

  <img src="http://i.imgur.com/T9PmJ2V.png">
- This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

  <img src="http://i.imgur.com/lD1XQWa.png">
- Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
(I didn't get an email notification for this, maybe it will only be sent at 7 PM?)

  <img src="http://i.imgur.com/8gtcCLg.png">
