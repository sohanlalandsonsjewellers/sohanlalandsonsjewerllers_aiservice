from collections import defaultdict
from datetime import timedelta

from app.database import db

from app.ml.demandForecastModel.model_selector import ModelSelector
from app.ml.demand_forecast import DemandForecastModel


class DemandService:

    @staticmethod
    async def forecast(days: int = 30):

        orders = await db.Order.find(
            {
                "status": "ACCEPTED"
            },
            {
                "items": 1,
                "createdAt": 1
            }
        ).sort(
            "createdAt",
            1
        ).to_list(None)

        products = await db.Product.find(
            {},
            {
                "_id": 1,
                "name": 1,
                "category": 1,
                "sku": 1,
                "price": 1,
                "stock": 1
            }
        ).to_list(None)

        if not orders:

            return []

        start_date = orders[0]["createdAt"].date()

        end_date = orders[-1]["createdAt"].date()

        sales_history = defaultdict(
            lambda: defaultdict(int)
        )

        total_sold = defaultdict(int)

        for order in orders:

            order_date = order["createdAt"].date()

            for item in order.get("items", []):

                product_id = item["productId"]

                qty = int(
                    item.get(
                        "qty",
                        0
                    )
                )

                sales_history[
                    product_id
                ][order_date] += qty

                total_sold[
                    product_id
                ] += qty

        result = []

        for product in products:

            product_id = str(
                product["_id"]
            )

            history = []

            current = start_date

            while current <= end_date:

                history.append(

                    sales_history[
                        product_id
                    ][current]

                )

                current += timedelta(
                    days=1
                )

            strategy = ModelSelector.select(
                history
            )

            forecast = strategy.forecast(
                history,
                days
            )

            result.append({

                "productId": product_id,

                "name": product["name"],

                "category": product.get(
                    "category"
                ),

                "sku": product["sku"],

                "price": float(
                    product.get(
                        "price",
                        0
                    )
                ),

                "stock": int(
                    product.get(
                        "stock",
                        0
                    )
                ),

                "history": history,

                "forecast": forecast,

                "forecastModel": strategy.__class__.__name__,

                "historyLength": len(history),

                "totalSold": total_sold[
                    product_id
                ]

            })

        return result

    @staticmethod
    async def demand_insights(days: int = 30):

        products = await DemandService.forecast(
            days
        )

        helper = DemandForecastModel()

        result = []

        for product in products:

            forecast = product["forecast"]

            stock = product["stock"]

            total_sold = product["totalSold"]

            predicted_demand = helper.total_demand(
                forecast
            )

            average_daily = helper.average_daily_demand(
                forecast
            )

            if average_daily > 0:

                days_left = round(
                    stock / average_daily,
                    1
                )

            else:

                days_left = None

            if predicted_demand > 0:

                stock_coverage = round(
                    (stock / predicted_demand) * 100,
                    1
                )

            else:

                stock_coverage = 0

            demand_score = helper.demand_score(

                total_sold,

                predicted_demand,

                stock

            )

            sales_category = helper.sales_category(
                total_sold
            )

            trend = helper.trend(
                forecast
            )

            risk = helper.stock_risk(

                stock,

                predicted_demand

            )

            inventory_health = helper.inventory_health(

                stock,

                total_sold

            )

            priority = helper.product_priority(

                demand_score,

                stock

            )

            recommendation = helper.business_recommendation(

                stock,

                total_sold,

                risk,

                sales_category

            )

            result.append({

                "productId": product["productId"],

                "name": product["name"],

                "category": product["category"],

                "sku": product["sku"],

                "price": product["price"],

                "currentStock": stock,

                "totalSold": total_sold,

                "predictedDemand": predicted_demand,

                "averageDailyDemand": average_daily,

                "daysOfStockLeft": days_left,

                "stockCoveragePercent": stock_coverage,

                "demandScore": demand_score,

                "priority": priority,

                "salesCategory": sales_category,

                "inventoryHealth": inventory_health,

                "trend": trend,

                "stockRisk": risk,

                "businessRecommendation": recommendation,

                "forecastModel": product["forecastModel"]

            })

        priority_order = {

            "Highest": 0,

            "High": 1,

            "Medium": 2,

            "Low": 3

        }

        result.sort(

            key=lambda x: (

                priority_order.get(

                    x["priority"],

                    99

                ),

                -x["demandScore"],

                x["currentStock"]

            )

        )

        return result