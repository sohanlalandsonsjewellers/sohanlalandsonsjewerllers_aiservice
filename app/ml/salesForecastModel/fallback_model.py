from .forecast_strategy import ForecastStrategy


class RuleBasedSalesForecast(ForecastStrategy):

    def forecast(self, history, days):

        if not history:
            return [0] * days

        recent = history[-7:]

        avg = sum(recent) / len(recent)

        return [

            round(avg, 2)

            for _ in range(days)

        ]