import re
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
    
    def get_weights(self, cls=None):
        items_list = []
        weights = []
        grades_dict = self.grades or self.classes[cls].grades
        for grade in grades_dict:
            i, w = grades_dict[grade].get_items_and_weights()
            items_list += i
            weights += w
        return items_list, weights


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
    
    def get_items_and_weights(self):
        items_list = []
        weights = []
        for item in self.grade_items:
            items_list.append(self.grade_items[item].name)
            weights.append(float(self.grade_items[item].chance.rstrip('%')) / 100)
        return items_list, weights
    

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
    def __init__(self, name=None, quantity=None, chance=None, grade=None):
        self.grade = grade
        self.name = name
        if '[L]' in self.name or '[E]' in self.name or '[R]' in self.name:
            self.name = re.sub(r'\[L\]|\[E\]|\[R\]', grade, self.name)
        if grade and not self.name.startswith(grade):
            self.name = f'{grade} {self.name}'
        self.quantity = quantity
        self.chance = chance

    def __str__(self) -> str:
        return self.name    
    
    def __dict__(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'chance': self.chance,
            'grade': self.grade,
        }
  
