My answers to the questions are here !!!

# Prerequisites - Setup the environment
Prior to the interview I had already signed up for Datadog to play along the tool and interfaces with my own company name Cogitos Consulting. After the interview I have changed the company name to “Datadog Recruiting Candidate” and start to write down this document.

I've gone with the ready captive environmet of mine and used one of my linux installs with Ubuntu distrubution with version 18.04 Bionic on VirtualBox.

# Collecting Metrics:

* Adding tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

My host prior to adding tags

<a data-flickr-embed="true" href="https://www.flickr.com/photos/187392514@N02/49649359148/in/dateposted-public/" title="hostmap_00"><img src="https://live.staticflickr.com/65535/49649359148_8620b9abcb_c.jpg" width="800" height="403" alt="hostmap_00">

I added three tags to my host via editing datadog.yaml file

<pre class="contents "><span class="cmd command">edit file</span>
<span class="output computeroutput">tag edit
tags:
         - environment:dev
         - hostdbapp:pgsql
         - hostwebapp:tomcat
</span>
</pre>



<a data-flickr-embed="true" href="https://www.flickr.com/photos/187392514@N02/49649939656/in/dateposted-public/" title="001_tags_on_datadog_yaml_file"><img src="https://live.staticflickr.com/65535/49649939656_e1a86822f6_c.jpg" width="800" height="129" alt="001_tags_on_datadog_yaml_file">
