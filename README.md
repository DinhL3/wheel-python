# Wheel of fortune: code for receiving data from Arduino and send to frontend via Websocket

## Installation
* Make sure all the components are properly set up, and Arduino is connected via USB.
* Clone this repo
* Install necessary libraries and environment (depending on Windows or Linux)
* Run the `read-serial.py` file
* If the file runs without error, the server is up and running and you can see the serial output received from Arduino

## Troubleshooting
* If there's no output received from Arduino, open Arduino IDE on the server machine, and check which USB port Arduino is connected to. In our case, using a Raspberry Pi, it is `/dev/ttyUSB0`, it might be different if you run this code on Windows
