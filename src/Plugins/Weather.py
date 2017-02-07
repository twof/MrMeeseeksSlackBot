# -*- coding: utf-8 -*-
from ..Models.Plugin import Plugin, Plugin_Type
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import json
import re


class Weather(Plugin):
    """Tells us the weather in a detected city."""

    weather_api_url = "http://api.openweathermap.org/data/2.5/weather"
    city_api_url = "http://gd.geobytes.com/AutoCompleteCity"
    format_string = "{city} is experiencing {desc} and is {temp}°F"

    def __init__(self):
        super().__init__(Plugin_Type.contains, "weather", "WeatherFollowup")

        self.api_key = os.getenv("OPEN_WEATHER_KEY")

    def _which_city_builder(self, message, cities):
        response = "Which city did you mean?"
        self.new_listener(message.user_id, cities,
                          self.followups["SpecifyCity"])
        for index, city in enumerate(cities):
            response += str(index) + ". " + city

        return response

    def _levenshtein_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1],
                                               distances[i1 + 1],
                                               distances_[-1])))
            distances = distances_

        average_len = (float(len(s1)) + float(len(s2)))/2
        return distances[-1]/average_len

    def _find_city(self, message):
        regex = re.compile('[^a-zA-Z\s]')
        purged_content = regex.sub('', message.content)
        words = purged_content.split()

        for index, word in enumerate(words):
            params = {"q": word,
                      "filter": "US,CA"}  # currently limited to us and ca
            params_encoded = urlencode(params)
            url_with_params = Weather.city_api_url + "?" + params_encoded

            content = urlopen(url_with_params).read().decode('utf8')
            cities = json.loads(content)

            if index < len(words) - 1 and len(cities) > 0\
                    and not (cities[0] == '' or cities[0] == '%s'):
                extended_city = word + ' ' + words[index + 1]
                params = {"q": extended_city,
                          "filter": "US,CA"}
                params_encoded = urlencode(params)
                url_with_params = Weather.city_api_url + "?" + params_encoded

                content = urlopen(url_with_params).read().decode('utf8')
                extended_cities = json.loads(content)

                if len(extended_cities) > 0\
                        and len(extended_cities) < len(cities)\
                        and extended_cities[0] != '':

                    edit_distance = self._levenshtein_distance(
                        extended_cities[0].split(", ")[0],
                        extended_city)

                    if edit_distance < 0.2:
                        return extended_cities
                    else:
                        continue
                elif len(extended_cities) < 2:
                    first_city = cities[0].split(", ")[0]

                    edit_distance = self._levenshtein_distance(
                        word,
                        first_city)

                    if edit_distance < 0.2:
                        return cities[0].split(", ")[0]
                    else:
                        continue
            elif index == len(words) - 1 and len(cities) > 0\
                    and not (cities[0] == '' or cities[0] == '%s'):
                first_city = cities[0].split(", ")[0]

                edit_distance = self._levenshtein_distance(
                    word,
                    first_city)

                if edit_distance < 0.2:
                    return cities[0].split(", ")[0]
                else:
                    continue
            else:
                continue

        return None

    def callback(self, message):
        found_cities = self._find_city(message)

        if len(found_cities) > 1:
            return self._which_city_builder(message, found_cities)
        elif len(found_cities) == 1:
            found_city = found_cities
        else:
            found_city = None

        if found_city:
            params = {"appid": self.api_key,
                      "units": "imperial",
                      "q": found_city}
        else:
            params = {"appid": self.api_key,
                      "units": "imperial",
                      "q": "san francisco"}

        params_encoded = urlencode(params)
        url_with_params = Weather.weather_api_url + "?" + params_encoded

        content = urlopen(url_with_params).read().decode('utf8')
        parsed_json = json.loads(content)

        city_name = parsed_json["name"]
        description = parsed_json["weather"][0]["description"]
        temp = str(parsed_json["main"]["temp"])

        weather_description = Weather.format_string.format(city=city_name,
                                                           desc=description,
                                                           temp=temp)

        return weather_description

    def tests(self):
        return []

    def usage(self):
        return "usage: weather -> sends the weather for a city of choice if"\
            + " you mentioned one and San Francisco if you didn't"
