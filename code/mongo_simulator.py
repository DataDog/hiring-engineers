import pymongo
import time
import randint

conneciton = MongoClient('localhost', 27017)

db = connection.test

names = db.names

run_time_hours = 8
interval_minutes = 1
sleep_seconds = interval_minutes * 60
loops = run_time_hours*run_time_hours

index = 0

while index < loops:
	print ' '
	reads = randint(20, 76)

	i = 0
	while i < reads:
		name = names.find_one();
		i += 1
	
	print 'got %s names' % reads

	

	writes = randint(0, 100)

	while j < writes:

		name_number = randint(0,100000)

		name_object = {'first':'Josh',
						'last': 'Brown',
						'number':randint}
		names.insert_one(name_object)

		j += 1

	print 'wrote %s name objects'

	index += 1

	print ' on loop %s of %s' %(index, loops)
	print '  '

	time.sleep(sleep_seconds)

