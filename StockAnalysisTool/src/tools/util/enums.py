CHROME_DRIVER_PATH = 'StockAnalysisTool/drivers/chromedriver.exe'
TRADING_VIEW_URL   = 'https://www.tradingview.com/symbols/'
CONFIG_JSON        = 'StockAnalysisTool/json/config.json'


class FileMode:
    """
    Open text file for reading.  The stream is positioned at the
        beginning of the file.    
    """
    READ_ONLY = "r"

    """
    Open for reading and writing.  The stream is positioned at the
        beginning of the file.
    """
    READ_WRITE = "r+"

    """
    Truncate file to zero length or create text file for writing.
         The stream is positioned at the beginning of the file.    
    """
    WRITE_TRUNCATE = "w"

    """
    Open for reading and writing.  The file is created if it does not
         exist, otherwise it is truncated.  The stream is positioned at
         the beginning of the file.
         """
    READ_WRITE_CREATE = "w+"

    """
    Open for writing.  The file is created if it does not exist.  The
        stream is positioned at the end of the file.  Subsequent writes
        to the file will always end up at the then current end of file,
        irrespective of any intervening fseek(3) or similar.
    """

    WRITE_APPEND = "a"

    """
   Open for reading and writing.  The file is created if it does not
        exist.  The stream is positioned at the end of the file.  Subse-
        quent writes to the file will always end up at the then current
        end of file, irrespective of any intervening fseek(3) or similar.
    
    """
    READ_WRITE_APPEND = "a+"

    """
    Configuration file for the rake bot to use on users account and wallets
    """


class TradingViewData:
    MARKET_CAP = 'Market Capitalization'
    ENTERPRISE_VALUE = 'Enterprise Value (MRQ)'
    ENTERPRISE_VALUE_EBITDA = 'Enterprise Value/EBITDA (TTM)'
    TOTAL_SHARES = 'Total Shares Outstanding (MRQ)'
    NUM_EMPLOYEES = 'Number of Employees'
    NUM_SHAREHOLDERS = 'Number of Shareholders'
    PRICE_TO_EARNINGS_RATIO = 'Price to Earnings Ratio (TTM)'
    PRICE_TO_REVENUE_RATIO = 'Price to Revenue Ratio (TTM)'
    PRICE_TO_BOOK = 'Price to Book (FY)'        
    PRICE_TO_SALES = 'Price to Sales (FY)'
    QUICK_RATIO = 'Quick Ratio (MRQ)'
    CURRENT_RATIO = 'Current Ratio (MRQ)'        
    DEBT_TO_EQUITY_RATIO = 'Debt to Equity Ratio (MRQ)'
    NET_DEBT = 'Net Debt (MRQ)'
    TOTAL_DEBT = 'Total Debt (MRQ)'
    TOTAL_ASSETS = 'Total Assets (MRQ)'
    RETURN_ON_ASSETS = 'Return on Assets (TTM)'
    RETURN_ON_EQUITY = 'Return on Equity (TTM)'
    RETURN_ON_INVESTED_CAPITOL = 'Return on Invested Capital (TTM)'
    REVENUE_PER_EMPLOYEE = 'Revenue per Employee (TTM)'
    AVERAGE_VOL_10DAY = 'Average Volume (10 day)'
    ONE_YEAR_BETA = '1-Year Beta'
    YEAR_HIGH = '52 Week High'
    YEAR_LOW = '52 Week Low'
    DIVIDENDS_PAID = 'Dividends Paid (FY)'
    DIVIDENDS_YIELD = 'Dividends Yield (FY)'
    DIVIDENDS_PER_SHARE = 'Dividends per Share (FY)'
    NET_MARGIN = 'Net Margin (TTM)'
    GROSS_MARGIN = 'Gross Margin (TTM)'
    OPERATING_MARGIN = 'Operating Margin (TTM)'
    PRETAX_MARGIN = 'Operating Margin (TTM)'
    BASIC_EPS_FY = 'Basic EPS (FY)'
    BASIC_EPS_TTM = 'Basic EPS (TTM)'
    EPS_DILUTED = 'EPS Diluted (FY)'
    NET_INCOME = 'Net Income (FY)'
    EBITDA = 'EBITDA (TTM)'
    GROSS_PROFIT_MRQ = 'Gross Profit (MRQ)'
    GROSS_PROFIT_YR = 'Gross Profit (FY)'
    LAST_YEAR_REVENUE = 'Last Year Revenue (FY)'
    TOTAL_REVENUE = 'Total Revenue (FY)'
    FREE_CASH_FLOW = 'Free Cash Flow (TTM)'

    # these values below are scraped differently than the values above
    CURRENT_PRICE = 'Current Price'
    DIVIDENDS = 'Dividends'


    CURRENT_PRICE_XPATH = '//div[starts-with(@class, "tv-symbol-price-quote__value js-symbol-last")]'
    GENERAL_DATA_XPATH = '//div[starts-with(@class, "tv-widget-fundamentals__item")]'


class Browser:
    WINDOW_SIZE = "--window-size=1920,1200"