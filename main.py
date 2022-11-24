from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
from collections import defaultdict
import re
import random


def summoning(browser, print_items=False):
    grades = {'Uncommon', 'Rare', 'Epic', 'Legendary'}
    classes = ['Warrior', 'Sorcerer', 'Taoist', 'Lancer', 'Arbalist']
    material = defaultdict(lambda: [])
    material_rarity = defaultdict(lambda: 0)
    spirit = defaultdict(lambda: [])
    spirit_rarity = defaultdict(lambda: 0)
    tome = [defaultdict(lambda: []) for _ in range(len(classes))]
    tome_rarity = [defaultdict(lambda: 0) for _ in range(len(classes))]
    matches = browser.find_elements(By.TAG_NAME, 'tr')
    curr_grade = None
    class_counter = -1
    curr_sum = 0
    with open('summons.dat', 'w', encoding='utf-8') as f:  # TODO: store all summon rates in files
        for i, match in enumerate(matches):
            if match.find_element(By.XPATH, r'./td[1]').text == '2':
                break
            t = match.find_element(By.XPATH, r'./td[1]').text
            if re.match(r'^[0-9-].+?$', t):
                name = match.find_element(By.XPATH, r'./td[2]').text
                print(f'{name} table found')
                f.write(f'{name}\n')
                if 'Material' in name:
                    curr_dict = material
                    curr_rarity = material_rarity
                elif 'Spirit' in name:
                    curr_dict = spirit
                    curr_rarity = spirit_rarity
                elif 'Tome' in name:
                    continue
                elif name in classes:
                    class_counter += 1
                    curr_dict = tome[class_counter]
                    curr_rarity = tome_rarity[class_counter]
                curr_sum = 0
                continue
            try:
                t1 = match.find_element(By.XPATH, r'./td[1]').text
                if t1 == 'sum':
                    continue
                if t1 in grades:
                    curr_grade = t1
                    t2 = match.find_element(By.XPATH, r'./td[2]').text  # grade chance
                    curr_rarity[t1] = round(float(t2[:-1])/100, 6)
                    t3 = match.find_element(By.XPATH, r'./td[3]').text
                    t3 = ' '.join(t3.split()[1:])  # item name without grade
                    t5 = match.find_element(By.XPATH, r'./td[5]').text
                    t5 = round(float(t5[:-1])/100, 6)
                    curr_sum += t5
                    curr_dict[curr_grade].append((t3, curr_sum))
                else:
                    t1 = match.find_element(By.XPATH, r'./td[1]').text
                    t1 = ' '.join(t1.split()[1:])
                    t3 = match.find_element(By.XPATH, r'./td[3]').text
                    if curr_grade and t1:
                        t3 = round(float(t3[:-1])/100, 6)
                        curr_sum += t3
                        curr_dict[curr_grade].append((t1, curr_sum))
            except UnicodeEncodeError:
                print(f'Skipping match {i}...')
        print('Done!')
    if print_items:
        print('Materials:')
        for i, c in enumerate(material):
            print(f'~~~~~~{c}')
            print(f'{material[c]}')

        print('Spirit:')
        for i, c in enumerate(spirit):
            print(f'~~~~~~{c}')
            print(f'{spirit[c]}')

        print('Tomes:')
        for i, c in enumerate(tome):
            for key in c:
                print(f'~~~~~~{key} - {classes[i]}')
                print(c[key])
    return (material, spirit, tome)


def summon_menu(material, spirit, tome):
    print('~~~~ MIR4 Summoning ~~~~')
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
    summon_material, summon_spirit, summon_tome = [], [], [[] for _ in range(5)]
    for grade in material:
        for item, chance in material[grade]:
            summon_material.append((chance, f'{grade} {item}'))
    summon_material.sort()
    for grade in spirit:
        for item, chance in spirit[grade]:
            summon_spirit.append((chance, f'{grade} {item}'))
    summon_spirit.sort()
    for i, t in enumerate(tome):
        for grade in t:
            for item, chance in t[grade]:
                summon_tome[i].append((chance, f'{grade} {item}'))
        summon_tome[i].sort()
    while (c := input(summon_msg)) != '0':
        try:
            c = int(c)
        except ValueError:
            print('You must enter a number!\n')
            continue
        summoned_items = defaultdict(lambda: 0)
        if c == 1:
            print('>> Dragon Material Summon<<\n')
            low, high = 0, summon_material[-1][0]
            try:
                cl = int(input(quant_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if cl <= 0 or cl > 3:
                if cl != 0:
                    print('\tInvalid option!\n')
                continue
            x = [1, 10, 100][cl - 1]
            for i in range(x):
                r = random.uniform(low, high)  # generate a new random number
                for chance, item in summon_material:
                    if r <= chance:  # compare the random number with the summon chances
                        # print(f'You just summoned {item}!')
                        summoned_items[f'{item}'] += 1
                        break
            print(f'***Summon {x}x Results***')
            for item in summoned_items:
                if summoned_items[item] > 0:
                    print(f'   -{item} {summoned_items[item]}x')

        elif c == 2:
            print('>> Spirit Summon<<\n')
            low, high = 0, summon_spirit[-1][0]
            try:
                cl = int(input(quant_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if cl <= 0 or cl > 3:
                if cl != 0:
                    print('\tInvalid option!\n')
                continue
            x = [1, 10, 100][cl - 1]
            for i in range(x):
                r = random.uniform(low, high)  # generate a new random number
                for chance, item in summon_spirit:
                    if r <= chance:  # compare the random number with the summon chances
                        # print(f'You just summoned {item}!')
                        summoned_items[f'{item}'] += 1
                        break
            print(f'***Summon {x}x Results***')
            for item in summoned_items:
                if summoned_items[item] > 0:
                    print(f'   -{item} {summoned_items[item]}x')

        elif c == 3:
            print('>> Skill Tome Summon<<\n')
            try:
                cl = int(input(class_msg))
            except:
                print('\tInvalid option!\n')
                continue
            if cl == 1:
                print('\t\t>>> Warrior Skill Tome')
            elif cl == 2:
                print('\t\t>>> Sorcerer Skill Tome')
            elif cl == 3:
                print('\t\t>>> Taoist Skill Tome')
            elif cl == 4:
                print('\t\t>>> Lancer Skill Tome')
            elif cl == 5:
                print('\t\t>>> Arbalist Skill Tome')
        else:
            print('Invalid option!\n')


def main():
    service = Service(ChromeDriverManager().install())
    website = 'https://forum.mir4global.com/post/67'
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(service=service, options=options)
        browser.get(website)
    except (WebDriverException, NoSuchWindowException):
        print('Browser not found. Exiting...')
    else:
        material, spirit, tome = summoning(browser)
        browser.quit()
        summon_menu(material, spirit, tome)    
        # print(material)
        # print(spirit)
        # print(tome)


if __name__ == '__main__':
    main()