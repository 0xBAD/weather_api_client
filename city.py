import pprint
import requests
from dateutil.parser import parse
import yaml

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

token = cfg["weatherstack"]["token"]

class WeatherStackForecast:

    def __init__(self):
        self._city_cache = {}

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache[city]

        url = f"http://api.weatherstack.com/current?access_key={token}&query={city}"
        data = requests.get(url).json()

        forecast = [{
            "location": data["location"]["name"],
            "temperature": data["current"]["temperature"],
            "descriptions": data["current"]["weather_descriptions"],
            "localdatetime": parse(data["location"]["localtime"])
        }]
        self._city_cache[city] = forecast
        return forecast


class CityInfo:

    def __init__(self, city, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or WeatherStackForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    city_info = CityInfo("Moscow")
    forecast = city_info.weather_forecast()
    pprint.pprint(forecast)


if __name__ == "__main__":
    _main()
