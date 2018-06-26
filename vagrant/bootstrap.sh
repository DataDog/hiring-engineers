# Update Packages
apt-get update

# Upgrade Packages
apt-get upgrade

# Install DataDog Ubuntu agent
DD_API_KEY=8981e5f870f9dec4f52bd04bb81d4f90 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"