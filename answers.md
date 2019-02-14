<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">


<body lang=EN-US link=blue vlink="#954F72" style='tab-interval:.5in'>

<div class=WordSection1>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal;mso-outline-level:2'><b><span style='font-size:18.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>Prerequisites
- Setup the environment<o:p></o:p></span></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>I used a Windows Server 2012 R2 with
SQL Server and Python installed for the exercise. hostname: PATAM10 tags: #<span
class=SpellE>bs:citidirect</span> #database #prod<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>For the next step ---&gt;
&quot;Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the
“Company” field), get the Agent reporting metrics from your local
machine.&quot;<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>I went to the datadoghq.com website
and signed up for my own account following the instruction prompts. On the
first login I followed the getting started instructions to install the agent.
It is very easy to get the agent started as there is a <span class=SpellE>one
step</span> install command for Windows.<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image001.JPG" alt="Image 001"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>In a very short time, the agent
started reporting data:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image001-1.jpg" alt="Image 002"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image002.jpg" alt="Image 003"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image004.jpg" alt="Image 004"><o:p></o:p></span></p>

<div class=MsoNormal align=center style='margin-bottom:0in;margin-bottom:.0001pt;
text-align:center;line-height:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>

<hr size=2 width="100%" align=center>

</span></div>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><span
style='font-size:16.0pt;mso-bidi-font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Collecting Metrics:<o:p></o:p></span></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Add tags in the Agent config file
and show us a screenshot of your host and its tags on the Host Map page in
Datadog. <o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>I added host tags and users tags as
shown in the screenshot:<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image005.jpg" alt="Image 005"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Install a database on your machine
(MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog
integration for that database.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>For SQL Server monitoring, I
followed the steps outlined in the documentation: </span></i></b><span
style='font-size:12.0pt;font-family:"Times New Roman",serif;mso-fareast-font-family:
"Times New Roman"'><a href="https://docs.datadoghq.com/integrations/sqlserver/">https://docs.datadoghq.com/integrations/sqlserver/</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image003.png" alt="Image 003">
SQL YAML Config<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Create a custom Agent check that
submits a metric named <span class=SpellE>my_metric</span> with a random value
between 0 and 1000. Change your check's collection interval so that it only
submits the metric once every 45 seconds.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>I created a <span class=SpellE>my_metric</span>
check using documentation link: </span></i></b><span style='font-size:12.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'><a
href="https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6">https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image007.png" alt="Image 007"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Bonus Question Can you change the
collection interval without modifying the Python check file you created?<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>It is possible to change the
interval without modifying the .<span class=SpellE>py</span> file, you can
change it in the YAML<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image008.png" alt="Image 008"><o:p></o:p></span></p>

<div class=MsoNormal align=center style='margin-bottom:0in;margin-bottom:.0001pt;
text-align:center;line-height:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>

<hr size=2 width="100%" align=center>

</span></div>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><span
style='font-size:16.0pt;mso-bidi-font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Visualizing Data:<o:p></o:p></span></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Utilize the Datadog API to create a <span
class=SpellE>Timeboard</span> that contains:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Your custom metric scoped over your
host. Any metric from the Integration on your Database with the anomaly
function applied. Your custom metric with the rollup function applied to sum up
all the points for the past hour into one bucket<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Please be sure, when submitting your
hiring challenge, to include the script that you've used to create this <span
class=SpellE>Timeboard</span>.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span class=SpellE><b style='mso-bidi-font-weight:normal'><i
style='mso-bidi-font-style:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>Timeboard</span></i></b></span><b
style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:normal'><span
style='font-size:12.0pt;font-family:"Times New Roman",serif;mso-fareast-font-family:
"Times New Roman"'> script:</span></i></b><span style='font-size:12.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>
<u><span style='color:blue'><a
href="https://github.com/patam01/hiring-engineers/blob/master/API%20Timeboard.py">https://github.com/patam01/hiring-engineers/blob/master/API%20Timeboard.py</a></span></u><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Once this is created, access the
Dashboard from your Dashboard List in the UI:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image008-2.jpg" alt="Image 008-2"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>I set the <span class=SpellE>Timeboard's</span>
timeframe to the past 5 minutes Using &quot;ALT + ]&quot; I zoomed to 5 min
interval Take a snapshot of this graph and use the @ notation to send it to
yourself.<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image008-1.jpg" alt="Image 008-1"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Bonus Question: What is the Anomaly
graph displaying?<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>The part of the &quot;Anomalies <span
class=SpellE>Sql</span> Batch Requests&quot; graph that are shown in RED are
showing that for this metric the value is outside of normal. In this case the
mathematical formula used ('1e-3', direction='above') for any spikes above the
value of 1e-3 will be highlighted as outside of the normal. It uses the history
of the metric to predict the future values. If the value is outside of the
expected range it will color it red on the graph.<o:p></o:p></span></i></b></p>

<div class=MsoNormal align=center style='margin-bottom:0in;margin-bottom:.0001pt;
text-align:center;line-height:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>

<hr size=2 width="100%" align=center>

