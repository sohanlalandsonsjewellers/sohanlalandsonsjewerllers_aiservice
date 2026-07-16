from app.ml.reorderModel.linear_reorder import LinearReorder
from app.ml.reorderModel.random_forest_reorder import RandomForestReorder
from app.ml.reorderModel.lstm_reorder import LSTMReorder
from app.ml.reorderModel.prophet_reorder import ProphetReorder


class ReorderModelSelector:

    @staticmethod
    def select(
        history_length: int,
        seasonal: bool = False
    ):

        # ----------------------------------
        # Very Small Dataset
        # ----------------------------------

        if history_length < 30:

            return LinearReorder()

        # ----------------------------------
        # Seasonal Dataset
        # ----------------------------------

        if seasonal:

            return ProphetReorder()

        # ----------------------------------
        # Medium Dataset
        # ----------------------------------

        if history_length < 365:

            return RandomForestReorder()

        # ----------------------------------
        # Large Dataset
        # ----------------------------------

        return LSTMReorder()