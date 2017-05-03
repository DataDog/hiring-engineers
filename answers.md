Your answers to the questions go here.

# Getting Started with DataDog

## Overview
This document will provide a walkthrough on how to set up a monitored host in Datadog, and from there, add a custom metric with checks and alerts. 

Each level will be broken up into 2 sections.
1. Walkthrough: This catalogues the steps you would take to accomplish the tasks in the level. It's written as though it might be used as a guide for a customer
2. Thinkthrough: This section is to give you insight into my process going through the level. I'll share what was straightforward, where I encountered problems, how I approached those problems, how I fixed them (if I did), and other insights.

## Prework
This project was started on May 3, 2017.
Before I started the levels, I read through the reference material and took notes in order to prime myself on the material. You can find those notes in notes.md. 
I also did a quick tutorial online[^1] for writing in markdown so that I could write a good-looking answers.md. 
I had originally planned to write this all in Google docs, but after seeing the repository, 
I decided it made more sense to use markdown. Especially sense most github readme's tend to use it!

## Level 0 (optional) - Setup an Ubuntu VM
Optional Step to avoid dependency issues

## Level 1 - Collecting your Data
You will create a DataDog Account, modify the Agent's configuration, install a database, add the DataDog integration for that DB, and write a custom agent check.

Bonus question: In your own words, what is the Agent?  
Reference link: http://docs.datadoghq.com/guides/basic_agent_usage/  
Idea: Draw a diagram outlining the 3 key components and how they work together

### Walkthrough

### My Thinking for each Step

## Level 2 - Visualizing your Data
You will clone the starting dashboard, add additional metrics, and make sure your email recieves a snapshot with @notification.

Bonus question: What is the difference between a timeboard and a screenboard?

## Level 3 - Alerting on your Data
You will set up a monitor for your metric (it should alert you within 15 minutes).

Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.  
Bonus: Since this monitor is going to alert pretty often, you don't want to be alerted when you are out of the office. Set up a scheduled downtime for this monitor that silences it from 7pm to 9am daily. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.


## Appendix

### Software Used
- VIM - for editing Markdown files

### Online Reference Material
- [^1]: [Markdown Tutorial](http://www.markdowntutorial.com/)
- [Markdown Quick Reference](https://en.support.wordpress.com/markdown-quick-reference/)
