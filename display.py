import sh1106
import machine
from sensor import read_temt6000

i2c = machine.SoftI2C(scl=machine.Pin(6), sda=machine.Pin(5))
oled = sh1106.SH1106_I2C(128, 64, i2c)

def display_text(lines):
    brightness = round((read_temt6000() / 4095) * 255)
    print(f"🔦brightness: {brightness}")

    if brightness < 4:
        oled.rotate(180)
        oled.fill(0)
        for i, line in enumerate(lines):
            oled.text(line, 0, i * 10)
        oled.contrast(4)
        oled.show()
    else:
        oled.rotate(180)
        oled.fill(0)
        for i, line in enumerate(lines):
            oled.text(line, 0, i * 10)
        oled.contrast(brightness)
        oled.show()
