import numpy as np

from sklearn.linear_model import LinearRegression

from app.ml.demandForecastModel.forecast_strategy import ForecastStrategy


class LinearForecast(ForecastStrategy):

    def __init__(self):

        self.model = LinearRegression()

    def forecast(self, history, days):

        if len(history) < 2:

            return []

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

        result = []

        for day, qty in enumerate(

            prediction,

            start=1

        ):

            result.append({

                "day": day,

                "predictedQty": max(
                    0,
                    round(float(qty))
                )

            })

        return result