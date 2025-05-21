import tkinter as tk
from tkinter import ttk


class OrderBookPanel:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Order Book (Top 10 Levels)")

        self.tree = ttk.Treeview(self.frame, columns=("Price", "Amount", "Type"), show="headings", height=10)
        self.tree.heading("Price", text="Price")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Side")
        self.tree.pack(fill="both", expand=True)

    def update_orderbook(self, bids, asks):
        self.tree.delete(*self.tree.get_children())

        for price, amount in asks[:10][::-1]:
            self.tree.insert("", "end", values=(price, amount, "Ask"))

        for price, amount in bids[:10]:
            self.tree.insert("", "end", values=(price, amount, "Bid"))
