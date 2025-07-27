import uasyncio as asyncio
import time
from machine import Pin 

# import custom written functions
from display import display_text
from wifi_manager import connect_wifi
from sensor import read_dht, read_mq7
from location_service import get_public_ip, get_timezone
from config_manager import load_config, save_config
from time_sync import sync_api
from server import web_server
from weather_forecast import weather_today

# global variables
found_time = False
ip = None
timezone = None
RESET_BUTTON_PIN = 2
RESET_HOLD_TIME = 5
month_arr = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]
config = None

async def check_reset_button():
    # check if reset button is held during boot
    try:
        # initialize button with pullup pin
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
    global config
    accumulated_time_cur = 0
    accumulated_time_long = 0
    first_weather_fetch = True
    weather = None
    cur_weather = None

    while True:
        temp, hum = read_dht()
        co_ppm = read_mq7()
        cur_time = time.localtime()
        cur_city = config.get('city', '')
        formatted_time = f"{cur_time[2]} {month_arr[cur_time[1]-1]}, {cur_time[3]:02}:{cur_time[4]:02}"
        
        if cur_city != '':
            if accumulated_time_cur >= 1800 or first_weather_fetch:
                print(f"Fetching weather for {cur_city}")
                
                if accumulated_time_long >= 10800 or first_weather_fetch:
                    weather = await weather_today(cur_city, True)
                    cur_weather = weather
                    accumulated_time_long = 0
                    print("Fetched long-term weather")
                else: 
                    cur_weather = await weather_today(cur_city, False)
                    print("Fetched current weather")
                
                first_weather_fetch = False
                accumulated_time_cur = 0


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

        # display current, mix and max temp
        if cur_weather is not None:
            display_lines.append(f"Teraz: {round(cur_weather['curtemp'], 1)}C")

            if weather is not None:
                display_lines.append(f"{round(weather['mintemp'], 1)}C/{round(weather['maxtemp'], 1)}C")

        display_text(display_lines)
        accumulated_time_cur +=5
        accumulated_time_long +=5
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

async def handle_web_server_data(ssid, password, city):
    # handle data received from the web server
    await save_config(ssid, password, city)
    return True

# main ¯\_(ツ)_/¯
async def main():
    global timezone, config
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
        # connect to WiFi with SSID and passwd saved in config.txt file
        if await connect_wifi(ssid, password):
            if await locate_time():
                sync_api(timezone)
            await read_and_display()

if __name__ == "__main__":
    asyncio.run(main())
