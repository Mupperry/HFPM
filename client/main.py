import config
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as _paho

# pinNumber: pin that should be listened to
# returns the time (POSIX) for when a pulse was detected
def getNextPulse(pinNumber):
    # Start waiting for a pulse
    GPIO.wait_for_edge(pinNumber, GPIO.RISING)
    # When pulse is detected, return current time
    return time.time()

# Initialise GPIO, MQTT
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.pulsePin, GPIO.IN)
    mq.on_connect = on_connect
    mq.connect(config.mqttBroker, port=1883, keepalive=60)
    mq.loop_start()

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code", str(rc))

def publishTime(timeToPublish):
    print("Publishing:", timeToPublish)
    mq.publish(config.mqttTopic, payload=timeToPublish, qos=2, retain=False)

if __name__ == "__main__":
    mq = _paho.Client(client_id="", clean_session=True, userdata=None, protocol=_paho.MQTTv311, transport="tcp")
    setup()
    prevP = getNextPulse(config.pulsePin)
    while 1:
        try:
            currP = getNextPulse(config.pulsePin)
            publishTime(currP)
            prevP = currP    # Prepare previous timestamp for next run
            time.sleep(1)   # Basic ratelimiting
        except KeyboardInterrupt:
            mq.loop_stop()
            GPIO.cleanup()
            exit()