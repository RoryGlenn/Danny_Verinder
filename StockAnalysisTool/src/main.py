import os

from tools.scraper.trading_view_web_scraper import TradingViewWebScraper
from tools.util.globals                     import G


def run() -> None:
    G.log.directory_create()
    G.log.file_create()
    
    TradingViewWebScraper().scrape_data()
    return


if __name__ == '__main__':
    os.system("cls")
    run()
