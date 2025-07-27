# ESP32-C3 Environmental Monitoring Station - BEng thesis

A comprehensive IoT indoor monitoring system built for ESP32-C3 microcontroller as part of a Bachelor's of Engineering degree thesis. This project creates a smart weather station that monitors indoor air quality, displays real-time weather data, and provides web-based configuration capabilities.

## Features

### Environmental Monitoring

- **Temperature & Humidity**: DHT22 sensor for indoor climate monitoring
- **Air Quality**: MQ7 sensor for carbon monoxide (CO) detection with PPM readings
- **Light Sensing**: TEMT6000 ambient light sensor for automatic display brightness adjustment

### Display System

- **OLED Display**: SH1106 128x64 OLED screen with automatic brightness control
- **Real-time Data**: Displays current time, temperature, humidity, CO levels, and weather forecasts
- **Polish Localization**: Month names and interface in Polish language

### Weather Integration

- **OpenWeatherMap API**: Fetches current weather and 24-hour forecasts
- **Location-based**: Automatic city detection using IP geolocation
- **Smart Caching**: Intelligent data fetching to minimize API calls (30min current, 3h forecast)

### Location & Time Services

- **IP Geolocation**: Automatic public IP detection for timezone identification
- **Time Synchronization**: Real-time clock sync via TimeAPI with timezone awareness
- **Geographic Context**: Location-aware weather and time display

### Network & Configuration

- **WiFi Management**: Automatic connection with fallback to Access Point mode
- **Web Configuration**: Browser-based setup interface when no WiFi credentials exist
- **Reset Functionality**: Hardware button for factory reset (5-second hold)
- **Auto-provisioning**: Creates ESP32-C3-AP hotspot for initial setup

### Smart Features

- **Asynchronous Operation**: Non-blocking sensor readings and network operations
- **Time Synchronization**: API-based time sync with timezone detection
- **Modular Design**: Clear separation across multiple modules

## Hardware Requirements

- ESP32-C3 microcontroller
- SH1106 OLED Display (I2C: SCL=GPIO6, SDA=GPIO5)
- DHT22 Temperature/Humidity sensor (GPIO4)
- MQ7 Carbon Monoxide sensor (GPIO0)
- TEMT6000 Light sensor (GPIO1)
- Reset button (GPIO2)

## Software Architecture

The project is organized into modular components:

- **`main.py`**: Main application loop and coordinator
- **`sensor.py`**: Hardware sensor interfaces (DHT22, MQ7, TEMT6000)
- **`display.py`**: OLED display management with brightness control
- **`wifi_manager.py`**: WiFi connection and network management
- **`server.py`**: Web server for Access Point configuration mode
- **`weather_forecast.py`**: OpenWeatherMap API integration
- **`location_service.py`**: IP-based geolocation and timezone detection
- **`time_sync.py`**: Network time synchronization with timezone support
- **`config_manager.py`**: Configuration file and environment variable handling

## Configuration

The system uses two configuration files:

- **`config.txt`**: WiFi credentials and city settings
- **`.env`**: API keys and service URLs

## Development Tools

### PowerShell Upload Script

The project includes `upload.ps1`, a PowerShell automation script that streamlines the development workflow by:

- **Batch Upload**: Automatically uploads all Python files to the ESP32-C3 via mpremote
- **Silent Operation**: Suppresses verbose output for cleaner development experience
- **Sequential Processing**: Uploads files one by one with proper timing delays
- **Auto-Connect**: Establishes terminal connection after upload completion

Usage: `.\upload.ps1` from the project directory

This script significantly reduces development time by eliminating the need to manually upload each file during testing and deployment phases.

## Getting Started

1. **Hardware Setup**: Connect sensors according to the pin configuration
2. **Initial Boot**: Power on the ESP32-C3
3. **Configuration**: If no WiFi config exists, connect to "ESP32-C3-AP" (password: 12345678)
4. **Web Setup**: Navigate to http://192.168.4.1 and enter WiFi credentials
5. **Operation**: Device will restart and begin normal monitoring operation

## API Dependencies

- **OpenWeatherMap**: Weather data and forecasts
- **TimeAPI.io**: Real-time clock synchronization and timezone data
- **AWS CheckIP**: Public IP address detection for location services

## Reset Function

Hold the reset button (GPIO2) for 5 seconds during startup to clear all configuration and return to setup mode.

This project demonstrates practical IoT development, combining multiple sensors, web interfaces, and cloud services into a cohesive environmental monitoring solution.
