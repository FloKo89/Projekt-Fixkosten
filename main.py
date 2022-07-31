import tkinter as tk
from tkinter import ttk

class Fixkosten(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("880x500")
        #self.minsize(width=900, height=500)
        self.resizable(False, False)
        self.title("Fixkosten")

        self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=1)
        #self.columnconfigure(2, weight=1)
        #self.rowconfigure(0, weight=1)

        #Header(self).grid(column=0, row=0, columnspan=3, sticky="ew")
        Column0(self).grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        Column1(self).grid(column=1, row=0, sticky=tk.NW, padx=5, pady=5)
        #Column2(self).grid(column=2, row=0)
        #SeparatorHorizontal(self).grid(column=0, row=1, columnspan=3, sticky="ew")


class Header(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        label_column_0 = ttk.Label(self, text="Spalte für die Eingabe", font="Roboto, 16")
        label_column_0.grid(column=0, row=0)

        label_column_1 = ttk.Label(self, text="Aktuelle Fixkosten", font="Roboto, 16")
        label_column_1.grid(column=1, row=0)

        label_column_2 = ttk.Label(self, text="Spalte für die Auswertung", font="Roboto, 16")
        label_column_2.grid(column=2, row=0)

class Column0(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        label_net_income = ttk.Label(self, text="Nettoeinkommen:", font="Roboto, 14")
        label_net_income.grid(column=0, row=0, padx=20, pady=10)

        entry_net_income = ttk.Entry(self, width=15)
        entry_net_income.focus()
        entry_net_income.grid(column=1, row=0, padx=20)

        label_currency = ttk.Label(self, text="€", font="Roboto, 14")
        label_currency.grid(column=2, row=0)

        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=3, sticky="ew")

        label_new_fixed_costs = ttk.Label(self, text="Neue Fixkosten hinzufügen:", font="Roboto, 14")
        label_new_fixed_costs.grid(column=0, row=2, columnspan=3, sticky="ew", padx=20, pady=10)

        label_reciever = ttk.Label(self, text="Empfänger:", font="Roboto, 14")
        label_reciever.grid(column=0, row=3, sticky="w", padx=20)

        entry_reciever = ttk.Entry(self, width=30)
        entry_reciever.grid(column=1, row=3)

        label_sum = ttk.Label(self, text="Betrag:", font="Roboto, 14")
        label_sum.grid(column=0, row=4, sticky="w", padx=20, pady=5)

        entry_sum = ttk.Entry(self, width=15)
        entry_sum.grid(column=1, row=4)

        label_sum_surrency = ttk.Label(self, text="€", font="Roboto, 14")
        label_sum_surrency.grid(column=2, row=4)

        label_debiting_interval = ttk.Label(self, text="Abbuchungsintervall:", font="Roboto, 14")
        label_debiting_interval.grid(column=0, row=5, padx=20)

        selected_debiting_interval = tk.StringVar()
        radiobutton_debiting_interval_monthly = ttk.Radiobutton(self, text="monatlich", variable=selected_debiting_interval, value="monatlich")
        radiobutton_debiting_interval_quarter = ttk.Radiobutton(self, text="quartalsmäßig", variable=selected_debiting_interval, value="quartalsmäßig")
        radiobutton_debiting_interval_semiannual = ttk.Radiobutton(self, text="halbjährlich", variable=selected_debiting_interval, value="halbjährlich")
        radiobutton_debiting_interval_yearly = ttk.Radiobutton(self, text="jährlich", variable=selected_debiting_interval, value="jährlich")
        radiobutton_debiting_interval_monthly.grid(column=1, row=5, sticky="e")
        radiobutton_debiting_interval_quarter.grid(column=1, row=6, sticky="e")
        radiobutton_debiting_interval_semiannual.grid(column=1, row=7, sticky="e")
        radiobutton_debiting_interval_yearly.grid(column=1, row=8, sticky="e")



class Column1(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        list = ttk.Treeview(self, columns=("reciever", "sum", "debit interval"))
        list.pack(pady=15, padx=20)

        list.heading("#0", text="Tree Column")
        list.heading("reciever", text="Empfänger")
        list.heading("sum", text="Betrag")
        list.heading("debit interval", text="Abbuchungsintervall")
        list.column("#0", width=0, stretch=tk.NO)
        list.column("reciever", width=220)
        list.column("sum", width=115)
        list.column("debit interval", width=120)


class Column2(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)


class SeparatorHorizontal(ttk.Separator):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.config(orient="horizontal")


root = Fixkosten()
root.mainloop()
