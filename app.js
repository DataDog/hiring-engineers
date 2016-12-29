const dogapi = require("dogapi");
const secrets = require("./secrets");

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