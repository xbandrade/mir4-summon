import json
import os

from item_classes import Category, Grade, Item, PlayerClass
from utils import print_data


def serialize(data):
    json_str = json.dumps({k: v.__dict__() for k, v in data.items()})
    with open('data.json', 'w') as f:
        f.write(json_str)
    

def deserialize(data):
    file = 'data.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            json_str = f.read()
        data_dict = json.loads(json_str)
        curr_category = curr_class = curr_grade = curr_item = None
        for category in data_dict:
            category_dict = data_dict[category]
            curr_category = Category(category_dict['name'])
            data[category_dict['name']] = curr_category
            if curr_category == 'Skill Tome':
                for cls in category_dict['classes']:
                    class_dict = category_dict['classes'][cls]
                    curr_class = PlayerClass(class_dict['name'])
                    curr_category.classes[class_dict['name']] = curr_class
                    for grade in class_dict['grades']:
                        grade_dict = class_dict['grades'][grade]
                        curr_grade = Grade(grade_dict['name'], grade_dict['rate'])
                        curr_class.grades[grade_dict['name']] = curr_grade
                        for item in grade_dict['items']:
                            item_str = grade_dict['items'][item]
                            curr_item = Item(item_str['name'], item_str['quantity'], item_str['chance'], item_str['grade'])
                            curr_grade.grade_items[item_str['name']] = curr_item
            else:
                for grade in category_dict['grades']:
                    grade_dict = category_dict['grades'][grade]
                    curr_grade = Grade(grade_dict['name'], grade_dict['rate'])
                    curr_category.grades[grade_dict['name']] = curr_grade
                    for item in grade_dict['items']:
                        item_str = grade_dict['items'][item]
                        curr_item = Item(item_str['name'], item_str['quantity'], item_str['chance'], item_str['grade'])
                        curr_grade.grade_items[item_str['name']] = curr_item
        # print_data(data)
        return True
    else:
        print(f'File {file} does not exist')
        return False
    

if __name__ == '__main__':
    data = []
    deserialize(data)
