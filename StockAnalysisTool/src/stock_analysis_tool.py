# https://www.scrapingbee.com/blog/selenium-python/
# https://www.youtube.com/watch?v=qT1_exOHP84

import os
import json
import time

import pandas             as pd

import selenium

import selenium.webdriver as webdriver

from selenium.webdriver.support.ui           import WebDriverWait, Select
from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.chrome.options       import Options
from selenium.webdriver.common.by            import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys          import Keys
from selenium.common import exceptions  

from bs4                                     import BeautifulSoup

from pprint                                  import pprint

from util.config                             import g_config
from util.enums                              import *



if __name__ == '__main__':
    os.system("cls")
    dividends_dict = dict()

    # load chrome with gui
    # browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    # browser.get('https://google.com')

    # load chrome without gui
    options          = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    browser = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

    stock_count = 1

    for stock_symbol in g_config.stock_list:
        print(f"Fetching data for {stock_symbol} {stock_count} / {len(g_config.stock_list)}")
        url = MAIN_PAGE + stock_symbol + '/'
        browser.get(url)

        time.sleep(0.5)

        # get the div element that is associated with divedends
        categories = browser.find_elements(By.XPATH, '//div[starts-with(@class, "tv-widget-fundamentals__item")]')
        # categories = browser.find_elements(By.XPATH, '//span[starts-with(@class, "tv-widget-fundamentals__label apply-overflow-tooltip")]')

        for category in categories:
            try:
                data = category.text.split('\n')

                if data[0] == 'Dividends':
                    dividends_dict[stock_symbol] = [{
                        'Dividends Paid (FY)':      '—',
                        'Dividends Yield (FY)':     '—',
                        'Dividends per Share (FY)': '—'}]

                    while len(data) > 0:
                        dividend_title = data.pop(0)

                        if dividend_title == 'Dividends Paid (FY)':
                            dividend_data = data.pop(0)
                            dividends_dict[stock_symbol][0]['Dividends Paid (FY)'] = dividend_data
                        elif dividend_title == 'Dividends Yield (FY)':
                            dividend_data = data.pop(0)
                            dividends_dict[stock_symbol][0]['Dividends Yield (FY)'] = dividend_data
                        elif dividend_title == 'Dividends per Share (FY)':
                            dividend_data = data.pop(0)
                            dividends_dict[stock_symbol][0]['Dividends per Share (FY)'] = dividend_data
            except EC.NoSuchElementException:
                print(f"No such element was found: {stock_symbol}")
            except exceptions.StaleElementReferenceException as e:
                print(e)
            except Exception as e:
                print(e)
                print(stock_symbol)
        stock_count += 1

    pprint(dividends_dict)
    browser.quit()



