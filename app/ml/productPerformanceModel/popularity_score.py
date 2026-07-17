class PopularityScore:

    """
    Product popularity based on
    Views
    Wishlist
    Cart
    Orders
    """

    @staticmethod
    def calculate(
            views: int,
            wishlist: int,
            cart: int,
            orders: int
    ) -> float:

        score = (
                views * 0.20 +
                wishlist * 0.20 +
                cart * 0.25 +
                orders * 0.35
        )

        return round(min(score, 100), 2)