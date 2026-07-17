class DeadStockDetector:
    """
    Detect products which are not selling.
    """

    @staticmethod
    def detect(
            stock: int,
            units_sold: int,
            days_since_last_sale: int
    ):

        score = 0

        if stock > 0:
            score += 20

        if units_sold == 0:
            score += 40

        elif units_sold <= 2:
            score += 20

        if days_since_last_sale >= 60:
            score += 40

        return {
            "isDeadStock": score >= 70,
            "score": score
        }