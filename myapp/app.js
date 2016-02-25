var express = require('express');  
var path = require('path');  
var app = express();  
var router = express.Router();
var cons = require('consolidate');

// view engine setup
app.engine('html', cons.swig)
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'html');
app.use(router); 
 
// Data dog Node js 
var metrics = require('datadog-metrics');
metrics.init({ host: 'localhost', prefix: 'app.', tags: 'support' });

//Homepage route -chat app
app.get('/', function (req, res) { 
  	var start_time = Date.now();
   	res.render('chatapp');
   	var duration = Date.now() - start_time;
  	metrics.increment('web.page_views', 1 ,['page:home', 'support']);
  	metrics.histogram('web.latency.time', duration,['page:home', 'support']);
});

//Page 1 Tetris
app.get('/page1', function (req, res) {
 
  	var start_time = Date.now();
   	res.render('tetris');
   	var duration = Date.now() - start_time;
  	metrics.increment('web.page_views', 1 ,['page:page1', 'support']);
  	metrics.histogram('web.latency.time', duration,['page:page1', 'support']);
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
module.exports = app;

//Collect memory stats of app
function collectMemoryStats() {
    var memUsage = process.memoryUsage();
    metrics.gauge('memory.rss', memUsage.rss);
    metrics.gauge('memory.heapTotal', memUsage.heapTotal);
    metrics.gauge('memory.heapUsed', memUsage.heapUsed);
    metrics.increment('memory.statsReported');
}

setInterval(collectMemoryStats, 5000);