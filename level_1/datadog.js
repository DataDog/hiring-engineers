var dataDog = require('dogapi');
var nodemailer = require('nodemailer');

var options = {
  api_key: "0676cc82c8b37aadc3b0014028e87f98",
  app_key: "fcf990aa197aaa558d4e93acbccd75263d4db2ec"
};

dataDog.initialize(options);

var transporter = nodemailer.createTransport();

var title = "1st test event";
var text = "this is a test to see if it worked";

dataDog.event.create(title, text, function(err, results) {
  if (err) {
    console.log(err);
  };
  var mailOptions = {
    from: 'test@datadog.com',
    to: 'alex.schofield816@gmail.com',
    subject: results.event.title,
    text: results.event.text
  };
  transporter.sendMail(mailOptions, function(error, info){
    if(error){
      console.log(error);
    }
    console.log(info);
  });
  console.log(results);
});