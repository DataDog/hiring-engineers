FROM datadog/docker-dd-agent
ADD datadog.conf /etc/dd-agent/datadog.conf
ADD checks.d/check_random.py /etc/dd-agent/checks.d/check_random.py
ADD conf.d/check_random.yaml /etc/dd-agent/conf.d/check_random.yaml
ADD conf.d/redisdb.yaml /etc/dd-agent/conf.d/redisdb.yaml
ADD conf.d/mongo.yaml /etc/dd-agent/conf.d/mongo.yaml
