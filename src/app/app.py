

import tkinter as tk
from tkinter import ttk
from src.app.left_panel import LeftPanel
from src.app.right_panel import RightPanel

class TradeSimulatorApp:
    def __init__(self, root):
        root.title("Real-Time Trade Simulator")
        root.geometry("900x500")
        
        # Main layout
        self.input_panel = LeftPanel(root)
        self.input_panel.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_panel = RightPanel(root)
        self.output_panel.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
