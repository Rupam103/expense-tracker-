class Expense:
    
    def __init__(self, name, category, amount) -> None:
        self.none = None
        self.name = name
        self.category = category
        self.amount= float(amount) 
        
    def __repr__(self):
        return f"<Activity: {self.category}, {self.name}, {self.amount:.2f}/->"