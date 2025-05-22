"""
Maker/Taker proportion model for the Trade Simulator
"""
import logging
import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MakerTakerModel:
    """Model for predicting the proportion of maker vs taker orders."""

    def __init__(self):
        """Initialize the model and training data."""
        self.model = LogisticRegression()
        self.is_trained = False
        self.training_data_x = []
        self.training_data_y = []

        logger.info(" Maker/Taker model initialized.")

    def predict(self, data: Dict[str, Any]) -> float:
        """
        Predict the proportion of maker orders.
        Returns a float between 0.0 (all taker) to 1.0 (all maker).
        """
        try:
            logger.debug(f" Input data for prediction: {data}")
            features = self._extract_features(data)

            if data["order_type"] == "market":
                maker_proportion = 0.0  # Market orders are fully taker
                logger.debug(" Market order detected. Maker proportion = 0.0")
            elif self.is_trained:
                maker_proportion = self.model.predict_proba([features])[0][1]
                logger.debug(f" Model prediction (trained): {maker_proportion:.4f}")
            else:
                # Heuristic until model is trained
                spread_pct = data.get("spread_pct", 0)
                quantity = data.get("quantity", 1)

                base_proportion = 0.5
                spread_factor = min(0.3, spread_pct / 10)
                quantity_factor = min(0.2, 10 / quantity)

                maker_proportion = min(1.0, base_proportion + spread_factor + quantity_factor)
                logger.debug(f" Heuristic prediction (untrained): {maker_proportion:.4f}")

            self._collect_training_data(features, maker_proportion)
            return maker_proportion

        except Exception as e:
            logger.error(f" Error predicting maker/taker proportion: {e}")
            return 0.0

    def _extract_features(self, data: Dict[str, Any]) -> list:
        """Convert input dict into feature list for the model."""
        try:
            order_type_num = 0 if data["order_type"] == "market" else 1
            features = [
                order_type_num,
                data.get("quantity", 1),
                data.get("spread_pct", 0),
                data.get("imbalance", 0.5),
                data.get("depth_ratio", 1.0),
                data.get("volatility", 0.01)
            ]
            logger.debug(f"Extracted features: {features}")
            return features
        except KeyError as ke:
            logger.error(f" Missing key in input data: {ke}")
            raise

    def _collect_training_data(self, features: list, observed_proportion: float):
        """Convert proportion to binary label and train when enough data is available."""
        label = 1 if observed_proportion > 0.5 else 0

        self.training_data_x.append(features)
        self.training_data_y.append(label)

        logger.debug(f" Training sample added. Label: {label}, Features: {features}")
        logger.debug(f" Current dataset size: {len(self.training_data_y)}")

        if not self.is_trained and len(self.training_data_y) >= 100:
            self._train_model()
        elif self.is_trained and len(self.training_data_y) % 100 == 0:
            self._train_model()

    def _train_model(self):
        """Train logistic regression on collected data."""
        try:
            X = np.array(self.training_data_x)
            y = np.array(self.training_data_y)

            self.model.fit(X, y)
            self.is_trained = True

            logger.info(f" Maker/Taker model trained with {len(y)} samples.")
        except Exception as e:
            logger.error(f" Error training model: {e}")
