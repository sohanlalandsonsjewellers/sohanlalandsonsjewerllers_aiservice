class ReorderPriority:

    """
    Determines reorder priority based on
    stock level and forecast demand.
    """

    @staticmethod
    def calculate(

        current_stock: int,

        predicted_demand: int,

        safety_stock: int

    ):

        available_stock = current_stock - safety_stock

        if available_stock <= 0:

            return {

                "priority": "Critical",

                "score": 100

            }

        coverage = available_stock / max(

            predicted_demand,

            1

        )

        if coverage <= 0.25:

            return {

                "priority": "High",

                "score": 85

            }

        elif coverage <= 0.50:

            return {

                "priority": "Medium",

                "score": 65

            }

        elif coverage <= 1:

            return {

                "priority": "Low",

                "score": 40

            }

        return {

            "priority": "None",

            "score": 10

        }