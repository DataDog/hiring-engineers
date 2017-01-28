Level 1

-The agent is currently reporting 41 metrics for my machine:
collection_timestamp
datadog.dogstatsd.packet.count
datadog.dogstatsd.serialization_status
ntp.offset
system.cpu.idle
system.cpu.iowait
system.cpu.stolen
system.cpu.system
system.cpu.user
system.disk.free
system.disk.in_use
system.disk.total
system.disk.used
system.fs.inodes.free
system.fs.inodes.in_use
system.fs.inodes.total
system.fs.inodes.used
system.io.bytes_per_s
system.load.1
system.load.15
system.load.5
system.load.norm.1
system.load.norm.15
system.load.norm.5
system.mem.free
system.mem.pct_usable
system.mem.usable
system.mem.used
system.net.bytes_rcvd
system.net.bytes_sent
system.net.packets_in.count
system.net.packets_in.error
system.net.packets_out.count
system.net.packets_out.error
system.net.tcp.rcv_packs
system.net.tcp.retrans_packs
system.net.tcp.sent_packs
system.swap.free
system.swap.used
system.uptime
uuid

-The agent is software that sends information (for example, the number of packets received) from a machine to DataDog, so that the user may make some sense of their machine's performance. 

-Screenshot of tags in file DataDogTags.

-Installed MongoDB integration. See file mongo.yaml.

-Custom agent check found in files randomCheck.py and randomCheck.yaml. test.support.random is appearing in the metrics explorer. Screenshot in file NewMetric. 


Level 2

-The cloned dashboard is called MongoDBClone. I added graphs for the test.support.random metric and the mongodb.uptime metric.
Screenshot in file AddedMetrics.

-Timeboards show a specific time range for all event graphs, while screenboards allow the user to position widgets where they want and allows these widgets to have different time ranges. Screenboards can be shared live and read-only so that others can get a high-level look at the system in question, whereas timeboards can only be shared individually (graph-by-graph).

-Screenshot of the snapshot in file SpikeInMetric.


Level 3


- Created new monitor named "Random Metric Above 0.9". Monitor is multi-alert by host. Screenshot of the monitor in file Monitor.

-Screenshot of the email alert in file AlertEmail.

-Screenshot of the email regarding scheduled downtime in file ScheduledDowntime.

Link to dashboard: https://p.datadoghq.com/sb/24161fe7d-bc7ccd51ef

