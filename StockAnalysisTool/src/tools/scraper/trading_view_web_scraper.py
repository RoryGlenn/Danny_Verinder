import time

import selenium.webdriver as webdriver

from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.common.by                   import By
from selenium.webdriver.chrome.options              import Options
from pprint                                         import PrettyPrinter
from ..util.enums                                   import *
from ..util.globals                                 import G


class TradingViewWebScraper():
    def __init__(self, is_gui: bool=False) -> None:
        self.is_gui                   = is_gui
        self.browser                  = None
        self.current_price            = dict()
        self.total_shares_outstanding = dict()
        self.eps                      = dict()
        self.dividends                = dict()
        self.data                     = dict()
        return

    def set_gui(self) -> None:
        if self.is_gui:
            # load chrome with gui
            self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        else:
            # load chrome without gui
            options          = Options()
            options.headless = True
            options.add_argument(Browser.WINDOW_SIZE)
            self.browser = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)            
        return

    def set_current_price(self, stock_symbol: str) -> None:
        if stock_symbol not in self.current_price.keys():
            try:
                categories = self.browser.find_elements(By.XPATH, TradingViewData.CURRENT_PRICE_XPATH)

                for category in categories:
                    self.current_price[stock_symbol] = category.text
            except Exception as e:
                G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)
        return

    def set_shares(self, stock_symbol: str, data: list) -> None:
        if TradingViewData.TOTAL_SHARES in data:
            self.total_shares_outstanding[stock_symbol] = dict({TradingViewData.TOTAL_SHARES: '-'})

            while len(data) > 0:
                if data.pop(0) == TradingViewData.TOTAL_SHARES:
                    self.total_shares_outstanding[stock_symbol][TradingViewData.TOTAL_SHARES] = data.pop(0)
                    break
        return

    def set_dividends(self, stock_symbol: str, data: list) -> None:
        if TradingViewData.DIVIDENDS in data:
            if data[0] == TradingViewData.DIVIDENDS:
                self.dividends[stock_symbol] = [{
                    TradingViewData.DIVIDENDS_PAID:      '-',
                    TradingViewData.DIVIDENDS_YIELD:     '-',
                    TradingViewData.DIVIDENDS_PER_SHARE: '-'}]

                while len(data) > 0:
                    dividend_title = data.pop(0)

                    if dividend_title == TradingViewData.DIVIDENDS_PAID:
                        self.dividends[stock_symbol][0][TradingViewData.DIVIDENDS_PAID] = data.pop(0)
                    elif dividend_title == TradingViewData.DIVIDENDS_YIELD:
                        self.dividends[stock_symbol][0][TradingViewData.DIVIDENDS_YIELD] = data.pop(0)
                    elif dividend_title == TradingViewData.DIVIDENDS_PER_SHARE:
                        self.dividends[stock_symbol][0][TradingViewData.DIVIDENDS_PER_SHARE] = data.pop(0)
        return
    
    def set_eps(self, stock_symbol: str, data: list) -> None:
        # price to earnings ratio
        if TradingViewData.PRICE_TO_EARNINGS_RATIO in data:
            self.eps[stock_symbol] = dict({TradingViewData.PRICE_TO_EARNINGS_RATIO: '-'})

            while len(data) > 0:
                if data.pop(0) == TradingViewData.PRICE_TO_EARNINGS_RATIO:
                    self.eps[stock_symbol][TradingViewData.PRICE_TO_EARNINGS_RATIO] = data.pop(0)
                    break
        return

    def set_data(self, stock_symbol: str) -> None:
        self.data[stock_symbol] = {
            TradingViewData.CURRENT_PRICE:           self.current_price[stock_symbol],
            TradingViewData.TOTAL_SHARES:            self.total_shares_outstanding[stock_symbol][TradingViewData.TOTAL_SHARES],
            TradingViewData.DIVIDENDS:               self.dividends[stock_symbol][0], 
            TradingViewData.PRICE_TO_EARNINGS_RATIO: self.eps[stock_symbol][TradingViewData.PRICE_TO_EARNINGS_RATIO]}
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

        for stock_symbol in G.config.stock_list:
            G.log.print_and_log(f"Fetching data for {stock_symbol} {stock_count} / {len(G.config.stock_list)}")
            
            url = TRADING_VIEW_URL + stock_symbol + '/'
            self.browser.get(url)

            time.sleep(0.5)

            self.set_current_price(stock_symbol)

            categories = self.browser.find_elements(By.XPATH, TradingViewData.GENERAL_DATA_XPATH)

            for category in categories:
                try:
                    data = category.text.split('\n')
                    self.set_shares(stock_symbol, data)
                    self.set_eps(stock_symbol, data)
                    self.set_dividends(stock_symbol, data)
                except NoSuchElementException:
                    G.log.print_and_log(f"No such element was found: {stock_symbol}")
                except Exception as e:
                    G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)

            self.set_data(stock_symbol)
            self.reset_data()
            stock_count += 1

        G.log.print_and_log(f"{PrettyPrinter().pformat(self.data)}")
        self.browser.quit()
        return