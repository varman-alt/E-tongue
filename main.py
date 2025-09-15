#Code to get the input of herb from hardware(sensors)
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ds18x20
import adafruit_onewire.bus

# -----------------------
# ADC Setup (ADS1115 for analog sensors)
# -----------------------
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Create analog input channels for each sensor
ph_channel = AnalogIn(ads, ADS.P0)           # pH sensor connected to A0
conductivity_channel = AnalogIn(ads, ADS.P1) # Conductivity sensor → A1
na_channel = AnalogIn(ads, ADS.P2)           # Na⁺ ISE sensor → A2
amperometric_channel = AnalogIn(ads, ADS.P3) # Amperometric sensor → A3

# -----------------------
# Temperature sensor setup (DS18B20 on GPIO4)
# -----------------------
ow_bus = adafruit_onewire.bus.OneWireBus(board.D4)
ds18 = adafruit_ds18x20.DS18X20(ow_bus, ow_bus.scan()[0])

# -----------------------
# Helper functions
# -----------------------
def read_ph():
    voltage = ph_channel.voltage
    # Convert voltage to pH (needs calibration curve)
    ph_value = 7 + ((voltage - 2.5) * 3.5)   # Example formula
    return round(ph_value, 2)

def read_conductivity():
    voltage = conductivity_channel.voltage
    # Convert voltage to conductivity (needs calibration)
    conductivity = voltage * 10              # Example scaling
    return round(conductivity, 2)

def read_na():
    voltage = na_channel.voltage
    # Convert voltage to Na⁺ concentration (calibration required)
    na_value = voltage * 100
    return round(na_value, 2)

def read_amperometric():
    voltage = amperometric_channel.voltage
    # Convert to arbitrary scale (depends on sensor calibration)
    amp_value = voltage * 1.0
    return round(amp_value, 2)

def read_temp():
    return round(ds18.temperature, 2)

# -----------------------
# Main loop
# -----------------------
if __name__ == "__main__":
    while True:
        ph = read_ph()
        cond = read_conductivity()
        na = read_na()
        amp = read_amperometric()
        temp = read_temp()

        print(f"pH={ph}, Conductivity={cond}, Na⁺={na}, Amperometric={amp}, Temp={temp} °C")

        time.sleep(2)


