# Solution Engineer Technical Exercise Submission - Pabel Martin

Here are my answers for this technical exercise along with all supporting links, screenshots, and color commentary.

What will be fairly obvious is that this exercise was fun to get through, but **very** challenging.  For better or worse, almost all of this was a first for me in many areas:
  * I'd never heard of Vagrant, Flask, YAML, or Markdown until working on this exercise
  * I've heard of Python, Ubuntu, MongoDB, and GitHub prior to this exercise, but have never worked with any directly
  * The only thing I'd done before that was a part of this exercise was google liberally (always) and execute some command line stuff (years since I'd done this) so I was pretty rusty.
  
If I had to characterize what it was like to go through this, I would say that it was just brute force trial and error.  Throughout the whole exercise I was reminded me of the scene in the Matrix where Neo first sees Matrix code 'falling' on the monitor and asks Cypher if he always looks at it encoded. Cypher responds that he has to because of all the information coming through but that he's used to it and now just sees the people in the matrix that the code represents.  In this exercise, it felt like all I ever saw was green falling code.  Eventually after following enough instructions and steps it worked, but I honestly don't fully know how or understand the details of how/why everything worked.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene1.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/scene2.png)

This submission, for example, is something I've never done before.  I had a developer friend walk me through GitHub and what forks, commits, branches, pull requests, and markdown were and how they were used.  I haven't had experience with any of these to-date so I used [this](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and [this](https://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown/16426829#16426829) to create this submission.  It's entirely possible I haven't submitted as expected on the right branch so enjoy a chuckle if I didn't even get this first part right.  :)

You'll also see this in the submission, but two major mistakes for me were not coming back to the main exercise GitHub page.  I missed the update to use Ubuntu 16.04 instead of 12.04 as well as the update to the Flask app for host name.  If I'd seen that, I would have saved myself a ton of grief/time; a mistake I'll strive to only make once.



## Table of Contents

  * [Setup the Environment](#setup-the-environment)
  * [Collecting Metrics](#collecting-metrics)
  * [Visualizing Data](#visualizing-data)
  * [Monitoring Data](#monitoring-data)
  * [Collecting APM Data](#collecting-apm-data)
  * [Final Question](#final-question)
  


## Setup the Environment

I followed the steps outlined in the **Setting Up Vagrant** link from the Reference section and setup Vagrant on my Macbook Pro.  The exercise page as of 5/27/18 when I started referenced setting up a machine with Ubuntu 12.04 so I used the 'precise' argument in the command line referenced in the [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/) page.

This caused an issue later on in the exercise when trying to install MongoDB and Flask as it kept hitting issues/errors from dependencies.  I upgraded the box manually to Ubuntu 14 and that helped clear the MongoDB issues.  I still hit issues installing Flask later on that I couldn't get past so I was back on the exercise's GitHub page trying to find a workaround.  That's when I noticed that it was updated to reference Ubuntu 16.04 so I started the exercise from scratch with a new box on that version.

These screenshots will show the details of my Datadog trial account along with the Infrastructure List page showing both boxes I configured.  The configuration files documented below are the same on both boxes for the datadog-agent so I've only included one copy for review.

![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/DDenv.png)
![alt text](https://github.com/pabel330/hiring-engineers/blob/solutions-engineer/infrahostlist.png)


## Collecting Metrics




**Bonus Question**




## Visualizing Data


## Monitoring Data


## Collecting APM Data


## Final Question




