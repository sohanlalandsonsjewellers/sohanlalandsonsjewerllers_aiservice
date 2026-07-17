from collections import defaultdict
from typing import Optional

from bson import ObjectId

from app.database import db
from app.ml.productPerformanceModel.performance_engine import (
    PerformanceEngine
)


class ProductPerformanceService:

    @staticmethod
    async def get_product_performance(
            category: Optional[str] = None,
            grade: Optional[str] = None,
            moving: Optional[str] = None,
            trend: Optional[str] = None
    ):

        product_filter = {}

        if category:
            product_filter["category"] = category

        # -----------------------------
        # Load Products
        # -----------------------------

        products = await db.Product.find(product_filter).to_list(None)

        if not products:

            return {

                "success": True,

                "count": 0,

                "summary": {},

                "data": []

            }

        # -----------------------------
        # Load Orders
        # -----------------------------

        orders = await db.Order.find().to_list(None)

        # -----------------------------
        # Load Events
        # -----------------------------

        events = await db.Event.find().to_list(None)

        # ==========================================================
        # ORDER AGGREGATION
        # ==========================================================

        sales_map = defaultdict(

            lambda: {

                "unitsSold": 0,

                "revenue": 0.0,

                "orders": 0,

                "lastSale": None

            }

        )

        for order in orders:

            created = order.get("createdAt")

            for item in order.get("items", []):

                sku = item.get("sku")

                if not sku:
                    continue

                qty = int(
                    item.get("qty", 0)
                )

                price = float(
                    item.get("price", 0)
                )

                sales_map[sku]["unitsSold"] += qty

                sales_map[sku]["revenue"] += (
                        qty * price
                )

                sales_map[sku]["orders"] += 1

                if created:

                    last = sales_map[sku]["lastSale"]

                    if last is None or created > last:

                        sales_map[sku]["lastSale"] = created

        # ==========================================================
        # EVENT AGGREGATION
        # ==========================================================

        event_map = defaultdict(

            lambda: {

                "views": 0,

                "clicks": 0,

                "wishlist": 0,

                "cart": 0

            }

        )

        product_lookup = {}

        for p in products:

            product_lookup[
                str(p["_id"])
            ] = p["sku"]

        for event in events:

            product_id = event.get("productId")

            if not product_id:
                continue

            sku = product_lookup.get(
                str(product_id)
            )

            if not sku:
                continue

            event_type = event.get(
                "eventType"
            )

            if event_type == "PRODUCT_VIEW":

                event_map[sku]["views"] += 1

            elif event_type == "PRODUCT_CLICK":

                event_map[sku]["clicks"] += 1

            elif event_type == "ADD_TO_CART":

                event_map[sku]["cart"] += 1

            elif event_type == "ADD_TO_WISHLIST":

                event_map[sku]["wishlist"] += 1

        # ==========================================================
        # MAX VALUES
        # ==========================================================

        max_sales = 1
        max_revenue = 1

        for value in sales_map.values():

            max_sales = max(

                max_sales,

                value["unitsSold"]

            )

            max_revenue = max(

                max_revenue,

                value["revenue"]

            )

        prepared_products = []

        for product in products:

            sku = product["sku"]

            stats = sales_map.get(

                sku,

                {

                    "unitsSold": 0,

                    "revenue": 0,

                    "orders": 0,

                    "lastSale": None

                }

            )

            popularity = event_map.get(

                sku,

                {

                    "views": 0,

                    "wishlist": 0,

                    "cart": 0,

                    "clicks": 0

                }

            )

            prepared_products.append(

                {

                    "product": product,

                    "sales": stats,

                    "events": popularity

                }

            )
            
            # ==========================================================
        # PERFORMANCE EVALUATION
        # ==========================================================

        from datetime import datetime

        results = []

        summary = {

            "excellent": 0,
            "good": 0,
            "average": 0,
            "poor": 0

        }

        for row in prepared_products:

            product = row["product"]

            sales = row["sales"]

            events = row["events"]

            # ---------------------------------------------
            # Days Since Last Sale
            # ---------------------------------------------

            if sales["lastSale"]:

                days_since_last_sale = (

                    datetime.utcnow() -

                    sales["lastSale"]

                ).days

            else:

                days_since_last_sale = 999

            # ---------------------------------------------
            # Sales History
            # (Current schema doesn't store history.
            # Temporary intelligent fallback.)
            # ---------------------------------------------

            units = sales["unitsSold"]

            if units <= 0:

                sales_history = [0]

            elif units <= 5:

                sales_history = [

                    max(0, units - 1),

                    units

                ]

            elif units <= 20:

                sales_history = [

                    int(units * 0.70),

                    int(units * 0.85),

                    units

                ]

            else:

                sales_history = [

                    int(units * 0.50),

                    int(units * 0.70),

                    int(units * 0.90),

                    units

                ]

            # ---------------------------------------------
            # Estimated Profit
            #
            # Since purchase price does not exist
            # assume 25% margin.
            # ---------------------------------------------

            estimated_profit = round(

                sales["revenue"] * 0.25,

                2

            )

            # ---------------------------------------------
            # Engine Input
            # ---------------------------------------------

            engine_input = {

                "stock":

                    product.get("stock", 0),

                "unitsSold":

                    sales["unitsSold"],

                "revenue":

                    sales["revenue"],

                "profit":

                    estimated_profit,

                "views":

                    events["views"],

                "wishlist":

                    events["wishlist"],

                "cart":

                    events["cart"],

                "orders":

                    sales["orders"],

                "salesHistory":

                    sales_history,

                "daysSinceLastSale":

                    days_since_last_sale

            }

            ai = PerformanceEngine.evaluate(

                engine_input,

                max_sales,

                max_revenue,

                estimated_profit if estimated_profit > 0 else 1

            )

            record = {

                "productId":

                    str(product["_id"]),

                "sku":

                    product.get("sku"),

                "name":

                    product.get("name"),

                "category":

                    product.get("category"),

                "price":

                    product.get("price"),

                "stock":

                    product.get("stock"),

                "unitsSold":

                    sales["unitsSold"],

                "revenue":

                    round(

                        sales["revenue"],

                        2

                    ),

                "estimatedProfit":

                    estimated_profit,

                **ai

            }

            # ---------------------------------------------
            # Grade Filter
            # ---------------------------------------------

            if grade:

                if (

                    record["grade"]["grade"]

                    != grade

                ):

                    continue

            # ---------------------------------------------
            # Trend Filter
            # ---------------------------------------------

            if trend:

                if (

                    record["trend"]["trend"]

                    != trend

                ):

                    continue

            # ---------------------------------------------
            # Moving Filter
            # ---------------------------------------------

            if moving == "Fast":

                if not record["fastMoving"]["isFastMoving"]:

                    continue

            if moving == "Slow":

                if not record["slowMoving"]["isSlowMoving"]:

                    continue

            if moving == "Dead":

                if not record["deadStock"]["isDeadStock"]:

                    continue

            # ---------------------------------------------
            # Summary
            # ---------------------------------------------

            g = record["grade"]["grade"]

            if g in [

                "A+",

                "A"

            ]:

                summary["excellent"] += 1

            elif g == "B":

                summary["good"] += 1

            elif g == "C":

                summary["average"] += 1

            else:

                summary["poor"] += 1

            results.append(record)

        # ==========================================================
        # SORT
        # ==========================================================

        results = sorted(

            results,

            key=lambda x:

            x["grade"]["score"],

            reverse=True

        )

        return {

            "success": True,

            "count": len(results),

            "summary": summary,

            "data": results

        }
        
    