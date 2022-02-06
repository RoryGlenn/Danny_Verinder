import time

import selenium.webdriver as webdriver

from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.common.by            import By
from selenium.webdriver.chrome.options       import Options
from pprint                                  import PrettyPrinter, pprint
from util.config                             import g_config
from util.enums                              import *
from util.globals                            import G


class TradingViewWebScraper():
    def __init__(self, is_gui: bool=False) -> None:
        self.is_gui                   = is_gui
        self.browser                  = None
        self.current_price            = dict()
        self.total_shares_outstanding = dict()
        self.eps                      = dict()
        self.dividends                = dict()
        self.data                     = dict() # a dictionary[symbol] that holds dataframes
        return

    def set_gui(self) -> None:
        if self.is_gui:
            # load chrome with gui
            self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        else:
            # load chrome without gui
            options          = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1200")
            self.browser = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)            
        return

    def set_current_price(self, stock_symbol: str) -> None:
        if stock_symbol not in self.current_price.keys():
            try:
                categories = self.browser.find_elements(By.XPATH, '//div[starts-with(@class, "tv-symbol-price-quote__value js-symbol-last")]')

                for c in categories:
                    self.current_price[stock_symbol] = c.text
            except Exception as e:
                G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)
        return

    def set_shares(self, stock_symbol: str, data: list) -> None:
        if 'Total Shares Outstanding (MRQ)' in data:
            self.total_shares_outstanding[stock_symbol] = dict({'Total Shares Outstanding (MRQ)': '-'})

            while len(data) > 0:
                if data.pop(0) == 'Total Shares Outstanding (MRQ)':
                    self.total_shares_outstanding[stock_symbol]['Total Shares Outstanding (MRQ)'] = data.pop(0)
                    break
        return

    def set_dividends(self, stock_symbol: str, data: list) -> None:
        if 'Dividends' in data:
            if data[0] == 'Dividends':
                self.dividends[stock_symbol] = [{
                    'Dividends Paid (FY)':      '-',
                    'Dividends Yield (FY)':     '-',
                    'Dividends per Share (FY)': '-'}]

                while len(data) > 0:
                    dividend_title = data.pop(0)

                    if dividend_title == 'Dividends Paid (FY)':
                        self.dividends[stock_symbol][0]['Dividends Paid (FY)'] = data.pop(0)
                    elif dividend_title == 'Dividends Yield (FY)':
                        self.dividends[stock_symbol][0]['Dividends Yield (FY)'] = data.pop(0)
                    elif dividend_title == 'Dividends per Share (FY)':
                        self.dividends[stock_symbol][0]['Dividends per Share (FY)'] = data.pop(0)
        return
    
    def set_eps(self, stock_symbol: str, data: list) -> None:
        # price to earnings ratio
        if 'Price to Revenue Ratio (TTM)' in data:
            self.eps[stock_symbol] = dict({'Price to Revenue Ratio (TTM)': '-'})

            while len(data) > 0:
                if data.pop(0) == 'Price to Revenue Ratio (TTM)':
                    self.eps[stock_symbol]['Price to Revenue Ratio (TTM)'] = data.pop(0)
                    break
        return

    def set_data(self, stock_symbol: str) -> None:
        self.data[stock_symbol] = {
            'Current Price':                  self.current_price[stock_symbol],
            'Total Shares Outstanding (MRQ)': self.total_shares_outstanding[stock_symbol]['Total Shares Outstanding (MRQ)'],
            'Dividends':                      self.dividends[stock_symbol][0], 
            'Price to Revenue Ratio (TTM)':   self.eps[stock_symbol]['Price to Revenue Ratio (TTM)']}
        return
    
    def reset_data(self) -> None:
        self.current_price            = dict()
        self.total_shares_outstanding = dict()
        self.eps                      = dict()
        self.dividends                = dict()
        return

    def scrape_data(self) -> None:
        stock_count = 1
        self.set_gui()

        for stock_symbol in g_config.stock_list:
            G.log.print_and_log(f"Fetching data for {stock_symbol} {stock_count} / {len(g_config.stock_list)}")
            
            url = TRADING_VIEW_URL + stock_symbol + '/'
            self.browser.get(url)

            time.sleep(0.6)

            self.set_current_price(stock_symbol)

            # get the div element that is associated with divedends
            categories = self.browser.find_elements(By.XPATH, '//div[starts-with(@class, "tv-widget-fundamentals__item")]')

            for category in categories:
                try:
                    data = category.text.split('\n')
                    self.set_shares(stock_symbol, data)
                    self.set_eps(stock_symbol, data)
                    self.set_dividends(stock_symbol, data)
                except EC.NoSuchElementException:
                    G.log.print_and_log(f"No such element was found: {stock_symbol}")
                except Exception as e:
                    G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)

            self.set_data(stock_symbol)
            self.reset_data()
            stock_count += 1

        G.log.print_and_log(f"{PrettyPrinter().pformat(self.data)}")
        self.browser.quit()



