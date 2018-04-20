from ddtrace import tracer
import time
import threading
import random

@tracer.wrap(service='playgame')
def playGame():
	print("\nWould you like to play a game?")

@tracer.wrap(service='joke')	
def joke():
	print("\nJust kidding! We will let the computer play the game today!")
	
	
def areYouready():
	_ready = input("Are you ready to play?")
	return _ready.lower()

def timer(num):
	time.sleep(num)

@tracer.wrap(service='selectNumber')	
def selectNum():
	timer(random.randint(random.randint(1,20),random.randint(21,61)))
	return random.randint(1,100001)

@tracer.wrap(service='guessNumber')
def guessNumber():
	print("Guessing Number....")
	_numB = selectNum()
	print("\nIs the number " + str(_numB) + "?")
	return _numB
		

	

print ("Hello...")
playGame()
timer(random.randint(1,4))
joke()
print("\nWe are going to let the computer pick a random number between 1 and 100,000.\nThen it will continue to pick random numbers until it selects the same number")

print("\nSelecting number....")
numA = selectNum()

print("Ok! We have our number!\n")

numB = guessNumber()

while numB != numA:
	numB = guessNumber()
	if numB != numA:
		print ("\nNope! Guess again!\n")
print("\nYes! It is" + str(numA) + "!")	



		
	



	
	


	
	

