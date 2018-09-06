# pi_setup.sh Instructions

Note: This requires a RPI with a wifi card on it for the wireless access point aspect access point part to work.

## Installation

To setup the pi install rasbian stretch lite (no gui) from:
- https://www.raspberrypi.org/downloads/raspbian/

once installed download the pi_setup.sh script, make it executable then run it with the following commands:

- wget https://raw.githubusercontent.com/IRTSA-SoftwareProject/IRTSA-Server/master/src/pi_setup.sh
- chmod +x pi_setup.sh
- sudo ./pi_setup.sh

The raspberry pi will then be setup in access point mode and can be connected to with the IP address 10.0.0.1 either through a web browser or a ssh client (putty)

## Running the python script

To run the python demo script in the demo/ directory with:

- cd demo/

Then run the script passing in an argument for the desired name of the saved file with:

- python read_ris.py filename
