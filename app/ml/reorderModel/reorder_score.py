class ReorderScore:

    """
    Production AI Reorder Score
    """

    WEIGHTS = {

        "forecast": 0.25,

        "stock": 0.20,

        "sales": 0.20,

        "turnover": 0.10,

        "safety": 0.10,

        "lead_time": 0.05,

        "priority": 0.10

    }

    @staticmethod
    def calculate(

        forecast_score,

        stock_score,

        sales_score,

        turnover_score,

        safety_score,

        lead_time_score,

        priority_score

    ):

        score = (

            forecast_score * 0.25 +

            stock_score * 0.20 +

            sales_score * 0.20 +

            turnover_score * 0.10 +

            safety_score * 0.10 +

            lead_time_score * 0.05 +

            priority_score * 0.10

        )

        score = round(score)

        if score >= 85:

            level = "Critical"

        elif score >= 70:

            level = "High"

        elif score >= 50:

            level = "Medium"

        else:

            level = "Low"

        return {

            "score": score,

            "level": level

        }