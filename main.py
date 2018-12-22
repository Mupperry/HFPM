import conf
import powerCalc
#import RPi.GPIO as GPIO
import time

# pinNumber: pin that should be listened to
# returns the time (POSIX) for when a pulse was detected
def getNextPulse(pinNumber):
    # Start waiting for a pulse
    #GPIO.wait_for_edge(pinNumber, GPIO.RISING)
    time.sleep(4)
    # When pulse is detected, return current time
    return time.time()

# Initialise GPIO etc.
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(conf.pulsePin, GPIO.IN)


if __name__ == "__main__":  
    #setup()
    prevP = getNextPulse(conf.pulsePin)
    currP = 0.0
    accEnergy = 0.0
    while 1:
        try:
            currP = getNextPulse(conf.pulsePin)
            print("curP:", currP)
            print("prevP:", prevP)
            dt = currP - prevP
            print("dt:",dt)
            pow = powerCalc.timeToPower(deltaTime=dt, pulsesPerKwh=conf.pulsesPerKwh)
            energy = powerCalc.pulseToEnergy(pulsesPerKwh=conf.pulsesPerKwh)
            accEnergy += energy
            print("Power:",pow)
            print("Energy:", accEnergy)
            prevP = currP    # Prepare previous timestamp for next run
        except KeyboardInterrupt:
            #GPIO.cleanup()
            exit()