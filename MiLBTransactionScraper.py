#! python3 -i FLgTransactions.py
# a script that prints minor league transactions.

import datetime as dt
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import SoupStrainer
import links # make sure in proper folder. more info: https://stackoverflow.com/questions/17255737/importing-variables-from-another-file

options = Options()  # makes Webdriver wait for the entire page is loaded when set to 'normal'
options.page_load_strategy = 'normal' # for more info on page loading: https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
driver = webdriver.Chrome(options=options)

link = [SOU] # imported variable links to be looped through


def FLgTransact():
    start = dt.datetime.now()
    print('~' * 70 + ' \nStart Time: ' + start.strftime("%b, %d | %H:%M:%S %p") + '\n' + '~' * 70)
    for url in link:
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            milbcontent = driver.page_source.encode('utf-8').strip()
            milbtbody = SoupStrainer('tbody')  # to parse only a specific html section; link: https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=resultset#parsing-only-part-of-a-document
            milbsoup = BeautifulSoup(milbcontent, 'lxml', parse_only=milbtbody)

            driver.close()
            dates = re.findall(r'\d{2}/\d{2}/\d{4}', str(milbsoup))  # reported date of transaction
            
            headers = re.findall(r'">(\D+?)</', str(milbsoup))[:5]  # a Regex that finds the headers

            # a Regex that finds the transactions cells
            transaction_cells = re.findall(r'">([123\D]+?)</', str(milbsoup))[6:]  # will always be a multiple of 4 i.e. 4,8,12,etc.

            # string whitespacing
            e = len(dates[0])
            f = e + 15
            g = f + 15

            print('-' * 70)
            print('TRANSACTIONS FOR ' + headers[0] + '. \nLink: ' + url)
            print(dt.datetime.now().strftime('%b, %d | %H:%M:%S %p'))
            print('-' * 70)
            print('DATE'.rjust(e, ' '), end='')
            print('LEAGUE TRANSACTIONS'.rjust(f, ' '), end='')
            print('TRANSACTIONS DESCRIPTION'.rjust(g, ' '))
            m = 0
            for x in range(3, len(transaction_cells), 4):
                print(dates[m], end=" | ") # prints transaction date
                print(headers[0] + ' | ', end='') # prints league
                print(transaction_cells[x]) # prints transaction
                m += 1
            end = dt.datetime.now()
            print('+' * 70 + ' \nEnd Time: ' + dt.datetime.now() + '\n' + '+' * 70)
            print('Total Web Scraping Time: ' + str(end - start), end='\n') # total script time
        except AttributeError:
            print('!' * 70)
            print('NO TRANSACTIONS FOR LINK: ' + url)
            print('!' * 70)
            continue


FLgTransact()
