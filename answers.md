Your answers to the questions go here.

CANDIDATE

Paulo Monteiro (ThyWoof)


BONUS QUESTIONS

1. What is an agent?

	An agent is a software daemon that gathers system and application metrics from hosts and sends them to a data collector for further analysis, trending, alerting, troubleshooting, etc.

2. What is the difference between a timeboard and a screenboard?

	Timeboards are used for troubleshooting and correlation where all graphs are always scoped to the same time. Timeboards also use an automatic layout.

	Screenboards allow mix widgets and timeframes as well as a custom drag-and-drop layout.


STEP-BY-STEP

1. Installed vagrant

	# removed embedded curl in vagrant bin directory as it fails to bind curl dylib in Mac OS X Sierra

2. Installed virtualbox

3. Deployed 3 Ubuntu hosts with vagrant

	cd ~/Vagrant/ubuntu1
	vagrant init hashicorp/precise64

	# set hostname in Vagrantfile with config.vm.hostname = "ubuntu1"
	# disabled default forwarded port with config.vm.network :forwarded_port, guest: 22, host: 2222, id: "ssh", disabled: true
	# set forwarded port to 2201 with config.vm.network :forwarded_port, guest: 2201, host: 22

	vagrant up

	cd ~/Vagrant/ubuntu2
	vagrant init hashicorp/precise64

	# set hostname in Vagrantfile with config.vm.hostname = "ubuntu2"
	# disabled default forwarded port with config.vm.network :forwarded_port, guest: 22, host: 2222, id: "ssh", disabled: true
	# set forwarded port to 2202 with config.vm.network :forwarded_port, guest: 2202, host: 22

	vagrant up

	cd ~/Vagrant/ubuntu3
	vagrant init hashicorp/precise64

	# set hostname in Vagrantfile with config.vm.hostname = "ubuntu3"
	# disabled default forwarded port with config.vm.network :forwarded_port, guest: 22, host: 2222, id: "ssh", disabled: true
	# set forwarded port to 2203 with config.vm.network :forwarded_port, guest: 2203, host: 22

	vagrant up

4. Installed DD agent (without default startup) on 3 Ubuntu hosts

	vagrant ssh
	sudo apt-get update
	sudo apt-get install curl
	DD_INSTALL_ONLY=true DD_API_KEY=de8da8514bf762cc4e493241d222c783 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

5. Configured DD agent on 3 Ubuntu hosts

	sudo vi /etc/dd-agent/datadog.conf

	5.1. Added following tags on ubuntu1 host

	tags: env:prod, role:database, datacenter:san_diego, service:mysql

	5.2. Added following tags on ubuntu2 host

	tags: env:prod, role:database, datacenter:boston, service:mongodb

	5.3. Added following tags on ubuntu3 host

	tags: env:prod, role:database, datacenter:new_york, service:postgresql

6. Started DD agent on 3 Ubuntu hosts

	sudo service datadog-agent start

7. Installed mysql on ubuntu1 / Configure DD mysql.yaml

	sudo apt-get install mysql-server

	sudo mysql
	CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'IbkM06RPObbMCvXTOdGELdFi';
	GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
	GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
	GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

	sudo /etc/init.d/datadog-agent restart
	sudo /etc/init.d/datadog-agent info

8. Installed mongodb on ubuntu2

	sudo apt-get install mongodb

	mongo
	use admin
	db.auth("admin", "admin-password")
	db.addUser("datadog", "bxniIBNxFOgaktJ4lRKzfGNG", true)

	sudo /etc/init.d/datadog-agent restart
	sudo /etc/init.d/datadog-agent info

9. Installed postgresql on ubuntu3

	sudo apt-get install postgresql

	sudo -u postgres psql postgres
	create user datadog with password 'EFRmwHx6FVGh3CDOjJcZ9Dnt';
	grant SELECT ON pg_stat_database to datadog;

	sudo /etc/init.d/datadog-agent restart
	sudo /etc/init.d/datadog-agent info

10. Write a custom agent check on ubuntu1

	test.py

	import random
	from checks import AgentCheck
	class HelloCheck(AgentCheck):
	    def check(self, instance):
        	self.gauge('test.support.random', random.random())

	check.yaml

	init_config:

	instances:
		[{}]

11. Created a snapshot with a box showing the spike. Unfortunately never got an email on this one. Reached out to Stephen at support, he confirmed I did it right, and is now checking DD logs why my email never got sent.

	# In fact Stephen and I found the issue here, and I asked him to file a bug. Somehow DD is not sending emails on snapshots if the email has a + sign. (Full support comm. at the end of this file)

12. Created a new Dashboard as a clone of "MySQL Dashboard". Added a widget with test.support.random

13. Created a monitor on my test metric

