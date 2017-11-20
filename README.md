<span class="c5">[https://github.com/DataDog/hiring-engineers/tree/solutions-engineer](https://www.google.com/url?q=https://github.com/DataDog/hiring-engineers/tree/solutions-engineer&sa=D&ust=1511158846197000&usg=AFQjCNFPvx4HNjdqzRVwQ3dcQghosEmm-Q)</span>

<span class="c0"></span>

<span class="c0">Installed datadog agent on my local machine and tried to set up dashboard/metrics.</span>

<span class="c0"></span>

<span class="c0">While setting up a screenboard dashboard, I ran into a webpage display issue on Google Chrome:</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 422.67px;">![](https://lh3.googleusercontent.com/hFYIiBG_lZozja_FByjLCMu27KtVaplg776fZ1LVx-cvrnmQsY4KN7yhPgetGgh5Zi6CuaUX2G4HR1-LzmJYrcJCUFVaaV0-yxjAqP_SuT_jochklP_lJr1gMascNv_gxN6MG12p)</span>

<span class="c0"></span>

<span class="c0">While trying to add an event list, I found that the search query field was not intuitive to use, as I couldn’t get it to filter with the “Romans-Macbook-Air” string. I suspect there is a special escape character I need to use for dashes, but couldn’t see an obvious way to get to search query documentation (it really should be next to the search query field title). I tried the typical backslash as an escape character but was still unable to get desired search query results.</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 456.00px;">![](https://lh3.googleusercontent.com/116PNGTiwFGUHxHFwhyYEC23ZM-XShj-cKreeAQgpYIXVfaCGlOVSeK6TLZlWXKWFnGCJ7YrFxnPZHTQYnSW5snUXjUKon_btgCIuCse9B33QClpl2MDnyow8IljkshdyBjLjULt)</span>

<span class="c0"></span>

<span class="c0">I set up an Ubuntu server on Amazon Lightsail for the agent tagging and database portions of the exercise. The agent one-line install was really nice, and I was able to edit tags in the configuration file easily enough. I also edited the hostname to more easily identify the host in the datadog UI.</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 408.00px;">![](https://lh4.googleusercontent.com/h5zn1ZPyCtCQQ4fDM_xPQp9_lJzwH0TVnI9o-k3HHfY21UGva_ORSullBYmfKlZk5BeECmsG7_DmW4TGPLyUMCwQJ4yAAtmhA5vEV3funW6c_KYhwYhEC7C19hTXURA18ZI2J0PA)</span>

<span class="c0"></span>

<span class="c0"></span>

<span class="c0">The mongodb integration was a little bit more involved. Copying and pasting the mongodb.yaml configuration didn’t work due to spacing issues (or so it seems). It was unfortunate that I had to restart the agent and check the info command each time to see if the config file was correctly read. Afterwards I saw that you could use a YAML parser to check the config file, which would have been helpful during setup.</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 361.33px;">![](https://lh5.googleusercontent.com/NlIwJ2vtFt7JFQLRoTdRTRB7tXpeZ8Ie6Qz0TOoMsgnnlPqEAq_yVuo4_iPxbYYUt7aB8pPdWXJz7m2lG2rnIUt78l1Gpud-j96tUJLPwftQTxE-PN9PLYpe46Oatzxyz_zrNHuY)</span>

<span class="c0"></span>

<span class="c0">check() {</span>

<span class="c0">self.increment(“my_metric”,random_value_int)</span>

<span class="c0">}</span>

<span class="c0"></span>

<span>Despite this help article -</span><span> [](https://www.google.com/url?q=https://help.datadoghq.com/hc/en-us/articles/206955236-Metric-types-in-Datadog&sa=D&ust=1511158846200000&usg=AFQjCNFHKwNaSPB_C-ie2njQziossMWxKw) </span><span class="c5">[https://help.datadoghq.com/hc/en-us/articles/206955236-Metric-types-in-Datadog](https://www.google.com/url?q=https://help.datadoghq.com/hc/en-us/articles/206955236-Metric-types-in-Datadog&sa=D&ust=1511158846201000&usg=AFQjCNGOnqy-S5VXZt9pgkN11KnM-EVKCA)</span> <span class="c0">- it was unclear when you would use gauge metrics vs counter metrics.</span>

<span class="c0"></span>

<span class="c0">After reading through custom agent checks, I got my_metric to report the random 0-1000 value.</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 348.00px;">![](https://lh4.googleusercontent.com/DOXHJbVWiZD0O7K7_aa2IX8LItBYAI_XDHGHkdrijCCnr21W7saD8gGy8xcXdXk2PM-6XDuZqlY0QWNtR9eW_N6xQZAnTtcJR_JduWZP4rz4Yi2COYwOPJLDqTiBYDo4eipus6Mp)</span>

<span class="c0"></span>

<span class="c0"></span>

<span class="c0">To change check's collection interval so that it only submits the metric once every 45 seconds I edited the .yaml configuration file and added the following line to init_config:</span>

<span class="c0">min_collection_interval: 45</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 461.33px;">![](https://lh6.googleusercontent.com/lrwU7sAks0oPow2Yn7q4lvuCNtEMDpXORz7PLzxp8XNktkvwfoFk8brIyDfxMW27kK55Wevf99dwfv2Eoy1aSWq31bp6YngA9u0eDV1UQzDyvs11rB-uC9gdAm8SnCKDIASc6afX)</span>

<span class="c0"></span>

<span class="c0">Bonus Question Can you change the collection interval without modifying the Python check file you created?</span>

<span class="c0">*Maybe using dogstatsd, or manually keep track of time in the python file using time-based methods</span>

<span class="c0"></span>

<span class="c0">---</span>

<span class="c0"></span>

<span class="c0">I got the 5 minute interval by dragging the cursor over a 5 minute period on a graph.</span>

<span class="c0"></span>

<span>The anomaly graph is displaying unexpected spikes and dips in the database resident memory. Since it uses the basic algorithm, it determines what’s unexpected using a lagging rolling quantile computation.</span> <span class="c5">[https://docs.datadoghq.com/guides/anomalies/](https://www.google.com/url?q=https://docs.datadoghq.com/guides/anomalies/&sa=D&ust=1511158846203000&usg=AFQjCNELYVMw5rE3b8Rqit040bqAPinJbw)</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 358.67px;">![](https://lh3.googleusercontent.com/SDD7_Mpqw9vs6Ebk3Gv2OO1Q9x2X0Y0P1g4aiZz43hZlIzzLKdRc7P1Z73qyDdkukKDt-USKo-GiSAFBhxLximCmopy0nIkxgtJWEAyH9fle37a1-zRl0TNIpLsq_hPF7KnzYFyR)</span>

<span class="c0"></span>

<span class="c0">I scheduled downtime as well for M-F 7p-9a and Sat-Sun.</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 353.33px;">![](https://lh5.googleusercontent.com/CnQZwyWVbZo-KvO2oFS_sy7JclnWTf9LbVAzeYvGq-nfDSqGjH9ONh1gfiG8Bk5XON02Ys6JWYfnrnCVwAD9QIF2XUbv8w10vDHga8izkoucIH77GRyAqPLDmlG6oNlcw71_8FYU)</span>

<span class="c0"></span>

<span class="c0">---</span>

<span class="c0"></span>

<span class="c5">[https://p.datadoghq.com/sb/aa5f65a0f-6c9a9e1a64](https://www.google.com/url?q=https://p.datadoghq.com/sb/aa5f65a0f-6c9a9e1a64&sa=D&ust=1511158846204000&usg=AFQjCNFuSXBx-ZA3jY_9AdtVyxPM36h26w)</span>

<span class="c0"></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 469.33px;">![](https://lh5.googleusercontent.com/HL1no9IehTrEwRDOtmNIKWjz7w7ozYAJyPweeDGEsboySNcGIUfpVeQnqc9fd0d2H29m-FUjYhje5w6ap79U1IB34H-qwU543QhHeMNzS7qWPMRgrnP0uxcuPE0DH_U-Y_J-pXaD)</span>

<span class="c0"></span>

<span class="c0">---</span>

<span class="c0"></span>

<span class="c0">I think an interesting use for Datadog would be monitoring Brooklyn Bridge pedestrian and bicyclist traffic. With a few well placed sensors, you could track pure daily numbers, see the difference between holiday traffic and regular traffic, and tell when biking across the bridge is most difficult due to all the tourists :).</span>
