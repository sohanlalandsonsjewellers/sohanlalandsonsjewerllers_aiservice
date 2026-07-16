class ReorderStrategy:

    """
    Final business decision.
    """

    @staticmethod
    def decide(

        priority,

        reorder_qty

    ):

        if reorder_qty == 0:

            return {

                "action": "No Reorder Needed",

                "reason": "Current inventory is sufficient."

            }

        if priority == "Critical":

            return {

                "action": "Order Immediately",

                "reason": "Stock is below safety stock."

            }

        if priority == "High":

            return {

                "action": "Reorder This Week",

                "reason": "Demand is expected to exceed stock."

            }

        if priority == "Medium":

            return {

                "action": "Monitor Inventory",

                "reason": "Inventory is reducing steadily."

            }

        return {

            "action": "No Immediate Action",

            "reason": "Inventory is healthy."

        }