class InventoryTurnover:

    """
    Inventory Turnover Ratio

    Formula:

    Units Sold / Average Stock
    """

    @staticmethod
    def calculate(
            units_sold: int,
            average_stock: int
    ):

        if average_stock <= 0:
            return {
                "turnover": 0,
                "status": "No Stock"
            }

        turnover = units_sold / average_stock

        if turnover >= 2:
            status = "Excellent"

        elif turnover >= 1:
            status = "Good"

        elif turnover >= 0.5:
            status = "Average"

        else:
            status = "Poor"

        return {
            "turnover": round(turnover, 2),
            "status": status
        }