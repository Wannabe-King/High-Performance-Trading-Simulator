Sure! Here's a detailed markdown documentation that satisfies all your criteria:

---

# Maker/Taker and Market Impact Modeling Documentation

## Overview

This documentation outlines the rationale, methodology, and implementation details behind the **Maker/Taker Proportion Model** and the **Market Impact Model** used in the Trade Simulator. These models are critical for accurately simulating order execution behavior in financial markets.

---

## 1. Model Selection and Parameters

### Maker/Taker Model

The **Maker/Taker Model** is designed to estimate the probability that a given order will act as a *maker* (adds liquidity) or *taker* (removes liquidity).

* **Model Chosen**: Logistic Regression
* **Rationale**:

  * Logistic Regression is interpretable, efficient, and suitable for binary classification.
  * It provides probabilistic output (`predict_proba`) to represent the likelihood of maker behavior.
  * Low risk of overfitting with proper regularization and scaling.

**Parameters**:

* `order_type`: Market or Limit
* `quantity`: Size of the order
* `spread_pct`: Percentage difference between bid and ask
* `imbalance`: Bid-ask volume imbalance
* `depth_ratio`: Ratio of smaller to larger book depth
* `volatility`: Estimated short-term market volatility

---

### Market Impact Model

The **Market Impact Model** estimates how an order of a given size will affect the execution price based on the Almgren-Chriss framework.

* **Model Chosen**: Almgren-Chriss Market Impact Model
* **Rationale**:

  * Widely used in quantitative finance for estimating price slippage.
  * Decomposes market impact into temporary (execution cost) and permanent (price change) components.

**Parameters**:

* `sigma`: Market volatility
* `eta`: Market depth parameter (temporary impact sensitivity)
* `gamma`: Market resilience parameter (permanent impact sensitivity)
* `quantity`: Order size
* `V`: Estimated daily volume

---

## 2. Regression Techniques Chosen

The maker/taker prediction uses **Logistic Regression** from `scikit-learn`:

```python
from sklearn.linear_model import LogisticRegression
```

* **Feature Engineering**:

  * Converts categorical variables (order type) to numeric
  * Scales numerical inputs (volatility, quantity, etc.)
* **Training Strategy**:

  * Online learning-style data collection
  * Model trains after collecting 100+ samples
  * Retraining occurs every additional 100 samples after 500

Advantages:

* Fast convergence
* Low computational overhead
* Works well with small-to-medium datasets

---

## 3. Market Impact Calculation Methodology

The market impact is calculated using the **Almgren-Chriss model**, which separates impact into two components:

### 1. Temporary Impact:

Represents the immediate price impact due to order book pressure.

$$
I_{\text{temp}} = \eta \cdot \sigma \cdot \sqrt{\frac{Q}{V}}
$$

* `Q`: Quantity of the order
* `V`: Estimated daily volume
* `σ`: Volatility
* `η`: Market depth factor

### 2. Permanent Impact:

Represents the persistent price movement after execution.

$$
I_{\text{perm}} = \gamma \cdot \sigma \cdot \frac{Q}{V}
$$

* `γ`: Market resilience parameter

### Total Market Impact:

$$
I_{\text{total}} = I_{\text{temp}} + I_{\text{perm}}
$$

The final result is expressed as a **percentage of price impact**.

---

## 4. Performance Optimization Approaches

### a. Feature Preprocessing

* Feature extraction and normalization are done before training.
* Avoids runtime computation bottlenecks.

### b. Efficient Data Collection

* Training data is collected incrementally.
* Retraining is batched to avoid frequent overhead.

### c. Model Retraining Thresholds

* Avoids overfitting and excessive compute by retraining at controlled intervals (every 100 new samples after 500).

### d. Exception Handling

* Graceful fallback for market impact and prediction errors.
* Ensures continuity of simulation even if data is sparse or malformed.

### e. Adaptive Parameters

* `eta` and `gamma` are dynamically estimated from orderbook depth and spread.
* Enables responsive behavior in volatile or illiquid markets.

---

## Conclusion

This modeling setup provides a practical and efficient solution for simulating realistic trade execution behaviors in a dynamic market. With a balance of financial theory and engineering efficiency, the models allow for flexible and extensible market simulations.

---

