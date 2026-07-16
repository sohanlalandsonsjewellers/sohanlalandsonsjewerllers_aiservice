class ReorderExplainer:

    """
    Explain why AI generated a reorder recommendation.
    This is useful for Admin Dashboard and AI Reports.
    """

    @staticmethod
    def explain(

        predicted_demand: int,

        current_stock: int,

        safety_stock: int,

        priority: str,

        reorder_score: int,

        lead_time_days: int

    ):

        reasons = []

        # ---------------------------------
        # Demand
        # ---------------------------------

        if predicted_demand <= 0:

            reasons.append(

                "No significant demand is forecast."

            )

        elif predicted_demand > current_stock:

            reasons.append(

                "Forecasted demand exceeds available stock."

            )

        else:

            reasons.append(

                "Current stock can satisfy forecast demand."

            )

        # ---------------------------------
        # Safety Stock
        # ---------------------------------

        if current_stock <= safety_stock:

            reasons.append(

                "Current stock is below the recommended safety stock."

            )

        # ---------------------------------
        # Lead Time
        # ---------------------------------

        if lead_time_days >= 10:

            reasons.append(

                "Supplier lead time is long."

            )

        elif lead_time_days >= 7:

            reasons.append(

                "Supplier lead time is moderate."

            )

        else:

            reasons.append(

                "Supplier lead time is short."

            )

        # ---------------------------------
        # Priority
        # ---------------------------------

        priority_message = {

            "Critical": "Immediate purchase is recommended.",

            "High": "Reorder should be planned immediately.",

            "Medium": "Monitor inventory closely.",

            "Low": "Inventory is currently sufficient.",

            "None": "No reorder is required."

        }

        reasons.append(

            priority_message.get(

                priority,

                "Inventory status is normal."

            )

        )

        # ---------------------------------
        # Confidence
        # ---------------------------------

        if reorder_score >= 85:

            confidence = "Very High"

        elif reorder_score >= 70:

            confidence = "High"

        elif reorder_score >= 50:

            confidence = "Medium"

        else:

            confidence = "Low"

        return {

            "confidence": confidence,

            "reasons": reasons

        }