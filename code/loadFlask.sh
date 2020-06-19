#!/bin/bash

# Quick test workload against flask to demo APM tracing
# .$delay is random delay between 0 and 1.0 seconds

count="1"
loop="1000"

while [ $count -le $loop ]; do
	#echo $count
	let "count+=1"
	delay=$(( ( RANDOM % 10 )  + 0 ))
	echo $delay
	sleep .$delay
	curl http://0.0.0.0:5050/
done



