class ReorderQuantityCalculator:

    """
    EOQ-style business rule.

    Future:

        MOQ

        Budget

        Supplier constraints

    """

    @staticmethod
    def calculate(

        current_stock,

        predicted_demand,

        safety_stock

    ):

        qty = (

            predicted_demand

            +

            safety_stock

            -

            current_stock

        )

        qty = max(

            0,

            round(qty)

        )

        return {

            "recommendedQty": qty

        }