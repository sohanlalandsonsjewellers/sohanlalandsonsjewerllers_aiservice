from .fallback_model import RuleBasedSalesForecast

from .linear_model import LinearSalesForecast

from .random_forest_model import RandomForestSalesForecast


class ModelSelector:

    @staticmethod
    def select(history):

        n = len(history)

        non_zero = sum(

            1

            for x in history

            if x > 0

        )

        if non_zero < 5:

            return RuleBasedSalesForecast()

        if n < 180:

            return LinearSalesForecast()

        return RandomForestSalesForecast()