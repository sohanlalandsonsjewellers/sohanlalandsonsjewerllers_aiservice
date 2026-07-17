class ProductValidator:

    @staticmethod
    def validate(product: dict):

        required = [
            "stock",
            "unitsSold",
            "revenue",
            "profit",
            "views",
            "wishlist",
            "cart",
            "orders"
        ]

        missing = [
            field
            for field in required
            if field not in product
        ]

        if missing:
            return {
                "valid": False,
                "missing": missing
            }

        return {
            "valid": True,
            "missing": []
        }