from collections import defaultdict
from datetime import timedelta

from app.database import db

from app.ml.salesForecastModel.model_selector import ModelSelector


class SalesService:

    @staticmethod
    async def forecast(days: int = 30):

        orders = await db.Order.find(
            {
                "status": "ACCEPTED"
            },
            {
                "createdAt": 1,
                "totalAmount": 1
            }
        ).sort(
            "createdAt",
            1
        ).to_list(None)

        if not orders:

            return []

        start_date = orders[0]["createdAt"].date()

        end_date = orders[-1]["createdAt"].date()

        daily_sales = defaultdict(float)

        for order in orders:

            order_date = order["createdAt"].date()

            daily_sales[
                order_date
            ] += float(

                order.get(
                    "totalAmount",
                    0
                )

            )

        history = []

        current = start_date

        while current <= end_date:

            history.append(

                round(

                    daily_sales[
                        current
                    ],

                    2

                )

            )

            current += timedelta(
                days=1
            )

        strategy = ModelSelector.select(
            history
        )

        prediction = strategy.forecast(
            history,
            days
        )

        result = []

        future_date = end_date

        for index, revenue in enumerate(

            prediction,

            start=1

        ):

            future_date += timedelta(
                days=1
            )

            result.append({

                "day": index,

                "date": future_date.isoformat(),

                "predictedRevenue": revenue

            })

        return {

            "historyLength": len(history),

            "forecastModel": strategy.__class__.__name__,

            "history": history,

            "forecast": result

        }