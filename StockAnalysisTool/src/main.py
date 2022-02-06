import os

from util.trading_view_web_scrapper import TradingViewWebScraper


if __name__ == '__main__':
    os.system("cls")
    
    tv_webscrapper = TradingViewWebScraper()
    tv_webscrapper.get_data()

