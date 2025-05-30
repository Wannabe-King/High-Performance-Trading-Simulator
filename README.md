Here’s a complete `README.md` for your **Trade Simulator** project:

---

```markdown
# Trade Simulator

A modular, real-time **Trade Simulator** that predicts maker/taker proportions and calculates market impact based on live order book data. Designed to assist in evaluating trade execution strategies using financial models like **Logistic Regression** and **Almgren-Chriss**.

---

## Features

- 📈 **Maker/Taker Proportion Prediction** using Logistic Regression
- 🧮 **Market Impact Estimation** using Almgren-Chriss Model
- 🔍 Real-time Order Book Processing
- ⚙️ Configurable Parameters for Quantity, Volatility, and Depth
- 🧠 Automatic Model Retraining
- 📊 Live Feedback for Trade Strategy Simulations

---

## Project Structure

GOQUANT/
├── documentations/
│ └── models.md # Model explanation and methodology
├── src/
│ ├── app/ # Main UI and simulation interface
│ │ ├── app.py # Simulation entry point
│ │ ├── left_panel.py # Order input panel
│ │ ├── orderbook_panel.py # Visualizes live order book
│ │ └── right_panel.py # Output panel (market impact, fees, etc.)
│ ├── data/
│ │ ├── ws_backend.py # WebSocket backend for real-time data
│ │ └── ws_test.py # WebSocket test script
│ └── models/
│ ├── config.py # Global configuration
│ ├── fee_model.py # Transaction fee calculation
│ ├── maker_taker_model.py # Logistic regression-based prediction
│ ├── market_impact.py # Almgren-Chriss based market impact model
│ ├── spillage.py # Slippage modeling (future use)
│ └── main.py # Entry point for model orchestration
├── venv/ # Python virtual environment
├── README.md
└── requirements.txt # Required packages

```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/trade-simulator.git
cd trade-simulator
````

### Install Dependencies

Make sure you have Python 3.8+

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Simulation

```bash
python src/app.py
```

The simulator will begin reading order book data and output maker/taker probabilities and market impact results for simulated orders.

### Configuration Options

You can tweak parameters such as:

* **Order Type**: market or limit
* **Quantity**: amount of asset to trade
* **Volatility**: as a percentage (e.g., 1.5%)
* **Spread & Depth**: automatically computed from order book

---

## Models Overview

### 1. Maker/Taker Proportion Model

* Type: **Logistic Regression**
* Input Features:

  * `order_type`
  * `quantity`
  * `spread_pct`
  * `imbalance`
  * `depth_ratio`
  * `volatility`
* Output: Probability of order being a **maker**

### 2. Market Impact Model

* Type: **Almgren-Chriss**
* Computes:

  * **Temporary Impact**: Based on order book liquidity and volatility
  * **Permanent Impact**: Based on order size and market depth

---


## Core Functionalities

### Maker/Taker Proportion Model (`maker_taker_model.py`)

* **Model**: Logistic Regression
* **Features**:

  * `order_type` (market/limit)
  * `quantity`
  * `spread_pct`
  * `imbalance`
  * `depth_ratio`
  * `volatility`
* **Output**: Probability that an order is a **maker**

### Market Impact Model (`market_impact.py`)

* **Model**: Almgren-Chriss
* **Calculates**:

  * Temporary market impact (short-term price pressure)
  * Permanent market impact (long-term price shift)
* **Inputs**:

  * Order size
  * Execution time horizon
  * Market volatility
  * Market depth/liquidity

### Fee & Slippage Models

* `fee_model.py`: Calculates transaction cost based on maker/taker roles
* `spillage.py`: Models execution spillage (price deviation from expected)

---

## Configuration

Use `config.py` to define:

* Default volatility
* Order book depth threshold
* Fee rates
* Execution time horizon

---

## Model Training

* Logistic Regression is retrained when new prediction data accumulates
* Retraining happens every 100 new samples after 500 total
* Training data is collected live from predictions with labels auto-inferred

---

## Data Input/Output

* WebSocket input from:

  * `ws_backend.py`: Live feed
  * `ws_test.py`: Simulated/test data
* Order book is visualized using `orderbook_panel.py`

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a new branch (`feature/my-feature`)
3. Commit your changes
4. Open a Pull Request

---

## License

MIT License

---

## Acknowledgements

* Almgren, R. and Chriss, N. (2000). Optimal execution of portfolio transactions.
* scikit-learn for machine learning utilities

```