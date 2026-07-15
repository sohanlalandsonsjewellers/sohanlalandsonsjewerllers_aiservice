class BusinessScoreModel:

    WEIGHTS = {

        "revenue": 0.35,

        "orders": 0.20,

        "inventory": 0.20,

        "sales": 0.10,

        "customer": 0.10,

        "operations": 0.05

    }

    @staticmethod
    def revenue_score(total_revenue):

        if total_revenue <= 0:

            return 0

        elif total_revenue >= 500000:

            return 100

        elif total_revenue >= 250000:

            return 90

        elif total_revenue >= 150000:

            return 80

        elif total_revenue >= 100000:

            return 70

        elif total_revenue >= 50000:

            return 60

        elif total_revenue >= 25000:

            return 40

        else:

            return 20

    @staticmethod
    def order_score(total_orders):

        if total_orders <= 0:

            return 0

        elif total_orders >= 100:

            return 100

        elif total_orders >= 75:

            return 90

        elif total_orders >= 50:

            return 80

        elif total_orders >= 30:

            return 70

        elif total_orders >= 20:

            return 60

        elif total_orders >= 10:

            return 40

        else:

            return 20

    @staticmethod
    def operational_score(

        pending_orders,

        cancelled_orders

    ):

        score = 100

        score -= pending_orders * 2

        score -= cancelled_orders * 5

        return max(

            0,

            min(

                100,

                score

            )

        )

    @classmethod
    def calculate(

        cls,

        total_revenue,

        total_orders,

        inventory_score,

        sales_score,

        customer_score,

        pending_orders,

        cancelled_orders

    ):

        revenue = cls.revenue_score(

            total_revenue

        )

        orders = cls.order_score(

            total_orders

        )

        operations = cls.operational_score(

            pending_orders,

            cancelled_orders

        )

        final_score = (

            revenue *

            cls.WEIGHTS["revenue"]

            +

            orders *

            cls.WEIGHTS["orders"]

            +

            inventory_score *

            cls.WEIGHTS["inventory"]

            +

            sales_score *

            cls.WEIGHTS["sales"]

            +

            customer_score *

            cls.WEIGHTS["customer"]

            +

            operations *

            cls.WEIGHTS["operations"]

        )

        final_score = round(

            final_score

        )

        if final_score >= 90:

            grade = "A+"

        elif final_score >= 80:

            grade = "A"

        elif final_score >= 70:

            grade = "B"

        elif final_score >= 60:

            grade = "C"

        elif final_score >= 50:

            grade = "D"

        else:

            grade = "E"

        return {

            "score": final_score,

            "grade": grade,

            "breakdown": {

                "revenue": revenue,

                "orders": orders,

                "inventory": inventory_score,

                "sales": sales_score,

                "customer": customer_score,

                "operations": operations

            }

        }