from typing import Optional


class RevenueScore:

    """
    Calculates normalized revenue score (0-100)
    based on generated revenue.
    """

    @staticmethod
    def calculate(
            revenue: float,
            max_revenue: Optional[float] = None
    ) -> float:

        if revenue <= 0:
            return 0.0

        if not max_revenue or max_revenue <= 0:
            max_revenue = max(revenue, 1)

        score = (revenue / max_revenue) * 100

        return round(min(score, 100), 2)