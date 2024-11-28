import json
import datetime

class DataManager:
    def __init__(self):
        self.entries = []
        self.observers = []
        self.current_month = "ทั้งหมด"
        self.data_file = "account_data.json"
        self.load_data()

    def add_entry(self, date, amount, note):
        # เปลี่ยน date เป็น string ที่นี่
        self.entries.append((date.strftime("%Y-%m-%d"), amount, note))
        self.save_data()
        self.notify_observers()

    def delete_entry(self, date, amount, note):
        # ลบ strftime ออก
        entry_to_remove = (date, amount, note)  # ใช้ date string โดยตรง
        if entry_to_remove in self.entries:
            self.entries.remove(entry_to_remove)
            self.save_data()
            self.notify_observers()

    def filter_data(self, month):
        self.current_month = month
        self.notify_observers()

    def get_filtered_data(self):
        if self.current_month == "ทั้งหมด":
            return self.entries

        filtered = []
        for date_str, amount, note in self.entries:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                if f"{date_obj.month:02}" == self.current_month: # หรือ if date_obj.month == int(self.current_month):
                    filtered.append((date_str, amount, note))
            except ValueError:
                print(f"Invalid date format: {date_str}")
        return filtered

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def save_data(self):
        # สร้าง list new_entries เพื่อเก็บข้อมูลที่จะบันทึก
        new_entries = []

        for date_str, amount, note in self.entries:
            try:
                # แปลง amount เป็น string ก่อนบันทึก
                amount_str = str(amount)
                new_entries.append((date_str, amount_str, note))
            except (TypeError, ValueError): # จัดการข้อผิดพลาด
                 print(f"Invalid amount for saving: {amount}")

        with open(self.data_file, 'w') as f:
            json.dump(new_entries, f) # บันทึก new_entries

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.entries = json.load(f)

            # แปลง amount เป็น float หลังจากโหลดข้อมูล
            new_entries = []
            for date_str, amount_str, note in self.entries:
                try:
                    amount = float(amount_str)
                    new_entries.append((date_str, amount, note))
                except ValueError as e: # จัดการข้อผิดพลาด
                    print(f"Error converting amount: {amount_str}")

            self.entries = new_entries

        except FileNotFoundError:
            pass