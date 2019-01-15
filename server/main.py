import config
import powerCalc
import time
import paho.mqtt.client as _paho

mq = _paho.Client(client_id="", clean_session=True, userdata=None, protocol=_paho.MQTTv311, transport="tcp")
prevP = -1.0
currP = 0.0
accEnergy = 0.0

# Initialise MQTT
def setup():
    mq.on_connect = on_connect
    mq.on_message = on_message
    mq.connect(config.mqttBroker, port=1883, keepalive=60)
    mq.loop_start()

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code", str(rc))
    print("Subscribing to", config.mqttTopicListen)
    mq.subscribe(config.mqttTopicListen)

def on_message(client, userdata, msg):
    global prevP
    global currP
    global accEnergy
    timestamp = msg.payload.decode("utf-8")
    print("Recieved:", timestamp)
    timestamp = float(timestamp)
    # Check if this is the first message we have recieved since start
    if(prevP < 0):
        prevP = timestamp
    else:
        currP = timestamp
        dt = currP - prevP
        print("dt:",dt)
        power = powerCalc.timeToPower(deltaTime=dt, pulsesPerKwh=config.pulsesPerKwh)
        energy = float(powerCalc.pulseToEnergy(pulsesPerKwh=config.pulsesPerKwh))
        accEnergy += energy
        print("Power:",power)
        print("Energy:", accEnergy)
        prevP = currP    # Prepare previous timestamp for next run
        publishPowerEnergy(power, accEnergy)


def publishPowerEnergy(power,energy):
    fPower = int(round(power, 0))
    fEnergy = round(energy, 2)
    mq.publish(config.mqttTopicPublishPower, payload=fPower, qos=0, retain=True)
    mq.publish(config.mqttTopicPublishEnergy, payload=fEnergy, qos=0, retain=True)

if __name__ == "__main__":  
    setup()
    while(1):
        time.sleep(3600*24)
