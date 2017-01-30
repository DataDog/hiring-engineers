**************Level-1:
The agent collects events and metrcis from all sources in the system flushes it to the datadog servers every 10 seconds.


**************Level-2:

Page load time histograms:

Graph for page views/sec:
https://app.datadoghq.com/graph/embed?token=26acc002a8a27325951d2c716f267fdb8f49b3857ed574e22bec7891baab6c27&height=300&width=600&legend=true

Average:
https://app.datadoghq.com/graph/embed?token=b8dbf1b7d4952a6314a9ce01cd353da601f5b46ea00d94772ec6c8bcffcee323&height=300&width=600&legend=true

Count:
https://app.datadoghq.com/graph/embed?token=3fdee0cb2a91a4d236bf343a4f8e2e71f22013664cd86102d71d2cf5b05a3786&height=300&width=600&legend=true

Max:
https://app.datadoghq.com/graph/embed?token=cafed532f5bd7d8d610be50ca7d7297edf26b9cba78a1cfe0e5201009c68c012&height=300&width=600&legend=true

Median:
https://app.datadoghq.com/graph/embed?token=d5c0c893cdf53356675684427ca006f4e2abad1a4d9f2124891bac630382a510&height=300&width=600&legend=true

95th Percentile:
https://app.datadoghq.com/graph/embed?token=4bdb7e4544021d4df959c72da4d0423b3ab0d955b6bcb56853c92b0b2287df37&height=300&width=600&legend=true



**************Level-3:

Home:
https://app.datadoghq.com/graph/embed?token=50c2b19aaef8bc956099ed569cc3935fad065879db24bbd08ed61cc8989dc1c1&height=400&width=800&legend=true

Main:
https://app.datadoghq.com/graph/embed?token=49f6f37d3b014a457d5d9d16fb4a549c33df73b71980b2d6bc151f8235254a07&height=400&width=800&legend=true

About Page:
https://app.datadoghq.com/graph/embed?token=c629ca80f6be20163f6f6f873284674cdfdc88f0f97b68130ba5ba79112f7ff6&height=400&width=800&legend=true

Average for Stacked Areas (level-3):
https://app.datadoghq.com/graph/embed?token=346cc70d4fc1615a46b37c9ef904d4a250a6eaa3305027e44fe8db606391ce34&height=300&width=600&legend=true


**************Level-4: 
JSON Query:
Cumulative Sum for a count of all page hits:
"q": "cumsum(sum:web.page_count{*})"
by all pages.

Graphs: 
All Pages:
https://app.datadoghq.com/graph/embed?token=e0626879c243cd29a31492431664b03aac8675653ac6ac92c1ffd128ad9df27f&height=400&width=800&legend=true

Main:
https://app.datadoghq.com/graph/embed?token=cf3f4d76633f26f3107fa9a5242220ce3396df8c01e7e9e7a4d1a488f48d8a6f&height=400&width=800&legend=true

Home:
https://app.datadoghq.com/graph/embed?token=8c04c1b074a1ce8c07e9b23f7a57fd81c699de69f7d5a1d7c0fcd013a84bb59e&height=400&width=800&legend=true

About:
https://app.datadoghq.com/graph/embed?token=f4a28dbd8e4fb40d9791dc6927493161152cd5625a9ae8fd07cdcf74290d7b91&height=400&width=800&legend=true

All Page Count Top List:
https://app.datadoghq.com/graph/embed?token=3fe28186587ddd0cb00318d6eba8d8a644e67b10c416dd333114ee1099606511&height=400&width=800&legend=true

Page Count Dist by Page:
https://app.datadoghq.com/graph/embed?token=847601181f9d65f8f2fdc95c3fe80e753dde248ba8ee79991a7b4355d5bb6532&height=400&width=800&legend=true

*************Level-5 - Graph URL:
https://app.datadoghq.com/graph/embed?token=d55c13d44eff2ce34c03f0290d4617550724e6ffef576041ceaa8351416adc80&height=400&width=800&legend=true
