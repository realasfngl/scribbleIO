from datetime    import datetime
from colorama    import Fore
from threading   import Lock
from time        import time

class Log:
    
    
    colours: dict = {
        'SUCCESS': Fore.LIGHTGREEN_EX,
        'ERROR': Fore.LIGHTRED_EX,
        'INFO': Fore.LIGHTWHITE_EX
    }
    
    lock = Lock()
    
    @staticmethod
    def _log(level, prefix, message):
        
        timestamp = datetime.fromtimestamp(time()).strftime("%H:%M:%S")
        log_message = (
            f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}{timestamp}{Fore.RESET}{Fore.LIGHTBLACK_EX}]{Fore.RESET} "
            f"{prefix} {message}"
        )
        
        with Log.lock:
            print(log_message)

    @staticmethod
    def Success(message, prefix="[+]", color=colours['SUCCESS']):
        
        Log._log("SUCCESS", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Error(message, prefix="[!]", color=colours['ERROR']):
        
        Log._log("ERROR", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Info(message, prefix="[!]", color=colours['INFO']):
        
        Log._log("INFO", f"{color}{prefix}{Fore.RESET}", message)