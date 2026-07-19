class CustomerRecommendation:

    @staticmethod
    def recommend(customer):

        if customer.get("daysSinceLastOrder") is not None:

            if customer["daysSinceLastOrder"] >= 90:

                return {

                    "title": "Win Back",

                    "message": "Send a win-back coupon to encourage another purchase.",

                    "priority": "High"

                }

        segment = customer.get("segment")

        if segment == "VIP":

            return {

                "title": "VIP Reward",

                "message": "Offer premium membership and early access to new collections.",

                "priority": "High"

            }

        if segment == "Premium":

            return {

                "title": "Loyalty Offer",

                "message": "Provide an exclusive loyalty discount.",

                "priority": "Medium"

            }

        if segment == "Regular":

            return {

                "title": "Cross Sell",

                "message": "Recommend matching jewellery and combo products.",

                "priority": "Medium"

            }

        return {

            "title": "Welcome",

            "message": "Send a welcome coupon and onboarding offers.",

            "priority": "Low"

        }