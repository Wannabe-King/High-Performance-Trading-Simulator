# src/ui/output_panel.py

import tkinter as tk
from tkinter import ttk

class RightPanel:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Output Parameters")

        self.labels = {}
        for key in [
            "Expected Slippage", "Expected Fees", "Market Impact", 
            "Net Cost", "Maker/Taker Proportion", "Internal Latency"
        ]:
            label = ttk.Label(self.frame, text=f"{key}: --", anchor="w")
            label.pack(fill="x", padx=5, pady=2)
            self.labels[key] = label

    def update(self, data):
        for key, value in data.items():
            if key in self.labels:
                self.labels[key].config(text=f"{key}: {value}")
