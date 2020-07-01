sudo docker run -d --name docker-dd-agent \
  --network ddnetwork \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /home/datadog/dd_config/conf.d:/conf.d:ro \
  -v /home/datadog/dd_config/checks.d:/checks.d:ro \
  -v /home/datadog/dd_config/run:/opt/docker-dd-agent/run:rw \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e API_KEY=75cc324da0bc265b8883ce646853b814 \
  -e SD_BACKEND=docker \
  -e NON_LOCAL_TRAFFIC=false \
  -e DD_LOGS_ENABLED=true \
  -e DD_AC_EXCLUDE="name:datadog-agent" \
  -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \
  -e DD_APM_ENABLED=true \
  -e DD_APM_NON_LOCAL_TRAFFIC=true \
  -e TAGS=docker:agent,env:testing \
  datadog/docker-dd-agent:latest

