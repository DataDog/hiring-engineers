const dogapi = require("dogapi");
const secrets = require("./secrets");

//this package has a few advantages over the one in the Datadog docs:
//1. it's published so can be installed from the command line with npm
//2. it has much more functionality
//3. it has a command line interface itself!
//it can be found at https://www.npmjs.com/package/dogapi

//secrets.js is in .gitignore so that my api/app keys aren't exposed on github
const options = {
	api_key: secrets.apiKey,
	app_key: secrets.appKey
}

dogapi.initialize(options);

dogapi.event.create("FitMix is crashing!", "Oh no! FitMix is crashing! Do something!", { alert_type: "error" }, 
	function(err, res){
		if(err) console.dir(err);
		else console.dir(res);
	}
);