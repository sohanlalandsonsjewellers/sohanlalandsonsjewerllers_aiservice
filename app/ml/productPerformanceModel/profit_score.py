from typing import Optional


class ProfitScore:

    """
    Calculates normalized profit score (0-100)
    based on actual profit.
    """

    @staticmethod
    def calculate(
            profit: float,
            max_profit: Optional[float] = None
    ) -> float:

        if profit <= 0:
            return 0.0

        if not max_profit or max_profit <= 0:
            max_profit = max(profit, 1)

        score = (profit / max_profit) * 100

        return round(min(score, 100), 2)