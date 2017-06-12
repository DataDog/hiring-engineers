import subprocess
import time

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        # set up logging and Log what we're doing
        myLogger = self.log
        myLogger.info("NewGenerateDBLoad.py has started and is running.")

        # Retrieve configuration from the instance parameters
        userName = instance.get('userName', 'root')
        userPassword = instance.get('userPassword', 'Chestnut1999')
        iterations = instance.get('iterations', 5)
        concurrentUsers = instance.get('concurrentUsers', 100)

	logFormatString='running user is {0}, Iterations is {1}, concurrentUsers is {2}'
	myLogger.info(logFormatString.format(userName, iterations, concurrentUsers))
    	
	# Build the command-line that will be called.
        commandline = ['mysqlslap', 
                       '-u', userName, 
                       '-p'+userPassword, 
                       '--auto-generate-sql', 
                       '--iterations='+str(iterations), 
                       '--concurrency='+str(concurrentUsers) ]

        # Start conting time, run the command then find out how long it took
        start_time = time.time()
    	subprocess.check_output(commandline) 
        end_time = time.time()
        timing = end_time - start_time

	# Record that this ran and how long it took.
        self.gauge('newloadgeneration.mysql.done', 1)
        self.gauge('newloadgeneration.mysql.time', timing)
        self.gauge('newloadgeneration.mysql.loops', (iterations*concurrentUsers))
        myLogger.info("NewGenerateDBLoad has completed and is exiting.")
