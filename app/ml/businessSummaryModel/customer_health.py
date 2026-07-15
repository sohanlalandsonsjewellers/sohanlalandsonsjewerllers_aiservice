class CustomerHealthModel:

    @staticmethod
    def calculate(

        total_customers,

        vip,

        premium,

        regular,

        new

    ):

        if total_customers == 0:

            return {

                "score": 0,

                "status": "No Customers",

                "vip": 0,

                "premium": 0,

                "regular": 0,

                "new": 0

            }

        loyal = vip + premium

        score = round(

            (loyal / total_customers) * 100

        )

        if score >= 50:

            status = "Excellent"

        elif score >= 30:

            status = "Healthy"

        elif score >= 15:

            status = "Average"

        else:

            status = "Weak"

        return {

            "score": score,

            "status": status,

            "vip": vip,

            "premium": premium,

            "regular": regular,

            "new": new

        }