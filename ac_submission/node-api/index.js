const tracer = require('dd-trace').init()


tracer.init({
  analytics: true
})


const db = require('./queries')
const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const port = 8080


app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)


app.get('/', (request, response) => {
  response.json({ info: 'Entryppoint to Application' })
})

app.get('/api/apm', (request, response) => {
  response.json({ info: 'Getting APM Started' })
})

app.get('/api/trace', (request, response) => {
  response.json({ info: 'Posting Traces' })
})

//  This end point pulls a list of users from postgres datadog.users;
//  The call simulates a node blocking call as well as a long running
//  query
app.get('/users', db.getUsers)




app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
