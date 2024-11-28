import tkinter as tk

class SummaryFrame(tk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.data_manager.observers.append(self.update_summary)
        self.create_widgets()

    def create_widgets(self):
        self.income_label = tk.Label(self, text="รายรับ: 0.00", fg="blue")  # สีฟ้าเริ่มต้น
        self.income_label.grid(row=0, column=0, sticky="w")  # sticky="w" ให้ชิดซ้าย

        self.expense_label = tk.Label(self, text="รายจ่าย: 0.00", fg="red")  # สีแดงเริ่มต้น
        self.expense_label.grid(row=0, column=1, sticky="w") # sticky="w" ให้ชิดซ้าย

        self.balance_label = tk.Label(self, text="ยอดคงเหลือ: 0.00", fg="black")  # สีดำเริ่มต้น
        self.balance_label.grid(row=0, column=2, sticky="w") # sticky="w" ให้ชิดซ้าย

    def update_summary(self):
        data = self.data_manager.get_filtered_data()
        income = sum(amount for _, amount, _ in data if amount > 0)
        expense = abs(sum(amount for _, amount, _ in data if amount < 0))
        balance = income - expense

        self.income_label.config(text=f"รายรับ: {income:.2f}", fg="blue")
        self.expense_label.config(text=f"รายจ่าย: {expense:.2f}", fg="red")

        if balance >= 0:
            self.balance_label.config(text=f"ยอดคงเหลือ: {balance:.2f}", fg="blue") # สีฟ้าถ้าบวก
        else:
            self.balance_label.config(text=f"ยอดคงเหลือ: {balance:.2f}", fg="red")  # สีแดงถ้าลบ