from expense import Expense
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    print(f"Running Expense Tracker: ")
    

    a=int(input("Who?\n1. Akanksha\n2. Rupam"))
    if a==1:
        expense_file_path= "akanksha.csv"
    else:
        expense_file_path= "expense.csv"
    
    n=int(input("1.Enter a expense record\n2.Display graph\n3.Do both\n4.Diaplay monthly expense graph\nEnter your choice: "))
    if n==1:
        exp = get_user_expense()
        save_expense_to_file(exp, expense_file_path)
    elif n==2:
        Visualising_user_expense(expense_file_path)
    elif n==3:
        exp = get_user_expense()
        save_expense_to_file(exp, expense_file_path)
        Visualising_user_expense(expense_file_path)
    else :
        Visualising_monthly_expense(expense_file_path)

def get_user_expense():
    print(f"Getting user expense information: ")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter amount spent by the category in rupees: "))
    print(f"You've entered {expense_name}, {expense_amount}")
    
    expense_categories = [
       "Food", 
       "Ghar ka samaan", 
       "Education", 
       "Exercise",  
       "Travel", 
       "Enjoyment",
       "Miscellaneous",
       "Savings"
    ]
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i+1}. {category_name}")
            
        value_range= f"[1 - {len(expense_categories)}]"
        selected_Index = int(input(f"Enter a category number {value_range}: ")) -1
        
        if(selected_Index in range(len(expense_categories))):
            selected_category = expense_categories[selected_Index]
            new_exp = Expense(name=expense_name, category=selected_category, amount=expense_amount )
            return new_exp
        else:
            print("Ivalid category. Please try again!")
            
def save_expense_to_file(exp, expense_file_path):
    print(f"Saving user expense: {exp}")
    today = datetime.now().strftime('%d-%m-%Y')
    with open(expense_file_path, "a") as f:
        f.write(f"{today}, {exp.category}, {exp.name}, {exp.amount}\n")

def Visualising_user_expense(expense_file_path):
    choosen_date = input("Enter the date (DD-MM-YYYY): ")
    print(f"Visualizing user expense :")
    expenses : list[Expense]= []
    
    with open(expense_file_path, "r")  as f: 
        lines = f.readlines()
        for line in lines: 
            expense_date, expense_category, expense_name, expense_amount = line.strip().split(",")
            if expense_date == choosen_date:
                line_expense = Expense(
                    name= expense_name, category= expense_category, amount=expense_amount
                )
                expenses.append(line_expense)

    if not expenses:
        print(f"No expenses recordrd for{choosen_date}.")
        return 
    
    amount_by_category ={}
    tot=0.00
    for exps in expenses:
        key = exps.category
        if key in amount_by_category:
            amount_by_category[key] += exps.amount
            tot+=exps.amount
        else:
            amount_by_category[key] = exps.amount
            tot+=exps.amount
    
    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())
    plot(amounts, categories, choosen_date, tot)

def show_amount(pct, allvals):
    total = sum(allvals)
    amount = pct/100 * total
    return f"₹{amount:.2f}\n({pct:.1f}%)"

def Visualising_monthly_expense(expense_file_path):
    month_year = input("Enter month and year (MM-YYYY): ")
    print("Visualizing monthly expense:")
    expenses = []

    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_date, expense_category, expense_name, expense_amount = line.strip().split(", ")
            date_parts = expense_date.split("-")
            file_month_year = date_parts[1] + "-" + date_parts[2]

            if file_month_year == month_year:
                exp = Expense(
                    name=expense_name,
                    category=expense_category,
                    amount=float(expense_amount)
                )
                expenses.append(exp)

    if not expenses:
        print(f"No expenses found for {month_year}")
        return


    amount_by_category = {}
    tot=0.00
    for exp in expenses:
        if exp.category in amount_by_category:
            amount_by_category[exp.category] += exp.amount
            tot+=exp.amount
        else:
            amount_by_category[exp.category] = exp.amount
            tot+=exp.amount

    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())
    plot(amounts, categories, month_year, tot)

def plot(amounts, categories, date, tot):
    plt.figure(figsize=(8, 8))

    plt.pie(
        amounts,
        labels=categories,
        autopct=lambda pct: show_amount(pct, amounts),
        startangle=90
    )

    plt.title(f"Monthly Expense Distribution ({date})\nTotal amount spent: {tot}/-")

    plt.axis('equal')
    plt.show()


    
if __name__=='__main__':
    main()