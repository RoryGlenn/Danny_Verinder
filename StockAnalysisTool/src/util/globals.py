"globals.py - Uses global variables that are shared between files in order to write to the log file."

from util.log  import Log

class Globals:
    log: Log = Log()


# Global variable "G" is shared between files and classes
G: Globals = Globals()
