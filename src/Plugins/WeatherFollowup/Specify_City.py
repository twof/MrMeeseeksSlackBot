from src.Models.Plugin import Plugin, Plugin_Type
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import os


class SpecifyCity(Plugin):
    codio_key = "a803c085cc5a98c307853fac03735a535d949ac"
    codio_base_url = "https://api.geocod.io/v1/geocode?"
    format_string = "{city} is experiencing {desc} and is {temp}°F"
    oweather_api_url = "http://api.openweathermap.org/data/2.5/weather?"

    def __init__(self):
        super().__init__(Plugin_Type.regex, "^[0-9]+$")

        self.oweather_api_key = os.getenv("OPEN_WEATHER_KEY")

    def callback(self, message, context_arr):
        if int(message.content) > len(context_arr):
            return "Choice invalid try again"
        else:
            found_city = context_arr[int(message.content)-1].split(', ')

            codio_params = {"api_key": SpecifyCity.codio_key,
                            "units": "imperial",
                            "city": found_city[0],
                            "state": found_city[1],
                            "country": found_city[2]}
            codio_params_encoded = urlencode(codio_params)
            codio_url_with_params = SpecifyCity.codio_base_url\
                + codio_params_encoded

            content = urlopen(codio_url_with_params).read().decode('utf8')
            city = json.loads(content)

            try:
                found_city_lon = city["results"][0]["location"]["lng"]
                found_city_lat = city["results"][0]["location"]["lat"]
            except IndexError:
                return "I CAN'T FIND THAT CITY JERRY! "\
                    + "ARE YOU SQUARING YOUR SHOULDERS?"

            oweather_params = {"appid": self.oweather_api_key,
                               "units": "imperial",
                               "lat": found_city_lat,
                               "lon": found_city_lon}
            oweather_params_encoded = urlencode(oweather_params)
            oweather_url_with_params = SpecifyCity.oweather_api_url\
                + oweather_params_encoded

            content = urlopen(oweather_url_with_params).read().decode('utf8')
            parsed_json = json.loads(content)

            city_name = parsed_json["name"]
            description = parsed_json["weather"][0]["description"]
            temp = str(parsed_json["main"]["temp"])

            weather_description =\
                SpecifyCity.format_string.format(city=city_name,
                                                 desc=description,
                                                 temp=temp)
            return weather_description

    def tests(self):
        cases = [("1",),
                 ("2",)]
        return cases

    def usage(self):
        return "Asks the user to specify which city they meant if their request\
        was ambiguous"
