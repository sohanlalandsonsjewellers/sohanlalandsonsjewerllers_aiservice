class ProductStrategy:
    """
    AI Recommendation Strategy
    """

    @staticmethod
    def recommend(
            grade: str,
            trend: str,
            fast: bool,
            slow: bool,
            dead: bool
    ):

        if dead:
            return {
                "action": "Clear Stock",
                "priority": "Critical"
            }

        if fast and trend == "Growing":
            return {
                "action": "Increase Stock",
                "priority": "High"
            }

        if fast:
            return {
                "action": "Maintain High Inventory",
                "priority": "High"
            }

        if slow:
            return {
                "action": "Run Promotion",
                "priority": "Medium"
            }

        if trend == "Declining":
            return {
                "action": "Review Pricing",
                "priority": "Medium"
            }

        if grade in ["A+", "A"]:
            return {
                "action": "Maintain Stock",
                "priority": "Normal"
            }

        return {
            "action": "Monitor Performance",
            "priority": "Low"
        }