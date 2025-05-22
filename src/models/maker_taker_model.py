"""
Maker/Taker Proportion Model for the Trade Simulator
Predicts likelihood of an order being a maker using logistic regression.
"""

import logging
import numpy as np
from typing import Dict, Any, List
from sklearn.linear_model import LogisticRegression

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MakerTakerModel:
    """
    Predicts the probability that a given order is a maker.
    Trains a logistic regression model using real-time order data.
    """

    def __init__(self) -> None:
        """Initialize model and training data."""
        self.model = LogisticRegression()
        self.is_trained = False
        self.training_data_x: List[List[float]] = []
        self.training_data_y: List[int] = []
        logger.info("Initialized Maker/Taker Model.")

    def predict(self, data: Dict[str, Any]) -> float:
        """
        Predict the probability that the given order is a maker.

        Args:
            data (Dict[str, Any]): Order-level input features.

        Returns:
            float: Maker probability (0.0 = taker, 1.0 = maker)
        """
        try:
            logger.debug(f"Prediction input: {data}")
            features = self._extract_features(data)

            if data["order_type"] == "market":
                logger.debug("Detected market order. Maker proportion = 0.0")
                maker_prob = 0.0
            elif self.is_trained:
                maker_prob = self.model.predict_proba([features])[0][1]
                logger.debug(f"Predicted maker proportion (trained): {maker_prob:.4f}")
            else:
                maker_prob = self._heuristic_prediction(data)
                logger.debug(f"Heuristic prediction (untrained): {maker_prob:.4f}")

            self._collect_training_data(features, data)
            return maker_prob

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.0

    def _extract_features(self, data: Dict[str, Any]) -> List[float]:
        """
        Extract numerical features from input data.

        Returns:
            List[float]: Feature vector.
        """
        try:
            order_type_num = 0 if data["order_type"] == "market" else 1
            features = [
                order_type_num,
                data.get("quantity", 1.0),
                data.get("spread_pct", 0.0),
                data.get("imbalance", 0.5),
                data.get("depth_ratio", 1.0),
                data.get("volatility", 0.01),
            ]
            logger.debug(f"Extracted features: {features}")
            return features
        except KeyError as ke:
            logger.error(f"Missing key in input data: {ke}")
            raise

    def _heuristic_prediction(self, data: Dict[str, Any]) -> float:
        """
        Compute a fallback maker probability using heuristics.

        Returns:
            float: Estimated maker probability.
        """
        spread_pct = data.get("spread_pct", 0)
        quantity = data.get("quantity", 1)

        base = 0.5
        spread_factor = min(0.3, spread_pct / 10)
        quantity_factor = min(0.2, 10 / max(quantity, 1))

        return min(1.0, base + spread_factor + quantity_factor)

    def _collect_training_data(self, features: List[float], data: Dict[str, Any]) -> None:
        """
        Collect labeled data and trigger model training.

        Args:
            features (List[float]): Extracted features.
            data (Dict[str, Any]): Original order data.
        """
        label = 0 if data["order_type"] == "market" else 1
        self.training_data_x.append(features)
        self.training_data_y.append(label)

        logger.debug(f"Added training sample - Label: {label}, Features: {features}")
        logger.debug(f"Training dataset size: {len(self.training_data_y)}")

        if not self.is_trained and len(self.training_data_y) >= 100:
            self._train_model()
        elif self.is_trained and len(self.training_data_y) % 100 == 0:
            self._train_model()

    def _train_model(self) -> None:
        """
        Train logistic regression model on collected samples.
        """
        try:
            X = np.array(self.training_data_x)
            y = np.array(self.training_data_y)

            if len(np.unique(y)) < 2:
                logger.warning("Only one class in data. Skipping model training.")
                return

            self.model.fit(X, y)
            self.is_trained = True
            logger.info(f"Trained Maker/Taker model on {len(y)} samples.")

        except Exception as e:
            logger.error(f"Model training failed: {e}")
