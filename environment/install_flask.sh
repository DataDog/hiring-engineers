echo "Flask Install Script - Started"

echo "Install pip"
sudo apt update

sudo apt install python3-pip

pip3 --version

echo "Install virtualenv"
sudo apt-get install python3-venv

echo "Create App Directory"
mkdir apm

cd apm

echo "Create & Activate Python Virtual Environment"
sudo python3 -m venv venv

source venv/bin/activate

echo "Install Flask & ddtrace on Virtual Environment"
sudo pip install Flask
sudo pip install ddtrace

echo "Flask Install Script - Completed"