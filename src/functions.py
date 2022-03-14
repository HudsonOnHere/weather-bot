import requests as r
from datetime import datetime

class Misc_Functions:
    def __init__(self):
        pass

    def API_status(self):
        url = f"https://api.weather.gov/"
        response = r.get(url).json()
        
        if response['status'] == "OK":
            status = f"""api.weather.gov/ is available, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
            return status
        
        elif response['status'] != "OK":
            status = f"""api.weather.gov/ is unavailable, and returning status code: {response['status']}\n\nLast checked: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
            return status

    def legal_info(self):
        url = f"https://raw.githubusercontent.com/HudsonOnHere/weather-bot/main/LICENSE"
        return r.get(url).text


class Geo_Functions:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def update_geocoding(self):
        points = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
        points_data = r.get(points).json()
        self.grid_id = points_data['properties']['gridId']
        self.grid_x = points_data['properties']['gridX']
        self.grid_y = points_data['properties']['gridY']

    def get_alerts(self):
        endpoint = f"https://api.weather.gov/alerts/active?point={self.latitude},{self.longitude}"
        alerts_data = r.get(endpoint).json()
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
        
    def get_forecast(self):
        endpoint = f"""https://api.weather.gov/gridpoints/{self.grid_id}/{self.grid_x},{self.grid_y}/forecast"""
        forecast_data = r.get(endpoint).json()
        forecast_data_list = ""
        footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""

        for forecast in forecast_data['properties']['periods']:

            if forecast['number'] in range(0,7):

                forecast_data_list += f"""{forecast['name']}: {forecast['temperature']}˚ {forecast['temperatureUnit']}\n{forecast['detailedForecast']}\n\n"""

        forecast_data_list += f"{footer}"
        
        return forecast_data_list

    def get_hourly_forecast(self):
        endpoint = f"""https://api.weather.gov/gridpoints/{self.grid_id}/{self.grid_x},{self.grid_y}/forecast/hourly"""
        hourly_data = r.get(endpoint).json()
        hourly_data_list = ""
        footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""

        for hourly in hourly_data['properties']['periods']:

            if hourly['number'] in range(0,13):

                hourly_data_list += f"""{hourly['name']}: {hourly['temperature']}˚ {hourly['temperatureUnit']}\n{hourly['detailedForecast']}\n\n"""

        hourly_data_list += f"{footer}"
        
        return hourly_data_list
