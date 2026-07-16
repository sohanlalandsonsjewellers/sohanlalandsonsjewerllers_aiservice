import math


class SafetyStockCalculator:

    """
    Safety Stock Calculator

    Purpose:
    Prevent stock-out due to unexpected demand.
    """

    DEFAULT_PERCENT = 0.20

    @classmethod
    def calculate(

        cls,

        predicted_demand: int,

        lead_time_days: int = 7,

        service_level: float = 0.95

    ):

        if predicted_demand <= 0:

            return {

        "safetyStock": 0,

        "averageDailyDemand": 0,

        "leadTimeDays": lead_time_days,

        "serviceLevel": service_level,

        "method": "No Demand"

        }

        average_daily_demand = (

            predicted_demand / 30

        )

        safety_stock = math.ceil(

            average_daily_demand *

            lead_time_days *

            cls.DEFAULT_PERCENT

        )

        return {

            "safetyStock": max(

                1,

                safety_stock

            ),

            "averageDailyDemand": round(

                average_daily_demand,

                2

            ),

            "leadTimeDays": lead_time_days,

            "serviceLevel": service_level,

            "method": "Average Daily Demand"

        }