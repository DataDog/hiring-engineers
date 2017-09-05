# Make file to drive Datadog Docker demo
# Mark targets that are not for general users with a single octothorpe

build:  ## Builds the demo containers 
	@echo "Building demo containers"
	docker-compose build

change_sql_creds: # Just a necessary evil for update_sql_creds target so we can build after.  Otherwise the new creds don't get baked into new containers
	@echo "Updating up MySQL creds"
	sh ./set_pass.sh

git_ready: ## Strip credentails from repo so you can git safely
	@echo "Sanitizing mysql container"
	sed -i "/MYSQL_ROOT_PASSWORD=/c\MYSQL_ROOT_PASSWORD=" ./mysql/.env 
	sed -i "/MYSQL_PASSWORD=/c\MYSQL_PASSWORD=" ./mysql/.env 
	@echo "\nSanitizing datadog container"
	sed -i "/pass:/c\    pass:" ./datadog/conf.d/mysql.yaml

help:   ## Datadog Docker Demo Help
	@echo "Datadog Docker Demo"
	@echo "To just get to the demo run this command --> make it_just_work"
	@echo "Make Targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: set_dd_api_key update_mysql_creds build ## Initalize Demo environment

it_just_work: init start ## For when you don't care and just want it work

purge:  # Scorch the earth with docker system prune.  
	@echo "Read the command above and warning below carefully!" 
	docker system prune

set_dd_api_key: ## Set a new Datadog API Key
	@read -p "Enter new Datadog API key: " dd_key; \
	echo "API_KEY=$$dd_key" > ./datadog/.dontcommit.env ; \

start:  ## Start the demo
	@echo "Starting demo"
	docker-compose up

stop:   ## Stop the demo
	@echo "Stopping demo"
	docker-compose down

update_mysql_creds: change_sql_creds build ## Change all mysql creds and rebuild containers

.DEFAULT_GOAL := help
.PHONY: help
