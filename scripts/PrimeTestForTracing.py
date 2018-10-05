from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def prime_num():
	num = random.randint(1,100000)

	# prime numbers are greater than 1
	if num > 1:
	   # check for factors
	   for i in range(2,num):
		   if (num % i) == 0:
			   output = "Random number %d is not a prime number." % num
			   break
	   else:
		   output = "Random number %d is a prime number." % num

	# if input number is less than
	# or equal to 1, it is not prime
	else:
	   output = "Random number %d is not a prime number." % num

	return output

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5100')

