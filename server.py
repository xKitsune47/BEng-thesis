import network
import socket
from machine import Pin
import time
import utime
import os
import asyncio

# AP config
AP_SSID = 'ESP32-C3-AP'
AP_PASSWORD = '12345678'  
AP_AUTHMODE = network.AUTH_WPA_WPA2_PSK

# HTML content
html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WiFi details form</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <div class="container">
            <h2 style="text-align: center;">WiFi details form</h2>
            <div class="status">
                AP Status: Active
            </div>
            <form method="POST">
                <div class="form-group">
                    <label for="ssid">WiFi SSID:</label>
                    <input type="text" id="ssid" name="ssid" required>
                </div>
                <div class="form-group">
                    <label for="passwd">WiFi password:</label>
                    <input type="text" id="passwd" name="passwd" required>
                </div>

                <div class="form-group">
                    <label for="city">City (optional):</label>
                    <input type="text" id="city" name="city">
                </div>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
'''

def setup_ap():
    """set up ESP32-C3 as AP"""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=AP_AUTHMODE)
    
    while not ap.active():
        time.sleep(1)
        print('Waiting for AP to be active...')
    
    print('Access Point Created')
    print('SSID:', AP_SSID)
    print('Password:', AP_PASSWORD)
    print('Network Config:', ap.ifconfig())
    return ap.ifconfig()[0]  # return ip for connecting

def parse_form_data(request_data):
    try:
        form_data_str = request_data.split('\r\n\r\n')[1]
        fields = form_data_str.split('&')
        data = {}
        for field in fields:
            key, value = field.split('=')
            value = value.replace('+', ' ')
            data[key] = value
        return data
    except:
        return None

async def web_server(callback=None):
    ip = setup_ap()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False)
    
    print(f'Web server started at http://{ip}')
    
    while True:
        try:
            try:
                conn, addr = s.accept()
            except OSError:
                await asyncio.sleep(0.1)
                continue
                
            print('Client connected from:', addr)
            try:
                request = conn.recv(1024).decode()
            except OSError:
                conn.close()
                continue
            
            if request.startswith('POST'):
                # handle form submission
                form_data = parse_form_data(request)
                if form_data:
                    print('Received form data:')
                    ssid = form_data.get('ssid', '')
                    password = form_data.get('passwd', '')
                    city = form_data.get('city', '')
                    print('SSID:', ssid)
                    print('Password:', password)
                    print('City:', city)

                    if callback:
                        await callback(ssid, password, city)
                    
                    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
                    response += '<html><body>'
                    response += '<div>'
                    response += '<h2>Data received successfully!</h2>'
                    response += '<p>Device will restart in 5 seconds...</p>'
                    response += '</div></body></html>'
                    
                    conn.send(response.encode())
                    conn.close()
                    
                    await asyncio.sleep(5)
                    return  # shut down web server
                else:
                    response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
            else:
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
            
            conn.send(response.encode())
            conn.close()
            
        except Exception as e:
            print('Error:', e)
            try:
                conn.close()
            except:
                pass
        
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(web_server())