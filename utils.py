def print_data(data):
    for category in data:
        print(f'{category}')
        if category == 'Skill Tome':
            print(f'\tClasses: ')
            for cls in data[category].classes:
                class_obj = data[category].classes[cls]
                print(f'\t\t{class_obj}\n\t\tGrades: ')
                for grade in class_obj.grades:
                    grade_obj = class_obj.grades[grade]
                    print(f'\t\t{grade_obj} - {grade_obj.rate}')
                    for item in grade_obj.grade_items:
                        item_obj = grade_obj.grade_items[item]
                        print(f'\t\t\t{item_obj} - {item_obj.chance}')
        else:
            print(f'\tGrades: ')
            for grade in data[category].grades:
                grade_obj = data[category].grades[grade]
                print(f'\t\t{grade_obj} - {grade_obj.rate}')
                for item in grade_obj.grade_items:
                    item_obj = grade_obj.grade_items[item]
                    print(f'\t\t\t{item_obj} - {item_obj.chance}')
        print('\n')
