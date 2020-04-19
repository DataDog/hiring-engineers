Using Ansible
===============

From:
 https://docs.ansible.com/ansible/latest/modules/datadog_monitor_module.html
``ansible-galaxy init roles/zero2datadog`` produces a directory structure like this::
	roles
	└── zero2datadog
		├── README.md
		├── defaults
		│   └── main.yml
		├── files
		├── handlers
		│   └── main.yml
		├── meta
		│   └── main.yml
		├── tasks
		│   └── main.yml
		├── templates
		├── tests
		│   ├── inventory
		│   └── test.yml
		└── vars
			└── main.yml

# Create a metric monitor
- datadog_monitor:
    type: "metric alert"
    name: "Test monitor"
    state: "present"
    query: "datadog.agent.up.over('host:host1').last(2).count_by_status()"
    message: "Host [[host.name]] with IP [[host.ip]] is failing to report to datadog."
    api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
    app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

# Deletes a monitor
- datadog_monitor:
    name: "Test monitor"
    state: "absent"
    api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
    app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

# Mutes a monitor
- datadog_monitor:
    name: "Test monitor"
    state: "mute"
    silenced: '{"*":None}'
    api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
    app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

# Unmutes a monitor
- datadog_monitor:
    name: "Test monitor"
    state: "unmute"
    api_key: "9775a026f1ca7d1c6c5af9d94d9595a4"
    app_key: "87ce4a24b5553d2e482ea8a8500e71b8ad4554ff"

