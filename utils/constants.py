from enum import Enum


class Plugin_Type(Enum):
    everything = 1
    equals = 2
    starts_with = 3
    contains = 4
    regex = 5
