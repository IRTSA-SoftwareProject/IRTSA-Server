#!/bin/bash
# This script will setup the desktop image of Rasbian
# ( https://downloads.raspberrypi.org/rpd_x86_latest )
# as the IRTSA server, simply install the image from 
# the raspberry pi website then run this script in the
# GUI's terminal and when complete the server will 
# restart as the server with the IP address 10.0.0.1
#
if [ "$EUID" -ne 0 ]
  then echo "Please run as root by execution sudo ./pi_setup_vm.sh"
  exit
fi

echo  " ________________________________"
echo "|                                |"
echo "|      Setup RPI VM Script!      |"
echo "|________________________________|"
echo 
echo 
echo .. Installing required packages
apt-get install dnsmasq hostapd apache2 python python3 build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y > /dev/null 2>&1
wait
echo ... Python 3.7: Downloading Python 3.7
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz > /dev/null 2>&1
wait
tar xf Python-3.7.0.tar.xz > /dev/null 2>&1
wait
cd Python-3.7.0/
wait
echo .... Python 3.7: Configuring Installation
./configure --prefix=/usr/local/lib/python-3.7.0 > /dev/null 2>&1
wait
make > /dev/null 2>&1
wait
echo ..... Python 3.7: Installing
make install > /dev/null 2>&1
wait
echo ...... Python 3.7: Creating Symlinks
ln -s /usr/local/lib/python-3.7.0/bin/pydoc3.7 /usr/bin/pydoc3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/python3.7 /usr/bin/python3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/python3.7m /usr/bin/python3.7m > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/pyvenv-3.7 /usr/bin/pyvenv-3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/pip3.7 /usr/bin/pip3.7 > /dev/null 2>&1
wait
cd ..
wait

echo ....... Configuring static IP for eth0
echo "# profile static_eth0" >> /etc/dhcpcd.conf
echo interface eth0 >> /etc/dhcpcd.conf
echo static ip_address=10.0.0.1/24 >> /etc/dhcpcd.conf
echo static routers=10.0.0.1 >> /etc/dhcpcd.conf
echo static domain_name_servers=10.0.0.1 >> /etc/dhcpcd.conf

echo ........ Configuring dnsmasq.conf
echo "#define interface that clients connect to" >> /etc/dnsmasq.conf
echo interface=eth0 >> /etc/dnsmasq.conf
echo "#define server to use for dns" >> /etc/dnsmasq.conf
echo server=10.0.0.1 >> /etc/dnsmasq.conf
echo "#define lease IP range and lease duration" >> /etc/dnsmasq.conf
echo dhcp-range=10.0.0.2,10.0.0.50,255.255.255.0,24h >> /etc/dnsmasq.conf

echo ......... Creating irscans storage directory
mkdir /var/www/html/irscans
wait
chown -R pi:pi /var/www/html/irscans
echo .......... Editing apache2.conf
echo "<Directory /var/www/html/irscans>" >> /etc/apache2/apache2.conf
echo Options +Indexes +FollowSymLinks >> /etc/apache2/apache2.conf
echo AllowOverride None >> /etc/apache2/apache2.conf
echo Require all granted >> /etc/apache2/apache2.conf
echo ServerSignature Off >> /etc/apache2/apache2.conf
echo "</Directory>" >> /etc/apache2/apache2.conf

echo ........... Creating index.html
echo "<!DOCTYPE html>" > /var/www/html/index.html
echo "<html lang="en">" >> /var/www/html/index.html
echo "<head>" >> /var/www/html/index.html
echo "        <meta charset="utf-8" />" >> /var/www/html/index.html
echo "        <meta name="description" content="IRTSA Homepage" />" >> /var/www/html/index.html
echo "        <meta name="keywords" content="IRscans, IRTSA" />" >> /var/www/html/index.html
echo "        <meta name="author" content="IRTSA Group" />" >> /var/www/html/index.html
echo "        <title>IRTSA Software Project</title>" >> /var/www/html/index.html
echo "</head>" >> /var/www/html/index.html
echo "<body>" >> /var/www/html/index.html
echo "        <h1>IRTSA Web Server</h1>" >> /var/www/html/index.html
echo "        <p>Infra-Red Scans are stored on this server for retrieval by the native android application being developed for this project</p>" >> /var/www/html/index.html
echo "        <p>Images can be found in the irscans folder: <em><a href="/irscans">irscans</a></em></p>" >> /var/www/html/index.html
echo "</body>" >> /var/www/html/index.html
echo "</html>" >> /var/www/html/index.html

