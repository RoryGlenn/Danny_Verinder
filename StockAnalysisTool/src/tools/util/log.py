import datetime
import os

from .enums import *


class Log():
    def __init__(self):
        self.log_directory_path = "StockAnalysisTool/logs"
        self.log_file_path      = "StockAnalysisTool/logs" + "/" + str(datetime.date.today()) + ".txt"

    def get_current_time(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def get_current_date(self) -> str:
        return datetime.datetime.today().strftime("%d/%m/%Y")

    def directory_create(self) -> None:
        try:
            if not os.path.exists(self.log_directory_path):
                os.mkdir(self.log_directory_path)
        except Exception as e:
            print(f"ERROR: || {e}, {type(e).__name__} {__file__} {e.__traceback__.tb_lineno}" )
        return

    def file_create(self):
        try:
            if not os.path.exists(self.log_file_path):
                # create the file
                file = open(self.log_file_path, FileMode.READ_WRITE_CREATE)
                file.close()

            # If its out first time opening the file since we started up,
            # write a new line to make it a little neater
            with open(self.log_file_path, FileMode.WRITE_APPEND, encoding='utf-8') as file:
                file.write("\n=========================================================================================\n")
        except Exception as e:
            print(f"ERROR: || {e}, {type(e).__name__} {__file__} {e.__traceback__.tb_lineno}" )
        return

    def write(self, text):
        """Writes to the end of the log file"""
        try:
            file_path="StockAnalysisTool/logs/" + str(datetime.date.today()) + ".txt"
            with open(file_path, FileMode.WRITE_APPEND, encoding='utf-8') as file:
                file.write(f"{text}\n")
        except Exception as e:
            print(f"ERROR: || {e}, {type(e).__name__} {__file__} {e.__traceback__.tb_lineno}" )
        return


    def print_and_log(self, message: str = "", e=False, error_type: str = "", filename: str = "", tb_lineno: str = "") -> None:
        """Print to the console and write to the log file. 
        If something went wrong, just print the error to console."""
        try:
            current_time = self.get_current_time()
            current_date = self.get_current_date()
            
            result = f"[{current_date} {current_time}] {message}"

            if e:
                print(f"{result} ERROR: || {e}, {error_type} {filename} {tb_lineno}" )
                self.write(f"{result} ERROR: || {e}, {error_type} {filename} {tb_lineno}")
                return
            else:
                print(     result)
                self.write(result)
        except Exception as e:
            print(e)
        return
    