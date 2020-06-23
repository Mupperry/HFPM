# Leave as 127.0.0.1 if the broker runs on the same system as the power monitor.
mqttBroker = "127.0.0.1"

mqttTopic = "topic/to/publish/to"

# What pin to listen for pulses on (according to the "Board" pin numbering scheme)
pulsePin = 11

# How many pulses the power meter produces per kWh used (normally written on power meter, e.g. imp/kWh)
pulsesPerKWh = 100

# Needed if using Thingsboard. Called "username" in MQTT-speak
accessToken = ""

# Minimum time between pulses in seconds. Used for basic rate limiting, can be lowered if measuring 
# power >14kW to avoid missing pulses. If you are unsure, leave as is. 
rateLimitTime = 0.25