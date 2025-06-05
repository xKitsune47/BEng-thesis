async def load_config(filename='config.txt'):
    # load config from file
    try:
        with open(filename, 'r') as file:
            config = {}
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
            return config
    except:
        return {'ssid': '', 'passwd': '', 'city': ''}

async def save_config(ssid, password, city, filename='config.txt'):
    # save config to file
    with open(filename, 'w') as file:
        file.write(f"ssid={ssid}\npasswd={password}\ncity={city}")