# Happy Fun Power Monitor
A simple way to read a power meter and collect usage data.

## Hardware

**Power meter**
The power meter in question needs to have an LED* that pulses for every set amount of energy delivered. Common values are 100 or 1000 blinks/kWh.

*To be fair, this is not necessarily true. Some meters have a signal output that behaves in much the same way as the LED mentioned would. However, that involves accessing the inside of your fuse box, which might not be wise/legal depending on where you are and your qualifications.

**Raspberry Pi**
Any version of the Raspberry Pi that supports the 'RPi.GPIO' Python library should work. Tested on model 1b running Raspbian.

**Sensor circuit**
A circuit that can detect when the LED on the power meter blinks is needed. This circuit will make a GPIO-pin on the Raspberry Pi go high or low depending on the state of the LED. One crude but effective way of doing this is using a photo resistor and a regular resistor to create a voltage divider. Adding a capacitor as a low-pass filter is strongly recommended, otherwise EMI might cause false readings when high current loads are switched on or off (e.g. oven, water heater etc.). Below is similar to what has been running well for months.

<Insert diagram here>

There is some room for improvement here
- Use a potentiometer instead of a resistor for XXXX, so that the divider can be adjusted easily.
- Buffer the divider with a comparator, so that the Raspberry Pi sees a clean square wave instead of a slow rise and fall.

## Software
In order to make the readings from the power monitor available on other devices, **MQTT** is used, where the power monitor acts as a client. This means that we also need an MQTT broker. Have a look at [Mosquitto](https://mosquitto.org/) for a simple broker or [Thingsboard](https://thingsboard.io/) if you want more functionality in a single package.

The broker can be run on the same Raspberry Pi that is acting as the power monitor device, although this has not been tested.

## Set-up and Configuration
1. Clone this repository to the Raspberry Pi. 'git' works well for this.

2. Change the values in the 'config.py' file to suit your environment.

3. Run the monitor using 'sudo python main.py'. Sudo is needed since we have to access GPIO, which by default means we need to be root.

4. You can now test your setup. Temporarily bridging 3.3V to the GPIO in question can be useful for debugging.

When running day-to-day it can be useful to configure a service that handles stopping and starting the script during reboot for example.

## Known issues/limitations
The MQTT traffic is transmitted unencrypted, which is generally acceptable in a home LAN, but not so much over the internet. If you intend to send data to an MQTT broker on the internet rather than your LAN, modify this code accordingly to use encrypted MQTT transmission.

When trying to exit the client from a terminal using Ctrl-C, the client will only exit once a pulse arrives because of the blocking 'wait_for_edge' call. Wait for a pulse to arrive or open another terminal session and kill the previous one manually.