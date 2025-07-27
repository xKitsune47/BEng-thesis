import network
import uasyncio as asyncio

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

async def connect_wifi(ssid, password):
    wlan.connect(ssid, password)

    for _ in range(10):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f"✅ Połączono! IP: {ip}")
            return True
        print("⏳ Próba połączenia...")
        await asyncio.sleep(2)

    print("❌ Błąd połączenia!")
    return False