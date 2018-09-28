FROM datadog/agent:latest
ADD conf.d/mongo.d/conf.yaml /etc/datadog-agent/conf.d/mongo.d/conf.yaml
ADD conf.d/datadog.yaml /etc/datadog-agent/datadog.yaml
ADD mymetric.py /etc/datadog-agent/checks.d/mymetric.py
ADD mymetric.yaml /etc/datadog-agent/conf.d/mymetric.yaml
