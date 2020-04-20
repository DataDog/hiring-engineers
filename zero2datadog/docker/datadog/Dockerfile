FROM datadog/agent:7  # I pin the image version because the road to hell is paved with the 'latest' tag.
ARG DD_CONFIG_HOME
ENV DD_CONFIG_HOME=$DD_CONFIG_HOME  # make this dynamic to ease building on various environments
ARG MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
ADD $DD_CONFIG_HOME/conf.d /etc/datadog-agent/
ADD $DD_CONFIG_HOME/datadog.yaml /etc/datadog-agent/  # This config file is more generic than the one on my local host
