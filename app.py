import tkinter as tk
from input_frame import InputFrame
from table_frame import TableFrame
from graph_frame import GraphFrame
from data_manager import DataManager
from summary_frame import SummaryFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("โปรแกรมบัญชีส่วนบุคคล")
        self.data_manager = DataManager()
        self.create_widgets()

    def create_widgets(self):
        self.input_frame = InputFrame(self, self.data_manager)
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        table_and_summary_frame = tk.Frame(self)
        table_and_summary_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

        self.table_frame = TableFrame(self, self.data_manager)
        self.table_frame.grid(row=0, column=1, sticky="nsew")

        self.summary_frame = SummaryFrame(self, self.data_manager)
        self.summary_frame.grid(row=1, column=2, sticky="nsew",padx=80)

        self.graph_frame = GraphFrame(self, self.data_manager)
        self.graph_frame.grid(row=0, column=2, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        table_and_summary_frame.grid_rowconfigure(0, weight=1)
        table_and_summary_frame.grid_rowconfigure(1, weight=0)  # ให้ SummaryFrame ไม่ขยายในแนวตั้ง
        table_and_summary_frame.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()