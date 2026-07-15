from datetime import datetime

from app.database import db

from app.ml.businessSummaryModel.business_score import BusinessScoreModel
from app.ml.businessSummaryModel.inventory_health import InventoryHealthModel
from app.ml.businessSummaryModel.sales_health import SalesHealthModel
from app.ml.businessSummaryModel.customer_health import CustomerHealthModel
from app.ml.businessSummaryModel.alert_engine import AlertEngine
from app.ml.businessSummaryModel.recommendation_engine import RecommendationEngine


class BusinessSummaryService:

    @staticmethod
    async def summary():

        # -----------------------------
        # Orders
        # -----------------------------

        total_orders = await db.Order.count_documents({})

        accepted_orders = await db.Order.count_documents({
            "status": "ACCEPTED"
        })

        pending_orders = await db.Order.count_documents({
            "status": "PENDING"
        })

        cancelled_orders = await db.Order.count_documents({
            "status": "CANCELLED"
        })

        # -----------------------------
        # Revenue
        # -----------------------------

        revenue_result = await db.Order.aggregate([

            {
                "$match": {
                    "status": "ACCEPTED"
                }
            },

            {
                "$group": {

                    "_id": None,

                    "revenue": {

                        "$sum": "$totalAmount"

                    }

                }

            }

        ]).to_list(1)

        total_revenue = (

            revenue_result[0]["revenue"]

            if revenue_result

            else 0

        )

        # -----------------------------
        # Products
        # -----------------------------

        total_products = await db.Product.count_documents({})

        inventory_result = await db.Product.aggregate([

            {

                "$group": {

                    "_id": None,

                    "inventoryValue": {

                        "$sum": {

                            "$multiply": [

                                "$price",

                                "$stock"

                            ]

                        }

                    },

                    "totalStock": {

                        "$sum": "$stock"

                    }

                }

            }

        ]).to_list(1)

        inventory_value = (

            inventory_result[0]["inventoryValue"]

            if inventory_result

            else 0

        )

        total_stock = (

            inventory_result[0]["totalStock"]

            if inventory_result

            else 0

        )

        low_stock = await db.Product.count_documents({

            "stock": {

                "$lte": 2

            }

        })

        out_of_stock = await db.Product.count_documents({

            "stock": 0

        })

        # -----------------------------
        # Customer Summary
        # -----------------------------

        customers = await db.Order.aggregate([

            {

                "$match": {

                    "status": "ACCEPTED"

                }

            },

            {

                "$group": {

                    "_id": "$customerPhone",

                    "customerName": {

                        "$first": "$customerName"

                    },

                    "totalOrders": {

                        "$sum": 1

                    },

                    "totalSpent": {

                        "$sum": "$totalAmount"

                    }

                }

            }

        ]).to_list(None)

        vip = 0
        premium = 0
        regular = 0
        new = 0

        for customer in customers:

            spent = customer["totalSpent"]
            orders = customer["totalOrders"]

            if spent >= 50000 or orders >= 20:

                vip += 1

            elif spent >= 20000 or orders >= 10:

                premium += 1

            elif spent >= 5000 or orders >= 2:

                regular += 1

            else:

                new += 1

        customer_health = CustomerHealthModel.calculate(

            total_customers=len(customers),

            vip=vip,

            premium=premium,

            regular=regular,

            new=new

        )
        
            # -----------------------------
        # Inventory Health
        # -----------------------------

        inventory_health = InventoryHealthModel.calculate(

            total_products=total_products,

            low_stock=low_stock,

            out_of_stock=out_of_stock

        )

        # -----------------------------
        # Sales Health
        # -----------------------------

        sales_health = SalesHealthModel.calculate(

            revenue=total_revenue,

            orders=accepted_orders

        )

        # -----------------------------
        # Business Score
        # -----------------------------

        business_score = BusinessScoreModel.calculate(

            total_revenue=total_revenue,

            total_orders=accepted_orders,

            inventory_score=inventory_health["score"],

            sales_score=100
            if sales_health["status"] == "Excellent"
            else
            85
            if sales_health["status"] == "Growing"
            else
            70
            if sales_health["status"] == "Stable"
            else
            50,

            customer_score=customer_health["score"],

            pending_orders=pending_orders,

            cancelled_orders=cancelled_orders

        )

        # -----------------------------
        # Alerts
        # -----------------------------

        alerts = AlertEngine.generate(

            low_stock=low_stock,

            out_of_stock=out_of_stock,

            pending_orders=pending_orders

        )

        # -----------------------------
        # Recommendations
        # -----------------------------

        recommendations = RecommendationEngine.generate(

            low_stock=low_stock,

            out_of_stock=out_of_stock,

            sales_status=sales_health["status"]

        )

        # -----------------------------
        # Average Order Value
        # -----------------------------

        average_order_value = 0

        if accepted_orders:

            average_order_value = round(

                total_revenue / accepted_orders,

                2

        )
            
        # -----------------------------
        # Final Response
        # -----------------------------

        return {

            "generatedAt": datetime.utcnow().isoformat(),

            "orders": {

                "total": total_orders,

                "accepted": accepted_orders,

                "pending": pending_orders,

                "cancelled": cancelled_orders

            },

            "products": {

                "total": total_products,

                "totalStock": total_stock,

                "lowStock": low_stock,

                "outOfStock": out_of_stock,

                "inventoryValue": round(

                    inventory_value,

                    2

                )

            },

            "customers": {

                "total": len(customers),

                "health": customer_health

            },

            "sales": {

                "totalRevenue": round(

                    total_revenue,

                    2

                ),

                "averageOrderValue": average_order_value,

                "health": sales_health

            },

            "businessScore": business_score,

            "inventoryHealth": inventory_health,

            "alerts": alerts,

            "recommendations": recommendations

        }