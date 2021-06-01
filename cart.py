from random import randint
import socket
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class CartCheck(AgentCheck):
    def check(self, instance):
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print("Hostname :  ",host_name)
            print("IP : ",host_ip)
            tag = ['ip:' + host_ip];
        except:
            print("Unable to get Hostname and IP")
            tag = []
        self.count('cart.dollar_total', randint(20, 200), tags=tag + self.instance.get('tags', ['metric_submission_type:count']))
