from ..Utils.constants import Plugin_Type
from ..Models.Plugin import Plugin
from ..Models.Singleton import Singleton
from urllib.request import urlopen
import os
import json


class Weather(Plugin, Singleton):
    '''Tells us the weather in San Francisco'''
    def __init__(self):
        super(Weather, self).__init__(Plugin_Type.contains, "weather")

        self.api_key = os.getenv("OPEN_WEATHER_KEY")

    def callback(self, message):
        some_url = "http://api.openweathermap.org/data/2.5/weather?"\
            "q=san%20francisco&units=imperial&appid=" + self.api_key

        content = urlopen(some_url).read().decode('utf8')
        parsed_json = json.loads(content)
        city_name = parsed_json["name"]
        description = parsed_json["weather"][0]["description"]
        temp = str(parsed_json["main"]["temp"])
        weather_description = city_name + " is experiencing " + description\
            + " and is " + temp + "°F"
        return weather_description
