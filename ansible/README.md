# demo

## Local Setup

* Create a new Python virtual environment `virtualenv env`
* Activate the virtualenv and install the requirements `source env/bin/activate; pip install -r requirements.txt`
* Download the Ansible Galaxy roles `ansible-galaxy install -r requirements.yml`

## Testing Ansible
* Use Ansible to test connectivity
`$ ansible -i inventories/production/hosts.ini demo -m ping`


## Deploy All The Things

To deploy to all known servers:

`./scripts/deploy`

To deploy to a set of servers:

`./scripts/deploy --limit <inventory_group>`

To deploy to a set of servers using tags:

`./scripts/deploy --limit <inventory_group> --tags "some,tags,go,here"`
