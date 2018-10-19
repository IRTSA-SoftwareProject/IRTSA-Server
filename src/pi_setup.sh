#!/bin/bash
# This script will setup a raspberry pi 3B or 3B+ as the IRTSA
# server.  This script requires a rpi with RASBIAN STRETCH LITE
# ( https://downloads.raspberrypi.org/raspbian_lite_latest ) 
# installed and an internet connection via the rpi's ethernet
# port.  After the script has run the RPI will be accessable as
# a wireless access point with the SSID being "IRTSA-AP" and password
# being "Th3rmalHotspot" and can be access with the IP address 10.0.0.1
#
if [ "$EUID" -ne 0 ]
  then echo "Please run as root by execution sudo ./pi_setup.sh"
  exit
fi

echo  " _________________________________"
echo "|                                 |"
echo "|        Setup RPI Script!        |"
echo "|   Please wait as installation   |"
echo "|      can take over 2 hours      |"
echo "|_________________________________|"
echo
echo 
echo . Increasing Swap for Installation
# Create a swap partition for extra memory storage during installation
dd if=/dev/zero of=/var/swap.1 bs=1M count=1024 > /dev/null 2>&1
wait
mkswap /var/swap.1 > /dev/null 2>&1
wait
chmod 600 /var/swap.1
wait
swapon /var/swap.1 > /dev/null 2>&1
wait 
echo .. Installing required packages
# Update apache and install all required packages needed to run services and programs on the microcontrollers
apt-get update > /dev/null 2>&1
wait
apt-get install dnsmasq hostapd apache2 -y > /dev/null 2>&1
wait
apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y > /dev/null 2>&1
wait
apt-get install libsm6 libjpeg9-dev -y > /dev/null 2>&1
wait
apt-get install libopenblas-dev gcc gfortran cmake -y > /dev/null 2>&1
wait
echo ... Python 3.7: Downloading Python 3.7
# Download source for python3.7
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz > /dev/null 2>&1
wait
tar xf Python-3.7.0.tar.xz > /dev/null 2>&1
wait
cd Python-3.7.0/
wait
echo .... Python 3.7: Configuring Installation
# Configure and make installer for python3.7
./configure --prefix=/usr/local/lib/python-3.7.0 > /dev/null 2>&1
wait
make > /dev/null 2>&1
wait
echo ..... Python 3.7: Installing
# Install Python 3.7
make install > /dev/null 2>&1
wait
echo ...... Python 3.7: Creating Symlinks
# Create symlinks to execute python commands from cli
ln -s /usr/local/lib/python-3.7.0/bin/pydoc3.7 /usr/bin/pydoc3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/python3.7 /usr/bin/python3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/python3.7m /usr/bin/python3.7m > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/pyvenv-3.7 /usr/bin/pyvenv-3.7 > /dev/null 2>&1
ln -s /usr/local/lib/python-3.7.0/bin/pip3.7 /usr/bin/pip3.7 > /dev/null 2>&1
wait
cd ..
wait
echo "....... Configuring hostapd.conf (Wireless Access Point)"
# Setup hostapd to allow the microcontroller to act as an Access Point
echo "#interface settings" > /etc/hostapd/hostapd.conf
echo interface=wlan0 >> /etc/hostapd/hostapd.conf
echo driver=nl80211 >> /etc/hostapd/hostapd.conf
echo hw_mode=g >> /etc/hostapd/hostapd.conf
echo channel=6 >> /etc/hostapd/hostapd.conf
echo ieee80211n=1 >> /etc/hostapd/hostapd.conf
echo auth_algs=1 >> /etc/hostapd/hostapd.conf
echo ignore_broadcast_ssid=0 >> /etc/hostapd/hostapd.conf
echo "#AP settings" >> /etc/hostapd/hostapd.conf
echo ssid=IRTSA-AP >> /etc/hostapd/hostapd.conf
echo wpa=2 >> /etc/hostapd/hostapd.conf
echo wpa_passphrase=Th3rmalHotspot >> /etc/hostapd/hostapd.conf
echo wpa_key_mgmt=WPA-PSK >> /etc/hostapd/hostapd.conf
echo rsn_pairwise=CCMP >> /etc/hostapd/hostapd.conf
wait
echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' >> /etc/default/hostapd
wait
echo ........ Configuring interfaces
# Edit wpa_supplicant settings country to enable Wifi interface
echo ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev > /etc/wpa_supplicant/wpa_supplicant.conf
echo update_config=1 >> /etc/wpa_supplicant/wpa_supplicant.conf
echo country=AU >> /etc/wpa_supplicant/wpa_supplicant.conf
wait
# Set interface settings for wlan0
echo allow-hotplug wlan0 > /etc/network/interfaces
echo iface wlan0 inet static >> /etc/network/interfaces
echo address 10.0.0.1 >> /etc/network/interfaces
echo netmask 255.255.255.0 >> /etc/network/interfaces
echo network 10.0.0.0 >> /etc/network/interfaces
echo broadcast 10.0.0.255 >> /etc/network/interfaces
wait
echo ......... Editing dhcpcd.conf
# Set dhcp configuration for wlan0
echo "# profile static_wlan0" >> /etc/dhcpcd.conf
echo interface wlan0 >> /etc/dhcpcd.conf
echo static ip_address=10.0.0.1/24 >> /etc/dhcpcd.conf
echo static routers=10.0.0.1 >> /etc/dhcpcd.conf
echo static domain_name_servers=10.0.0.1 >> /etc/dhcpcd.conf
wait
echo .......... Configuring dnsmasq.conf
# Define settings to offer DHCP leases
echo "#define interface that clients connect to" >> /etc/dnsmasq.conf
echo interface=wlan0 >> /etc/dnsmasq.conf
echo "#define server to use for dns" >> /etc/dnsmasq.conf
echo server=10.0.0.1 >> /etc/dnsmasq.conf
echo "#define lease IP range and lease duration" >> /etc/dnsmasq.conf
echo dhcp-range=10.0.0.2,10.0.0.50,255.255.255.0,24h >> /etc/dnsmasq.conf
wait
echo ........... Creating irscans storage directory
# Make folder to store IR scans on a webserver and set permissions to be writeable
mkdir /var/www/html/irscans
wait
chown -R pi:pi /var/www/html/irscans
wait
echo ............ Editing apache2.conf
# Make irscans directory accessible to view in a web browser
echo "<Directory /var/www/html/irscans>" >> /etc/apache2/apache2.conf
echo Options +Indexes +FollowSymLinks >> /etc/apache2/apache2.conf
echo AllowOverride None >> /etc/apache2/apache2.conf
echo Require all granted >> /etc/apache2/apache2.conf
echo ServerSignature Off >> /etc/apache2/apache2.conf
echo "</Directory>" >> /etc/apache2/apache2.conf
wait
echo ............. Creating index.html
# Create a index landing page
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
wait
echo .............. Downloading IRTSA Server and Demo
# Get server files to create socket server and perform scans
wget https://github.com/IRTSA-SoftwareProject/IRTSA-Server/archive/master.zip > /dev/null 2>&1
wait
echo ............... Unzipping
unzip master.zip > /dev/null 2>&1
wait
mkdir scans
wait
mkdir "scans/png/"
wait
mv IRTSA-Server-master/src/scans/* scans/png/
wait
chown -R pi:pi scans
wait
mkdir server
wait
mv IRTSA-Server-master/server/* server/
wait
chown -R pi:pi server

echo ................ Removing Files
# Clean up downloaded files no longer needed.
rm master.zip
rm -rf IRTSA-Server-master
rm -rf Python-3.7*

echo ................. Installing required python libraries: numpy
pip3.7 install numpy > /dev/null 2>&1
wait
echo ................. Installing required python libraries: Rx
pip3.7 install Rx > /dev/null 2>&1
wait
echo ................. Installing required python libraries: websockets
pip3.7 install websockets > /dev/null 2>&1
wait
echo ................. Installing required python libraries: asyncio
pip3.7 install asyncio > /dev/null 2>&1
wait
echo ................. Installing required python libraries: imageio
# Download and manually install imageio
wget https://www.piwheels.org/simple/imageio/imageio-2.4.1-py3-none-any.whl > /dev/null 2>&1
wait
pip3.7 install *.whl > /dev/null 2>&1
wait
rm *.whl
wait
echo ................. Installing required python libraries: scipy
# Download source for scipy and manually build and install
pip3.7 install Cython > /dev/null 2>&1
wait
wget https://github.com/scipy/scipy/releases/download/v1.0.1/scipy-1.0.1.tar.gz > /dev/null 2>&1
wait
tar xzf scipy-1.0.1.tar.gz > /dev/null 2>&1
wait
cd scipy-1.0.1
wait
python3.7 setup.py build > /dev/null 2>&1
wait
python3.7 setup.py install > /dev/null 2>&1
wait
cd ..
wait
rm scipy-1.0.1.tar.gz
rm -rf scipy-1.0.1
wait	
echo ................. Installing required python libraries: opencv
# Download source for opencv and manually build with cmake to install
wget https://github.com/opencv/opencv/archive/3.4.3.zip -O opencv-3.4.3.zip > /dev/null 2>&1
wait
unzip opencv-3.4.3.zip > /dev/null 2>&1
wait
mkdir opencv-3.4.3/build
wait
cd opencv-3.4.3/build
wait
# build opencv without GUI options, stating python version and installation directory.
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local/lib/python-3.7.0/ -D PYTHON3_EXECUTABLE=/usr/local/lib/python-3.7.0/bin/python3.7 -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF -D WITH_OPENCL=OFF -D WITH_CUDA=OFF -D BUILD_opencv_gpu=OFF -D BUILD_opencv_gpuarithm=OFF -D BUILD_opencv_gpubgsegm=OFF -D BUILD_opencv_gpucodec=OFF -D BUILD_opencv_gpufeatures2d=OFF -D BUILD_opencv_gpufilters=OFF -D BUILD_opencv_gpuimgproc=OFF -D BUILD_opencv_gpulegacy=OFF -D BUILD_opencv_gpuoptflow=OFF -D BUILD_opencv_gpustereo=OFF -D BUILD_opencv_gpuwarping=OFF .. > /dev/null 2>&1
wait
make > /dev/null 2>&1
wait
make install > /dev/null 2>&1
wait
cd /home/pi
wait
rm opencv-3.4.3.zip
rm -rf opencv-3.4.3
wait
echo .................. Creating IRTSA Socket Server Service
# Create systemd script for the socket server to run on boot
echo [Unit] > /lib/systemd/system/IRTSAserver.service
echo Description=IRTSA Socket Server Service >> /lib/systemd/system/IRTSAserver.service
echo After=hostapd.service >> /lib/systemd/system/IRTSAserver.service
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
echo ................... Enabling Services
systemctl daemon-reload > /dev/null 2>&1
wait
systemctl enable hostapd > /dev/null 2>&1
systemctl enable dnsmasq > /dev/null 2>&1
systemctl enable ssh > /dev/null 2>&1
systemctl enable apache2 > /dev/null 2>&1
systemctl enable IRTSAserver > /dev/null 2>&1
wait
echo .................... Updating Hosts File and Hostname
# Change hostname for microcontroller from default
echo IRTSA-Controller > /etc/hostname
wait
# Create new hosts file
echo "127.0.0.1       localhost" > /etc/hosts
echo "::1             localhost ip6-localhost ip6-loopback" >> /etc/hosts
echo "ff02::1         ip6-allnodes" >> /etc/hosts
echo "ff02::2         ip6-allrouters" >> /etc/hosts
echo  >> /etc/hosts
echo "10.0.0.1        IRTSA-Controller" >> /etc/hosts
wait
echo ..................... Removing Swap Partition
# Remove Swap partition created for installation
swapoff /var/swap.1 > /dev/null 2>&1
wait
rm /var/swap.1
wait
echo ...................... DONE!! REBOOTING IN 5 SECONDS
sleep 1
echo ...................... DONE!! REBOOTING IN 4 SECONDS
sleep 1
echo ...................... DONE!! REBOOTING IN 3 SECONDS
sleep 1
echo ...................... DONE!! REBOOTING IN 2 SECONDS
sleep 1
echo "...................... DONE!! IT'S GO TIME BOIII!!!!"
sleep 1
reboot