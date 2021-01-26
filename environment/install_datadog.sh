echo "Datadog Install & Configuration Script - Started"

echo "Datadog Agent Install - Replace DD_API_KEY to change accounts"
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=d76729997c912addc8e121967b543a27 DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

echo "Datadog Agent Configuration Move"
sudo cp /vagrant/config/datadog.yaml /etc/datadog-agent/datadog.yaml 

echo "Datadog MongoDB Integration Configuration Move"
sudo cp /vagrant/config/conf.yaml /etc/datadog-agent/conf.d/mongo.d/conf.yaml

echo "Datadog Custom Check - my_metric Configuration Move"
sudo cp /vagrant/checks/custom_metric_check.py /etc/datadog-agent/checks.d/custom_metric_check.py
sudo cp /vagrant/checks/custom_metric_check.yaml /etc/datadog-agent/conf.d/custom_metric_check.yaml

echo "Datadog HTTP Check - Configuration Move"
sudo cp /vagrant/checks/http_check.d/conf.yaml /etc/datadog-agent/conf.d/http_check.d/conf.yaml

echo "Execute Custom Check"
sudo -u dd-agent -- datadog-agent check custom_metric_check

echo "Restart Datadog Agent"
sudo service datadog-agent restart

echo "Datadog Install & Configuration Script - Completed"