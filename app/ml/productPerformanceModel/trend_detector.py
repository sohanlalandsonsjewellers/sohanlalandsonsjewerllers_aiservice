from typing import List


class TrendDetector:
    """
    Detect product sales trend by comparing
    historical sales periods.

    Output:
    - Growing
    - Declining
    - Stable
    - New
    """

    @staticmethod
    def detect(history: List[float]):

        if not history:
            return {
                "trend": "Unknown",
                "growth": 0.0
            }

        if len(history) == 1:
            return {
                "trend": "New",
                "growth": 0.0
            }

        previous_avg = sum(history[:-1]) / max(len(history[:-1]), 1)
        current = history[-1]

        if previous_avg <= 0:
            growth = 100 if current > 0 else 0
        else:
            growth = ((current - previous_avg) / previous_avg) * 100

        if growth >= 20:
            trend = "Growing"

        elif growth <= -20:
            trend = "Declining"

        else:
            trend = "Stable"

        return {
            "trend": trend,
            "growth": round(growth, 2)
        }