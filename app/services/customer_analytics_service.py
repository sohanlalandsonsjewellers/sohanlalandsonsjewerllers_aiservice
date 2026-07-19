from collections import defaultdict
from datetime import datetime, timezone

from app.database import db
from app.ml.customerModel.customer_segmentation_model import CustomerSegmentationModel
from app.ml.customerModel.customer_recommendation import CustomerRecommendation


class CustomerAnalyticsService:

    @staticmethod
    async def _load_users():
        users = []
        async for user in db.User.find(
            {},
            {
                "_id": 1,
                "name": 1,
                "email": 1,
                "phoneNumber": 1,
                "created_at": 1,
            },
        ):
            users.append(
                {
                    "id": str(user["_id"]),
                    "name": user.get("name"),
                    "email": user.get("email"),
                    "phone": user.get("phoneNumber"),
                    "createdAt": user.get("created_at"),
                }
            )
        return users

    @staticmethod
    async def _load_orders():
        orders = []
        async for order in db.Order.find(
            {},
            {
                "_id": 1,
                "userId": 1,
                "totalAmount": 1,
                "status": 1,
                "createdAt": 1,
            },
        ):
            if not order.get("userId"):
                continue

            orders.append(
                {
                    "id": str(order["_id"]),
                    "userId": str(order["userId"]),
                    "totalAmount": float(order.get("totalAmount") or 0),
                    "status": order.get("status"),
                    "createdAt": order.get("createdAt"),
                }
            )
        return orders

    @staticmethod
    def _group_orders(orders):
        grouped = defaultdict(list)
        for order in orders:
            grouped[order["userId"]].append(order)
        return grouped

    @staticmethod
    def _calculate_customer_metrics(users, grouped_orders):
        customers = []
        now = datetime.now(timezone.utc)

        for user in users:
            orders = grouped_orders.get(user["id"], [])
            total_orders = len(orders)
            total_spent = sum(order["totalAmount"] for order in orders)

            average_order_value = (
                round(total_spent / total_orders, 2) if total_orders else 0
            )

            first_order = None
            last_order = None

            if orders:
                sorted_orders = sorted(
                    orders,
                    key=lambda x: x["createdAt"],
                )
                first_order = sorted_orders[0]["createdAt"]
                last_order = sorted_orders[-1]["createdAt"]

            days_since_last = None
            if last_order:
                if last_order.tzinfo is None:
                    last_order = last_order.replace(tzinfo=timezone.utc)
                days_since_last = (now - last_order).days

            customers.append(
                {
                    "customerId": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "phone": user["phone"],
                    "totalOrders": total_orders,
                    "totalSpent": round(total_spent, 2),
                    "averageOrderValue": average_order_value,
                    "customerLifetimeValue": round(total_spent, 2),
                    "firstOrder": first_order,
                    "lastOrder": last_order,
                    "daysSinceLastOrder": days_since_last,
                    "isRepeatCustomer": total_orders > 1,
                    "isNewCustomer": total_orders <= 1,
                }
            )
        return customers

    @staticmethod
    def _segment_customers(customers):
        if not customers:
            return customers
        model = CustomerSegmentationModel()
        return model.segment(customers)

    @staticmethod
    def _apply_recommendation(customers):
        result = []
        for customer in customers:
            customer["recommendation"] = CustomerRecommendation.recommend(customer)
            result.append(customer)
        return result

    @staticmethod
    def _build_summary(customers):
        total_customers = len(customers)
        repeat_customers = sum(
            1 for customer in customers if customer["isRepeatCustomer"]
        )
        new_customers = sum(
            1 for customer in customers if customer["isNewCustomer"]
        )
        vip_customers = sum(
            1 for customer in customers if customer.get("segment") == "VIP"
        )
        premium_customers = sum(
            1 for customer in customers if customer.get("segment") == "Premium"
        )
        regular_customers = sum(
            1 for customer in customers if customer.get("segment") == "Regular"
        )
        new_segment_customers = sum(
            1 for customer in customers if customer.get("segment") == "New Customer"
        )

        total_orders = sum(customer["totalOrders"] for customer in customers)
        total_spent = sum(customer["totalSpent"] for customer in customers)

        average_order_value = (
            round(total_spent / total_orders, 2) if total_orders else 0
        )
        average_lifetime_value = (
            round(total_spent / total_customers, 2) if total_customers else 0
        )

        return {
            "totalCustomers": total_customers,
            "repeatCustomers": repeat_customers,
            "newCustomers": new_customers,
            "vipCustomers": vip_customers,
            "premiumCustomers": premium_customers,
            "regularCustomers": regular_customers,
            "newSegmentCustomers": new_segment_customers,
            "totalOrders": total_orders,
            "totalRevenue": round(total_spent, 2),
            "averageOrderValue": average_order_value,
            "averageLifetimeValue": average_lifetime_value,
        }

    @staticmethod
    def _sort(customers):
        priority = {
            "VIP": 0,
            "Premium": 1,
            "Regular": 2,
            "New Customer": 3,
        }
        customers.sort(
            key=lambda customer: (
                priority.get(customer.get("segment"), 99),
                -customer["totalSpent"],
                -customer["totalOrders"],
                customer["name"] or "",
            )
        )
        return customers

    @staticmethod
    async def get_customer_analytics(
        segment: str | None = None,
        customer_type: str | None = None,
        at_risk: bool = False,
    ):
        users = await CustomerAnalyticsService._load_users()
        orders = await CustomerAnalyticsService._load_orders()
        grouped_orders = CustomerAnalyticsService._group_orders(orders)

        customers = CustomerAnalyticsService._calculate_customer_metrics(
            users, grouped_orders
        )
        customers = CustomerAnalyticsService._segment_customers(customers)
        customers = CustomerAnalyticsService._apply_recommendation(customers)

        # Remove users who have never placed an order
        customers = [customer for customer in customers if customer["totalOrders"] > 0]

        # Hide internal ML fields & apply filtering
        for customer in customers:
            customer.pop("cluster", None)

        if segment:
            customers = [
                customer
                for customer in customers
                if customer.get("segment", "").lower() == segment.lower()
            ]

        if customer_type:
            customer_type = customer_type.lower()
            if customer_type == "repeat":
                customers = [
                    customer for customer in customers if customer["isRepeatCustomer"]
                ]
            elif customer_type == "new":
                customers = [
                    customer for customer in customers if customer["isNewCustomer"]
                ]

        if at_risk:
            customers = [
                customer
                for customer in customers
                if customer.get("daysSinceLastOrder") is not None
                and customer["daysSinceLastOrder"] >= 60
            ]

        customers = CustomerAnalyticsService._sort(customers)
        summary = CustomerAnalyticsService._build_summary(customers)

        segments = {
            "VIP": 0,
            "Premium": 0,
            "Regular": 0,
            "New Customer": 0,
        }

        for customer in customers:
            segment_name = customer.get("segment", "Regular")
            if segment_name in segments:
                segments[segment_name] += 1

        return {
            "success": True,
            "summary": summary,
            "segments": segments,
            "count": len(customers),
            "data": customers,
        }