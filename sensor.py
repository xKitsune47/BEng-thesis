import dht
import machine
import time

dht_pin = machine.Pin(4)
dht_sensor = dht.DHT22(dht_pin)

# MQ7 setup
mq7_pin = machine.ADC(machine.Pin(0))
mq7_pin.atten(machine.ADC.ATTN_11DB)  # full range: 0-3.3V

# MQ7 calibration values
R0 = 10  # sensor resistance in clean air 
RL = 10  # load resistance in kΩ

# TEMT6000 setup
temt6000_pin = machine.ADC(machine.Pin(1))
temt6000_pin.atten(machine.ADC.ATTN_11DB)
temt6000_pin.width(machine.ADC.WIDTH_12BIT)

# read CO PPM from MQ7 sensor
def read_mq7():
    try:
        # read analog value
        adc_value = mq7_pin.read()
        
        # convert to voltage
        voltage = (adc_value / 4095.0) * 3.3
        
        # calculate sensor resistance
        RS = ((3.3 * RL) / voltage) - RL
        
        # calculate ratio RS/R0
        ratio = RS / R0
        
        # convert to PPM (using MQ7 characteristic curve)
        # PPM = a * (RS/R0)^b
        a = 100
        b = -1.53
        ppm = (a * pow(ratio, b))/12
        
        return round(ppm, 1)
    except Exception as e:
        print(f"❌ Błąd MQ7: {e}")
        return None

# read temperature and humidity from DHT22
def read_dht():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except OSError:
        print("❌ Błąd DHT22!")
        return None, None
    
# read light value from TEMT6000
def read_temt6000():
    try:
        light_value = temt6000_pin.read()
        return light_value
    except Exception as e:
        print(f"❌ Błąd TEMT6000: {e}")
        return 4095