Your answers to the questions go here.

# Data Dog Solutions Engineer Exercises - George Smith-Sweeper

## Prerequisites - Setup the environment

I choose to use vagrant and virtual-box to complete these exercises. Since I’ve been using HomeBrew as my package manager I chose to install vagrant and virtual box via the command-line.

`brew cask install vagrant`
[BrewInstllVagrantCommand](images/VagrantInstall.png)
`brew cask install virtualbox`
[BrewInstallVirtualBoxInstall](images/VirtualBoxInstall.png)

Once these have been installed it’s time to spin up a fresh Ubuntu VM. The first step is to create a new folder for the exercises `mkdir dataDogExercises` and the jump into that newly created folder `cd dataDogExercise`.

In order to avoid dependency issues I searched the [vagrant cloud](https://app.vagrantup.com/boxes/search) for a Ubuntu 16.04 LTS build (ubuntu/xenial64) and initialized my vagrant with this build. `vagrant init ubuntu/xenial64`.

[Photo of command line prompts initializing Vagrant](images/InitializeVagrant)

Now that Vagrant has been initialized you have to run `vagrant up` to start the VM. Once the VM is up and running typing`vagrant ssh` into the command prompt will log you into the to the newly started VM.

When done correctly, your prompt should now look similar to the one below:
[Vagrant Prompt](images/VagrantPrompt)

After logging into the new virtual machine, you must sign up for data dog in order to get access to my Data Dog agent metrics, your API KEY, and Dashboard.

[Datadog sign up](images/DD_API_KEY)

I suggest using copying the entire provided prompt and pasting it into the prompt in your VM. Doing this will install DataDogs agent onto your VM, store your API_KEY, and provide access to the DataDog dashboard.

[Installing DataDog Agent messages](images/InstallingAgent)
[Data Dog Agent Installed messages](images/AgentInstalled)

## Collecting Metrics:

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

## Visualizing Data:

* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

## Collecting APM Data:

* **Bonus Question**: What is the difference between a Service and a Resource?

## Final Question:
