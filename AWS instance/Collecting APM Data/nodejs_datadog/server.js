// server.js
// where your node app starts

// init project
require('dotenv').load();
const tracer = require('dd-trace').init();
const opentracing = require('opentracing');
const span = tracer.startSpan('web.request');
const scope = tracer.scopeManager().activate(span)
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var metrics = require('datadog-metrics');
var metricsLogger = new metrics.BufferedMetricsLogger({
    apiKey: '6fd01ef9774f7bb0fcfccc5cd4fdfd64',
    host: 'datadogapm-app-glitch',
    prefix: 'gltich.datadogapm-app',
    flushIntervalSeconds: 15,
    defaultTags: ['env:dev']
});
metricsLogger.gauge('nodejs_gauge', 42);
opentracing.initGlobalTracer(tracer);

app.use(bodyParser.urlencoded({ extended: true }));


function collectMemoryStats() {
    var memUsage = process.memoryUsage();
    metrics.gauge('memory.rss', memUsage.rss);
    metrics.gauge('memory.heapTotal', memUsage.heapTotal);
    metrics.gauge('memory.heapUsed', memUsage.heapUsed);
    metrics.increment('memory.statsReported');
}

setInterval(collectMemoryStats, 5000);

// we've started you off with Express, 
// but feel free to use whatever libs or frameworks you'd like through `package.json`.

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// init sqlite db
var fs = require('fs');
var dbFile = './sqlite.db';
var exists = fs.existsSync(dbFile);
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(dbFile);

// if ./.data/sqlite.db does not exist, create it, otherwise print records to console
db.serialize(function(){
  if (!exists) {
    db.run('CREATE TABLE Dreams (dream TEXT)');
    console.log('New table Dreams created!');
    
    // insert default dreams
    db.serialize(function() {
      db.run('INSERT INTO Dreams (dream) VALUES ("Find and count some sheep"), ("Climb a really tall mountain"), ("Wash the dishes")');
    });
  }
  else {
    console.log('Database "Dreams" ready to go!');
    db.each('SELECT * from Dreams', function(err, row) {
      if ( row ) {
        console.log('record:', row);
      }
    });
  }
});

// http://expressjs.com/en/starter/basic-routing.html
app.get('/', function(request, response) {
  const scope = tracer.scopeManager().active(); // the scope activated earlier
    const span = scope.span(); // the span wrapped by the scope

    
    
  span.setTag('apm_root', 'root');
  span.finish();
  scope.close();
  response.sendFile(__dirname + '/views/index.html');
});

// endpoint to get all the dreams in the database
// currently this is the only endpoint, ie. adding dreams won't update the database
// read the sqlite3 module docs and try to add your own! https://www.npmjs.com/package/sqlite3
app.get('/getDreams', function(request, response) {
  const scope = tracer.scopeManager().active(); // the scope activated earlier
    const span = scope.span(); // the span wrapped by the scope
 
  span.setTag('apm_getDreams', 'GETDREAMS');
  span.finish();
  scope.close();
  db.all('SELECT * from Dreams', function(err, rows) {
    response.send(JSON.stringify(rows));
  });
});

// listen for requests :)
var listener = app.listen(process.env.PORT, function() {
  console.log('Your app is listening on port ' + listener.address().port);
});
