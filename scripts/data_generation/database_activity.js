const { Pool, Client } = require('pg')
config = require('../../config.json')

const pool = new Pool({
  user: config.database_user,
  host: 'localhost',
  database: 'billdb',
  password: config.database_password,
  port: 5432,
})

pool.query('CREATE TABLE IF NOT EXISTS dummy_data(user_info text, action text, reason text);', (err, res) => {
  if (err) {
    console.log(err.stack)
  } else {
    console.log(res.rows[0])
  }
})

function insertData(){
	pool.query("INSERT INTO dummy_data(user_info, action, reason)VALUES('billsinfo', 'wrotecode', 'solvedproblem');", (err, res) => {
 		if (err) {
   			console.log(err.stack)
  		} else {
    		console.log(res.rows[0])
  		}	
	})
}

function queryData(){
	pool.query('SELECT * FROM dummy_data', (err, res) => {
 		if (err) {
   			console.log(err.stack)
  		} else {
    		console.log(res.rows[0])
  		}	
	})
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function recursiveLoop() {
	random_int = getRandomInt(2)
	if (random_int == 0) {
		insertData()
	} else {
		queryData()
	} 
	setTimeout(recursiveLoop, 30000);
}

recursiveLoop()