</span></div>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><span
style='font-size:16.0pt;mso-bidi-font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Monitoring Data<o:p></o:p></span></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Since you’ve already caught your
test metric going above 800 once, you don’t want to have to continually watch
this dashboard to be alerted when it goes above 800 again. So let’s make life
easier by creating a monitor.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Create a new Metric Monitor that
watches the average of your custom metric (<span class=SpellE>my_metric</span>)
and will alert if it’s above the following values over the past 5 minutes:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Warning threshold of 500 Alerting
threshold of 800 And also ensure that it will notify you if there is No Data
for this query over the past 10m.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Screen shot of creating 500 &amp;
800 threshold and No Data alert:<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image009.jpg" alt="Image 009"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Please configure the monitor’s
message so that it will: Send you an email whenever the monitor triggers.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Screen shot of breached alert email
notification<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image010.jpg" alt="Image 010"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Create different messages based on
whether the monitor is in an Alert, Warning, or No Data <span class=SpellE>staInclude</span>
the metric value that caused the monitor to trigger and host <span
class=SpellE>ip</span> when the Monitor triggers an Alert state.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Screen shot of email notification
for missing data for 10 mins:<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image011.jpg" alt="Image 011"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Bonus Question: Since this monitor
is going to alert <span class=GramE>pretty often</span>, you don’t want to be
alerted when you are out of the office. Set up two scheduled downtimes for this
monitor:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>One that silences it from 7pm to 9am
daily on M-F,<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Screen shot of scheduled downtime during
weekdays:<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image012.jpg" alt="Image 012"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>And one that silences it all day on
Sat-Sun.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><b style='mso-bidi-font-weight:normal'><i style='mso-bidi-font-style:
normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Screen shot of scheduled downtime
for weekend:<o:p></o:p></span></i></b></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image013.jpg" alt="Image 013"><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Make sure that your email is
notified when you schedule the downtime and take a screenshot of that
notification.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><b>Screen shots for scheduled
downtime email notification</b><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><img src="https://github.com/patam01/hiring-engineers/blob/master/Image014.jpg" alt="Image 014"><br><img src="https://github.com/patam01/hiring-engineers/blob/master/Image015.jpg" alt="Image 015">
<o:p></o:p></span></p>

<div class=MsoNormal align=center style='margin-bottom:0in;margin-bottom:.0001pt;
text-align:center;line-height:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>

<hr size=2 width="100%" align=center>

</span></div>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Collecting APM Data:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Given the following Flask app (or
any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM
solution:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Provide a link and a screenshot of a
Dashboard with both APM and Infrastructure Metrics.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><a
href="https://p.datadoghq.com/sb/ap338w9s48uq47nq-236d0816d44be41d11be22de7c950d8a">https://p.datadoghq.com/sb/ap338w9s48uq47nq-236d0816d44be41d11be22de7c950d8a</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'><a
href="https://github.com/patam01/hiring-engineers/blob/master/Image016.jpg">https://github.com/patam01/hiring-engineers/blob/master/Image016.jpg</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Bonus Question: What is the
difference between a Service and a Resource? From the documentation:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Services: <a
href="https://docs.datadoghq.com/tracing/visualization/#services">https://docs.datadoghq.com/tracing/visualization/#services</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>A service is a set of processes that
do the same job. For instance, a simple web application may consist of two
services:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>A single <span class=SpellE>webapp</span>
service and a single database service.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>While a more complex environment may
break it out into 6 services:<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>3 separate services: <span
class=SpellE>webapp</span>, admin, and query. 3 separate external service:
master-<span class=SpellE>db</span>, replica-<span class=SpellE>db</span>, and
yelp-<span class=SpellE>api</span>.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Resources: <a
href="https://docs.datadoghq.com/tracing/visualization/#resources">https://docs.datadoghq.com/tracing/visualization/#resources</a><o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>A Resource is a <span class=GramE>particular
action</span> for a service.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>For a web application: some examples
might be a canonical URL, such as /user/home or a handler function like <span
class=SpellE>web.user.home</span> (often referred to as “routes” in MVC
frameworks). For a SQL database: a resource is the query itself, such as SELECT
* FROM users WHERE id = ?.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Resources should be grouped together
under a canonical name, like /user/home rather than have /user/<span
class=SpellE>home?id</span>=100 and /user/<span class=SpellE>home?id</span>=200
as separate resources. APM automatically assigns names to your resources;
however you can also name them explicitly. See instructions for: Go, Java,
Python, Ruby.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>These resources can be found after
clicking on a <span class=GramE>particular service</span>.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Please include your fully
instrumented app in your submission, as well.<o:p></o:p></span></p>

<p class=MsoNormal style='mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;
line-height:normal'><span style='font-size:12.0pt;font-family:"Times New Roman",serif;
mso-fareast-font-family:"Times New Roman"'>Flask File: <a
href="https://github.com/patam01/hiring-engineers/blob/master/flask_data.py">https://github.com/patam01/hiring-engineers/blob/master/flask_data.py</a><o:p></o:p></span></p>

<div class=MsoNormal align=center style='margin-bottom:0in;margin-bottom:.0001pt;
text-align:center;line-height:normal'><span style='font-size:12.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:"Times New Roman"'>

<hr size=2 width="100%" align=center>

</span></div>

<p class=MsoNormal><o:p>&nbsp;</o:p></p>
Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?<br>

<b>A cool way to expand Datadog in the commercial world would be to imbed it into IoT devices. With the proliferation of connected devices in industries like manufacturing, to healthcare, to physical security etc., getting a view of this connected map would provide insights to the customers that are not available today. Wouldn’t it be cool if a health care organization had a view of all the medical devices in a hospital, a remote clinic, or in a patient’s house and be able to look at custom metrics and be able to take corrective action based on abnormal behavior. Think about how much better the patient’s care and experience would be and how the doctors could take that valuable data and provide better healthcare. Think about that emergency scenario where the medics on an ambulance can pull relevant data points on route to a patient and already have an action plan and also share that with the ER and Dr’s. The possibilities are endless and that excites me!</b>
</div>

</body>

</html>
