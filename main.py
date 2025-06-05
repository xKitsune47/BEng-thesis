import uasyncio as asyncio
import time
from machine import Pin 

# import custom written functions
from display import display_text
from wifi_manager import connect_wifi
from sensor import read_dht, read_mq7
from location_service import get_public_ip, get_timezone
from config_manager import load_config, save_config
from time_sync import sync_ntp, sync_api
from server import web_server

# global variables
found_time = False
ip = None
timezone = None
RESET_BUTTON_PIN = 2
RESET_HOLD_TIME = 5
month_arr = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]

async def check_reset_button():
    """check if reset button is held during boot"""
    try:
        # Initialize button with pull-up
        reset_btn = Pin(RESET_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        
        # check if button is pressed during boot
        if not reset_btn.value():
            print("Button pressed at boot")
            start = time.time()
            
            # countdown while button is pressed
            while not reset_btn.value():
                elapsed = time.time() - start
                remaining = RESET_HOLD_TIME - elapsed
                
                if remaining > 0:
                    display_text([
                        "Hold to Reset",
                        f"Time: {remaining:.1f}s"
                    ])
                    await asyncio.sleep(0.1)
                else:
                    print("Reset triggered")
                    display_text(["Resetting..."])
                    await save_config("", "")
                    await asyncio.sleep(1)
                    import machine
                    machine.reset()
            
            print("Button released before reset")
    except Exception as e:
        print(f"Reset button error: {str(e)}")

# function to read data and display on the screen
async def read_and_display():
    global found_time
    
    while True:
        temp, hum = read_dht()
        co_ppm = read_mq7()
        cur_time = time.localtime()
        print(cur_time)
        formatted_time = f"{cur_time[2]} {month_arr[cur_time[1]-1]}, {cur_time[3]:02}:{cur_time[4]:02}"

        # display lines array
        display_lines = []

        # display date and time
        display_lines.append(f"{formatted_time}")

        # display temperature and humidity
        if temp is not None and hum is not None:
            display_lines.extend([
                f"Temp: {temp}C",
                f"Wilg: {hum}%",
            ])
        else:
            display_lines.append("❌ Blad DHT22")

        # display carbon oxide PPM
        if co_ppm is not None:
            display_lines.append(f"CO: {co_ppm}ppm")
        else:
            display_lines.append("❌ Blad MQ7")

        display_text(display_lines)
        await asyncio.sleep(5)

async def locate_time():
    # locate timezone based on public IP
    global found_time, timezone
    
    while not found_time:
        ip = get_public_ip()
        if ip:
            tz = get_timezone(ip)
            if tz:
                timezone = tz
                found_time = True
                return True
        await asyncio.sleep(10)

# main ¯\_(ツ)_/¯
async def handle_web_server_data(ssid, password, city):
    # handle data received from the web server
    await save_config(ssid, password, city)
    return True

async def main():
    global timezone
    # RESET CONFIG.TXT FILE
    await check_reset_button()

    # load Wi-Fi credentials from config
    config = await load_config()
    ssid = config.get('ssid', '')
    password = config.get('passwd', '')

    if not ssid or not password:
        # if no credentials, start web server in AP mode
        display_text([
            "SETUP MODE",
            "SSID:ESP32-C3-AP",
            "PASSWD:12345678",
            "URL:192.168.4.1"
        ])
        await web_server(handle_web_server_data)
        # restart after receiving form data
        import machine
        machine.reset()
    else:
        # connect to WiFi with SSID and passwd in the config.txt file
        print(f"timezone! {timezone}")
        if await connect_wifi(ssid, password):
            if await locate_time():
                sync_ntp() or sync_api(timezone)
            await read_and_display()

if __name__ == "__main__":
    asyncio.run(main())

"""
- dodac obsluge ze jesli podane miasto w configu to pobiera dane z api openweatherapi, dodac funkcjonalnosc w mainie i w weather_forecast.py
- dodac obsluge TEMT6000 które mierzy natężenie światła i dostosowuje jasność wyświetlacza
"""