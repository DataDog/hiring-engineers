sudo docker run -d -p 5050:5050 -h datadog1 \
  --network ddnetwork \
  --name flaskapp \
  -e DD_AGENT_HOST=docker-dd-agent \
  -e DATADOG_TRACE_AGENT_PORT=8126 \
flaskapp:1.0