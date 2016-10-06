Your answers to the questions go here.

# Level 0

To ensure that we won't run into any OS or dependency issues, we'll start by create a new virtual machine running Ubuntu. After installing Virtual box and Vagrant, this can be done with the command

```
$ vagrant init hashicorp/precise64
```

which will add a new Vagrantfile to the project directory. Becuause we'll be editing the Datadog Agent config files on the vm to complete these challenges, it will be desirable to replicate those changes in the project directory so they can be pushed to the repo for submission. This can be done using Vagrant's folder sync ability by adding the following line to our Vagrantfile:

```
config.vm.synced_folder "dd-agent/", "/etc/dd-agent", create: true, mount_options: ["dmode=775, fmode=664"]
```

The create option will create the directory "dd-agent" in the project directory, and the mounnt_options are set to enable the Datadog Agent to write logs to the directory within the vm (NOTE: it is not advisable to give global write priveleges in general, but in the case of running dev on my laptop I think we're pretty ok).  
