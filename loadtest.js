const loadtest = require('loadtest');

var options = {
	url: 'http://localhost:3001',
	maxRequests: 720000,
}

loadtest.loadTest(options, function(error) {
    if (error) {
        return console.error('Got an error: %s', error);
    }
    console.log('Tests run successfully for home');
});

options.url = 'http://localhost:3001/wiki';
loadtest.loadTest(options, function(error) {
    if (error) {
        return console.error('Got an error: %s', error);
    }
    console.log('Tests run successfully for wiki');
});

options.url = 'http://localhost:3001/users';
loadtest.loadTest(options, function(error) {
    if (error) {
        return console.error('Got an error: %s', error);
    }
    console.log('Tests run successfully for users');
});