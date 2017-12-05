#!/usr/bin/env bash
# Credit https://gist.github.com/steakknife/9094991
set -e
set -x

### config
INSTALL_SSH_SERVER=1 # comment out to disable
INSTALL_NTPD_LOCALLY=1 # comment out to disable automatic network time synchronization via ntp
CONFIGURE_FIREWALL=1 # comment out to disable (insecure, proceed at your own peril)
### config

# never prompt in dpkg/apt/aptitude
export DEBIAN_FRONTEND=noninteractive

# install docker
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
echo 'deb https://get.docker.io/ubuntu docker main' | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends lxc-docker cgroup-lite

# enable swap resource limiting
sudo sed -i 's/\(GRUB_CMDLINE_LINUX_DEFAULT="\)"/\1cgroup_enable=memory swapaccount=1"/' /etc/default/grub
sudo update-grub


if [ -n "$INSTALL_SSH_SERVER" ]; then

  # install openssh server
  sudo apt-get install -y --no-install-recommends openssh-server

  if [ -n "$CONFIGURE_FIREWALL" ]; then
    # allow connections to this box's ssh server in through the firewall
    sudo ufw allow OpenSSH
  fi

  # start the ssh server right now
  sudo service ssh start || true

  # always run ssh server
  sudo update-rc.d ssh defaults || true
fi

if [ -n "$INSTALL_NTPD_LOCALLY" ]; then

  # install openssh server
  sudo apt-get install -y --no-install-recommends ntp

  # note: the ntp port is never opened to the outside, so there is no DDoS vulnerability
  # it also follows https://www.team-cymru.org/ReadingRoom/Templates/secure-ntp-template.html except for kod
  sudo tee /etc/ntp.conf << ETC_NTP_CONF
driftfile /var/lib/ntp/ntp.drift

statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable

server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org
server 3.pool.ntp.org

restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery

restrict lo

interface ignore wildcard
interface listen lo
ETC_NTP_CONF

  # start the ssh server right now
  sudo service ntp restart || true

  # always run ssh server
  sudo update-rc.d ntp defaults || true

fi

if [ -n "$CONFIGURE_FIREWALL" ]; then
  # start the firewall and enable it permanently
  sudo ufw enable
fi
