import json
import os

from item_classes import Category, Grade, Item, PlayerClass
from utils import print_data


def serialize(data):
    json_str = json.dumps([d.__dict__() for d in data])
    with open('data.json', 'w') as f:
        f.write(json_str)
    

def deserialize(data):
    file = 'data.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            json_str = f.read()
        data_list = json.loads(json_str)
        curr_category = curr_class = curr_grade = curr_item = None
        for category in data_list:
            curr_category = Category(category['name'])
            data.append(curr_category)
            if curr_category == 'Skill Tome':
                for cls in category['classes']:
                    class_str = category['classes'][cls]
                    curr_class = PlayerClass(class_str['name'])
                    curr_category.classes[class_str['name']] = curr_class
                    for grade in class_str['grades']:
                        grade_str = class_str['grades'][grade]
                        curr_grade = Grade(grade_str['name'], grade_str['rate'])
                        curr_class.grades[grade_str['name']] = curr_grade
                        for item in grade_str['items']:
                            item_str = grade_str['items'][item]
                            curr_item = Item(item_str['name'], item_str['quantity'], item_str['chance'])
                            curr_grade.grade_items[item_str['name']] = curr_item
            else:
                for grade in category['grades']:
                    grade_str = category['grades'][grade]
                    curr_grade = Grade(grade_str['name'], grade_str['rate'])
                    curr_category.grades[grade_str['name']] = curr_grade
                    for item in grade_str['items']:
                        item_str = grade_str['items'][item]
                        curr_item = Item(item_str['name'], item_str['quantity'], item_str['chance'])
                        curr_grade.grade_items[item_str['name']] = curr_item
        print_data(data)
        return True
    else:
        print(f'File {file} does not exist')
        return False
    

if __name__ == '__main__':
    data = []
    deserialize(data)
