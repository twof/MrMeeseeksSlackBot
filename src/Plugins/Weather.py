from ..Models.Plugin import Plugin, Plugin_Type
from urllib.request import urlopen
from urllib.parse import urlencode
import os
import json
import re


class Weather(Plugin):
    '''Tells us the weather in San Francisco'''
    weather_api_url = "http://api.openweathermap.org/data/2.5/weather"
    city_api_url = "http://gd.geobytes.com/AutoCompleteCity"
    format_string = "{city} is experiencing {desc} and is {temp}°F"
    # weather_format = "{} is experiencing {} and is {}°F"

    def __init__(self):
        super().__init__(Plugin_Type.contains, "weather")

        self.api_key = os.getenv("OPEN_WEATHER_KEY")

    def _levenshtein_distance(self, origin, comparison):
        print(origin)
        print(comparison)

        ORIGIN_LEN = len(origin) + 1
        COMPARISON_LENGTH = len(comparison) + 1

        matrix = [[0] * COMPARISON_LENGTH] * ORIGIN_LEN

        for i in range(1, len(origin)):
            matrix[i][0] = i

        for i in range(1, len(comparison)):
            matrix[0][i] = i

        for i in range(i, len(origin)):
            for j in range(i, len(comparison)):
                if origin[i-1] == comparison[j-1]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    matrix[i][j] = min([matrix[i-1][j],
                                        matrix[i][j-1],
                                        matrix[i-1][j-1] + 1])

        average_len = (len(origin) + len(comparison))/2
        matriv_val = matrix[len(origin)][len(comparison)]

        return matriv_val/average_len

    def _find_city(self, message):
        regex = re.compile('[^a-zA-Z\s]')
        purged_content = regex.sub('', message.content)
        words = purged_content.split()

        for index, word in enumerate(words):
            print(word)
            params = {"q": word}
            params_encoded = urlencode(params)
            url_with_params = Weather.city_api_url + "?" + params_encoded

            content = urlopen(url_with_params).read().decode('utf8')
            cities = json.loads(content)

            if index < len(words) - 1 and len(cities) > 0\
                    and not (cities[0] == '' or cities[0] == '%s'):
                extended_city = word + ' ' + words[index + 1]
                params = {"q": extended_city}
                params_encoded = urlencode(params)
                url_with_params = Weather.city_api_url + "?" + params_encoded

                content = urlopen(url_with_params).read().decode('utf8')
                extended_cities = json.loads(content)

                print(cities)
                print(extended_city)
                print(extended_cities)
                if len(extended_cities) > 0\
                        and len(extended_cities) < len(cities)\
                        and extended_cities[0] != '':
                    print('extended_cities')
                    print(extended_city)
                    print(extended_cities)
                    print(extended_cities[0].split(", ")[0])

                    edit_distance = self._levenshtein_distance(
                        extended_cities[0].split(", ")[0],
                        extended_city)

                    print(edit_distance)

                    if edit_distance < 2:
                        return extended_cities[0].split(", ")[0]
                    else:
                        continue
                elif len(extended_cities) < 2:
                    print('hit cities 1')
                    print(cities)
                    print(cities[0].split(", ")[0])
                    print(word)

                    edit_distance = self._levenshtein_distance(
                        extended_cities[0].split(", ")[0],
                        word)

                    print(edit_distance)

                    if edit_distance < 2:
                        return cities[0].split(", ")[0]
                    else:
                        continue
            else:
                print('hit continue')
                continue

        return None

    def callback(self, message):
        found_city = self._find_city(message)

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
