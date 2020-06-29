# Happy Fun Power Monitor
A simple way to read a power meter and collect usage data.

## Hardware

### Power meter
The power meter in question needs to have an LED* that pulses for every set amount of energy delivered. Common values are 100 or 1000 blinks/kWh.

*To be fair, this is not necessarily true. Some meters have a signal output that behaves in much the same way as the LED mentioned would. However, that involves accessing the inside of your fuse box, which might not be wise and/or legal depending on where you are and your qualifications.

### Raspberry Pi
Any version of the Raspberry Pi that supports the `RPi.GPIO` Python library should work. You also need the `paho-mqtt` library, which can be installed using pip. Tested on model 1b running Raspbian.  

### Sensor circuit
A circuit that can detect when the LED on the power meter blinks is needed. This circuit will make a GPIO-pin on the Raspberry Pi go high or low depending on the state of the LED. One crude but effective way of doing this is using a photo resistor and a regular resistor to create a voltage divider. Adding a capacitor as a low-pass filter is strongly recommended, otherwise EMI might cause false readings when high current loads are switched on or off (e.g. oven, water heater etc.). Below is similar to what has been running well for months.

![Circuit Diagram](https://raw.githubusercontent.com/Mupperry/HFPM/master/images/circuit_diagram.png)

These component values are not universally optimal by any stretch, they mostly serve as a starting point.
What the resistance of R2 should be mainly comes down to how much stray light the LDR (light dependant resistor) experiences. If there is little stray light, you can get away with using a high resistance (>10k), giving you a higher voltage at the GPIO when the LED pulses, making it easier to detect. In scenarios where stray light can not be avoided, it might be necessary to lower the resistance in order to make sure that the GPIO actually goes low when the LED is off.
The choice of C1 comes down to the amount of EMI affecting the circuit and how long the pulse from the LED lasts. Too low capacitance will cause false positives due to EMI, giving you unresonably high power and energy values. Too high capacitance on the other hand, will filter out the pulse from the LED, making it undetectable. Try something like 0.1 to 1 micro farad to begin with.

There is some room for improvement here:

- **Use a potentiometer** instead of a resistor for R2, so that the divider can be adjusted easily.
- Buffer the divider with a **comparator**, so that the Raspberry Pi sees a clean square wave instead of a slow rise and fall.

## Software
In order to make the readings from the power monitor available on other devices, **MQTT** is used, where the power monitor acts as a client. This means that we also need an MQTT broker. Have a look at [Mosquitto](https://mosquitto.org/) for a simple broker or [Thingsboard](https://thingsboard.io/) if you want more functionality in a single package.

The broker can be run on the same Raspberry Pi that is acting as the power monitor device, although this has not been tested.

## Set-up and Configuration
1. Clone this repository to the Raspberry Pi.

2. Change the values in the `config.py` file to suit your environment.

3. Run the monitor using `sudo python3 main.py`. Sudo is needed since we have to access GPIO, which by default means we need to be root.

4. You can now test your setup. Temporarily connecting the GPIO pin in question straight to 3.3V can be useful for debugging (don`t use 5V).

When running day-to-day it can be useful to configure a service that handles stopping and starting the script during reboot for example.

## Known issues/limitations
The MQTT traffic is transmitted unencrypted, which is generally acceptable in a home LAN, but not so much over the internet. If you intend to send data to an MQTT broker on the internet rather than your LAN, modify this code accordingly to use encrypted MQTT transmission.

For the energy metric there needs to be a sum function available on the system doing the logging, since we are just publishing e.g. 0.01 or 0.001 to the MQTT topic every time the LED blinks. This is not necessary for the power mnetric though.

If you are trying to figure out the average power use over some time, you **cannot** average the values from the **power** metric, you instead have to use the **energy** metric and calculate it from that. This is because the metrics are updated more often the higher the power use is, not just updated say every minute. This means that the higher power values will be overrepresented, scewing the average higher than it should be. This can probably be compensated for; if you have an idea for how to do that, please submit an issue.

When trying to exit the client from a terminal using Ctrl-C, the client will only exit once a pulse arrives because of the blocking `wait_for_edge` call. Wait for a pulse to arrive or open another terminal session and kill the previous one manually.