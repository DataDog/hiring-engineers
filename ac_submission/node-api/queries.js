const Pool = require('pg').Pool
const pool = new Pool({
  user: 'datadog',
  host: 'postgres',
  database: 'datadog',
  password: 'pgpass1234',
  port: 5432,
})

var theThing = null;
var theThingArray = [];

const getUsers = (request, response) => {

var replaceThing = function () {

        var priorThinngArray = theThingArray;
        var unused = function () {
            // 'unused' is the only place where 'priorThing' is referenced,
            // but 'unused' never gets invoked
            if (priorThing) {
                console.log("hi");
            }
        };

        //for (i = 1; i <= 12; i++) {
        for (i = 1; i <= 8; i++) {

            theThingArray[i] = {
                longStr: new Array(90000000).join('*'),  // create a 10MB object
                someMethod: function () {
                    console.log(i);
                }
            };

            //$(otherVar).something();
        };
    };
    replaceThing();
    theThingArray = [];


	    setImmediate(() => {
        for (let i = 0; i < 100000; i++) {
        }

    }); //300000000000
  pool.query('SELECT * FROM users, pg_sleep(20) ORDER BY id ASC', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports = {
  getUsers
}

