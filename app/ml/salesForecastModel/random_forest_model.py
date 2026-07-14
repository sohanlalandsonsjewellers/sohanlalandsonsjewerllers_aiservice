import numpy as np

from sklearn.ensemble import RandomForestRegressor

from .forecast_strategy import ForecastStrategy


class RandomForestSalesForecast(ForecastStrategy):

    def __init__(self):

        self.model = RandomForestRegressor(

            n_estimators=200,

            random_state=42

        )

    def forecast(self, history, days):

        X = np.arange(

            len(history)

        ).reshape(-1, 1)

        y = np.array(history)

        self.model.fit(

            X,

            y

        )

        future = np.arange(

            len(history),

            len(history) + days

        ).reshape(-1, 1)

        prediction = self.model.predict(

            future

        )

        return [

            max(

                0,

                round(float(x), 2)

            )

            for x in prediction

        ]