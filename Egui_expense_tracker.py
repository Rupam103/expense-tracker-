import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

from expense import Expense


FILE_PATH = "expense.csv"

class ExpenseApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("450x520")
        self.root.resizable(True, True)

        self.create_widgets()


    # ---------------- UI ---------------- #

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Expense Tracker",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)


        # Name
        tk.Label(self.root, text="Expense Name").pack()
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=5)


        # Amount
        tk.Label(self.root, text="Amount (₹)").pack()
        self.amount_entry = tk.Entry(self.root, width=30)
        self.amount_entry.pack(pady=5)


        # Category
        tk.Label(self.root, text="Category").pack()

        self.categories = [
            "Food",
            "Ghar ka samaan",
            "Education",
            "Exercise",
            "Travel",
            "Enjoyment",
            "Miscellaneous"
        ]

        self.category_box = ttk.Combobox(
            self.root,
            values=self.categories,
            state="readonly"
        )

        self.category_box.pack(pady=5)
        self.category_box.current(0)


        # Date
        tk.Label(self.root, text="Date (DD-MM-YYYY)").pack()

        self.date_entry = tk.Entry(self.root, width=30)
        self.date_entry.pack(pady=5)

        self.date_entry.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )


        # Buttons
        tk.Button(
            self.root,
            text="Add Expense",
            command=self.add_expense,
            bg="green",
            fg="white",
            width=22
        ).pack(pady=15)


        tk.Button(
            self.root,
            text="Daily Report",
            command=self.daily_report,
            width=22
        ).pack(pady=5)


        tk.Button(
            self.root,
            text="Monthly Report",
            command=self.monthly_report,
            width=22
        ).pack(pady=5)



    # ---------------- LOGIC ---------------- #

    def add_expense(self):

        name = self.name_entry.get()
        amount = self.amount_entry.get()
        category = self.category_box.get()
        date = self.date_entry.get()


        if not name or not amount:
            messagebox.showerror("Error", "Fill all fields")
            return


        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Invalid amount")
            return


        with open(FILE_PATH, "a") as f:
            f.write(f"{date}, {category}, {name}, {amount}\n")


        messagebox.showinfo("Success", "Expense Added")


        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)



    def daily_report(self):

        date = self.date_entry.get()
        self.plot_by_date(date)



    def monthly_report(self):

        try:
            date = datetime.strptime(
                self.date_entry.get(),
                "%d-%m-%Y"
            )

            month_year = date.strftime("%m-%Y")

        except:
            messagebox.showerror("Error", "Invalid date format")
            return


        self.plot_by_month(month_year)



    # ---------------- CHARTS ---------------- #

    def plot_by_date(self, choosen_date):

        data = {}
        tot=0.00

        try:

            with open(FILE_PATH, "r") as f:

                for line in f:

                    d, cat, name, amt = line.strip().split(",")

                    if d == choosen_date:
                        data[cat] = data.get(cat, 0) + float(amt)
                        tot+=float(amt)


        except FileNotFoundError:

            messagebox.showerror("Error", "No expense file found")
            return


        if not data:
            messagebox.showinfo("Info", "No data found")
            return


        self.show_pie(data,tot, f"Daily Report ({choosen_date})")



    def plot_by_month(self, month_year):

        data = {}
        tot=0.00

        try:

            with open(FILE_PATH, "r") as f:

                for line in f:

                    d, cat, name, amt = line.strip().split(",")

                    parts = d.split("-")

                    file_month = parts[1] + "-" + parts[2]


                    if file_month == month_year:
                        data[cat] = data.get(cat, 0) + float(amt)
                        tot+=float(amt)


        except FileNotFoundError:

            messagebox.showerror("Error", "No expense file found")
            return


        if not data:
            messagebox.showinfo("Info", "No data found")
            return


        self.show_pie(data,tot, f"Monthly Report ({month_year})")



    def show_pie(self, data,tot, title):

        categories = list(data.keys())
        amounts = list(data.values())


        def show_amount(pct):

            total = sum(amounts)
            val = pct / 100 * total

            return f"₹{val:.2f}\n({pct:.1f}%)"


        plt.figure(figsize=(7, 7))

        plt.pie(
            amounts,
            labels=categories,
            autopct=show_amount,
            startangle=90
        )


        plt.title(f"{title}\nTotal Money spent: {tot}")
        plt.axis("equal")
        plt.show()



# ---------------- RUN ---------------- #

if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseApp(root)

    root.mainloop()
