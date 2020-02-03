#!/bin/bash

DOCKER_CONTENT_TRUST=1

docker run -d --name dd-agent -v /var/run/docker.sock:/var/run/docker.sock:ro \
                              -v /proc/:/host/proc/:ro \
                              -p 127.0.0.1:8126:8126/tcp \
                              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
                              -e DD_API_KEY=87b7c220850533645bf5c6c2da43f91a \
                              -e DD_APM_ENABLED=true \
                              datadog/agent:7
