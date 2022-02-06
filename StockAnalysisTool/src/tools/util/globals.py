"globals.py - Uses global variables that are shared between files in order to write to the log file."

from .log    import Log
from .config import Config

class Globals:
    log:    Log    = Log()
    config: Config = Config()

# Global variable "G" is shared between files and classes
G: Globals = Globals()
