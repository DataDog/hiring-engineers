import subprocess

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
    	subprocess.check_output(['mysqlslap', '-u', 'root', '-pChestnut1999', '--auto-generate-sql', '--iterations=10', '--concurrency=100']) 
        self.gauge('loadgeneration.mysql.done', 1)
