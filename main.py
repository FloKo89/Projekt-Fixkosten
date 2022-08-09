import tkinter as tk
from tkinter import ttk


class Fixkosten(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("930x460")
        self.resizable(False, False)
        self.title("Fixkosten")
        self.style = ttk.Style()
        self.style.theme_use("xpnative")

        self.columnconfigure(0, weight=1)
        TopFrame(self).grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=2, sticky="ew")
        ResultFrame(self).grid(column=0, row=2, columnspan=2, sticky=tk.NW, padx=5, pady=5)


class TopFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        label_net_income = ttk.Label(self, text="Nettoeinkommen:", font=("Roboto", 14))
        label_net_income.grid(column=0, row=0, padx=20, pady=10)

        self.entry_net_income = ttk.Entry(self, width=15)
        self.entry_net_income.focus()
        self.entry_net_income.bind("<Return>", self.check)
        self.entry_net_income.grid(column=1, row=0, padx=20)

        label_currency = ttk.Label(self, text="€", font=("Roboto", 14))
        label_currency.grid(column=2, row=0)

        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=2, sticky="ew")

        label_new_fixed_costs = ttk.Label(self, text="Neue Fixkosten hinzufügen", font=("Roboto", 14))
        label_new_fixed_costs.grid(column=0, row=2, columnspan=2, sticky="ew", padx=20, pady=10)

        label_reciever = ttk.Label(self, text="Empfänger:", font=("Roboto", 14))
        label_reciever.grid(column=0, row=3, sticky="w", padx=20)

        self.entry_reciever = ttk.Entry(self, width=30)
        self.entry_reciever.grid(column=1, row=3)

        label_sum = ttk.Label(self, text="Betrag:", font=("Roboto", 14))
        label_sum.grid(column=0, row=4, sticky="w", padx=20, pady=5)

        self.entry_sum = ttk.Entry(self, width=15)
        self.entry_sum.grid(column=1, row=4)

        label_sum_currency = ttk.Label(self, text="€", font=("Roboto", 14))
        label_sum_currency.grid(column=2, row=4)

        label_debiting_interval = ttk.Label(self, text="Abbuchungsintervall:", font=("Roboto", 14))
        label_debiting_interval.grid(column=0, row=6, padx=20)

        button_add_fixed_cost = ttk.Button(self, text="Hinzufügen", width=20, command=self.add_to_list)
        button_add_fixed_cost.grid(column=0, row=8)

        self.selected_debiting_interval = tk.StringVar()
        self.radiobutton_debiting_interval_monthly = ttk.Radiobutton(self, text="monatlich", variable=self.selected_debiting_interval, value="monatlich")
        self.radiobutton_debiting_interval_quarterly = ttk.Radiobutton(self, text="quartalsmäßig", variable=self.selected_debiting_interval, value="quartalsmäßig")
        self.radiobutton_debiting_interval_semiannual = ttk.Radiobutton(self, text="halbjährlich", variable=self.selected_debiting_interval, value="halbjährlich")
        self.radiobutton_debiting_interval_yearly = ttk.Radiobutton(self, text="jährlich", variable=self.selected_debiting_interval, value="jährlich")
        self.radiobutton_debiting_interval_monthly.grid(column=1, row=6, sticky="e")
        self.radiobutton_debiting_interval_quarterly.grid(column=1, row=7, sticky="e")
        self.radiobutton_debiting_interval_semiannual.grid(column=1, row=8, sticky="e")
        self.radiobutton_debiting_interval_yearly.grid(column=1, row=9, sticky="e")

        self.treeview_fix_costs = ttk.Treeview(self, selectmode="extended", columns=("reciever", "sum", "debit interval"))
        self.treeview_fix_costs.grid(column=3, row=0, rowspan=7, pady=15)

        self.treeview_fix_costs.heading("#0", text="Tree Column")
        self.treeview_fix_costs.heading("reciever", text="Empfänger")
        self.treeview_fix_costs.heading("sum", text="Betrag")
        self.treeview_fix_costs.heading("debit interval", text="Abbuchungsintervall")
        self.treeview_fix_costs.column("#0", width=0, stretch=tk.NO)
        self.treeview_fix_costs.column("reciever", width=220)
        self.treeview_fix_costs.column("sum", width=115)
        self.treeview_fix_costs.column("debit interval", width=120)

        self.scrollbar_list = ttk.Scrollbar(self, orient="vertical", command=self.treeview_fix_costs.yview)
        self.scrollbar_list.grid(column=4, row=0, rowspan=7, sticky="ns")
        self.treeview_fix_costs.configure(xscrollcommand=self.scrollbar_list.set)

        button_remove_from_list = ttk.Button(self, text="Entfernen", width=20, command=self.delete_selected_fixed_costs)
        button_remove_from_list.grid(column=3, row=8, columnspan=2)

    def add_to_list(self):
        if self.entry_reciever.get() != "" and self.entry_sum.get() != "" and self.selected_debiting_interval.get() != "":
            self.treeview_fix_costs.insert(parent="", index="end", values=(self.entry_reciever.get(), self.entry_sum.get(), self.selected_debiting_interval.get()))
            self.entry_reciever.delete(0, tk.END)
            self.entry_sum.delete(0, tk.END)
            self.selected_debiting_interval.set("")
        else:
            print("Ungülige Eingabe")

    def check(self):
        self.net_income = float(self.entry_net_income.get())
        print(self.net_income)

    def delete_selected_fixed_costs(self):
        selected_fixed_costs = self.treeview_fix_costs.selection()
        if selected_fixed_costs != ():
            for selected_fixed_cost in selected_fixed_costs:
                self.treeview_fix_costs.delete(selected_fixed_cost)
        else:
            print("Nichts ausgewählt!")


