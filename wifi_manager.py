import network
import uasyncio as asyncio

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
connected = False

async def connect_wifi(ssid, password):
    """Łączy się z Wi-Fi"""
    global connected
    wlan.connect(ssid, password)

    for _ in range(10):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f"✅ Połączono! IP: {ip}")
            connected = True
            return True
        print("⏳ Próba połączenia...")
        await asyncio.sleep(1)

    print("❌ Błąd połączenia!")
    connected = False
    return False