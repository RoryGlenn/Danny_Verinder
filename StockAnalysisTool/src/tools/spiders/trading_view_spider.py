import time

import selenium.webdriver as webdriver

from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.common.by                   import By
from selenium.webdriver.chrome.options              import Options
from pprint                                         import PrettyPrinter
from ..util.enums                                   import *
from ..util.globals                                 import G


"""
Spiders   - define how a site should be scraped. Contains all the logic to extract the data from the site.
Selectors - Mechanisms for selecting data.
Items     - data extracted from the selector.

"""

class TradingViewSpider():
    def __init__(self, is_gui: bool=False) -> None:
        self._is_gui                   = is_gui
        self._browser                  = None
        self._current_price            = dict()
        self._total_shares_outstanding = dict()
        self._eps                      = dict()
        self._dividends                = dict()
        self._trading_below_value      = dict()
        self._data                     = dict()
        return

    def __set_gui(self) -> None:
        if self._is_gui:
            # load chrome with gui
            self._browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        else:
            # load chrome without gui
            options          = Options()
            options.headless = True
            options.add_argument(Browser.WINDOW_SIZE)
            self._browser = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)            
        return

    def __set_current_price(self, stock_symbol: str) -> None:
        if stock_symbol not in self._current_price.keys():
            try:
                categories = self._browser.find_elements(By.XPATH, Selectors.CURRENT_PRICE_XPATH)

                for category in categories:
                    self._current_price[stock_symbol] = category.text
            except Exception as e:
                G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)
        return

    def __set_shares(self, stock_symbol: str, data: list) -> None:
        if TVItems.TOTAL_SHARES in data:
            self._total_shares_outstanding[stock_symbol] = dict({TVItems.TOTAL_SHARES: '-'})

            while len(data) > 0:
                if data.pop(0) == TVItems.TOTAL_SHARES:
                    self._total_shares_outstanding[stock_symbol][TVItems.TOTAL_SHARES] = data.pop(0)
                    break
        return

    def __set_dividends(self, stock_symbol: str, data: list) -> None:
        if TVItems.DIVIDENDS in data:
            if data[0] == TVItems.DIVIDENDS:
                self._dividends[stock_symbol] = [{
                    TVItems.DIVIDENDS_PAID:      '-',
                    TVItems.DIVIDENDS_YIELD:     '-',
                    TVItems.DIVIDENDS_PER_SHARE: '-'}]

                while len(data) > 0:
                    dividend_title = data.pop(0)

                    if dividend_title == TVItems.DIVIDENDS_PAID:
                        self._dividends[stock_symbol][0][TVItems.DIVIDENDS_PAID] = data.pop(0)
                    elif dividend_title == TVItems.DIVIDENDS_YIELD:
                        self._dividends[stock_symbol][0][TVItems.DIVIDENDS_YIELD] = data.pop(0)
                    elif dividend_title == TVItems.DIVIDENDS_PER_SHARE:
                        self._dividends[stock_symbol][0][TVItems.DIVIDENDS_PER_SHARE] = data.pop(0)
        return
    
    def __set_eps(self, stock_symbol: str, data: list) -> None:
        # price to earnings ratio
        if TVItems.PRICE_TO_EARNINGS_RATIO in data:
            self._eps[stock_symbol] = dict({TVItems.PRICE_TO_EARNINGS_RATIO: '-'})

            while len(data) > 0:
                if data.pop(0) == TVItems.PRICE_TO_EARNINGS_RATIO:
                    self._eps[stock_symbol][TVItems.PRICE_TO_EARNINGS_RATIO] = data.pop(0)
                    break
        return

    def __set_data(self, stock_symbol: str) -> None:
        self._data[stock_symbol] = {
            TVItems.CURRENT_PRICE:           self._current_price[stock_symbol],
            TVItems.TOTAL_SHARES:            self._total_shares_outstanding[stock_symbol][TVItems.TOTAL_SHARES],
            TVItems.DIVIDENDS:               self._dividends[stock_symbol][0], 
            TVItems.PRICE_TO_EARNINGS_RATIO: self._eps[stock_symbol][TVItems.PRICE_TO_EARNINGS_RATIO],
            TVItems.TRADING_BELOW_BALUE:     self._trading_below_value[stock_symbol][TVItems.TRADING_BELOW_BALUE]
        }
        return
    

    def __set_trading_below(self, stock_symbol: str, data: list) -> None:
        """
            Trading below cash can be illustrated by a company that holds $2,000,000 in cash reserves,
            has $1,000,000 in outstanding liabilities, and has a total market capitalization equal to $650,000. 
            Its cash reserves less its liabilities are equal to $1,000,000 ($2MM - $1MM = $1MM), 
            while the total value of its stock is only $650,000.
        
        """

        if TVItems.DEBT_TO_EQUITY_RATIO in data:
            self._trading_below_value[stock_symbol] = dict({"Trading Below Value": False})

            while len(data) > 0:
                if data.pop(0) == TVItems.DEBT_TO_EQUITY_RATIO:
                    debt_to_equity_ratio = float(data.pop(0))
                    self._trading_below_value[stock_symbol][TVItems.DEBT_TO_EQUITY_RATIO] = False if debt_to_equity_ratio > 0 else True
                    break
        return

    def __reset_data(self) -> None:
        self._current_price            = dict()
        self._total_shares_outstanding = dict()
        self._eps                      = dict()
        self._dividends                = dict()
        return

    def scrape_data(self) -> None:
        stock_count = 1
        self.__set_gui()

        for stock_symbol in G.config.stock_list:
            G.log.print_and_log(f"Fetching data for {stock_symbol} {stock_count} / {len(G.config.stock_list)}")
            
            url = TRADING_VIEW_URL + stock_symbol + '/'
            self._browser.get(url)

            time.sleep(1)

            self.__set_current_price(stock_symbol)

            categories = self._browser.find_elements(By.XPATH, Selectors.GENERAL_DATA_XPATH)

            for category in categories:
                try:
                    data = category.text.split('\n')
                    self.__set_shares(stock_symbol, data)
                    self.__set_eps(stock_symbol, data)
                    self.__set_dividends(stock_symbol, data)
                    self.__set_trading_below(stock_symbol, data)
                except NoSuchElementException:
                    G.log.print_and_log(f"No such element was found: {stock_symbol}")
                except Exception as e:
                    G.log.print_and_log(e=e, error_type=type(e).__name__, filename=__file__, tb_lineno=e.__traceback__.tb_lineno)

            self.__set_data(stock_symbol)
            self.__reset_data()
            stock_count += 1

        G.log.print_and_log(f"{PrettyPrinter().pformat(self._data)}")
        self._browser.quit()
        return