echo ............ Downloading IRTSA Server and Demo
wget https://github.com/IRTSA-SoftwareProject/IRTSA-Server/archive/master.zip > /dev/null 2>&1
wait

echo ............. Unzipping
unzip master.zip > /dev/null 2>&1
wait
mkdir demo
wait
mv IRTSA-Server-master/src/demo/* demo/
wait
chown -R pi:pi demo
wait
mv IRTSA-Server-master/src/scans/* scans/
wait
chown -R pi:pi scans
wait
mkdir server
wait
mv IRTSA-Server-master/server/* server/
wait
chown -R pi:pi server

echo .............. Removing Files
rm master.zip
rm -rf IRTSA-Server-master
rm -rf Python-3.7*

echo ............... Installing required python libraries
pip3.7 install imageio scipy > /dev/null 2>&1
wait
pip3.7 install numpy re > /dev/null 2>&1
wait
pip3.7 install Rx websockets > /dev/null 2>&1
wait
echo ................ Creating IRTSAserver Service Script
echo [Unit] > /lib/systemd/system/IRTSAserver.service
echo Description=IRTSA Socket Server Service >> /lib/systemd/system/IRTSAserver.service
echo After=network.target >> /lib/systemd/system/IRTSAserver.service
echo  >> /lib/systemd/system/IRTSAserver.service
echo [Service] >> /lib/systemd/system/IRTSAserver.service
echo User=pi >> /lib/systemd/system/IRTSAserver.service
echo Group=pi >> /lib/systemd/system/IRTSAserver.service
echo WorkingDirectory=/home/pi >> /lib/systemd/system/IRTSAserver.service
echo Restart=always >> /lib/systemd/system/IRTSAserver.service
echo RestartSec=5 >> /lib/systemd/system/IRTSAserver.service
echo ExecStart=/usr/bin/python3.7 -m server >> /lib/systemd/system/IRTSAserver.service
echo  >> /lib/systemd/system/IRTSAserver.service
echo [Install] >> /lib/systemd/system/IRTSAserver.service
echo WantedBy=multi-user.target >> /lib/systemd/system/IRTSAserver.service
wait
echo ................. Enabling and Starting Services
systemctl daemon-reload > /dev/null 2>&1
wait
systemctl enable dnsmasq > /dev/null 2>&1
systemctl start dnsmasq > /dev/null 2>&1
systemctl enable ssh > /dev/null 2>&1
systemctl start ssh > /dev/null 2>&1
systemctl enable apache2 > /dev/null 2>&1
systemctl start apache2 > /dev/null 2>&1
systemctl enable IRTSAserver > /dev/null 2>&1
systemctl start IRTSAserver > /dev/null 2>&1
wait
echo .................. Uninstalling GUI and Unecessary Packages
apt-get remove --purge x11-common -y > /dev/null 2>&1
apt-get autoremove -y > /dev/null 2>&1
ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service > /dev/null 2>&1
echo ................... DONE!! REBOOTING IN 5 SECONDS
sleep 1
echo ................... DONE!! REBOOTING IN 4 SECONDS
sleep 1
echo ................... DONE!! REBOOTING IN 3 SECONDS
sleep 1
echo ................... DONE!! REBOOTING IN 2 SECONDS
sleep 1
echo "................... DONE!! IT'S GO TIME BOIII!!!!"
sleep 1
reboot