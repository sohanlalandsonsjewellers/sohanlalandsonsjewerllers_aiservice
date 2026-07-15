class RecommendationEngine:

    @staticmethod
    def generate(

        low_stock,

        out_of_stock,

        sales_status

    ):

        recommendations = []

        if low_stock:

            recommendations.append(

                "Restock fast-moving products."

            )

        if out_of_stock:

            recommendations.append(

                "Purchase similar jeweller designs."

            )

        if sales_status == "Needs Improvement":

            recommendations.append(

                "Run promotional offers."

            )

        if sales_status == "Growing":

            recommendations.append(

                "Increase inventory of popular categories."

            )

        if not recommendations:

            recommendations.append(

                "Business is performing well."

            )

        return recommendations