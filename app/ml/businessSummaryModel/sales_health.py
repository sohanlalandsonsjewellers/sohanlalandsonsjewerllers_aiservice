class SalesHealthModel:

    @staticmethod
    def calculate(

        revenue,

        orders

    ):

        if orders == 0:

            return {

                "status": "No Sales"

            }

        average = revenue / orders

        if average >= 5000:

            status = "Excellent"

        elif average >= 2500:

            status = "Growing"

        elif average >= 1000:

            status = "Stable"

        else:

            status = "Needs Improvement"

        return {

            "averageOrderValue": round(

                average,

                2

            ),

            "status": status

        }