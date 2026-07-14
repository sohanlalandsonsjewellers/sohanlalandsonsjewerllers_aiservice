from collections import defaultdict

from app.database import db
from app.ml.customer_segmentation import CustomerSegmentationModel


class SegmentationService:

    @staticmethod
    async def segment_customers():

        orders = await db.Order.find(
            {
                "status": "ACCEPTED"
            },
            {
                "customerName": 1,
                "customerPhone": 1,
                "totalAmount": 1
            }
        ).to_list(None)

        customer_map = defaultdict(

            lambda: {

                "customerName": "",

                "customerPhone": "",

                "totalOrders": 0,

                "totalSpent": 0

            }

        )

        for order in orders:

            phone = order.get("customerPhone")

            if not phone:
                continue

            customer = customer_map[phone]

            customer["customerName"] = order.get(
                "customerName",
                ""
            )

            customer["customerPhone"] = phone

            customer["totalOrders"] += 1

            customer["totalSpent"] += float(
                order.get("totalAmount", 0)
            )

        customers = list(
            customer_map.values()
        )

        model = CustomerSegmentationModel()

        return model.segment(
            customers
        )