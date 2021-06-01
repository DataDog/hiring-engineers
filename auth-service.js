
const { auth } = require('express-openid-connect');

const config = {
  authRequired: false,
  auth0Logout: true,
  baseURL: 'http://localhost:3000',
  clientID: '7Dx4VL7F0apzQy10OikhzsOJg4aw7dl9',
  issuerBaseURL: 'https://dev-u7srx07i.us.auth0.com',
  secret: '8d3a8a223182aeb07263af1ef467d36623b87a2ef5fcada5d24a01b7bbbedd69'
};

var request = require("request");

var options = { method: 'POST',
  url: 'https://dev-u7srx07i.us.auth0.com/oauth/token',
  headers: { 'content-type': 'application/json' },
  body: '{"client_id":"WBkfHKpeF5Ows6mJO4rA4kb7tn7d8w82","client_secret":"JwYEOpNw7z51igASZWSuJjeefkgmqOpIpOOosa8dmsYblqYYMMS56vULkyI2Gm2M","audience":"https://quickstarts/api","grant_type":"client_credentials"}' };

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