class ResultFrame(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=4)
        self.rowconfigure(0, weight=1)

        label_result_monthly = ttk.Label(self, text="monatliche Kosten:", font=("Roboto", 14))
        label_result_monthly.grid(column=0, row=0, sticky="w", padx=20)
        label_result_quarterly = ttk.Label(self, text="quartalsmäßige Kosten:", font=("Roboto", 14))
        label_result_quarterly.grid(column=0, row=1, sticky="w", padx=20)
        label_result_semiannual = ttk.Label(self, text="halbjährliche Kosten:", font=("Roboto", 14))
        label_result_semiannual.grid(column=0, row=2, sticky="w", padx=20)
        label_result_yearly = ttk.Label(self, text="jährliche Kosten:", font=("Roboto", 14))
        label_result_yearly.grid(column=0, row=3, sticky="w", padx=20)

        label_result_sum_monthly = ttk.Label(self, text="Summe in €", foreground="red", font=("Roboto", 14))
        label_result_sum_monthly.grid(column=1, row=0)
        label_result_sum_quarterly = ttk.Label(self, text="Summe in €", foreground="red", font=("Roboto", 14))
        label_result_sum_quarterly.grid(column=1, row=1)
        label_result_sum_semiannual = ttk.Label(self, text="Summe in €", foreground="red", font=("Roboto", 14))
        label_result_sum_semiannual.grid(column=1, row=2)
        label_result_sum_yearly = ttk.Label(self, text="Summe in €", foreground="red", font=("Roboto", 14))
        label_result_sum_yearly.grid(column=1, row=3)

        SeparatorVertical(self).grid(column=2, row=0, rowspan=4, sticky="ns", padx=35)

        label_result_sum_total = ttk.Label(self, text="Vom Nettogehalt bleiben im Schnitt übrig:", font=("Roboto", 14))
        label_result_sum_total.grid(column=3, row=1, padx=20)

        label_result_sum_total2 = ttk.Label(self, text="Betrag", foreground="red", font=("Roboto", 14))
        label_result_sum_total2.grid(column=4, row=1)

class SeparatorHorizontal(ttk.Separator):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.config(orient="horizontal")

class SeparatorVertical(ttk.Separator):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.config(orient="vertical")


root = Fixkosten()

application_menu = tk.Menu(root)
root.configure(menu=application_menu)
file_menu = tk.Menu(application_menu, tearoff=0)
file_menu.add_command(label="Datei laden")
file_menu.add_command(label="Datei speichern")
file_menu.add_separator()
file_menu.add_command(label="Drucken")
file_menu.add_separator()
file_menu.add_command(label="Beenden")
application_menu.add_cascade(label="Datei", menu=file_menu)

info_menu = tk.Menu(application_menu, tearoff=0)
info_menu.add_command(label="Version")
application_menu.add_cascade(label="Info", menu=info_menu)

root.mainloop()
