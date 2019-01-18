
# deltaTime: time elapsed in seconds since the previous pulse
# pulsesPerKwh: number of pulses made by powermeter per kwh used
# returns average power over the given time period in watts
def timeToPower (deltaTime, pulsesPerKWh):
    return 1000/(deltaTime*pulsesPerKwh/3600)

# returns the energy consumed for one pulse period in kwh
def pulseToEnergy (pulsesPerKWh):
    return 1/pulsesPerKwh