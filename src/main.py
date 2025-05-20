# src/main.py

import tkinter as tk
from src.app.app import TradeSimulatorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeSimulatorApp(root)
    root.mainloop()
