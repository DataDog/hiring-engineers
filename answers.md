### Prerequisites - Setup The Environment

###### GitHub
Fork the [repository](https://github.com/DataDog/hiring-engineers/tree/solutions-engineer) and clone [the fork](https://github.com/cwithac/hiring-engineers/tree/solutions-engineer) into my local environment, checking out _solutions-engineers_ and building branch "Cathleen_Wright_Solutions_Engineer" for unique access to the directory and _answers.md_ in the text editor [Atom](https://atom.io/).  

```shell
  $ git clone git@github.com:cwithac/hiring-engineers.git
  $ cd hiring-engineers
  $ git checkout solutions-engineer
  $ git checkout -b "Cathleen_Wright_Solutions_Engineer"
  $ atom .
```

###### Vagrant

Download and install [VirtualBox 5.2](https://www.virtualbox.org/), 5.2.16 platform packages for OS X hosts.  Download and install the [latest version of Vagrant](https://www.vagrantup.com/downloads.html) for macOS, 64-bit.  Initialize, activate and SSH into the virtual machine.  

```shell
  $ vagrant init hashicorp/precise64
  $ vagrant up
  $ vagrant ssh
```

_Welcome to your Vagrant-built virtual machine._

###### Datadog and Agent Reporting Metrics

Get Started with Datadog using Datadog Recruiting Candidate as the Company.  [Follow the instructions to install your first Datadog Agent for Ubuntu](https://i.imgur.com/nG4CXDv.png).  

```shell
The program 'curl' is currently not installed.  You can install it by typing:
$ sudo apt-get install curl

$ DD_API_KEY=c802ac74556f263f47de0d8cddd8131a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

[Agent is running and functioning properly](https://i.imgur.com/9cU6eQg.png).  Your first Datadog Agent is reporting.

[Initial Dashboard](https://i.imgur.com/YVjtSIO.png)

<hr>
### Candidate Information
Solutions Engineer Hiring Challenge - Cathleen Wright
- [LinkedIn](https://www.linkedin.com/in/cathleenmwright/)
- [GitHub](https://github.com/cwithac)
