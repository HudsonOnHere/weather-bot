import requests as r
from datetime import datetime
from bs4 import BeautifulSoup as bs

# in future versions, we will be able to handle geolocation data from telegram
# 45 e 1st street approx lat/long
latitude = '40.7239'
longitude = '-73.9899'

def API_okay():
    url = f"https://api.weather.gov/"
    response = r.get(url).json()
    
    if response['status'] == "OK":
        status = f"""api.weather.gov/ is available, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
        return status
    
    elif response['status'] != "OK":
        status = f"""api.weather.gov/ is unavailable, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
        return status

def get_alerts():
    # alerts_endpoint = f"https://api.weather.gov/alerts?point={latitude},{longitude}"
    alerts_endpoint = f"https://api.weather.gov/alerts/active?point={latitude},{longitude}"
    alerts_data = r.get(alerts_endpoint).json()
    
    alerts_data_list = ""
    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""

    for alert in alerts_data['features']:

        alerts_data_list += f"""{alert['properties']['headline']}:\n{alert['properties']['severity']}\n{alert['properties']['description']}\n\n"""

    if alerts_data_list == "":
        alerts_data_list = "Ain't no alerts, check Citizen if you want action.\n\n"

    else:
        alerts_data_list += f"""Idk here's some alerts or w/e:\n\n"""
    
    alerts_data_list += f"{footer}"

    return alerts_data_list

def get_forecast():
    forecast_endpoint = f"https://api.weather.gov/gridpoints/OKX/33,35/forecast"
    forecast_data = r.get(forecast_endpoint).json()

    forecast_data_list = ""

    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
   
    for forecast in forecast_data['properties']['periods']:
   
        if forecast['number'] in range(0,7):
   
            forecast_data_list += f"""{forecast['name']}: {forecast['temperature']}˚ {forecast['temperatureUnit']}\n{forecast['detailedForecast']}\n\n"""


    forecast_data_list += f"{footer}"

    return forecast_data_list

def get_hourly_forecast():
    hourly_endpoint = f"https://api.weather.gov/gridpoints/OKX/33,35/forecast/hourly"
    hourly_data = r.get(hourly_endpoint).json()

    hourly_data_list = ""

    footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""

    for hourly in hourly_data['properties']['periods']:

        start_time = datetime.fromisoformat(hourly['startTime']).strftime("%a %I:%M %p")

        if hourly['number'] in range(0,14):
            
            hourly_data_list += f"""{start_time}: {hourly['temperature']}˚ {hourly['temperatureUnit']}, {hourly['shortForecast']}\n{hourly['detailedForecast']}\n"""

    hourly_data_list += f"{footer}"

    return hourly_data_list

def get_info():
    url = f"https://github.com/HudsonOnHere/weather-bot/blob/main/README.md"
    data = r.get(url)
    soup = bs(data.text, 'html.parser')
    container = soup.find(class_="readme")
    tags = container.find_all('p')

    info_list = ""

    info_list += f"""{tags[0].text}\n\n{tags[4].text}\n\n{tags[5].text}"""

    return info_list