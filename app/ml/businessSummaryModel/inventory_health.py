class InventoryHealthModel:

    @staticmethod
    def calculate(

        total_products,

        low_stock,

        out_of_stock

    ):

        if total_products == 0:

            return {

                "score": 0,

                "status": "No Inventory"

            }

        risk = (

            low_stock +

            out_of_stock

        ) / total_products

        if risk < 0.10:

            return {

                "score": 100,

                "status": "Excellent"

            }

        if risk < 0.20:

            return {

                "score": 85,

                "status": "Healthy"

            }

        if risk < 0.40:

            return {

                "score": 70,

                "status": "Average"

            }

        return {

            "score": 50,

            "status": "Critical"

        }