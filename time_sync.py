import ntptime
import machine
import urequests
import time

def sync_ntp():
    return False
    try:
        print("⏳ Pobieranie czasu z NTP...")
        ntptime.settime()
        return True
    except Exception as e:
        print(f"❌ Błąd synchronizacji NTP: {e}")
        return False

def sync_api(timezone):
    try:
        response = urequests.get(f"https://timeapi.io/api/time/current/zone?timeZone={timezone}")
        data = response.json()
        response.close()

        if data:
            year = int(data.get("year") or 0)
            month = int(data.get("month") or 0)
            day = int(data.get("day") or 0)
            hour = int(data.get("hour") or 0)
            minute = int(data.get("minute") or 0)
            second = int(data.get("seconds") or 0)
            machine.RTC().datetime((year, month, day, 0, hour, minute, second, 0))
            return True
    except Exception as e:
        print(f"❌ Błąd pobierania czasu z API: {e}")
    return False
