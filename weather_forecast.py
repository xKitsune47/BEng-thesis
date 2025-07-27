import urequests
from config_manager import load_dotenv

async def weather_today(city, fetch_longterm = False):
    env = load_dotenv()
    API_URL = env.get('API_URL', '')
    API_KEY = env.get('API_KEY', '')

    data_longterm = None
    return_longterm = {"min": None, "max": None}

    # current weather
    response_current = urequests.get(f"{API_URL}/data/2.5/weather?q={city}&appid={API_KEY}")
    data_current = response_current.json()
    response_current.close()

    if fetch_longterm:
        response_longterm = urequests.get(f"{API_URL}/data/2.5/forecast?q={city}&cnt=8&appid={API_KEY}")
        data_longterm = response_longterm.json()
        response_longterm.close()

        lowest = None
        highest = None
        for element in data_longterm['list']:
            if lowest is None or element['main']['temp'] < lowest:
                lowest = element['main']['temp']

            if highest is None or element['main']['temp'] > highest:
                highest = element['main']['temp']

        return_longterm.update({"min": lowest})
        return_longterm.update({"max": highest})

        return {"curtemp": data_current['main']['temp'] - 273, "mintemp": return_longterm['min']-273, "maxtemp": return_longterm['max']-273}
    return {"curtemp": data_current['main']['temp'] - 273}