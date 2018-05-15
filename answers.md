Your answers to the questions go here.

## Prerequisites - Setting up!

I am working on an early 2015 MacBook Pro on macOS High Sierra (10.13.4), and spun up a virtual machine using Virtual Box and the Vagrant Ubuntu environment. I simply followed the installation instructions on the docs, but here's the TLDR:

1. Download and install [Virtual Box](https://download.virtualbox.org/virtualbox/5.2.10/VirtualBox-5.2.10-122088-OSX.dmg "Download VirtualBox for macOS")  and [Vagrant](https://releases.hashicorp.com/vagrant/2.1.1/vagrant_2.1.1_x86_64.dmg "Download Vagrant for macOS").
2. Make a directory where you'd like to do your work in (mine is called `datadog_vagrant`), `$cd` into this directory, and run:
```
$ vagrant init hashicorp/precise64
$ vagrant up
$ vagrant ssh
```
You should now see `vagrant@precise64:~$` in your terminal.
3. Create your username and all that jazz by clicking on the "Get Started Free" button at the top right of the data dog site. A form should come up that looks like this:
![alt text](https://s3.amazonaws.com/juliewongbandue-ddhiring/create_account_form.png "Form")
4. Now install curl by running `sudo apt-get install curl` and then run the sweet, sweet command on the DataDog docs:
```
DD_API_KEY=3840599a1d800170269b6a93c2471c73 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
It's always delicious to see when things work. If everything goes according to plan, you'll see this message in your terminal:
![confirmation message](https://s3.amazonaws.com/juliewongbandue-ddhiring/DDAgent_confirmation.png "Installation Confirmation")

## Collecting Metrics
+ Adding some tags using the configuration files!

⋅⋅⋅So, as per your Datadog's [documentation](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/), I found the yaml file by `$cd`-ing into the `/etc/datadog-agent/conf.d` directory and opening up the `datadog.yaml` using vim (after running `sudo at-get install vim`, of course).
![datdog.yaml](https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent.png)

⋅⋅⋅Because the file is a readme (that I didn't have the permissions to update and save the file, I ran `sudo vim datadog.yaml` and added some tags:  
- tag1:value1
- tag2:value2
- tag3:value3
![datadog.yaml updated tags](https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent_addedtags.png)

And this is what rendered in the UI:
![datadog hostmap](https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog.agent_addedtags.png)

However, it took me a little time to figure out that I had to restart the agent for the tags to happen. Whoops. And also... that I totally overlooked the whole "You see both forms in the yaml configuration files, but for the `datadog.yaml` init file only the first form is valid." (referring to the format below):

```
tags: key_first_tag:value_1, key_second_tag:value_2, key_third_tag:value_3
```

heh... so I updated the file to the correct format...
![datadog correct yaml](https://s3.amazonaws.com/juliewongbandue-ddhiring/vim_datadog_addedtags_correct.png)

And here's what it looked like in the UI.
![datadog hostmap correct](https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_tags_correct.png)
![datadog charts](https://s3.amazonaws.com/juliewongbandue-ddhiring/datadog_hostmap_charts.png)
