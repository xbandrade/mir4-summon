import random
from collections import defaultdict


def summon_menu(classes, material, spirit, tome):
    summon_msg = ('Choose a summon type:\n'
                  '\t1 - Dragon Material\n'
                  '\t2 - Spirit\n'
                  '\t3 - Skill Tome\n'
                  '\t0 - Exit\n'
                  '\t>>> ')
    class_msg = ('Choose a class:\n'
                 '\t1 - Warrior\n'
                 '\t2 - Sorcerer\n'
                 '\t3 - Taoist\n'
                 '\t4 - Lancer\n'
                 '\t5 - Arbalist\n'
                 '\t0 - Go Back\n'
                 '\t>>> ')
    quant_msg = ('Choose an option:\n'
                '\t1 - Summon 1x\n'
                '\t2 - Summon 10x\n'
                '\t3 - Summon 100x\n'
                '\t0 - Go Back\n'
                '\t>>> ')
    material.sort()
    spirit.sort()
    for i in range(len(tome)):
        tome[i].sort()
    while (c := input(summon_msg)) != '0':
        try:
            c = int(c)
        except ValueError:
            print('You must enter a number!\n')
            continue
        summoned_items = defaultdict(lambda: 0)
        if c == 1:
            print('\n>> Dragon Material Summon<<')
            low, high = 0, material[-1][0]
            try:
                quant = int(input(quant_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if quant <= 0 or quant > 3:
                if quant != 0:
                    print('\tInvalid option!\n')
                continue
            x = [1, 10, 100][quant - 1]
            for i in range(x):
                r = random.uniform(low, high)  # generate a new random number
                for chance, item in material:
                    if r <= chance:  # compare the random number with the summon chances
                        summoned_items[f'{item}'] += 1
                        break
            print(f'\n***Summon {x}x Results***')
            for item in summoned_items:
                if summoned_items[item] > 0:
                    print(f'   -{item} {summoned_items[item]}x')
            print()

        elif c == 2:
            print('\n>> Spirit Summon<<')
            low, high = 0, spirit[-1][0]
            try:
                quant = int(input(quant_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if quant <= 0 or quant > 3:
                if quant != 0:
                    print('\tInvalid option!\n')
                continue
            x = [1, 10, 100][quant - 1]
            for i in range(x):
                r = random.uniform(low, high)  # generate a new random number
                for chance, item in spirit:
                    if r <= chance:  # compare the random number with the summon chances
                        summoned_items[f'{item}'] += 1
                        break
            print(f'\n***Summon {x}x Results***')
            for item in summoned_items:
                if summoned_items[item] > 0:
                    print(f'   -{item} {summoned_items[item]}x')
            print()

        elif c == 3:
            print('\n>> Skill Tome Summon<<')
            try:
                cl = int(input(class_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if 1 <= cl <= len(classes):
                print(f'\n>>> {classes[cl - 1]} Skill Tome')
                low, high = 0, tome[cl - 1][-1][0]
                try:
                    quant = int(input(quant_msg))
                except:
                    print('\tInvalid option!\n')
                    continue
                if quant <= 0 or quant > 3:
                    if quant != 0:
                        print('\tInvalid option!\n')
                    continue
                x = [1, 10, 100][quant - 1]
                for i in range(x):
                    r = random.uniform(low, high)  # generate a new random number
                    for chance, item in tome[cl - 1]:
                        if r <= chance:  # compare the random number with the summon chances
                            summoned_items[f'{item}'] += 1
                            break
                print(f'\n***Summon {x}x Results***')
                for item in summoned_items:
                    if summoned_items[item] > 0:
                        print(f'   -{item} {summoned_items[item]}x')
                print()
                
        else:
            print('Invalid option!\n')

