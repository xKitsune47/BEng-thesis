import sh1106
import machine

i2c = machine.SoftI2C(scl=machine.Pin(6), sda=machine.Pin(5))
oled = sh1106.SH1106_I2C(128, 64, i2c)

def display_text(lines):
    oled.rotate(180)
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 10)
    oled.show()