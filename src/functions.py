import requests as r
from datetime import datetime

class Static_Functions:
    def __init__(self):
        pass

    def API_status(self):
        url = f"https://api.weather.gov/"
        response = r.get(url).json()

        if response['status'] == 'OK':
            return True
        else:
            return response['status']

    def legal_info(self):
        url = f"https://raw.githubusercontent.com/HudsonOnHere/weather-bot/main/LICENSE"
        return r.get(url).text


class Location_Functions:
    def __init__(self):
        self.grids = {}
        self.coordinates = {}

        self.grids['default'] = {
            'grid_id': 'OKX',
            'grid_x': '33',
            'grid_y': '36',
        }

        self.coordinates['default'] = {
            'latitude': '40.7560',
            'longitude': '-73.9867',
        }


    def update_geocoding(self, user_id, latitude, longitude):
        points = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_data = r.get(points).json()

        self.coordinates[user_id] = {
            'latitude': latitude,
            'longitude': longitude,
        }

        self.grids[user_id] = {
            'grid_id': points_data['properties']['gridId'],
            'grid_x': points_data['properties']['gridX'],
            'grid_y': points_data['properties']['gridY'],
        }

    def get_forecast(self, user_id):
        user_grid = self.grids[user_id]
        endpoint = f"""https://api.weather.gov/gridpoints/{user_grid['grid_id']}/{user_grid['grid_x']},{user_grid['grid_y']}/forecast"""
        forecast_data = r.get(endpoint).json()
        forecast_data_list = f"Here's the next 3 days for your area:\n\n"
        footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M %p")}"""

        for forecast in forecast_data['properties']['periods']:

            if forecast['number'] in range(0,7):

                forecast_data_list += f"""{forecast['name']}: {forecast['temperature']}˚ {forecast['temperatureUnit']}\n{forecast['detailedForecast']}\n\n"""

        forecast_data_list += f"{footer}"
        
        return forecast_data_list

    def get_hourly_forecast(self, user_id):
        user_grid = self.grids[user_id]
        endpoint = f"""https://api.weather.gov/gridpoints/{user_grid['grid_id']}/{user_grid['grid_x']},{user_grid['grid_y']}/forecast/hourly"""
        hourly_data = r.get(endpoint).json()
        hourly_data_list = f"Here's the next 12 hours for your area:\n\n"
        footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M %p")}"""

        for hourly in hourly_data['properties']['periods']:

            start_time = datetime.fromisoformat(hourly['startTime']).strftime("%a %I:%M %p")

            if hourly['number'] in range(0,13):

                hourly_data_list += f"""{start_time}: {hourly['temperature']}˚ {hourly['temperatureUnit']}\nWind Speed: {hourly['windSpeed']} {hourly['windDirection']}\nConditions: {hourly['shortForecast']}\n\n"""

        hourly_data_list += f"{footer}"
        
        return hourly_data_list

    def get_alerts(self, user_id):
        user_coords = self.coordinates[user_id]
        endpoint = f"https://api.weather.gov/alerts/active?point={user_coords['latitude']},{user_coords['longitude']}"
        alerts_data = r.get(endpoint).json()
        alerts_data_list = ""
        footer = f"""Last updated: {datetime.now().strftime("%b %d, %Y %I:%M:%S %p")}"""
        no_alerts_msg = f"""There are currently no active alerts in your area, that's probably a good thing.\n\n"""

        for alert in alerts_data['features']:

            alerts_data_list += f"""{alert['properties']['headline']}:\nSeverity: {alert['properties']['severity']}\n\n{alert['properties']['description']}\n\n"""

        if alerts_data_list == "":
            alerts_data_list += f"""{no_alerts_msg}\n\n{footer}"""

        else:
            alerts_data_list += f"""{footer}"""

        return alerts_data_list