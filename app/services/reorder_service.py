from app.services.demand_service import DemandService

from app.ml.reorderModel.reorder_engine import ReorderEngine


class ReorderService:

    @staticmethod
    async def reorder_plan(days: int = 30):

        forecast_data = await DemandService.forecast(days)

        result = []

        for product in forecast_data:

            forecast = product.get(

                "forecast",

                []

            )

            predicted_demand = sum(

                day.get(

                    "predictedQty",

                    0

                )

                for day in forecast

            )

            ai = ReorderEngine.calculate(

                history_length=product.get(

                    "historyLength",

                    len(

                        product.get(

                            "history",

                            []

                        )

                    )

                ),

                predicted_demand=predicted_demand,

                current_stock=product.get(

                    "stock",

                    0

                ),

                total_sold=product.get(

                    "totalSold",

                    0

                ),

                category=product.get(

                    "category"

                ),

                seasonal=False

            )

            result.append({

                "productId":

                    product["productId"],

                "name":

                    product["name"],

                "category":

                    product.get(

                        "category"

                    ),

                "sku":

                    product["sku"],

                "price":

                    product.get(

                        "price",

                        0

                    ),

                "currentStock":

                    product.get(

                        "stock",

                        0

                    ),

                "totalSold":

                    product.get(

                        "totalSold",

                        0

                    ),

                "historyLength":

                    product.get(

                        "historyLength",

                        len(

                            product.get(

                                "history",

                                []

                            )

                        )

                    ),

                "forecastModel":

                    ai["forecastModel"],

                "predictedDemand":

                    predicted_demand,

                "averageDailyDemand":

                    ai["averageDailyDemand"],

                "leadTimeDays":

                    ai["leadTimeDays"],

                "leadTimeSource":

                    ai["leadTimeSource"],

                "safetyStock":

                    ai["safetyStock"],

                "recommendedQty":

                    ai["recommendedQty"],

                "priority":

                    ai["priority"],

                "priorityScore":

                    ai["priorityScore"],

                "reorderScore":

                    ai["reorderScore"],

                "reorderLevel":

                    ai["reorderLevel"],

                "confidence":

                    ai["confidence"],

                "action":

                    ai["action"],

                "reason":

                    ai["reason"],

                "explanation":

                    ai["explanation"]

            })

        priority_order = {

            "Critical": 0,

            "High": 1,

            "Medium": 2,

            "Low": 3,

            "None": 4

        }

        result.sort(

            key=lambda item: (

                priority_order.get(

                    item["priority"],

                    99

                ),

                -item["reorderScore"],

                item["currentStock"],

                -item["predictedDemand"]

            )

        )

        summary = {

            "critical": sum(

                1

                for x in result

                if x["priority"] == "Critical"

            ),

            "high": sum(

                1

                for x in result

                if x["priority"] == "High"

            ),

            "medium": sum(

                1

                for x in result

                if x["priority"] == "Medium"

            ),

            "low": sum(

                1

                for x in result

                if x["priority"] == "Low"

            ),

            "none": sum(

                1

                for x in result

                if x["priority"] == "None"

            ),

            "totalRecommendedQty": sum(

                x["recommendedQty"]

                for x in result

            )

        }

        return {

            "days": days,

            "count": len(result),

            "summary": summary,

            "data": result

        }