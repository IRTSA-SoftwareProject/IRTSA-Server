#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root by execution sudo ./pi_setup.sh"
  exit
fi

echo  " ________________________________"
echo "|                                |"
echo "|        Setup RPI Script!       |"
echo "|________________________________|"
echo 
echo 
echo .. Installing packages
apt-get install dnsmasq hostapd apache2 python -y > /dev/null 2>&1
wait

echo ... Configuring hostapd.conf
echo "#interface settings" > /etc/hostapd/hostapd.conf
echo interface=wlan0 >> /etc/hostapd/hostapd.conf
echo driver=nl80211 >> /etc/hostapd/hostapd.conf
echo hw_mode=g >> /etc/hostapd/hostapd.conf
echo channel=6 >> /etc/hostapd/hostapd.conf
echo ieee80211n=1 >> /etc/hostapd/hostapd.conf
echo auth_algs=1 >> /etc/hostapd/hostapd.conf
echo ignore_broadcast_ssid=0 >> /etc/hostapd/hostapd.conf
echo "#AP settings" >> /etc/hostapd/hostapd.conf
echo ssid=rpi-AP >> /etc/hostapd/hostapd.conf
echo wpa=2 >> /etc/hostapd/hostapd.conf
echo wpa_passphrase=rpiAPpw1 >> /etc/hostapd/hostapd.conf
echo wpa_key_mgmt=WPA-PSK >> /etc/hostapd/hostapd.conf
echo rsn_pairwise=CCMP >> /etc/hostapd/hostapd.conf

echo .... Configuring interfaces
echo allow-hotplug wlan0 > /etc/network/interfaces
echo iface wlan0 inet static >> /etc/network/interfaces
echo address 10.0.0.1 >> /etc/network/interfaces
echo netmask 255.255.255.0 >> /etc/network/interfaces
echo network 10.0.0.0 >> /etc/network/interfaces
echo broadcast 10.0.0.255 >> /etc/network/interfaces

echo ..... Editing dhcpcd.conf
echo denyinterfaces wlan0 >> /etc/dhcpcd.conf

echo ...... Configuring dnsmasq.conf
echo "#define interface that clients connect to" >> /etc/dnsmasq.conf
echo interface=wlan0 >> /etc/dnsmasq.conf
echo "#define server to use for dns" >> /etc/dnsmasq.conf
echo server=10.0.0.1 >> /etc/dnsmasq.conf
echo "#define lease IP range and lease duration" >> /etc/dnsmasq.conf
echo dhcp-range=10.0.0.2,10.0.0.50,255.255.255.0,24h >> /etc/dnsmasq.conf

echo ....... Creating irscans storage directory
mkdir /var/www/html/irscans
wait
chown -R pi:pi /var/www/html/irscans
echo ........ Editing apach2e.conf
echo "<Directory /var/www/html/irscans>" >> /etc/apache2/apache2.conf
echo Options +Indexes +FollowSymLinks >> /etc/apache2/apache2.conf
echo AllowOverride None >> /etc/apache2/apache2.conf
echo Require all granted >> /etc/apache2/apache2.conf
echo ServerSignature Off >> /etc/apache2/apache2.conf
echo "</Directory>" >> /etc/apache2/apache2.conf

echo ......... Creating index.html
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

echo ............ Enabling and Starting Services
systemctl enable hostapd > /dev/null 2>&1
systemctl start hostapd > /dev/null 2>&1
systemctl enable dnsmasq > /dev/null 2>&1
systemctl start dnsmasq > /dev/null 2>&1
systemctl enable ssh > /dev/null 2>&1
systemctl start ssh > /dev/null 2>&1
systemctl enable apache2 > /dev/null 2>&1
systemctl start apache2 > /dev/null 2>&1
wait

echo ............. Downloading IRTSA Python Demo
wget https://github.com/IRTSA-SoftwareProject/IRTSA-Server-master/archive/master.zip > /dev/null 2>&1
wait
echo .............. Unzipping
unzip master.zip > /dev/null 2>&1
wait
mkdir demo
wait
mv IRTSA-Server-master/src/demo/* demo/
wait
chown -R pi:pi demo
echo ............... Removing Files
rm master.zip
rm -rf IRTSA-Server
echo ................ Installing required python libraries
pip install imageio scipy > /dev/null 2>&1
echo ................. DONE!!