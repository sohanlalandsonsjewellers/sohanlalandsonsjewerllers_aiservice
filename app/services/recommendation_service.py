from app.database import db


class RecommendationService:

    @staticmethod
    async def get_products():

        products = await db.Product.find(
            {},
            {
                "_id": 1,
                "name": 1,
                "category": 1,
                "subCategory": 1,
                "description": 1,
                "price": 1,
                "weight": 1
            }
        ).to_list(None)

        result = []

        for product in products:

            result.append({

                "id": str(product["_id"]),

                "name": product.get("name", ""),

                "category": product.get("category", ""),

                "subCategory": product.get("subCategory", ""),

                "description": product.get("description", ""),

                "price": float(
                    product.get("price", 0)
                ),

                "weight": float(
                    product.get("weight", 0)
                )

            })

        return result