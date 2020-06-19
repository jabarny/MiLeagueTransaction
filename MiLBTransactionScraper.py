#! python3 -i MiLBTransactionsv2.py
# a script that opens, scrapes minor league transactions from milb.com pages.

# standard lib
import calendar
import datetime as dt
import time
import re
import sys # if you want to call from terminal

# third party lib
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import \
    By  # Note: for the XPATHS elements more info: https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC  # NOTE: webdriverwait conditions
from selenium.webdriver.chrome.options import Options

#relative lib
from links import full_lg, CAL, SOU, EAS

options = Options()  # makes Webdriver wait for the entire page is loaded when set to 'normal'
options.page_load_strategy = 'normal'
# for more info on page loading: https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
driver = webdriver.Chrome(options=options)

# in order of html tree
milbtitle = SoupStrainer('title')
milbstatscontainer = SoupStrainer(id='statsContainer')

print('Minor League Transactions scraping started...')
def FLgTransact():
    # progress bar & month ranges
    starting_month = 6
    ending_month = 7
    total = len(full_lg) * int(ending_month - starting_month)
    completing = 0

    start = dt.datetime.now()
    print('~' * 70 + ' \nStart Time: ' + start.strftime("%b, %d | %H:%M:%S %p") + '\n' + '~' * 70)
    for url in full_lg:
        try:
            driver.get(url)
            for mon in range(starting_month, ending_month):  # range must begin at 1 for first month of year up to 13 for 12th month
                completing += 1
                progress = int(100 * completing / total)
                progress_bar = str(progress) + '%'

                month = calendar.month_name[mon]
                try:

                    # clicking through javascript
                    js_month_selector_xpath = '//*[@id="statsContainer"]/a'
                    # js_month_selector_elem = driver.find_element_by_xpath(js_month_selector_xpath)
                    js_month_selector_elem = ui.WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, js_month_selector_xpath)))
                    js_month_selector_elem.click()

                    js_month_xpath = '//*[@id="monthSelContainer"]/ul/li[{}]/a'.format(mon)
                    # js_month_elem = driver.find_element_by_xpath(js_month_xpath)
                    js_month_elem = ui.WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, js_month_xpath)))
                    js_month_elem.click()

                    time.sleep(2)

                    # note: html changes after reinitializing content and soup
                    # reassigning variables for new htmlsoup
                    milbcontent = driver.page_source.encode(
                        'utf-8').strip()  # note: since page is JS-rendered, using selenium


                    # to assign title
                    milbsoup = BeautifulSoup(milbcontent, 'lxml', parse_only=milbstatscontainer)

                    milbsouptitle = BeautifulSoup(milbcontent, 'lxml',
                                                  parse_only=milbtitle)  #todo javier research if this multiple initializations of BeautifulSoup affects performance
                    # regexes; note: transaction regex is saved in MiLBTransactionsv0.py
                    # a Regex that finds the headers from html <title> tag
                    title = re.findall(r'^[a-zA-Z ]+', milbsouptitle.text)[0].strip()
                    # transaction dates
                    dates = re.findall(r'\d{2}/\d{2}/\d{4}', str(
                        milbsoup.tbody))

                    year = milbsoup.find('span').text
                    if not dates:
                        print('!' * 70)
                        print('No {} for {} {} - {}.'.format(title, month, year, progress_bar))
                        print('!' * 70)
                    else:
                        # for string whitespacing
                        zero = 0
                        e = len(dates[zero])
                        f = e + 15
                        g = f + 15
                        print('-' * 70)
                        print('{} for {} {} - {}\nLink: '.format(title, month, year, progress_bar) + url)
                        print('Scripted started at {} | '.format(start.strftime('%H:%M:%S')), end='')
                        print('Current time: ' + dt.datetime.now().strftime('%b, %d | %H:%M:%S %p'))
                        print('-' * 70)
                        find_count = len(milbsoup.tbody.find_all('td', {'align': 'left'}))
                        date_inc = 0
                        comment_inc = 4
                        print('date'.rjust(e, ' ').upper(), end='')
                        print('league transactions'.rjust(f, ' ').upper(), end='')
                        print('transactions description'.rjust(g, ' ').upper())
                        for x in range(int(find_count / 5)):
                            print(milbsoup.tbody.find_all('td', {'align': 'left'})[date_inc].string, end=' | ')
                            print(title + ' | ', end='')
                            print(milbsoup.tbody.find_all('td', {'align': 'left'})[comment_inc].string)
                            date_inc += 5
                            comment_inc += 5
                except TimeoutException:
                    print('One of the XPath elements timed out...\nskipping {} for {}...'.format(month, url))

        except AttributeError:
            # code block vestige to milbtransactionsv0.py; should be handled by codes in line 105 to 109
            pass

    print('=' * 70)
    end = dt.datetime.now()
    print('Total Web Scraping Time: ' + str(end - start), end='\n')
    driver.close()


FLgTransact()
