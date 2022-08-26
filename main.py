import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("930x460")
        self.resizable(False, False)
        self.title("Fixkosten")
        self.style = ttk.Style()
        self.style.theme_use("vista")
        self.columnconfigure(0, weight=1)

        self.frames = {}

        window1 = TopFrame(self, self)
        window1.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=2, sticky="ew")
        window2 = ResultFrame(self, self)
        window2.grid(column=0, row=2, columnspan=2, sticky=tk.NW, padx=5, pady=5)

        self.frames[TopFrame] = window1
        self.frames[ResultFrame] = window2

        # Menu
        application_menu = tk.Menu(self)
        self.configure(menu=application_menu)
        file_menu = tk.Menu(application_menu, tearoff=0)
        file_menu.add_command(label="Datei laden", command=window1.open_file)
        file_menu.add_command(label="Datei speichern", command=window1.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Drucken")
        file_menu.add_separator()
        file_menu.add_command(label="Beenden")
        application_menu.add_cascade(label="Datei", menu=file_menu)

        info_menu = tk.Menu(application_menu, tearoff=0)
        info_menu.add_command(label="Version")
        application_menu.add_cascade(label="Info", menu=info_menu)


class TopFrame(ttk.Frame):

    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.dict_from_get_results = {}

        label_net_income = ttk.Label(self, text="Nettoeinkommen:", font=("Roboto", 14))
        label_net_income.grid(column=0, row=0, padx=20, pady=10)

        self.entry_net_income = ttk.Entry(self, width=15)
        self.entry_net_income.focus()
        self.entry_net_income.grid(column=1, row=0, padx=20)

        label_currency = ttk.Label(self, text="€", font=("Roboto", 14))
        label_currency.grid(column=2, row=0)

        SeparatorHorizontal(self).grid(column=0, row=1, columnspan=2, sticky="ew")

        label_new_fixed_costs = ttk.Label(self, text="Neue Fixkosten hinzufügen", font=("Roboto", 14))
        label_new_fixed_costs.grid(column=0, row=2, columnspan=2, sticky="ew", padx=20, pady=10)

        label_receiver = ttk.Label(self, text="Empfänger:", font=("Roboto", 14))
        label_receiver.grid(column=0, row=3, sticky="w", padx=20)

        self.entry_receiver_var = tk.StringVar()
        self.entry_receiver = ttk.Entry(self, width=30, textvariable=self.entry_receiver_var)
        self.entry_receiver.grid(column=1, row=3)

        label_sum = ttk.Label(self, text="Betrag:", font=("Roboto", 14))
        label_sum.grid(column=0, row=4, sticky="w", padx=20, pady=5)

        self.entry_sum_var = tk.StringVar()
        self.entry_sum = ttk.Entry(self, width=15, textvariable=self.entry_sum_var)
        self.entry_sum.grid(column=1, row=4)

        label_sum_currency = ttk.Label(self, text="€", font=("Roboto", 14))
        label_sum_currency.grid(column=2, row=4)

        label_debiting_interval = ttk.Label(self, text="Abbuchungsintervall:", font=("Roboto", 14))
        label_debiting_interval.grid(column=0, row=6, padx=20)

        button_add_fixed_cost = ttk.Button(self, text="Hinzufügen", width=20, command=self.add_to_list)
        button_add_fixed_cost.grid(column=0, row=8)

        self.selected_debiting_interval = tk.StringVar()
        self.radiobutton_debiting_interval_monthly = ttk.Radiobutton(self, text="monatlich",
                                                                     variable=self.selected_debiting_interval,
                                                                     value="monatlich")
        self.radiobutton_debiting_interval_quarterly = ttk.Radiobutton(self, text="quartalsmäßig",
                                                                       variable=self.selected_debiting_interval,
                                                                       value="quartalsmäßig")
        self.radiobutton_debiting_interval_semiannual = ttk.Radiobutton(self, text="halbjährlich",
                                                                        variable=self.selected_debiting_interval,
                                                                        value="halbjährlich")
        self.radiobutton_debiting_interval_yearly = ttk.Radiobutton(self, text="jährlich",
                                                                    variable=self.selected_debiting_interval,
                                                                    value="jährlich")
        self.radiobutton_debiting_interval_monthly.grid(column=1, row=6, sticky="e")
        self.radiobutton_debiting_interval_quarterly.grid(column=1, row=7, sticky="e")
        self.radiobutton_debiting_interval_semiannual.grid(column=1, row=8, sticky="e")
        self.radiobutton_debiting_interval_yearly.grid(column=1, row=9, sticky="e")

        self.treeview_fix_costs = ttk.Treeview(self, selectmode="extended",
                                               columns=("receiver", "sum", "debit interval"))
        self.treeview_fix_costs.grid(column=3, row=0, rowspan=7, columnspan=2, pady=15)

        self.treeview_fix_costs.heading("#0", text="Tree Column")
        self.treeview_fix_costs.heading("receiver", text="Empfänger")
        self.treeview_fix_costs.heading("sum", text="Betrag")
        self.treeview_fix_costs.heading("debit interval", text="Abbuchungsintervall")
        self.treeview_fix_costs.column("#0", width=0, stretch=tk.NO)
        self.treeview_fix_costs.column("receiver", width=220)
        self.treeview_fix_costs.column("sum", width=115)
        self.treeview_fix_costs.column("debit interval", width=120)

        self.scrollbar_list = ttk.Scrollbar(self, orient="vertical", command=self.treeview_fix_costs.yview)
        self.scrollbar_list.grid(column=5, row=0, rowspan=7, sticky="ns")
        self.treeview_fix_costs.configure(xscrollcommand=self.scrollbar_list.set)

        button_remove_from_list = ttk.Button(self, text="Entfernen", width=20, command=self.delete_selected_fixed_costs)
        button_remove_from_list.grid(column=4, row=8)

        button_calculate = ttk.Button(self, text="Berechnen", width=20, command=self.get_sum_monthly)
        button_calculate.grid(column=3, row=8)

    def add_to_list(self):
        if self.entry_receiver_var.get() != "" and self.entry_sum_var.get() != "" \
                and self.selected_debiting_interval.get() != "":
            self.treeview_fix_costs.insert(parent="", index="end",
                                           values=(self.entry_receiver_var.get(), self.entry_sum_var.get(),
                                                   self.selected_debiting_interval.get()))
            self.entry_receiver.delete(0, tk.END)
            self.entry_sum.delete(0, tk.END)
            self.selected_debiting_interval.set("")
        else:
            print("Ungültige Eingabe")

    def delete_selected_fixed_costs(self):
        selected_fixed_costs = self.treeview_fix_costs.selection()
        if selected_fixed_costs != ():
            for selected_fixed_cost in selected_fixed_costs:
                self.treeview_fix_costs.delete(selected_fixed_cost)
        else:
            print("Nichts ausgewählt!")

    def get_results(self):
        list_monthly = []
        list_quarterly = []
        list_semiannual = []
        list_yearly = []
        for child in self.treeview_fix_costs.get_children():
            print(self.treeview_fix_costs.item(child))
            if "monatlich" in self.treeview_fix_costs.item(child)["values"]:
                list_monthly.append(self.treeview_fix_costs.item(child)["values"][1])
            elif "quartalsmäßig" in self.treeview_fix_costs.item(child)["values"]:
                list_quarterly.append(self.treeview_fix_costs.item(child)["values"][1])
            elif "halbjährlich" in self.treeview_fix_costs.item(child)["values"]:
                list_semiannual.append(self.treeview_fix_costs.item(child)["values"][1])
            elif "jährlich" in self.treeview_fix_costs.item(child)["values"]:
                list_yearly.append(self.treeview_fix_costs.item(child)["values"][1])

        list_results = (sum(list_monthly), sum(list_quarterly), sum(list_semiannual), sum(list_yearly))
        list_debit_interval = ("monatlich", "quartalsmäßig", "halbjährlich", "jährlich")
        dict_from_get_results = dict(zip(list_debit_interval, list_results))
        print(dict_from_get_results)

        return self.dict_from_get_results

    def open_file(self):
        file_name = filedialog.askopenfilename(initialdir="C:/Users/fkotu/Desktop/Fixkosten", title="Datei öffnen")
        with open(file_name, "r") as my_file:
            file = csv.reader(my_file, delimiter=',')

            for row in file:
                print('load row:', row)
                self.treeview_fix_costs.insert("", 'end', values=row)

    def save_file(self):
        file_name = filedialog.asksaveasfilename(initialdir="C:/Users/fkotu/Desktop/Fixkosten", title="Datei speichern")
        with open(file_name, "w", newline='') as my_file:
            file = csv.writer(my_file, delimiter=',')

            for row_id in self.treeview_fix_costs.get_children():
                row = self.treeview_fix_costs.item(row_id)['values']
                print('save row:', row)
                file.writerow(row)


    def get_sum_monthly(self):
        list_monthly = []
        for child in self.treeview_fix_costs.get_children():
            if "monatlich" in self.treeview_fix_costs.item(child)["values"]:
                list_monthly.append(self.treeview_fix_costs.item(child)["values"][1])

        print(list_monthly)
        return sum(list_monthly)

    def set_sum_monthly(self, value):
        self.sum_monthly = value

    sum_monthly = property(get_sum_monthly, set_sum_monthly)




class ResultFrame(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
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

        sum_monthly = tk.StringVar()
        sum_monthly.set(TopFrame.sum_monthly.getter)
        label_result_sum_monthly = ttk.Label(self, text=sum_monthly, textvariable=sum_monthly, foreground="red", font=("Roboto", 14))
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


root = MainWindow()
root.mainloop()
