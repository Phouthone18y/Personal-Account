import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

import datetime
import numpy as np

class GraphFrame(tk.Frame):
    def __init__(self, master, data_manager):
        super().__init__(master)
        self.data_manager = data_manager
        self.data_manager.observers.append(self.update_graph)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        data = self.data_manager.get_filtered_data()

        if not data:
            self.ax.set_title("No data to display")
            self.fig.canvas.draw()
            return

        daily_positive_sums = {}  # เก็บผลรวมของค่าบวก
        daily_negative_sums = {}  # เก็บผลรวมของค่าลบ

        for date_str, amount, note in data:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date().day
            if amount >= 0:
                daily_positive_sums[date] = daily_positive_sums.get(date, 0) + amount
            else:
                daily_negative_sums[date] = daily_negative_sums.get(date, 0) + amount

        all_dates = sorted(set(daily_positive_sums.keys()) | set(daily_negative_sums.keys()))  # รวมวันที่ทั้งหมด

        positive_amounts = [daily_positive_sums.get(date, 0) for date in all_dates]
        negative_amounts = [daily_negative_sums.get(date, 0) for date in all_dates]

        # สร้างกราฟแท่งสองชุด
        self.ax.bar(all_dates, positive_amounts, label='Income', color='skyblue')
        self.ax.bar(all_dates, negative_amounts, label='Expenses', color='red')

        self.ax.set_xlabel('Day')
        self.ax.set_ylabel('Amount (Baht)')

        month_name = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December',
            'ทั้งหมด': 'All'
        }
        self.ax.set_title(f'Expenses for {month_name[self.data_manager.current_month]}')
        self.ax.set_xticks(all_dates)
        self.ax.legend()  # เพิ่ม legend

        self.fig.canvas.draw()