async def load_config(filename='config.txt'):
    """Ładuje konfigurację z pliku"""
    try:
        with open(filename, 'r') as file:
            config = {}
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
            return config
    except:
        return {'ssid': '', 'passwd': ''}

async def save_config(ssid, password, filename='config.txt'):
    """Zapisuje konfigurację do pliku"""
    with open(filename, 'w') as file:
        file.write(f"ssid={ssid}\npasswd={password}")