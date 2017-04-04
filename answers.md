Your answers to the questions go here.

##Paula Lee - Support Engineer Hiring Challenge

#Level 1 - Collecting your Data
  -Bonus question: In your own words, what is the Agent?
    -The Agent is exactly that, an agent, in which the software gathers
     information on my behalf so that I can better assess and utilize my
     monitoring and performance data.

  -Add tags in the Agent config file and show us a screenshot
   of your host and its tags on the Host Map page in Datadog.
   -http://imgur.com/a/DuKT1

  -Installed PostgreSQL and the Datadog integration
    -http://i.imgur.com/3gV4ldj.png

  -Write a custom Agent check. Metric 'test.support.random'
    > import random
      from checks import AgentCheck
      \n
      class TestCheck(AgentCheck):
        def check(self, instance):
            self.gauge('test.support.random', random.random())

#Level 2 - Visualizing your Data
  -Cloned Postgres integration dashboard

  -Bonus question: What is the difference between a timeboard and a screenboard?
    -A timeboard has all of the graphs scanned at the same time.
      -The graphs are grid-like, easier to troubleshoot, shows correlation better,
       and can be shared individually.
    -A screenboard is more customizable, high-level, and flexible.
      -They have drag-and-drop widgets, which allow them to have different time lines.
      -Screenboards can be shared as a whole and have read-only access.

  -Take a snapshot of your 'test.support.random' graph and draw a box around a section
   show it going above 0.90.
      -http://i.imgur.com/CJLt0XA.png

#Level 3 - Alerting on your Data
  -Added multi-alert by host

  -Screenshot of the monitor alert
    -http://i.imgur.com/dJ90hkZ.png

  -Screenshot of the downtime schedule
    -**Note:** Instead of 7pm - 9am, I put 2am - 10am so that the message will show
     currently 1:41am
    -http://i.imgur.com/xcxwNM3.png




[dashboard link](https://app.datadoghq.com/graph/embed?token=509c61ab2ff4a860e96df1739bc636897e2003d214acdab6f86a3dd0b8a66b32&height=300&width=600&legend=false)
