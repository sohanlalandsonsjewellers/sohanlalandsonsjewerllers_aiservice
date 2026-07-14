from collections import defaultdict

from app.database import db
from app.ml.inventory_insights import InventoryInsightsModel


class InventoryService:

    @staticmethod
    async def get_inventory_insights():

        products = await db.Product.find(
            {},
            {
                "_id": 1,
                "name": 1,
                "stock": 1,
                "price": 1,
                "sku": 1
            }
        ).to_list(None)

        orders = await db.Order.find(
            {
                "status": "ACCEPTED"
            },
            {
                "items": 1
            }
        ).to_list(None)

        sold_map = defaultdict(int)

        for order in orders:

            items = order.get("items", [])

            for item in items:

                product_id = item.get("productId")

                qty = int(item.get("qty", 0))

                sold_map[product_id] += qty

        inventory = []

        for product in products:

            product_id = str(product["_id"])

            inventory.append({

                "id": product_id,

                "name": product.get("name"),

                "sku": product.get("sku"),

                "price": float(
                    product.get("price", 0)
                ),

                "stock": int(
                    product.get("stock", 0)
                ),

                "sold": sold_map.get(
                    product_id,
                    0
                )

            })

        model = InventoryInsightsModel()

        result = model.analyze(
            inventory
        )

        result.sort(

            key=lambda x: (

                x["stock"],

                -x["sold"]

            )

        )

        return result