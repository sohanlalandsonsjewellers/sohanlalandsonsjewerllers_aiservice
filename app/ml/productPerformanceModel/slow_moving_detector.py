class SlowMovingDetector:
    """
    Detect slow moving products.
    """

    @staticmethod
    def detect(
            units_sold: int,
            turnover: float,
            days_since_last_sale: int
    ):

        score = 0

        if units_sold <= 10:
            score += 35

        if turnover < 1:
            score += 35

        if days_since_last_sale >= 30:
            score += 30

        return {
            "isSlowMoving": score >= 60,
            "score": score
        }