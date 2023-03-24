from collections import defaultdict


class Category:
    def __init__(self, name=None):
        self.name = name
        self.grades = defaultdict(Grade)
        self.classes = defaultdict(PlayerClass)

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Category):
            return self.name == str(other)
        return False
    
    def __dict__(self):
        return {
            'name': self.name,
            'grades': {k: v.__dict__() for k, v in self.grades.items()},
            'classes': {k: v.__dict__() for k, v in self.classes.items()}
        }
    

class Grade:
    def __init__(self, name=None, rate=None):
        self.name = name
        self.rate = rate
        self.grade_items = defaultdict(Item)

    def __str__(self) -> str:
        return self.name

    def __dict__(self):
        return {
            'name': self.name,
            'rate': self.rate,
            'items': {k: v.__dict__() for k, v in self.grade_items.items()}
        }
    

class PlayerClass:
    def __init__(self, name=None):
        self.name = name
        self.grades = defaultdict(Grade)

    def __str__(self) -> str:
        return self.name
    
    def __dict__(self):
        return {
            'name': self.name,
            'grades': {k: v.__dict__() for k, v in self.grades.items()},
        }


class Item:
    def __init__(self, name=None, quantity=None, chance=None):
        self.name = name
        self.quantity = quantity
        self.chance = chance

    def __str__(self) -> str:
        return self.name    
    
    def __dict__(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'chance': self.chance,
        }
  
