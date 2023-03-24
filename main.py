from selenium import webdriver
from selenium.common.exceptions import (NoSuchWindowException,
                                        WebDriverException)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scraper import scrape
from serializer import deserialize
from summon import summon_menu
from utils import print_data


def main():
    print('~~~~ MIR4 Summoning ~~~~')
    data = []
    summon_msg = ('Choose an option:\n'
                  '\t1 - Summoning Menu\n'
                  '\t2 - Update Summoning Data\n'
                  '\t3 - Display Summoning Data\n'
                  '\t0 - Exit\n'
                  '\t>>> ')
    while (c := input(summon_msg)) != '0':
        try:
            c = int(c)
        except ValueError:
            print('You must enter a number!\n')
            continue
        if c == 1:
            if deserialize(data):
                summon_menu(data)
            else:
                print(f'Failed to deserialize data.json, try updating summoning data first!\n')
        elif c == 2:
            print('Updating summoning data!\n')
            service = Service(ChromeDriverManager().install())
            website = 'https://forum.mir4global.com/post/67'
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                browser = webdriver.Chrome(service=service, options=options)
                browser.get(website)
            except (WebDriverException, NoSuchWindowException):
                print('Browser not found!\n')
            else:
                scrape(browser)
                browser.quit()
        elif c == 3:
            print('Displaying data!\n')
            print_data(data)

        else:
            print('Invalid option!\n')
    else:
        print('Exiting...')


if __name__ == '__main__':
    main()