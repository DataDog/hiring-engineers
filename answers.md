# Level 1
* Sign up for Datadog: done!
* Bonus question: what is the agent?
  * The agent is software that runs on your hosts, and collects events and metrics. It then delivers this data to Datadog so that you can use the information for performance and monitoring.
  * It's made up of three parts:
    1. the collector: this monitors your current machine for installed integrations, and tracks your system metrics (such as CPU and memory).
    2. dogstatsd: this is a StatsD backend server which you can use to send custom metrics from an application.
    3. the forwarder: this fetches the data from #'s 1 and 2, and then prepares said data for transfer to Datadog.
  * (P.S. I don't want to be *that* guy, but I noticed a typo in the first line under the first heading [here](http://docs.datadoghq.com/guides/basic_agent_usage/): "a" is missing before "piece of software".)
* Submit an event via the API:
  * I instrumented code for a MEAN stack app called [Loci](https://github.com/kwwalter/MemoryPalace), using the dogapi npm package):

  ```javascript
  var dogapi = require('dogapi');

  // dogapi configuration
  var options = {
    api_key: process.env.DD_API_KEY,
    app_key: process.env.DD_APP_KEY
  };

  dogapi.initialize(options);

  // dummy event submission via API

  var title = "It works!",
      text  = "Loci app successfully accessed through Heroku!",
      properties = {
        priority: "low",
        tags: ["loci", "heroku"],
        alert_type: "info"
      };

  dogapi.event.create(title, text, properties, function(err, res){
    if (err) {
      console.log("error posting dummy event to dogapi: ", err);
    } else {
      console.log("here's the response: ", res);
    }
  });
  ```

* Get an event to appear in your email inbox:
  ![event-email](screenshots/dd-email-alert.png)

# Level 2
* Instrument a web app with dogstatsd (used a different app, [Collaboetry](https://github.com/kwwalter/Collaboetry), as well as the node-dogstatsd npm package):

  ```javascript
  var StatsD = require('node-dogstatsd').StatsD;

  // node-dogstatsd setup
  var dogstatsd = new StatsD();

  // increment
  router.get('/login', function(req, res){
    dogstatsd.increment('collaboetry.page_views');
    res.render('users/login');
  });
  ```

* While running a load test for a few minutes, visualize page views per second. Send a link to the graph.
  * Note: instead of using ab or tsung, I used an npm package called loadtest.
  * With loadtest, using this: `loadtest -c 100 -n 10000 http://localhost:3788/users/login`, and I executed the test a few times.
  * The last test I ran completed the 10000 requests in 46.79s, with the longest request taking 1123ms.
  ![load-test](screenshots/dd-page-views-per-second.png)
  * [Link to the graph](https://app.datadoghq.com/metric/explorer?live=false&page=0&is_auto=false&from_ts=1452531330055&to_ts=1452531938344&tile_size=l&exp_metric=collaboetry.page_views&exp_scope=&exp_agg=avg&exp_row_type=metric&exp_calc_as_rate=true)

* Create a histogram to see the latency; also give us the link to the graph
  * I did a couple of tests here:
    1. Load one poem/post: `collaboetry-1poem.latency`
      ```javascript
        router.get('/authors/:authorID/:poemID', function(req, res) {
          var start = Date.now();

          if (res.locals.userLoggedIn) {
            Poem.findOne( {
              _id: req.params.poemID
            }, function(err, foundPoem) {
              if (err) {
                console.log("Error finding individual poem with id: ", req.params.poemID);
              } else {
                console.log("found poem is: ", foundPoem);
                var latency = Date.now() - start;
                dogstatsd.histogram('collaboetry-1poem.latency', latency);
                dogstatsd.increment('collaboetry.page_views');

                res.render('poems/show', {
                  poem: foundPoem,
                  currentUser: req.session.currentUser
                });
              }
            });
          } else {
            res.redirect(302, '/');
          }
        });
      ```
      * [Link to the collaboetry-1poem graph](https://app.datadoghq.com/dash/integration/custom%3Acollaboetry_1poem?live=true&page=0&is_auto=false&from_ts=1452528204714&to_ts=1452531804714&tile_size=m)
    2. And a simpler example, for accessing and rendering the login page (in keeping with what I did for the load test): `collaboetry-login.latency`
      ```javascript
      router.get('/login', function(req, res){
        var start = Date.now();

        var latency = Date.now() - start;
        dogstatsd.histogram('collaboetry-login.latency', latency);
        dogstatsd.increment('collaboetry.page_views');

        res.render('users/login');
      });
      ```
      * [Link to the collaboetry-login graph](https://app.datadoghq.com/dash/integration/custom%3Acollaboetry_login?live=true&page=0&is_auto=false&from_ts=1452528176353&to_ts=1452531776353&tile_size=m)
* [Here's a dashboard I put together](https://app.datadoghq.com/dash/90969/collaboetry-latency--views?live=true&page=0&is_auto=false&from_ts=1452529467468&to_ts=1452533067468&tile_size=m)

# Level 3
* tag your metrics with `support` (one tag for all metrics). Building on the same example from Level 2, I've added the `support` tag to both `collaboetry-login.latency` and `collaboetry.page_views`, as well as `collaboetry-1poem.page_views`:
  ```javascript
  router.get('/login', function(req, res){
    var start = Date.now();

    var latency = Date.now() - start;
    dogstatsd.histogram('collaboetry-login.latency', latency, ['support']);
    dogstatsd.increment('collaboetry.page_views', ['support']);

    res.render('users/login');
  });
  ```
* tag your metrics per page
  * I went through and added page-specific metrics throughout my app, with tags such as:

  ```javascript
  dogstatsd.increment('collaboetry.page_views', ['support', 'page:root']);
  dogstatsd.increment('collaboetry.page_views', ['support', 'page:home']);
  dogstatsd.increment('collaboetry.page_views', ['support', 'page:404']);
  dogstatsd.increment('collaboetry.page_views', ['support', 'page:all-author-poems']);
  dogstatsd.increment('collaboetry.page_views', ['support', 'page:all-authors']);
  <etc.>
  ```
  You can see them all here:
  ![metrics page-tags](screenshots/dd-page-tags.png)

* visualize the latency by page on a graph (using stacked areas, with one color per `page`)
  I updated the code to calculate the latency for each distinct route (and had 14 unique `page` tags), and this is the resultant graph:
  ![latency by page](screenshots/dd-latency-by-page.png)

  I also made a simple dashboard for this [here](https://app.datadoghq.com/dash/91007/collaboetry-latency-by-page?live=true&page=0&is_auto=false&from_ts=1452535878526&to_ts=1452539478526&tile_size=m).

# Level 4
* NOTE: because I had to be logged in to access particular pages, the numbers here are low because they're just the result of me clicking around in the app. If I do the load test, I'd just be bumping up the total page views on the login page.
* count the overall number of page views using dogstatsd counters
  ![total page views](screenshots/dd-total-views2.png)

  You can see the results on [this dashboard](https://app.datadoghq.com/dash/90969/collaboetry-latency--views?live=false&page=0&is_auto=false&from_ts=1452524208016&to_ts=1452542317147&tile_size=m) as well.
* count the number of page views, split by page (hint: use tags), and visualize the results on a graph
  ![total views by page](screenshots/dd-total-views-by-page2.png)

  These results can be found on the [same dashboard](https://app.datadoghq.com/dash/90969/collaboetry-latency--views?live=false&page=0&is_auto=false&from_ts=1452524208016&to_ts=1452542317147&tile_size=m) as well.
