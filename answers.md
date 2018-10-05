# Answers.md

Alright Reader buckle in because you're about to bear witness to my magnum opus AND learn how to use DataDog. If I've done my job right then by the end of this you'll find yourself a *big dog* at DataDog. Let's dive right into this


##1. Prerequisites 

###1.1 Preprerequisites

None(?)

###1.2 Setting up VirtualBox and Vagrant

Before we delve into using DataDog we're going to need to set up a fresh virtual machine environment. This guide will be using Vagrant with Ubuntu `v.16.04`. If you've got a different virtual machine installed congratulations you've tripped at the first hurdle. Anyway, battling on:


1. Download VirtualBox for *OS X hosts*: https://www.virtualbox.org/wiki/Downloads
2. Install the .dmg
3. Follower the installer
4. Download Vagrant for *macOS*: https://www.vagrantup.com/downloads.html
5. Follower the installer
6. Open up your terminal
7. run `vagrant -v` 
![Oh WOW! it's such a shame that you're looking at the alt text field for this image. This image was really something special. Too bad you can't see it. I mean really just eat your heart out. What an image. What. an. image.](media/vagrantVersion.png)
8. We can now create a new Vagrant environment for Ubuntu 16.04. Run the follower: `vagrant init ubuntu/xenial64`
9. Let's try starting our vagrant environment: `vagrant up`

Congratulations! You have a working virtual machine. Try ssh'ing into it with `vagrant ssh`. Alternative you can destroy it with `vagrant destroy`.

###1.3 DataDog sign up

1. Head over to https://app.datadoghq.com/signup
2. Enter *Datadog Recruiting Candidate* in the *Company* field
3. Once you arrive at the *Agent Setup* page, click *Mac OS X*
4. Follow the instructions on the page
5. The DataDog Agent report will take around a minute or two to complete so while that's toiling away maybe go make yourself a cup of- oh cool okay it's done.
6. Click Finish

That was definitely the easiest part of the set up so far

##2. Collecting Metrics 
###2.1 Tags

A *tag* enables for finer granularity of your metrics. For instance you could group the CPUs of all your hosts across different regions, and then filter by that region.

1. Let's add some tags to our DataDog config file. Our DataDog confile file can be found at `/opt/datadog-agent/etc/datadog.yaml`
2. Open that file up with your editor of choice (vim, VS Code, Sublime, nano, Microsoft Word, etc)
3. Navigate to line 43 and add some tags<br>![datadog tags](media/dataDogTags.png)Caveat: For the `datadog.yaml` config file only an inline dictionary with list of values is valid.
4. Restart your agent to apply the changes. (Click *Restart* on the bone in the taskbar)
5. Navigate to [the datadog portal](https://app.datadoghq.com/)
6. Click on the third dropdown on the navbar, then click heatmap
7. Your tags and host should now be visible:<br>![tags and host](media/tagsAndHost.png)

###2.2 Installing a Database on your machine

