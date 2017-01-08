from random import choice
from time import sleep
from sense_hat import SenseHat
from datadog import initialize, statsd, api
import random
import web
from sys import argv

urls = (
    '/page1','pageOne',
    '/page2','pageTwo',
    '/page3','pageThree'
    )

support = 'support'
sense = SenseHat()


@statsd.timed('app.function_gettemp_time',tags=[support])
def get_temp():
    temp = sense.get_temperature() *9/5+32
    print("The temperature is "+str(temp))
    statsd.gauge('system.cpu_temp', temp)

class pageOne:
    @statsd.timed('app.function_web_request',tags=[support,"page:page1"])
    def GET(self):
        statsd.increment('app.page_views',tags=[support])
        get_temp()
        return "Page One"
    
class pageTwo:
    @statsd.timed('app.function_web_request',tags=[support,"page:page2"])
    def GET(self):
        statsd.increment('app.page_views',tags=[support])
        get_temp()
        return "Page Two"
    
class pageThree:
    @statsd.timed('app.function_web_request',tags=[support,"page:page3"])
    def GET(self):
        statsd.increment('app.page_views',tags=[support])
        get_temp()
        return "Page Three"
    
options = {
    'api_key':'1f0b70922dd3da30a39f5df10273f5fd',
    'app_key':'fddd6092b7130644b0149260ebbfcebf44a06683'
    }


initialize(**options)

if __name__ == '__main__':
    api.Event.create(title="A farce", text='A funny thing happened on the way to the forum1',priority='normal',tags=[support])
    
    app = web.application(urls, globals())
    app.run()


    



