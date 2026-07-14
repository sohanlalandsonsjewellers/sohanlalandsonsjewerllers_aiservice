from abc import ABC, abstractmethod


class ForecastStrategy(ABC):

    @abstractmethod
    def forecast(self, history, days):
        pass