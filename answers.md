Your answers to the questions go here.

Bonus Question 1: In your own words, what is the Agent?
   The agent is effectively a daemon that fills several
   rolls. It is somewhat similar to an http daemon (httpd) 
   like apache, but is much more specific in that it only
   connects and serves information to a specified site, or
   sites. The central purpose of the agent
   is to monitor other long-running processes while collecting
   data and serving it to a centralized location, on which
   the data can be compiled with data served by other agents
   to build a picture of one's infrastructure. 
   
Bonus Question 2: What is the difference between a timeboard and a screenboard?
   A timeboard and a screenboard are two different types of dashboard. The 
   obvious differences begin with an enforced layout for a timeboard, and a
   fluid drag-and-drop layout for a screenboard. The two boards represent two
   different types of monitoring of systems. A timeboard focuses on snapshots
   of system values over time, and primarily serves as a resource to see how
   resources are being utilized over time. A screenboard can also achieve this
   as they can have the same time graphs, but the purpose of a screenboard
   is generally to get an overview of an entire system, and I believe would
   probably be used to get a snapshot of *right now* for the things being 
   monitered. 

Link to Dashboard: https://app.datadoghq.com/dash/185301/postgresrandom-metric-dashboard?live=true&page=0&is_auto=false&from_ts=1474307023437&to_ts=1474310623437&tile_size=m

Link to Monitor: https://app.datadoghq.com/monitors#937913?group=all&live=4h 
Link to Downtime: https://app.datadoghq.com/monitors#downtime?id=195363148

Notes: I scheduled the downtime to be a few minutes ahead of the current time in 
order to get a screenshot and submit earlier, then deleted and redid the downtime
to be listed as 7:00 p.m. to 9:00 a.m. 

Bonus question approach: In answering these questions, I tried to minimize the amount
I looked at guides online. I wanted to determine if I could figure out what was happening 
purely based upon information on the machine and that I could derive from the app page. 
