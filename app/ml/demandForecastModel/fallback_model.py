import math

from app.ml.demandForecastModel.forecast_strategy import ForecastStrategy


class RuleBasedForecast(ForecastStrategy):

    def forecast(self, history, days):

        if not history:

            return []

        recent = history[-30:]

        avg = sum(recent) / len(recent)

        result = []

        for day in range(1, days + 1):

            qty = max(

                0,

                round(avg)

            )

            result.append({

                "day": day,

                "predictedQty": qty

            })

        return result