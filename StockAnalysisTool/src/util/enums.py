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
    data = [
        'Market Capitalization',
        'Enterprise Value (MRQ)',
        'Enterprise Value/EBITDA (TTM)',
        'Total Shares Outstanding (MRQ)',
        'Number of Employees',
        'Number of Shareholders',
        'Price to Earnings Ratio (TTM)',
        'Price to Revenue Ratio (TTM)',
        'Price to Book (FY)',
        'Price to Sales (FY)',
        'Quick Ratio (MRQ)',
        'Current Ratio (MRQ)',
        'Debt to Equity Ratio (MRQ)',
        'Net Debt (MRQ)',
        'Total Debt (MRQ)',
        'Total Assets (MRQ)',
        'Return on Assets (TTM)',
        'Return on Equity (TTM)',
        'Return on Invested Capital (TTM)',
        'Revenue per Employee (TTM)',
        'Average Volume (10 day)',
        '1-Year Beta',
        '52 Week High',
        '52 Week Low',
        'Dividends Paid (FY)',
        'Dividends Yield (FY)',
        'Dividends per Share (FY)',
        'Net Margin (TTM)',
        'Gross Margin (TTM)',
        'Operating Margin (TTM)',
        'Pretax Margin (TTM)',
        'Basic EPS (FY)',
        'Basic EPS (TTM)',
        'EPS Diluted (FY)',
        'Net Income (FY)',
        'EBITDA (TTM)',
        'Gross Profit (MRQ)',
        'Gross Profit (FY)',
        'Last Year Revenue (FY)',
        'Total Revenue (FY)',
        'Free Cash Flow (TTM)'
        ]