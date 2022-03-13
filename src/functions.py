
import requests as r
from datetime import datetime
from bs4 import BeautifulSoup as bs


FORECAST_GRID = 0
GRID_X = 0
GRID_Y = 0


def API_status():
    url = f"https://api.weather.gov/"
    response = r.get(url).json()
    
    if response['status'] == "OK":
        status = f"""api.weather.gov/ is available, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
        return status
    
    elif response['status'] != "OK":
        status = f"""api.weather.gov/ is unavailable, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
        return status


def geocoding(LATITUDE, LONGITUDE):
    points = f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}"
    points_data = r.get(points).json()

    global FORECAST_GRID
    global GRID_X
    global GRID_Y

    FORECAST_GRID = points_data['properties']['gridId']
    GRID_X = points_data['properties']['gridX']
    GRID_Y = points_data['properties']['gridY']
    
    print(f"Grid ID: {FORECAST_GRID}")
    print(f"Grid X: {GRID_X}")
    print(f"Grid Y: {GRID_Y}")

    return FORECAST_GRID, GRID_X, GRID_Y



def get_alerts(LATITUDE, LONGITUDE):
    alerts_endpoint = f"https://api.weather.gov/alerts/active?point={LATITUDE},{LONGITUDE}"
    alerts_data = r.get(alerts_endpoint).json()
    
    alerts_data_list = ""

    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
    no_alerts_msg = f"""There are currently no alerts in your area, that's probably a good thing.\n\n"""

    for alert in alerts_data['features']:

        alerts_data_list += f"""{alert['properties']['headline']}:\nSeverity: {alert['properties']['severity']}\n\n{alert['properties']['description']}\n\n"""

    if alerts_data_list == "":
        alerts_data_list += f"""{no_alerts_msg}\n\n{footer}"""

    else:
        alerts_data_list += f"""{footer}"""

    return alerts_data_list


def get_forecast(FORECAST_GRID, GRID_X, GRID_Y):
    forecast_endpoint = f"""https://api.weather.gov/gridpoints/{FORECAST_GRID}/{GRID_X},{GRID_Y}/forecast"""
    forecast_data = r.get(forecast_endpoint).json()

    forecast_data_list = ""

    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
   
    for forecast in forecast_data['properties']['periods']:
   
        if forecast['number'] in range(0,7):
   
            forecast_data_list += f"""{forecast['name']}: {forecast['temperature']}˚ {forecast['temperatureUnit']}\n{forecast['detailedForecast']}\n\n"""

    forecast_data_list += f"{footer}"

    return forecast_data_list


def get_hourly_forecast(FORECAST_GRID, GRID_X, GRID_Y):
    hourly_endpoint = f"https://api.weather.gov/{FORECAST_GRID}/{GRID_X},{GRID_Y}/forecast/hourly"
    hourly_data = r.get(hourly_endpoint).json()

    hourly_data_list = ""

    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""

    for hourly in hourly_data['properties']['periods']:

        start_time = datetime.fromisoformat(hourly['startTime']).strftime("%a %I:%M %p")

        if hourly['number'] in range(0,14):
            
            hourly_data_list += f"""{start_time}: {hourly['temperature']}˚ {hourly['temperatureUnit']}, {hourly['shortForecast']}\n{hourly['detailedForecast']}\n"""

    hourly_data_list += f"{footer}"

    return hourly_data_list


def legal_info():

    url = f"https://raw.githubusercontent.com/HudsonOnHere/weather-bot/main/LICENSE"
    data = r.get(url)
    soup = bs(data.text, 'html.parser')

    return soup


