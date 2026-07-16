class LinearReorder:

    """
    Simple reorder model.

    Suitable when sales history is small.
    """

    def predict(

        self,

        current_stock: int,

        predicted_demand: int,

        safety_stock: int

    ):

        reorder_qty = max(

            0,

            predicted_demand

            +

            safety_stock

            -

            current_stock

        )

        return {

            "recommendedQty": reorder_qty,

            "model": "LinearReorder"

        }