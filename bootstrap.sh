#!/usr/bin/env bash

DD_API_KEY=be24eb3b14a2bfc7dff74558dc4c864f bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"


helm install --name eager-datadog \
  --set datadog.apiKey=be24eb3b14a2bfc7dff74558dc4c864f stable/datadog