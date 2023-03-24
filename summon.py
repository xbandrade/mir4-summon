import random
from collections import Counter, defaultdict


def summon(category, cls=None):
    quant = get_quant()
    if not quant:
        return
    possible_summons, weights = category.get_weights(cls)
    summons = random.choices(possible_summons, weights=weights, k=[0, 1, 11, 110][quant])
    show_summon_results(Counter(summons), [0, 1, 11, 110][quant])


def get_quant():
    quant_msg = ('Choose an option:\n'
                '\t1 - Summon 1x\n'
                '\t2 - Summon 10 + 1x\n'
                '\t3 - Summon 100 + 10x\n'
                '\t0 - Go Back\n'
                '\t>>> ')
    try:
        quant = int(input(quant_msg))
        if quant <= 0 or quant > 3:
            raise ValueError('Invalid option!')
    except ValueError as e:
        print(f'\t{e}\n')
    else:
        return quant
    return 0


def show_summon_results(summons, quant):
    print(f'\n***Summon {quant}x Results***')
    for count in summons:
        print(f'\t-{count} {summons[count]}x')
    print('\n')


def summon_menu(data):
    class_id = {
        1: 'Warrior',
        2: 'Sorcerer',
        3: 'Taoist',
        4: 'Lancer',
        5: 'Arbalist',
    }
    summon_msg = ('Choose a summon type:\n'
                  '\t1 - Dragon Material\n'
                  '\t2 - Spirit\n'
                  '\t3 - Legendary Spirit\n'
                  '\t4 - Skill Tome\n'
                  '\t0 - Go Back\n'
                  '\t>>> ')
    class_msg = ('Choose a class:\n'
                 '\t1 - Warrior\n'
                 '\t2 - Sorcerer\n'
                 '\t3 - Taoist\n'
                 '\t4 - Lancer\n'
                 '\t5 - Arbalist\n'
                 '\t0 - Go Back\n'
                 '\t>>> ')
    while (c := input(summon_msg)) != '0':
        try:
            c = int(c)
        except ValueError:
            print('You must enter a number!\n')
            continue
        if c == 1:
            print('\n>> Dragon Material Summon<<')
            summon(data['Dragon Material'])
        elif c == 2:
            print('\n>> Spirit Summon<<')
            summon(data['Spirit'])
        elif c == 3:
            print('\n>> Legend Spirit Summon<<')
            summon(data['Legend Spirit Summon'])
        elif c == 4:
            print('\n>> Skill Tome Summon<<')
            try:
                cls = int(input(class_msg))
                if cls <= 0 or cls > 5:
                    raise ValueError('Invalid option!')
            except ValueError as e:
                print(f'\t{e}\n')
            else:
                summon(data['Skill Tome'], class_id[cls])
        else:
            print('Invalid option!\n')

