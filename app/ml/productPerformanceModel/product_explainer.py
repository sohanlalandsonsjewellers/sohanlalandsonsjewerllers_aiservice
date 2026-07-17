class ProductExplainer:

    @staticmethod
    def explain(
            grade,
            trend,
            fast,
            slow,
            dead,
            strategy
    ):

        reasons = []

        if fast:
            reasons.append(
                "Product has strong sales velocity."
            )

        if slow:
            reasons.append(
                "Sales movement is below expected level."
            )

        if dead:
            reasons.append(
                "No meaningful sales detected."
            )

        reasons.append(
            f"Current trend is {trend}."
        )

        reasons.append(
            f"Overall product grade is {grade}."
        )

        reasons.append(
            f"Recommended action: {strategy}"
        )

        return " ".join(reasons)