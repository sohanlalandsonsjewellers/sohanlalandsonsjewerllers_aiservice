class ProductGrade:
    """
    Assign overall product grade.
    """

    @staticmethod
    def calculate(
            sales_score: float,
            revenue_score: float,
            profit_score: float,
            turnover_score: float,
            popularity_score: float
    ):

        final_score = (
                sales_score * 0.25 +
                revenue_score * 0.25 +
                profit_score * 0.20 +
                turnover_score * 0.15 +
                popularity_score * 0.15
        )

        if final_score >= 85:
            grade = "A+"

        elif final_score >= 75:
            grade = "A"

        elif final_score >= 65:
            grade = "B"

        elif final_score >= 50:
            grade = "C"

        else:
            grade = "D"

        return {
            "grade": grade,
            "score": round(final_score, 2)
        }