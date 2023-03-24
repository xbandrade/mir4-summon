import re
from collections import defaultdict

from selenium.webdriver.common.by import By

from item_classes import Category, Grade, Item, PlayerClass
from serializer import serialize
from utils import print_data


def scrape(browser):
    grades = {'Uncommon', 'Rare', 'Epic', 'Legendary'}
    class_names = ['Warrior', 'Sorcerer', 'Taoist', 'Lancer', 'Arbalist', 'Darkist']
    classes = defaultdict(PlayerClass)
    for name in class_names:
        classes[name] = PlayerClass(name)
    table = browser.find_element(By.XPATH, '//table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    category_pattern = r'^\d+-\d+(-\d+)?\.$'
    data = []
    curr_category = curr_grade = curr_class = None
    print('Starting')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text.strip() for cell in cells]
        if row_data[0] in ('sum', '', 'Grade'):
            continue
        elif row_data[0] == '1-4.':
            break
        elif row_data[1] in classes:
            curr_class = PlayerClass(row_data[1])
            curr_category.classes[row_data[1]] = curr_class
        elif re.match(category_pattern, row_data[0]):
            curr_category = Category(row_data[1])
            data.append(curr_category)
        elif row_data[0] in grades:
            curr_grade = Grade(row_data[0], row_data[1])
            if curr_category != 'Skill Tome':
                curr_category.grades[row_data[0]] = curr_grade
            else:
                curr_class.grades[row_data[0]] = curr_grade
            new_item = Item(row_data[2], row_data[3], row_data[4])
            curr_grade.grade_items[row_data[2]] = new_item
        else:
            new_item = Item(row_data[0], row_data[1], row_data[2])
            curr_grade.grade_items[row_data[0]] = new_item
    serialize(data)
    print('Done!')
    # print_data(data)
    