import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1075x500")
        self.resizable(False, False)
        self.title("Fixkosten")
        self.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("vista")
        style.configure("Treeview", font=("Roboto", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("TButton", font=("Roboto", 12))
        style.configure("TLabel", font=("Roboto", 12))
        style.configure("TRadiobutton", font=("Roboto", 12))
        style.configure("TEntry", font=("Roboto", 12))
        style.configure("TMenuitem", font=("Roboto", 12))

        self.input_frame = InputFrame(self, self)
        self.input_frame.grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        separator_bottom_horizontal = ttk.Separator(self, orient="horizontal")
        separator_bottom_horizontal.grid(
            column=0, row=1, columnspan=2, sticky="ew", pady=15
        )
        self.result_frame = ResultFrame(self, self)
        self.result_frame.grid(
            column=0, row=2, columnspan=2, sticky=tk.NW, padx=5, pady=5
        )

        # Menu
        application_menu = tk.Menu(self)
        self.configure(menu=application_menu)
        file_menu = tk.Menu(application_menu, tearoff=0)
        file_menu.add_command(
            label="Datei laden", font=("Roboto", 10), command=self.input_frame.open_file
        )
        file_menu.add_command(
            label="Datei speichern",
            font=("Roboto", 10),
            command=self.input_frame.save_file,
        )
        file_menu.add_separator()
        file_menu.add_command(label="Drucken", font=("Roboto", 10))
        file_menu.add_separator()
        file_menu.add_command(
            label="Beenden", font=("Roboto", 10), command=self.input_frame.exit
        )
        application_menu.add_cascade(
            label="Datei",
            menu=file_menu,
        )

        info_menu = tk.Menu(application_menu, tearoff=0)
        info_menu.add_command(
            label="Version", font=("Roboto", 10), command=self.show_version_info
        )
        application_menu.add_cascade(label="Info", menu=info_menu)

    def show_version_info(self):
        version = "0.1.0"
        release_date = "23. August 2023"
        developer_info = "Entwickelt von FloKo. \nAlle Rechte vorbehalten.\n"
        contact_info = "Kontakt: f.kotulla@gmx.de"
        website_link = (
            "Für weitere Informationen besuchen Sie: https://shorturl.at/eru14"
        )
        info_text = f"Version: {version}\nVeröffentlicht am: {release_date}\n\n{developer_info}\n{contact_info}\n{website_link}"
        messagebox.showinfo("Version Informationen", info_text)


class InputFrame(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller

        self.is_saved = True

        self.sum_monthly = tk.DoubleVar(value=0.00)
        self.sum_quarterly = tk.DoubleVar(value=0.00)
        self.sum_semiannual = tk.DoubleVar(value=0.00)
        self.sum_yearly = tk.DoubleVar(value=0.00)
        self.sum_total = tk.DoubleVar(value=0.00)
        self.sum_net_income = tk.DoubleVar(value=0.00)

        label_net_income = ttk.Label(self, text="Nettoeinkommen:", font=("Roboto", 14))
        label_net_income.grid(column=0, row=0, padx=20, pady=10)

        self.entry_net_income = ttk.Entry(self, width=15, justify="right", font=14)
        self.entry_net_income.focus()
        self.entry_net_income.configure(
            validate="key", validatecommand=(self.validate_input, "%P")
        )
        self.entry_net_income.grid(column=1, row=0, sticky="e")

        label_currency = ttk.Label(self, text="€", font=("Roboto", 14), width=2)
        label_currency.grid(column=2, row=0, sticky="w")

        seperator_top_horizontal = ttk.Separator(self, orient="horizontal")
        seperator_top_horizontal.grid(column=0, row=1, columnspan=2, sticky="ew")

        label_new_fixed_costs = ttk.Label(
            self, text="Neue Fixkosten hinzufügen", font=("Roboto", 14)
        )
        label_new_fixed_costs.grid(
            column=0, row=2, columnspan=2, sticky="ew", padx=20, pady=10
        )

        label_receiver = ttk.Label(self, text="Empfänger:", font=("Roboto", 14))
        label_receiver.grid(column=0, row=3, sticky="w", padx=20)

        self.entry_receiver_var = tk.StringVar()
        self.entry_receiver = ttk.Entry(
            self, width=25, textvariable=self.entry_receiver_var, font=14
        )
        self.entry_receiver.grid(column=1, row=3, sticky="e")

        label_sum = ttk.Label(self, text="Betrag:", font=("Roboto", 14))
        label_sum.grid(column=0, row=4, sticky="w", padx=20, pady=5)

        self.entry_sum = ttk.Entry(self, width=15, justify="right", font=14)
        self.entry_sum.configure(
            validate="key", validatecommand=(self.validate_input, "%P")
        )
        self.entry_sum.grid(column=1, row=4, sticky="e")

        label_sum_currency = ttk.Label(self, text="€", font=("Roboto", 14), width=2)
        label_sum_currency.grid(column=2, row=4, sticky="w")

        label_debiting_interval = ttk.Label(
            self, text="Abbuchungsintervall:", font=("Roboto", 14)
        )
        label_debiting_interval.grid(column=0, row=6, padx=20)

        button_add_fixed_cost = ttk.Button(
            self, text="Hinzufügen", width=20, command=self.add_to_list
        )
        button_add_fixed_cost.grid(column=0, row=8)

        self.selected_debiting_interval = tk.StringVar()
        self.radiobutton_debiting_interval_monthly = ttk.Radiobutton(
            self,
            text="monatlich",
            variable=self.selected_debiting_interval,
            value="monatlich",
        )
        self.radiobutton_debiting_interval_quarterly = ttk.Radiobutton(
            self,
            text="quartalsmäßig",
            variable=self.selected_debiting_interval,
            value="quartalsmäßig",
        )
        self.radiobutton_debiting_interval_semiannual = ttk.Radiobutton(
            self,
            text="halbjährlich",
            variable=self.selected_debiting_interval,
            value="halbjährlich",
        )
        self.radiobutton_debiting_interval_yearly = ttk.Radiobutton(
            self,
            text="jährlich",
            variable=self.selected_debiting_interval,
            value="jährlich",
        )
        self.radiobutton_debiting_interval_monthly.grid(
            column=1, row=6, sticky="w", padx=100
        )
        self.radiobutton_debiting_interval_quarterly.grid(
            column=1, row=7, sticky="w", padx=100
        )
        self.radiobutton_debiting_interval_semiannual.grid(
            column=1, row=8, sticky="w", padx=100
        )
        self.radiobutton_debiting_interval_yearly.grid(
            column=1, row=9, sticky="w", padx=100
        )

        self.treeview_fix_costs = ttk.Treeview(
            self, selectmode="extended", columns=("receiver", "sum", "debit interval")
        )
        self.treeview_fix_costs.grid(column=3, row=0, rowspan=7, columnspan=4, pady=15)

        self.treeview_fix_costs.heading("#0", text="Tree Column")
        self.treeview_fix_costs.heading("receiver", text="Empfänger")
        self.treeview_fix_costs.heading("sum", text="Betrag")
        self.treeview_fix_costs.heading("debit interval", text="Abbuchung")
        self.treeview_fix_costs.column("#0", width=0, stretch=tk.NO)
        self.treeview_fix_costs.column("receiver", width=240)
        self.treeview_fix_costs.column("sum", width=100)
        self.treeview_fix_costs.column("debit interval", width=130)

        self.scrollbar_list = ttk.Scrollbar(
            self, orient="vertical", command=self.treeview_fix_costs.yview
        )
        self.scrollbar_list.grid(column=7, row=0, rowspan=7, sticky="ns")
        self.treeview_fix_costs.configure(xscrollcommand=self.scrollbar_list.set)

        button_remove_from_list = ttk.Button(
            self, text="Entfernen", width=20, command=self.delete_selected_fixed_costs
        )
        button_remove_from_list.grid(column=4, row=8)

        button_calculate = ttk.Button(
            self, text="Berechnen", width=20, command=self.calculate_sums
        )
        button_calculate.grid(column=3, row=8)

    def add_to_list(self):
        if (
            self.entry_receiver_var.get() != ""
            and self.entry_sum.get() != ""
            and self.selected_debiting_interval.get() != ""
        ):
            try:
                formatted_sum = (
                    f"{float(self.entry_sum.get().replace(',', '.')):.2f}".replace(
                        ".", ","
                    )
                )

                self.treeview_fix_costs.insert(
                    parent="",
                    index="end",
                    values=(
                        self.entry_receiver_var.get(),
                        formatted_sum,
                        self.selected_debiting_interval.get(),
                    ),
                )
                self.entry_receiver.delete(0, tk.END)
                self.entry_sum.delete(0, tk.END)
                self.selected_debiting_interval.set("")
            except ValueError:
                messagebox.showerror(
                    "Fehler",
                    "Empfänger, Betrag und Abbuchungsintervall müssen ausgefüllt sein!",
                )
        else:
            messagebox.showerror(
                "Fehler",
                "Empfänger, Betrag und Abbuchungsintervall müssen ausgefüllt sein!",
            )

        self.calculate_sums()
        self.is_saved = False

    def delete_selected_fixed_costs(self):
        selected_fixed_costs = self.treeview_fix_costs.selection()
        if selected_fixed_costs != ():
            for selected_fixed_cost in selected_fixed_costs:
                self.treeview_fix_costs.delete(selected_fixed_cost)
        else:
            messagebox.showerror("Fehler", "Nichts ausgewählt!")

        self.calculate_sums()
        self.is_saved = False

    def open_file(self):
        file_name = filedialog.askopenfilename(
            initialdir="savefiles",
            title="Datei öffnen",
            filetypes=(("CSV-Datei", "*.csv"),),
        )

        self.treeview_fix_costs.delete(*self.treeview_fix_costs.get_children())

        with open(file_name, "r") as my_file:
            file = csv.reader(my_file, delimiter=",")

            for row in file:
                self.treeview_fix_costs.insert("", "end", values=row)

        self.calculate_sums()
        self.is_saved = False

    def save_file(self):
        file_name = filedialog.asksaveasfilename(
            initialdir="savefiles",
            title="Datei speichern",
            defaultextension=".csv",
            filetypes=(("CSV-Datei", "*.csv"),),
        )
        with open(file_name, "w", newline="") as my_file:
            file = csv.writer(my_file, delimiter=",")

            for row_id in self.treeview_fix_costs.get_children():
                row = self.treeview_fix_costs.item(row_id)["values"]
                file.writerow(row)

        self.is_saved = True

    def exit(self):
        if not self.is_saved:
            response = messagebox.askyesno(
                "Warnung", "Es gibt nicht gespeicherte Änderungen. Trotzdem beenden?"
            )
            if response:
                self.controller.destroy()
        else:
            self.controller.destroy()

    def get_sum(self, interval):
        sum_list = []

        for child in self.treeview_fix_costs.get_children():
            if interval in self.treeview_fix_costs.item(child)["values"]:
                sum_list.append(
                    float(
                        self.treeview_fix_costs.item(child)["values"][1].replace(
                            ",", "."
                        )
                    )
                )
        return sum(sum_list)

    def calculate_sums(self):
        self.sum_monthly.set(f"{self.get_sum('monatlich'):.2f} €".replace(".", ","))
        self.sum_quarterly.set(
            f"{self.get_sum('quartalsmäßig'):.2f} €".replace(".", ",")
        )
        self.sum_semiannual.set(
            f"{self.get_sum('halbjährlich'):.2f} €".replace(".", ",")
        )
        self.sum_yearly.set(f"{self.get_sum('jährlich'):.2f} €".replace(".", ","))
        self.calculate_total()

    def calculate_total(self):
        try:
            net_income = float(self.entry_net_income.get().replace(",", "."))
            total = (
                net_income
                - self.get_sum("monatlich")
                - self.get_sum("quartalsmäßig") / 3
                - self.get_sum("halbjährlich") / 6
                - self.get_sum("jährlich") / 12
            )
            self.sum_total.set(f"{total:.2f} €".replace(".", ","))
        except ValueError:
            messagebox.showerror(
                "Fehler", "Nettoeinkommen muss ausgefüllt sein und eine Zahl sein!"
            )

    def validate_input(self, new_text):
        if new_text == "":
            return True

        new_text = new_text.replace(",", ".")
        try:
            float(new_text)
            self.entry_sum_var.set(new_text)
            return True
        except ValueError:
            return False


class ResultFrame(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)

        label_result_monthly = ttk.Label(
            self, text="monatliche Kosten:", font=("Roboto", 14)
        )
        label_result_monthly.grid(column=1, row=0, sticky="w", padx=20)

        label_result_quarterly = ttk.Label(
            self, text="quartalsmäßige Kosten:", font=("Roboto", 14)
        )
        label_result_quarterly.grid(column=1, row=1, sticky="w", padx=20)

        label_result_semiannual = ttk.Label(
            self, text="halbjährliche Kosten:", font=("Roboto", 14)
        )
        label_result_semiannual.grid(column=1, row=2, sticky="w", padx=20)

        label_result_yearly = ttk.Label(
            self, text="jährliche Kosten:", font=("Roboto", 14)
        )
        label_result_yearly.grid(column=1, row=3, sticky="w", padx=20)

        sum_monthly = controller.input_frame.sum_monthly

        label_result_sum_monthly = ttk.Label(
            self, textvariable=sum_monthly, foreground="red", font=("Roboto", 14)
        )
        label_result_sum_monthly.grid(column=2, row=0, sticky="ew")

        sum_quarterly = controller.input_frame.sum_quarterly
        label_result_sum_quarterly = ttk.Label(
            self, textvariable=sum_quarterly, foreground="red", font=("Roboto", 14)
        )
        label_result_sum_quarterly.grid(column=2, row=1, sticky="ew")

        sum_semiannual = controller.input_frame.sum_semiannual
        label_result_sum_semiannual = ttk.Label(
            self, textvariable=sum_semiannual, foreground="red", font=("Roboto", 14)
        )
        label_result_sum_semiannual.grid(column=2, row=2, sticky="ew")

        sum_yearly = controller.input_frame.sum_yearly
        label_result_sum_yearly = ttk.Label(
            self, textvariable=sum_yearly, foreground="red", font=("Roboto", 14)
        )
        label_result_sum_yearly.grid(column=2, row=3, sticky="ew")

        separator_vertical = ttk.Separator(self, orient="vertical")
        separator_vertical.grid(column=3, row=0, rowspan=4, sticky="ns", padx=35)

        label_result_total = ttk.Label(
            self, text="Vom Nettogehalt bleiben im Schnitt übrig:", font=("Roboto", 14)
        )
        label_result_total.grid(column=4, row=1, padx=20)

        sum_total = controller.input_frame.sum_total
        label_result_sum_total = ttk.Label(
            self, textvariable=sum_total, foreground="red", font=("Roboto", 14)
        )
        label_result_sum_total.grid(column=5, row=1)


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
