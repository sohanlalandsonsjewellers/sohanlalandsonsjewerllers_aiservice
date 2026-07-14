class DemandForecastModel:

    @staticmethod
    def total_demand(forecast):

        return sum(

            item["predictedQty"]

            for item in forecast

        )

    @staticmethod
    def average_daily_demand(forecast):

        if not forecast:

            return 0

        return round(

            DemandForecastModel.total_demand(
                forecast
            ) / len(forecast),

            2

        )

    @staticmethod
    def demand_score(

        total_sold,

        predicted_demand,

        stock

    ):

        score = (

            total_sold * 4

            +

            predicted_demand * 3

            +

            max(
                0,
                10 - stock
            )

        )

        return min(
            100,
            round(score)
        )

    @staticmethod
    def sales_category(total_sold):

        if total_sold >= 25:

            return "Best Seller"

        if total_sold >= 10:

            return "Fast Moving"

        if total_sold >= 5:

            return "Regular"

        if total_sold >= 1:

            return "Slow Moving"

        return "Dead Stock"

    @staticmethod
    def stock_risk(

        stock,

        predicted_demand

    ):

        if predicted_demand <= 0:

            return "Low"

        ratio = stock / predicted_demand

        if ratio <= 0.10:

            return "Critical"

        if ratio <= 0.30:

            return "High"

        if ratio <= 0.60:

            return "Moderate"

        return "Low"

    @staticmethod
    def trend(forecast):

        if len(forecast) < 2:

            return "No Data"

        first = forecast[0]["predictedQty"]

        last = forecast[-1]["predictedQty"]

        if last > first:

            return "Increasing"

        if last < first:

            return "Decreasing"

        return "Stable"

    @staticmethod
    def inventory_health(

        stock,

        total_sold

    ):

        if stock == 0:

            return "Out of Stock"

        if stock <= 2 and total_sold >= 10:

            return "Critical"

        if stock <= 5:

            return "Low Stock"

        return "Healthy"

    @staticmethod
    def product_priority(

        demand_score,

        stock

    ):

        if demand_score >= 90:

            return "Highest"

        if demand_score >= 70:

            return "High"

        if demand_score >= 40:

            return "Medium"

        return "Low"

    @staticmethod
    def business_recommendation(

        stock,

        total_sold,

        risk,

        sales_category

    ):

        if sales_category == "Dead Stock":

            return "Run Promotion"

        if risk == "Critical":

            if stock <= 1:

                return "Purchase Similar Designs"

            return "Increase Stock"

        if risk == "High":

            return "Increase Stock"

        if sales_category == "Fast Moving":

            return "Monitor Demand"

        return "No Action Required"