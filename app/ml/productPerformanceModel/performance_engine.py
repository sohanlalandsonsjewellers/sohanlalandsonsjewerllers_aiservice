from app.ml.productPerformanceModel.sales_score import SalesScore
from app.ml.productPerformanceModel.revenue_score import RevenueScore
from app.ml.productPerformanceModel.profit_score import ProfitScore
from app.ml.productPerformanceModel.inventory_turnover import InventoryTurnover
from app.ml.productPerformanceModel.popularity_score import PopularityScore

from app.ml.productPerformanceModel.fast_moving_detector import (
    FastMovingDetector,
)

from app.ml.productPerformanceModel.slow_moving_detector import (
    SlowMovingDetector,
)

from app.ml.productPerformanceModel.dead_stock_detector import (
    DeadStockDetector,
)

from app.ml.productPerformanceModel.trend_detector import (
    TrendDetector,
)

from app.ml.productPerformanceModel.product_grade import (
    ProductGrade,
)

from app.ml.productPerformanceModel.product_strategy import (
    ProductStrategy,
)

from app.ml.productPerformanceModel.product_explainer import (
    ProductExplainer,
)

from app.ml.productPerformanceModel.product_validator import (
    ProductValidator,
)


class PerformanceEngine:

    @staticmethod
    def evaluate(
        data: dict,
        max_sales: float,
        max_revenue: float,
        max_profit: float,
    ):

        validation = ProductValidator.validate(data)

        if not validation["valid"]:
            raise ValueError(validation["missing"])

        sales_score = SalesScore.calculate(
            data["unitsSold"],
            max_sales,
        )

        revenue_score = RevenueScore.calculate(
            data["revenue"],
            max_revenue,
        )

        profit_score = ProfitScore.calculate(
            data["profit"],
            max_profit,
        )

        turnover_result = InventoryTurnover.calculate(
        data["unitsSold"],
        data["stock"],
        )

        turnover = turnover_result["turnover"]

        popularity_score = PopularityScore.calculate(
            views=data["views"],
            wishlist=data["wishlist"],
            cart=data["cart"],
            orders=data["orders"],
        )

        trend = TrendDetector.detect(
            data["salesHistory"]
        )

        fast = FastMovingDetector.detect(
        units_sold=data["unitsSold"],
        turnover=turnover,
        days_since_last_sale=data["daysSinceLastSale"],
        )

        slow = SlowMovingDetector.detect(
            units_sold=data["unitsSold"],
            turnover=turnover,
            days_since_last_sale=data["daysSinceLastSale"],
        )

        dead = DeadStockDetector.detect(
            stock=data["stock"],
            units_sold=data["unitsSold"],
            days_since_last_sale=data["daysSinceLastSale"],
        )

        grade = ProductGrade.calculate(
            sales_score=sales_score,
            revenue_score=revenue_score,
            profit_score=profit_score,
            turnover_score=min(turnover * 50,100),
            popularity_score=popularity_score,
        )

        strategy = ProductStrategy.recommend(
            grade=grade["grade"],
            trend=trend["trend"],
            fast=fast["isFastMoving"],
            slow=slow["isSlowMoving"],
            dead=dead["isDeadStock"],
        )

        explanation = ProductExplainer.explain(
            grade=grade["grade"],
            trend=trend["trend"],
            fast=fast["isFastMoving"],
            slow=slow["isSlowMoving"],
            dead=dead["isDeadStock"],
            strategy=strategy["action"],
        )

        return {
            "salesScore": sales_score,
            "revenueScore": revenue_score,
            "profitScore": profit_score,
            "inventoryTurnover": turnover_result,
            "popularityScore": popularity_score,
            "trend": trend,
            "fastMoving": fast,
            "slowMoving": slow,
            "deadStock": dead,
            "grade": grade,
            "strategy": strategy,
            "explanation": explanation,
        }