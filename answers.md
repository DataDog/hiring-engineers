## Tiffany Monroe
Solutions Engineer Applicant

## Prerequisites - Setting up the environment

Used MacBook Pro OS High Sierra 10.13.4

### Github Setup

Forked Datadog Hiring Engineers Repository (https://github.com/DataDog/hiring-engineers/)

Cloned on local computer: ```git clone https://github.com/tiffanymonroe/hiring-engineers.git```

Changed directories: ```cd hiring-engineers```

Created new branch to work on: ```git checkout -b Tiffany_Monroe_Solutions_Engineer_Revised```

Used Atom to edit text in answers.md.

Checked Github:
```
git add .
git commit -m "new branch"
git push origin Tiffany_Monroe_Solutions_Engineer_Revised
```

Github worked.

### Vagrant Setup

Used instructions from
Downloaded [VirtualBox 5.2.18](https://www.virtualbox.org/wiki/Downloads) platform packages for OS X.

Installation failed: "System software from Oracle America, Inc. was blocked from loading."

Went to System Preferences to "allow" software to load, installation successful.

Downloaded and installed [Vagrant 2.1.5](https://www.vagrantup.com/downloads.html) 64-bit for OS X.

```
vagrant init hashicorp/precise64
vagrant up
```

<img src="img/0/vagrant_init.png"/>

<img src="img/0/vagrant_up.png"/>

Reviewed instructions, added SSH: ```vagrant ssh```

<img src="img/0/vagrant_ssh.png"/>

### Datadog Setup

Went to Datadog [website](https://datadoghq.com/), signed up for a free trial, put "Datadog Recruiting Candidate" in "Company" field, skipped the "Tell us about your stack" option.

Installed the [Agent](https://app.datadoghq.com/signup/agent) for OS X by typing provided code in Command Line: ```DD_API_KEY=ecbbdce5a2bc9bb8dc9145af1e490e3a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"
```

<img src="img/0/agent_installed.png"/>
