import tkinter as tk
from tkinter import ttk

class Fixkosten(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1200x500")
        self.minsize(width=1200, height=500)
        self.title("Fixkosten")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #self.rowconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)
        #self.rowconfigure(2, weight=1)

        Column0(self).grid(column=0, row=0)
        Column1(self).grid(column=1, row=0)
        Column2(self).grid(column=2, row=0)
        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=3, sticky="ew")

class Column0(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)


        title_column0 = ttk.Label(self, text="Spalte für die Eingabe", font="Roboto, 20")
        title_column0.grid(column=0, row=0)

        label1 = ttk.Label(self, text="Fixkosten", font="Roboto, 20")
        label1.grid(column=0, row=1)


class Column1(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        title_column1 = ttk.Label(self, text="Aktuelle Fixkosten", font="Roboto, 20")
        title_column1.grid(column=0, row=0)

        list = ttk.Treeview(self, columns=("reciever", "sum", "date"))
        list.grid(column=0, row=1, sticky="ew")

        list.heading("#0", text="Tree Column")
        list.heading("reciever", text="Empfänger")
        list.heading("sum", text="Betrag")
        list.heading("date", text="Wertstellung")
        list.column("#0", width=0, stretch=tk.NO)
        list.column("sum", width=115)
        list.column("date", width=115)


class Column2(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        title_column2 = ttk.Label(self, text="Spalte für die Auswertung", font="Roboto, 20")
        title_column2.grid(column=0, row=0)


class SeparatorHorizontal(ttk.Separator):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.config(orient="horizontal")


root = Fixkosten()
root.mainloop()
