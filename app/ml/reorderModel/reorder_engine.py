from app.ml.reorderModel.model_selector import ReorderModelSelector
from app.ml.reorderModel.lead_time import LeadTimeCalculator
from app.ml.reorderModel.safety_stock import SafetyStockCalculator
from app.ml.reorderModel.reorder_quantity import ReorderQuantityCalculator
from app.ml.reorderModel.reorder_priority import ReorderPriority
from app.ml.reorderModel.reorder_score import ReorderScore
from app.ml.reorderModel.reorder_strategy import ReorderStrategy
from app.ml.reorderModel.reorder_explainer import ReorderExplainer
from app.ml.reorderModel.reorder_validator import ReorderValidator


class ReorderEngine:

    @staticmethod
    def calculate(

        history_length,
        predicted_demand,
        current_stock,
        total_sold,
        category=None,
        seasonal=False

    ):

        # ------------------------------------
        # Model Selection
        # ------------------------------------

        model = ReorderModelSelector.select(

            history_length=history_length,
            seasonal=seasonal

        )

        # ------------------------------------
        # Lead Time
        # ------------------------------------

        lead = LeadTimeCalculator.calculate(

            category=category

        )

        # ------------------------------------
        # Safety Stock
        # ------------------------------------

        safety = SafetyStockCalculator.calculate(

            predicted_demand=predicted_demand,

            lead_time_days=lead["leadTimeDays"]

        )

        # ------------------------------------
        # Forecast Model
        # ------------------------------------

        prediction = model.predict(

            current_stock=current_stock,

            predicted_demand=predicted_demand,

            safety_stock=safety["safetyStock"]

        )

        # ------------------------------------
        # Reorder Quantity
        # ------------------------------------

        quantity = ReorderQuantityCalculator.calculate(

            current_stock=current_stock,

            predicted_demand=predicted_demand,

            safety_stock=safety["safetyStock"]

        )

        # ------------------------------------
        # Priority
        # ------------------------------------

        priority = ReorderPriority.calculate(

            current_stock=current_stock,

            predicted_demand=predicted_demand,

            safety_stock=safety["safetyStock"]

        )

        # ------------------------------------
        # Forecast Score
        # ------------------------------------

        forecast_score = min(

            predicted_demand,

            100

        )

        # ------------------------------------
        # Stock Score
        # ------------------------------------

        if current_stock == 0:

            stock_score = 100

        elif current_stock <= 2:

            stock_score = 90

        elif current_stock <= 5:

            stock_score = 70

        elif current_stock <= 10:

            stock_score = 50

        else:

            stock_score = 20

        # ------------------------------------
        # Sales Score
        # ------------------------------------

        sales_score = min(

            total_sold * 5,

            100

        )

        # ------------------------------------
        # Inventory Turnover
        # ------------------------------------

        if current_stock == 0:

            turnover_score = 100

        else:

            turnover = total_sold / max(

                current_stock,

                1

            )

            turnover_score = min(

                round(

                    turnover * 20

                ),

                100

            )

        # ------------------------------------
        # Safety Score
        # ------------------------------------

        safety_score = min(

            safety["safetyStock"] * 10,

            100

        )

        # ------------------------------------
        # Lead Time Score
        # ------------------------------------

        lead_time_score = min(

            lead["leadTimeDays"] * 10,

            100

        )

        # ------------------------------------
        # Final AI Score
        # ------------------------------------

        score = ReorderScore.calculate(

            forecast_score=forecast_score,

            stock_score=stock_score,

            sales_score=sales_score,

            turnover_score=turnover_score,

            safety_score=safety_score,

            lead_time_score=lead_time_score,

            priority_score=priority["score"]

        )

        # ------------------------------------
        # Business Strategy
        # ------------------------------------

        strategy = ReorderStrategy.decide(

            priority=priority["priority"],

            reorder_qty=quantity["recommendedQty"]

        )

        # ------------------------------------
        # Explainable AI
        # ------------------------------------

        explanation = ReorderExplainer.explain(

            predicted_demand=predicted_demand,

            current_stock=current_stock,

            safety_stock=safety["safetyStock"],

            priority=priority["priority"],

            reorder_score=score["score"],

            lead_time_days=lead["leadTimeDays"]

        )

        # ------------------------------------
        # Final Response
        # ------------------------------------

        result = {

            "forecastModel": prediction["model"],

            "leadTimeDays": lead["leadTimeDays"],

            "leadTimeSource": lead["source"],

            "averageDailyDemand": safety["averageDailyDemand"],

            "safetyStock": safety["safetyStock"],

            "recommendedQty": quantity["recommendedQty"],

            "priority": priority["priority"],

            "priorityScore": priority["score"],

            "reorderScore": score["score"],

            "reorderLevel": score["level"],

            "confidence": explanation["confidence"],

            "action": strategy["action"],

            "reason": strategy["reason"],

            "explanation": explanation["reasons"]

        }

        return ReorderValidator.validate(result)