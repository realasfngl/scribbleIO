from typing    import Callable, Any, Optional
from .logger   import Log
from functools import wraps


class Run:
    """
    Class to handle runtime
    """
    
    @staticmethod
    def Error(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Error function to catch errors
        
        @param func: The function to wrap.
        @return:     Custom error message
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Run.handle_error(e)
                return None 
        return wrapper

    @staticmethod
    def handle_error(exception: Exception) -> Optional[None]:
        """
        Handling an error
        
        @param exception: Exception that occured
        """
        Log.Error(f"Error occurred: {exception}")
        exit()