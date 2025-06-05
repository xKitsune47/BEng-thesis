import urequests

# get public ip
def get_public_ip():
    try:
        response = urequests.get("http://checkip.amazonaws.com")
        ip = response.text.strip()
        response.close()
        return ip
    except Exception as e:
        print(f"❌ Błąd pobierania IP: {e}")
        return None

# get timezone based on public ip
def get_timezone(ip):
    try:
        response = urequests.get(f"https://timeapi.io/api/timezone/ip?ipAddress={ip}")
        data = response.json()
        response.close()
        tz_name = data.get("timeZone")

        if tz_name:
            print(f"📍 timezone: {tz_name}")
            return tz_name
        else:
            print("❌ Brak miasta w odpowiedzi API")
            return None
    except Exception as e:
        print(f"❌ Błąd pobierania lokalizacji: {e}")
        return None