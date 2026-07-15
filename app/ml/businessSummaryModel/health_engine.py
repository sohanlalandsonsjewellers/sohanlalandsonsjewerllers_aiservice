from statistics import mean


class HealthEngine:

    @staticmethod
    def inventory_health(

        total_products,

        low_stock,

        out_of_stock

    ):

        if total_products == 0:

            return {

                "score": 0,

                "status": "No Inventory"

            }

        healthy_products = max(

            0,

            total_products -

            low_stock -

            out_of_stock

        )

        score = round(

            (

                healthy_products /

                total_products

            ) * 100

        )

        if score >= 90:

            status = "Excellent"

        elif score >= 75:

            status = "Healthy"

        elif score >= 50:

            status = "Warning"

        else:

            status = "Critical"

        return {

            "score": score,

            "status": status,

            "healthyProducts": healthy_products,

            "lowStockProducts": low_stock,

            "outOfStockProducts": out_of_stock

        }

    @staticmethod
    def sales_health(

        total_revenue,

        total_orders,

        revenue_history

    ):

        if total_orders == 0:

            return {

                "score": 0,

                "status": "No Sales",

                "averageOrderValue": 0,

                "growth": "Unknown"

            }

        average_order = round(

            total_revenue /

            total_orders,

            2

        )

        non_zero = [

            x

            for x in revenue_history

            if x > 0

        ]

        average_day = (

            mean(non_zero)

            if non_zero

            else 0

        )

        latest = (

            revenue_history[-1]

            if revenue_history

            else 0

        )

        if latest > average_day * 1.20:

            growth = "Positive"

        elif latest < average_day * 0.80:

            growth = "Negative"

        else:

            growth = "Stable"

        score = 100

        if average_order < 500:

            score -= 40

        elif average_order < 1500:

            score -= 25

        elif average_order < 3000:

            score -= 10

        if growth == "Negative":

            score -= 15

        elif growth == "Stable":

            score -= 5

        score = max(

            0,

            min(

                100,

                score

            )

        )

        if score >= 90:

            status = "Excellent"

        elif score >= 75:

            status = "Growing"

        elif score >= 60:

            status = "Stable"

        else:

            status = "Needs Improvement"

        return {

            "score": score,

            "status": status,

            "averageOrderValue": average_order,

            "growth": growth

        }

    @staticmethod
    def customer_health(

        total_customers,

        vip,

        premium,

        regular,

        new

    ):

        if total_customers == 0:

            return {

                "score": 0,

                "status": "No Customers"

            }

        loyal = vip + premium

        score = round(

            loyal /

            total_customers *

            100

        )

        if score >= 50:

            status = "Excellent"

        elif score >= 30:

            status = "Healthy"

        elif score >= 15:

            status = "Average"

        else:

            status = "Weak"

        return {

            "score": score,

            "status": status,

            "vip": vip,

            "premium": premium,

            "regular": regular,

            "new": new

        }