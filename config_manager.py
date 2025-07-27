# load config from config.txt
async def load_config(filename='config.txt'):
    try:
        with open(filename, 'r') as file:
            config = {}
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
            return config
    except:
        return {'ssid': '', 'passwd': '', 'city': ''}

# save config to config.txt
async def save_config(ssid, password, city, filename='config.txt'):
    with open(filename, 'w') as file:
        file.write(f"ssid={ssid}\npasswd={password}\ncity={city}")

# load env variables from .env
def load_dotenv(filename='.env'):
    env_vars = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().strip('"\'')
                    value = value.strip().strip('"\'')
                    env_vars[key] = value
    except OSError:
        print(f"Nie można odczytać pliku {filename}")
    return env_vars