14. Setup a downtime. Did a different time frame otherwise DD will fill up my mailbox pretty quickly ;-)

---

Ticket with Stephen

Location: USA (Carlsbad, CA)
Referred from: https://app.datadoghq.com/event/stream?tags_execution=and&show_private=true&per_page=30&aggregate_up=true&use_date_happened=false&display_timeline=true&from_ts=1478271600000&priority=normal&is_zoomed=false&status=all&to_ts=1478876400000&is_auto=false&incident=true&only_discussed=false&no_user=false&page=0&live=true&bucket_size=10800000
On page: https://app.datadoghq.com/account/team
IP address: 76.176.112.211
Talked with: stephen

USA (Carlsbad, CA) #4661
10:11 AM | Morning Support. I'm going through the new Hiring Training Exercise. It is going pretty well but the one thing that didn't work for me was when I created a snapshot using the @notification syntax. I never got an email for this particular snapshot.
10:12 AM | All other @notification I'm using (i.e: monitors, downtime) are correctly sending me emails.

stephen
10:12 AM | hey there Paolo, thanks for reaching out!
10:13 AM | that sounds odd. can you paste in the content of your comment?

USA (Carlsbad, CA) #7256
10:13 AM | You can check under my events list, about 9 hours ago, the snapshot I created with a box showing the spike on test.support.random.metric. I created the snapshot with this comment "@pauloesquilo+dd@gmail.com, it looks like our random is above 0.9 here".

stephen
10:16 AM | yeah, that looks about right. no luck in your spam folders?

USA (Carlsbad, CA) #5891
10:16 AM | nope. All other emails are coming in.
10:17 AM | Got downtime notification, alerts on my monitor, etc.

stephen
10:20 AM | bummer. i'll take a quick look at your email pref settings--maybe there's something that got set weird. just a second

pauloesquilo+dd@gmail.com | USA (Carlsbad, CA) #2161
10:20 AM | Thanks.
10:21 AM | I also have a 2nd question? I forked the repository on GitHub but not sure where I should pull my changes to answers.md: my forked one or DD repository.

stephen
10:28 AM | thanks for your patience here--i've verified that your email settings won't have gotten in the way of that comment communication. next thing for me to do there is to check through the email logs to make sure it got sent
10:29 AM | that'll take me a bit more time, but in the meantime for your second question
10:30 AM | when everything's all done and you're happy with your work, etc. you'll want to pull it to the DD repo

USA (Carlsbad, CA) #1114
10:32 AM | Cool. Will do today.

stephen
10:32 AM | awesome! still looking up those email logs

USA (Carlsbad, CA) #1114
10:33 AM | It isn't a big deal as at least from a test perspective I believe correctly did the annotation.
10:33 AM | "I believe I correctly..."

stephen
10:38 AM | yeah, that does look right. It'd at least be worth screenshotting what you did there and adding that you reached out to us on support to better understand why that notification didn't trigger.
10:48 AM | hmm, ok, so I can't seem to find it in our send-confirmation logs. checking some others now

USA (Carlsbad, CA) #1114
10:49 AM | Stephen, it isn't not a big deal at my end as I took a screenshot of the event list. Anyways it should have happened so I guess you wanna dive further as it might be happening to other customers.
10:50 AM | I like to use Gmail alias so not sure if the fact my email is pauloesquilo+DD@gmail.com might be causing it.
10:50 AM | I'll try a new one with my main email pauloesquilo@gmail.com and check what happens

stephen
10:50 AM | sounds like a good thought
10:51 AM | i tested it out on my end just now, but with no "+" sign, and it works fine for me

USA (Carlsbad, CA) #1114
10:52 AM | just did it. I'll wait a few and check both my inbox and spam folders
10:52 AM | Aha
10:52 AM | It works now. Can you please file a bug?
10:53 AM | Somehow it isn't correctly parsing the @notification if email has a + sign.
10:54 AM | I'm all cool now. Got the email, and took a screenshot.

stephen
10:55 AM | weird! that should def'ly not be happening, i'll try to reproduce on my end and see if we can dig a bit deeper on that
10:56 AM | thanks for bringing this up today--anything else i can help with in the meantime?

USA (Carlsbad, CA) #5607
10:58 AM | I'm ok. Please close this ticket.
10:58 AM | Hopefully I can meet you in person soon.

stephen
10:58 AM | will do. good work getting the notification working there in the end
10:58 AM | hopefully! looking forward to that!
10:58 AM | take care now!

USA (Carlsbad, CA) #5607
10:58 AM | Are you in Boston or NY?

stephen
10:59 AM | NYC

USA (Carlsbad, CA) #5607
10:59 AM | perfect. That's my next step with Dustin.
10:59 AM | visit NY HQ

stephen
11:00 AM | the big majority of the support team's in nyc. nice! good luck with all of it
