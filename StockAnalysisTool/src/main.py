import os

from trading_view_web_scrapper import TradingViewWebScraper
from util.globals              import G


def run() -> None:
    G.log.directory_create()
    G.log.file_create()
    
    TradingViewWebScraper().scrape_data()
    return


if __name__ == '__main__':
    os.system("cls")
    run()


