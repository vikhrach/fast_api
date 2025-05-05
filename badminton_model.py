from enum import StrEnum

import joblib
from pydantic import BaseModel


class OutlookContition(StrEnum):
    overcast = "overcast"
    rain = "rain"
    sunny = "sunny"


class TemperatureContition(StrEnum):
    cool = "cool"
    hot = "hot"
    mild = "mild"


class HumidityContition(StrEnum):
    high = "high"
    normal = "normal"


class WindContition(StrEnum):
    strong = "strong"
    weak = "weak"


class Weather(BaseModel):
    outlook: OutlookContition
    humidity: HumidityContition
    wind: WindContition
    temperature: TemperatureContition


class PredictedPlayability(BaseModel):
    playability: bool


class BadmintonModel(object):
    """ML model for calculating playable conditions for given weather"""

    def __init__(self, model_path):
        with open(model_path, "rb") as f:
            self._model = joblib.load(f)

    def predict(self, weather: Weather):
        def fill_list_with_one(pos, length):
            return [int(i == pos) for i in range(length)]

        feature_list = []
        feature_list += fill_list_with_one(list(OutlookContition).index(weather.outlook.value), 3)
        feature_list += fill_list_with_one(list(TemperatureContition).index(weather.temperature.value), 3)
        feature_list += fill_list_with_one(list(HumidityContition).index(weather.humidity.value), 2)
        feature_list += fill_list_with_one(list(WindContition).index(weather.wind.value), 2)
        return bool(self._model.predict([feature_list])[0])
