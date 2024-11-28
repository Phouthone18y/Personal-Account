import tkinter as tk
from tkinter import ttk
import datetime

class TableFrame(tk.Frame):

    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.data_manager.observers.append(self.update_table)
        self.create_widgets()

    def create_widgets(self):

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="กรองเดือน:").pack(side=tk.LEFT, padx=5)
        self.all_months = ["ทั้งหมด"] + [str(i) for i in range(1, 13)]
        self.current_month = tk.StringVar(value="ทั้งหมด")
        self.month_cb = ttk.Combobox(filter_frame, values=self.all_months, textvariable=self.current_month, state="readonly", width = 10)
        self.month_cb.pack(side=tk.LEFT)
        self.month_cb.current(0)  # ตั้งค่าเริ่มต้นเป็น "ทั้งหมด"
        self.month_cb.bind("<<ComboboxSelected>>", self.filter_data)

        self.tree = ttk.Treeview(self, columns=("Date", "Amount", "Note"), show='headings')
        self.tree.heading("Date", text="วันที่")
        self.tree.heading("Amount", text="จำนวนเงิน")
        self.tree.heading("Note", text="หมายเหตุ")
        self.tree.pack(padx=5, pady=5)

        delete_button = tk.Button(self, text="ลบข้อมูล", command=self.delete_entry)
        delete_button.pack(pady=10)

        self.update_table()

    def delete_entry(self):
        selected_item = self.tree.selection()
        if selected_item:
            date_str, amount_str, note = self.tree.item(selected_item)['values']

            # แปลง amount_str เป็น float
            amount = float(amount_str)

            self.data_manager.delete_entry(date_str, amount, note)

    def filter_data(self, event=None):
        selected_month = self.current_month.get()
        if selected_month != "ทั้งหมด":
            selected_month = f"{int(selected_month):02}" # แก้ไขตรงนี้
        print(f"Selected month: {selected_month}") # เพิ่ม print เพื่อ debug
        self.data_manager.filter_data(selected_month)
        self.update_table()

    def update_table(self):
        self.tree.delete(*self.tree.get_children())  # clear table
        data = self.data_manager.get_filtered_data()

        for item in data:
            self.tree.insert("", tk.END, values=item)