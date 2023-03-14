import math


def floor(x: float, decimal_places: int = 0):
    return math.floor(x * 10 ** decimal_places) / (10 ** decimal_places)