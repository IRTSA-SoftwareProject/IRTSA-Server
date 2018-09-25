# IRTSA Server

Note: This requires a RPI with a wifi card on it for the wireless access point aspect to work.

## Installation

To setup the server follow the instructions for either a RPI 3/3B+ or Virtual Machine depending on your test environment

### Raspberry Pi 3/3B+ Setup

Follow these steps in order to install and setup a Raspberry Pi as the IRTSA server:

- Download the Rasbian Stretch Lite image from: https://downloads.raspberrypi.org/raspbian_lite_latest
- Install this image onto a Raspberry Pi
- Connect the Raspberry Pi to the internet through the **ethernet interface**.
- download the setup script with the command: `wget https://raw.githubusercontent.com/IRTSA-SoftwareProject/IRTSA-Server/master/src/pi_setup.sh`
- Make the file executable with the command: `chmod +x pi_setup.sh`
- Execute the script with the command: `sudo ./pi_setup.sh`

This will setup the Raspberry Pi as in access point mode with the SSID of **rpi-AP** and password of **rpiAPpw1** and can be connected to with the IP address 10.0.0.1 either through a web browser or a ssh client (putty).


### Virtual Machine Setup

Follow these steps in order to install and setup a Virtual Machine as the IRTSA server:

- Download the Debian Stretch with Raspberry Pi Desktop image from: https://downloads.raspberrypi.org/rpd_x86_latest
- Create a new virtual machine with atleast 512MB of memory with networking set to NAT to connect to the internet
- Install the iso that was downloaded.
- Once installed Rasbian will be installed with a GUI.
- Open the terminal by clicking the terminal icon on the taskbar at the top of the screen
- Download the setup script with the command: `wget https://raw.githubusercontent.com/IRTSA-SoftwareProject/IRTSA-Server/master/src/pi_setup_vm.sh`
- Make the file executable with the command: `chmod +x pi_setup_vm.sh`
- Execute the script with the command: `sudo ./pi_setup_vm.sh`
- The Virtual Machine will then reboot and be setup as a server.
- Change the networking to Custom: vmnet1
- Open the virtual network editor in VMware from Edit > Virtual Network Editor.
- Ensure that the Host-Only radio box is checked and the Use Local DHCP check box is unticked.

*The following are Optional steps to follow which are only to be used when wanting the Android SDK Emulator to communicate with the Virtual Machine*
- Open your adapter settings on your host machine.
- Disable any wireless or ethernet adapters that are not **VMware Network Adapter VMnet1** and ensure that VMnet1 is Enabled.
- The VMnet 1 adapter will now get an IP address for the Virtual Machines DHCP server and the Emulator will be able to connect to the server with the IP 10.0.0.1.
- **Note: Once communication is not needed reverse these optional steps by activating your Wireless and/or Ethernet Adapters for your host machine to connect to the internet again**

This will setup a Virtual Machine to act as a Raspberry Pi server which will have the IP address of 10.0.0.1 which can be accessed by the Android SDK Emulator provided networking with the Virtual Network Editor in VMware has been setup correctly.

## Running the python script

To run the python demo script in the demo/ directory with:

- cd demo/

Then run the script passing in an argument for the desired name of the saved file with:

- python read_ris.py filename

## Running the websocket

The mobile app connects to the server using a websocket. If you don't have access to a RaspberryPi, 
you can run the code on a regular computer and get the mobile app to connect to that instead.

Start your virtual environment. This is optional but makes it easier to use different python 
versions in different projects. This command requires python3.7 to be installed on your system.

    virtualenv -p  $(which python3) server
    
Install the required packages

    pip install -r requirements.txt
    
Start the server. The server requires python3.7, if you created a virtual environment and it is 
active, the python version would have been configured for you automatically. If not, you'll have to
make sure `python --version` says 3.7 or try using `python3` in the command below.

    python -m server
    
This should print out a message indicating that the server is running and the address to connect to 
from the client.
