from datadog import initialize, api
import datetime
from subprocess import call


#JMeter Configuration
JMETER_HOME='/Users/michael.redman/Dropbox/AppDynamics/Development/JMeter/apache-jmeter-2.13JP1.3.1WD'
SCRIPT='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/load.jmx'
RESULTS='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/jmeter-results.jtl'
LOG='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/jmeter-log.log'

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

def post_event(t,m):
	initialize(**options)

	title = t
	text = m
	tags = ['version:1', 'application:web']

	api.Event.create(title=title, text=text, tags=tags)

def run_automation():
	start_event_name = 'perf_run_start: ' +  str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
	post_event(start_event_name, 'starting load.jmx')
	call([JMETER_HOME + "/bin/jmeter", "-n", "-t", SCRIPT, "-l", RESULTS, "-j", LOG])
	end_event_name = 'perf_run_end: ' +  str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
	post_event(end_event_name, 'end load.jmx')

# If you are programmatically adding a comment to this new event
# you might want to insert a pause of .5 - 1 second to allow the
# event to be available.

run_automation()
