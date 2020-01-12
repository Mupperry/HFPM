# Happy Fun Power Monitor
A simple way to read a power meter and collect usage data.

## Hardware

**Power meter**

The power meter in question needs to have an LED that pulses for every set amount of energy delivered. Common values are 100 or 1000 blinks/kWh.

**Raspberry Pi**

Any version of the raspberry pi that supports the ´RPi.GPIO´ Python library should work. Tested on model 1b.

**Sensor circuit**

A circuit that can detect when the LED on the power meter blinks is needed. This circuit will make a GPIO-pin on the Raspberry Pi go high or low depending on the state of the LED. A photoresistor and regular resistor can be used to create a voltage divider that achieves this. Consider adding a capacitor as a low-pass filter, otherwise EMI might cause problems when high current loads are switched on or off.

## Software
In order to make the readings from the power monitor available on other devices, **MQTT** is used, where the power monitor acts as a client. This means that we also need an MQTT broker. Have a look at [Mosquitto](https://mosquitto.org/) for a simple broker or [Thingsboard](https://thingsboard.io/) if you want more functionality in a single package.

The broker can probably be run on the same Raspberry Pi that is acting as the power monitor device.

## Set-up and Configuration
1. Clone this repository to the Raspberry Pi. `git` works well for this.

2. Change the values in the `config.py` file to suit your environment.

3. Run the monitor using `sudo python main.py`. Sudo is needed since we have to access GPIO, which by default means we need to be root.

4. You can now test your setup.

## Known issues
When trying to exit the client from a terminal using Ctrl-C, the client will only exit once a pulse arrives because of the blocking `wait_for_edge` call. Wait for a pulse to arrive or open another terminal session and kill the previous one manually.