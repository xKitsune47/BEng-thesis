import urequests

def get_public_ip():
    """Pobiera publiczny adres IP"""
    try:
        response = urequests.get("http://checkip.amazonaws.com")
        ip = response.text.strip()
        response.close()
        return ip
    except Exception as e:
        print(f"❌ Błąd pobierania IP: {e}")
        return None

def get_timezone(ip):
    """Pobiera miasto na podstawie publicznego IP"""
    try:
        response = urequests.get(f"https://timeapi.io/api/timezone/ip?ipAddress={ip}")
        data = response.json()
        response.close()
        tz_name = data.get("timeZone")
        
        # if city_name:
        #     print(f"📍 Miasto: {city_name}")
        #     return city_name
        # else:
        #     print("❌ Brak miasta w odpowiedzi API")
        #     return None
        if tz_name:
            print(f"📍 timezone: {tz_name}")
            return tz_name
        else:
            print("❌ Brak miasta w odpowiedzi API")
            return None
    except Exception as e:
        print(f"❌ Błąd pobierania lokalizacji: {e}")
        return None