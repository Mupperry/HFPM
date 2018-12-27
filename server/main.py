import config
import powerCalc
import time
import paho.mqtt.client as _paho

mq = _paho.Client()
prevP = -1.0
currP = 0.0
accEnergy = 0.0

# Initialise MQTT
def setup():
    mq.on_connect = on_connect
    mq.on_message = on_message
    mq.loop_start()

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code", str(rc))
    print("Subscribing to", config.mqttTopicListen)
    mq.subscribe(config.mqttTopicListen)

def on_message(client, userdata, msg):
    # Check if this is the first message we have recieved since start
    if prevP == -1.0:
        prevP = float(msg.payload)
    else:
        currP = float(msg.payload)
        print("curP:", currP)
        print("prevP:", prevP)
        dt = currP - prevP
        print("dt:",dt)
        pow = powerCalc.timeToPower(deltaTime=dt, pulsesPerKwh=config.pulsesPerKwh)
        energy = float(powerCalc.pulseToEnergy(pulsesPerKwh=config.pulsesPerKwh))
        accEnergy += energy
        print("Power:",pow)
        print("Energy:", accEnergy)
        prevP = currP    # Prepare previous timestamp for next run

if __name__ == "__main__":  
    setup()
    while(1):
        time.sleep(3600*24)
