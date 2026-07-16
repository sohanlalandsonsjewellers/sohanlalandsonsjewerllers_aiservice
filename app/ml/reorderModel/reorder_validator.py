class ReorderValidator:

    """
    Final validation layer before
    sending data to API.
    """

    ALLOWED_PRIORITY = {

        "Critical",

        "High",

        "Medium",

        "Low",

        "None"

    }

    ALLOWED_LEVEL = {

        "Critical",

        "High",

        "Medium",

        "Low"

    }

    @classmethod
    def validate(cls, result):

        # -------------------------
        # Recommended Quantity
        # -------------------------

        result["recommendedQty"] = max(

            0,

            int(result["recommendedQty"])

        )

        # -------------------------
        # Lead Time
        # -------------------------

        result["leadTimeDays"] = max(

            0,

            int(result["leadTimeDays"])

        )

        # -------------------------
        # Safety Stock
        # -------------------------

        result["safetyStock"] = max(

            0,

            int(result["safetyStock"])

        )

        # -------------------------
        # Priority
        # -------------------------

        if result["priority"] not in cls.ALLOWED_PRIORITY:

            result["priority"] = "Low"

        # -------------------------
        # Reorder Level
        # -------------------------

        if result["reorderLevel"] not in cls.ALLOWED_LEVEL:

            result["reorderLevel"] = "Low"

        # -------------------------
        # AI Score
        # -------------------------

        result["reorderScore"] = max(

            0,

            min(

                100,

                round(result["reorderScore"], 2)

            )

        )

        # -------------------------
        # Average Daily Demand
        # -------------------------

        result["averageDailyDemand"] = round(

            max(

                0,

                result["averageDailyDemand"]

            ),

            2

        )

        return result