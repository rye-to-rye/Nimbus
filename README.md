# 🌤️ Nimbus Weather App

A beautiful, modern weather application built with Python and PyQt5 that provides real-time weather information for cities worldwide.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue) ![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green) ![OpenWeather](https://img.shields.io/badge/API-OpenWeather-orange)

## ✨ Features

- **🌍 Global City Search** - Get weather for any city worldwide
- **🎨 Beautiful UI** - Modern gradient background with glass-morphism cards
- **📊 Comprehensive Data** - Temperature, humidity, wind speed, feels-like temperature, and weather descriptions
- **⚡ Real-time Updates** - Live weather data from OpenWeather API
- **🔄 Async Loading** - Non-blocking background data fetching with loading animations
- **📱 Responsive Design** - Adapts to different screen sizes
- **🎯 Error Handling** - Robust error handling with user-friendly messages

## 🛠️ How It's Built

### Architecture
The app follows a modular architecture with three main components:

1. **`WeatherInfo` Class** - Handles all weather data operations
2. **`GeoInfo` Class** - Manages geolocation data (city, state, country coordinates)
3. **PyQt5 GUI** - Modern user interface with smooth animations

### Key Technologies

- **Python 3.6+** - Core programming language
- **PyQt5** - GUI framework for the desktop application
- **OpenWeather API** - Weather data provider
- **Requests** - HTTP library for API calls
- **QThread** - Background processing for non-blocking UI

### Core Components

#### Weather Data Layer (`WeatherInfo`)
```python
- Fetches real-time weather data from OpenWeather API
- Handles geolocation conversion (city name → coordinates)
- Provides formatted weather metrics (temp, humidity, wind, etc.)
- Implements comprehensive error handling
