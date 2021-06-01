
const { auth } = require('express-openid-connect');

const config = {
  authRequired: false,
  auth0Logout: true,
  baseURL: 'http://localhost:3000',
  clientID: 'redacted',
  issuerBaseURL: 'https://dev-u7srx07i.us.auth0.com',
  secret: 'redacted'
};

var request = require("request");

var options = { method: 'POST',
  url: 'https://dev-u7srx07i.us.auth0.com/oauth/token',
  headers: { 'content-type': 'application/json' },
  body: '{"client_id":"redacted","client_secret":"redacted","audience":"https://quickstarts/api","grant_type":"client_credentials"}' };

const express = require('express')
const app = express()

app.use(auth(config));

app.get('/', (req, res) => {
  res.send(req.oidc.isAuthenticated() ? 'Logged in' : 'Logged out')

});

app.get('/token', (req, res) => {

  console.log('req > ', req)
  request(options, function (error, response, body) {
    if (error) throw new Error(error);
    res.send('tada!')
    console.log(body);
  });
});

app.get('/create', function (req, res) {
    res.status(200).send('create')
});


app.listen(3000, () => {
    console.log('Server running on port 3000')
})
