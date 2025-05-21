

import tkinter as tk
from tkinter import ttk
from src.app.left_panel import LeftPanel
from src.app.right_panel import RightPanel
from src.app.orderbook_panel import OrderBookPanel

from src.config import UI_WINDOW_TITLE, UI_WINDOW_SIZE, UI_REFRESH_RATE_MS

class TradeSimulatorApp:
    def __init__(self, root):
        root.title(UI_WINDOW_TITLE)
        root.geometry("1080x600")



        self.orderbook_panel = OrderBookPanel(root)
        self.orderbook_panel.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_panel = RightPanel(root)
        self.output_panel.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main layout
        self.input_panel = LeftPanel(root,self.orderbook_panel,self.output_panel)
        self.input_panel.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        def on_closing():
            self.input_panel.on_close()
            root.destroy()

        

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()



        
