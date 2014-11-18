import web
from statsd import statsd
import time

import random

render = web.template.render('templates/')

urls = ( '/index/(.*)' , 'index',
		 '/page1/(.*)', 'page1',
		 '/page2/(.*)', 'page1'
       )

db = web.database(dbn='mysql', user='root', pw='', db='mysql')

class index:
	def GET(self, name):
		start_time = time.time()
		users = db.select('user')
		duration = time.time() - start_time
		statsd.histogram('database.query.time', duration, tags = ["support"])
		statsd.increment('page.views', tags = ["support", "page:index"])
		return render.index(users[3])
		#return render.index(name)

class page1:
	def GET(self, name):
		randomNum = random.random()
		start_time = time.time()
		statsd.increment('page.views', tags = ["support", "page:page1"])
		statsd.histogram('test.support.random', random.random())
		return render.page1(randomNum)
		duration = time.time() - start_time
		statsd.histogram('database.query.time.avg', duration, tags = ["support"])


		


		


if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()