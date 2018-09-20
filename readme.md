# IRTSA Server

Note: This requires a RPI with a wifi card on it for the wireless access point aspect to work.

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
