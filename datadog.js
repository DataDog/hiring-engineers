#!/usr/bin/env node
var b = require('bonescript');
const https = require('https');
const os = require('os');

const METRIC_INTERVAL = 300000;

const inputPin1 = "P9_36";
const inputPin2 = "P9_38";

const VDD_ADC = 1.8



function sendMetrics(temp, light ) {

  var timestamp = Math.floor(new Date() / 1000);

  var metric_data = {
    series: [
      {
        host: os.hostname(),
        metric: 'env.temp',
        points: [
          [
            timestamp,
            temp
          ]
        ],
        tags: 'source:beaglebone,field',
        type: 'gauge'
      },
      {
        host: os.hostname(),
        metric: 'env.light',
        points: [
          [
            timestamp,
            light
          ]
        ],
        tags: 'source:beaglebone,field',
        type: 'gauge'
      }
    ]
  };


  var post_body = JSON.stringify(metric_data);
  var data = post_body;

  const options = {
    hostname: 'api.datadoghq.com',
    port: 443,
    path: '/api/v1/series?api_key=<KEY>',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length,
    }
  }


  const req = https.request(options, (res) => {
    console.log(`statusCode: ${res.statusCode}`)

    res.on('data', (d) => {
      process.stdout.write(d)
    })
  })

  req.on('error', (error) => {
    console.error(error)
  })

  req.write(data)
  req.end()


  console.log(post_body)
}


//in degrees celsius
function voltsToTemp(volts)
{
    var temp = 117.460*volts - 122.628;
    return temp;
}

//not really lux because I don't have a calibrator, but same order of magnitude
function voltsToLux(volts)
{
    var lux = Math.log10(volts);
    lux *= 10000;
    return lux;
}

loop();

function loop() {

    //Per best practice always sink current so subtract from ADC reference source
    var value1 = VDD_ADC - b.analogRead(inputPin1);
    var value2 = VDD_ADC - b.analogRead(inputPin2);

    console.log("pin 36 volts "+  value1);
    console.log("pin 38 volts "+  value2);

    var temp = voltsToTemp(value2);

    console.log("Temp: " + temp);

    var lux = voltsToLux(value1);
    console.log("Lux: " + lux);

    var temp_int = Math.round(temp);
    var light_int = Math.round(lux);


    sendMetrics(temp_int, light_int);



    setTimeout(loop, METRIC_INTERVAL);
}


