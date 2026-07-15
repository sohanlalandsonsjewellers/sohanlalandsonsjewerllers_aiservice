class AlertEngine:

    @staticmethod
    def generate(

        low_stock,

        out_of_stock,

        pending_orders

    ):

        alerts = []

        if low_stock > 0:

            alerts.append(

                f"{low_stock} products are low on stock."

            )

        if out_of_stock > 0:

            alerts.append(

                f"{out_of_stock} products are out of stock."

            )

        if pending_orders > 0:

            alerts.append(

                f"{pending_orders} pending orders require attention."

            )

        if not alerts:

            alerts.append(

                "Business is operating normally."

            )

        return alerts