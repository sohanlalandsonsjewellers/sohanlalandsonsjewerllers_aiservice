class InventoryInsightsModel:

    def analyze(self, products):

        result = []

        for product in products:

            stock = product["stock"]
            sold = product["sold"]

            if stock <= 5:

                status = "Low Stock"
                recommendation = "Restock Immediately"

            elif sold >= 10:

                status = "Fast Moving"
                recommendation = "Increase Stock"

            elif sold == 0:

                status = "No Sales"
                recommendation = "Run Promotion"

            else:

                status = "Healthy"
                recommendation = "No Action Required"

            result.append({

                **product,

                "status": status,

                "recommendation": recommendation

            })

        return result