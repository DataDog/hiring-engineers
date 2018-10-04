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
![vagrant version](media/vagrantVersion.png)
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

