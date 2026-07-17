from typing import Optional


class SalesScore:

    """
    Calculates normalized sales score (0-100)
    based on units sold.
    """

    @staticmethod
    def calculate(
            units_sold: int,
            max_units_sold: Optional[int] = None
    ) -> float:

        if units_sold <= 0:
            return 0.0

        if not max_units_sold or max_units_sold <= 0:
            max_units_sold = max(units_sold, 1)

        score = (units_sold / max_units_sold) * 100

        return round(min(score, 100), 2)