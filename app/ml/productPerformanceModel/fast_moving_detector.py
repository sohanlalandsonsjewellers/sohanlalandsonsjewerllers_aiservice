class FastMovingDetector:
    """
    Detect fast moving products based on:
    - Sales Velocity
    - Inventory Turnover
    - Last Sale
    """

    @staticmethod
    def detect(
            units_sold: int,
            turnover: float,
            days_since_last_sale: int
    ):

        score = 0

        if units_sold >= 50:
            score += 40
        elif units_sold >= 20:
            score += 25
        elif units_sold >= 10:
            score += 15

        if turnover >= 2:
            score += 40
        elif turnover >= 1:
            score += 25

        if days_since_last_sale <= 7:
            score += 20
        elif days_since_last_sale <= 15:
            score += 10

        return {
            "isFastMoving": score >= 70,
            "score": score
        }