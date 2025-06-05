import dht
import machine
import time

# Initialize sensors
dht_pin = machine.Pin(4)
dht_sensor = dht.DHT22(dht_pin)

# MQ7 setup on ADC pin
mq7_pin = machine.ADC(machine.Pin(1))  # Use appropriate ADC pin
mq7_pin.atten(machine.ADC.ATTN_11DB)  # Full range: 0-3.3V

# MQ7 calibration values
R0 = 10  # Sensor resistance in clean air (you need to calibrate this)
RL = 10  # Load resistance in kΩ

def read_mq7():
    """Reads CO PPM from MQ7 sensor"""
    try:
        # Read analog value
        adc_value = mq7_pin.read()
        
        # Convert to voltage
        voltage = (adc_value / 4095.0) * 3.3
        
        # Calculate RS (sensor resistance)
        RS = ((3.3 * RL) / voltage) - RL
        
        # Calculate ratio RS/R0
        ratio = RS / R0
        
        # Convert to PPM (using MQ7 characteristic curve)
        # PPM = a * (RS/R0)^b
        # These values need to be calibrated for your specific sensor
        a = 100
        b = -1.53
        ppm = a * pow(ratio, b)
        
        return round(ppm, 1)
    except Exception as e:
        print(f"❌ Błąd odczytu MQ7: {e}")
        return None

def read_dht():
    """Reads temperature and humidity from DHT22"""
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except OSError:
        print("❌ Błąd odczytu DHT22!")
        return None, None