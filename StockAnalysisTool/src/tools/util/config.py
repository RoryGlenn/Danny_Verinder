"""config.py - scans for config.json file and applies users settings."""

import json
import os
import sys

from .enums   import *


class Config():
    def __init__(self) -> None:
        self.stock_list = []
        self.set_values()
        return
    
    def set_values(self) -> None:
        if os.path.exists(CONFIG_JSON):
            with open(CONFIG_JSON) as file:
                try:
                    config = json.load(file)
                    
                    for symbol in config['stocks']:
                        self.stock_list.append(str(symbol).upper())
                    self.stock_list.sort()
                except Exception as e:
                    print(e)
                    sys.exit(1)
        else:
            print("Could not find config.json file")
            sys.exit(0)
        return


