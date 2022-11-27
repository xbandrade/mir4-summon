from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from collections import defaultdict
import re
import random


def scrape(browser, classes, print_items=False):
    grades = {'Uncommon', 'Rare', 'Epic', 'Legendary'}
    material = []
    spirit = []
    tome = [[] for _ in range(len(classes))]
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
                    curr_item = material
                elif 'Spirit' in name:
                    curr_item = spirit
                elif 'Tome' in name:
                    continue
                elif name in classes:
                    class_counter += 1
                    curr_item = tome[class_counter]
                curr_sum = 0
                continue
            try:
                t1 = match.find_element(By.XPATH, r'./td[1]').text
                if t1 == 'sum':
                    continue
                if t1 in grades:
                    curr_grade = t1
                    t3 = match.find_element(By.XPATH, r'./td[3]').text
                    t5 = match.find_element(By.XPATH, r'./td[5]').text
                    t5 = round(float(t5[:-1])/100, 6)
                    curr_sum += t5
                    if t3.startswith(curr_grade):
                        curr_item.append((curr_sum, t3))
                    else:
                        curr_item.append((curr_sum, f'{curr_grade} {t3}'))
                else:
                    t1 = match.find_element(By.XPATH, r'./td[1]').text
                    t2 = ' '.join(t1.split()[1:])
                    t3 = match.find_element(By.XPATH, r'./td[3]').text
                    if curr_grade and t2:
                        t3 = round(float(t3[:-1])/100, 6)
                        curr_sum += t3
                        if t1.startswith(curr_grade):
                            curr_item.append((curr_sum, t1))
                        else:
                            curr_item.append((curr_sum, f'{curr_grade} {t1}'))
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


def summon_menu(classes, material, spirit, tome):
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


def main():
    service = Service(ChromeDriverManager().install())
    website = 'https://forum.mir4global.com/post/67'
    try:
        classes = ['Warrior', 'Sorcerer', 'Taoist', 'Lancer', 'Arbalist']
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(service=service, options=options)
        browser.get(website)
    except (WebDriverException, NoSuchWindowException):
        print('Browser not found. Exiting...')
    else:
        material, spirit, tome = scrape(browser, classes)
        browser.quit()
        summon_menu(classes, material, spirit, tome)


if __name__ == '__main__':
    main()