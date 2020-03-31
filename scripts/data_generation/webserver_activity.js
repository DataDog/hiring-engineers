const request = require('request');

function hitIndex(){
	request('http://3.21.236.69/', (err, res, body) => {
	  if (err) { return console.log(err); }
	  console.log("query to '/'")
	});	
}

function hitApiApm(){
	request('http://3.21.236.69/api/apm', (err, res, body) => {
	  if (err) { return console.log(err); }
	  console.log("query to '/api/apm'")
	});	
}

function hitApiTrace(){
	request('http://3.21.236.69/api/trace', (err, res, body) => {
	  if (err) { return console.log(err); }
	  console.log("query to '/api/trace'")
	});	
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function recursiveLoop() {
	random_int = getRandomInt(3)
	if (random_int == 0) {
		hitIndex()
	} else if (random_int == 1) {
		hitApiApm()
	} else {
		hitApiTrace()
	}
	setTimeout(recursiveLoop, 3000);
}

recursiveLoop()