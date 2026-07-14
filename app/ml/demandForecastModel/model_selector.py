from app.ml.demandForecastModel.linear_model import LinearForecast

from app.ml.demandForecastModel.fallback_model import RuleBasedForecast


class ModelSelector:

    @staticmethod
    def select(history):

        total_sales = sum(history)

        non_zero_days = len(

            [

                x

                for x in history

                if x > 0

            ]

        )

        if total_sales < 20:

            return RuleBasedForecast()

        if non_zero_days < 10:

            return RuleBasedForecast()

        return LinearForecast()