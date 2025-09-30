import pytz
import math
from datetime import datetime
from typing import Union

GST_TIMEZONE = pytz.timezone('Asia/Dubai')  # GST is UTC+4

class ValueValidationError(Exception):
    """Custom exception for maze validation errors"""
    pass

def get_unique_id(prefix: str = '') -> str:
    currect_time = datetime.now(GST_TIMEZONE).strftime("%Y-%m-%d-%H-%M-%S-%f")
    return prefix + currect_time

def get_distance(x1: Union[int, float], y1: Union[int, float], x2: Union[int, float], y2: Union[int, float]) -> float:
    if not all([isinstance(coordinate, int) or isinstance(coordinate, float) for coordinate in [x1, y1, x2, y2]]):
        print("Warning: Provide correct numbers")
        return None
    
    return math.dist((x1, y1), (x2, y2))

def check_type(variable, expected_type, var_name=None):
    """Hard validation - raises exception"""
    if not isinstance(variable, expected_type):
        name = var_name or "variable"
        type_name = expected_type.__name__
        raise ValueValidationError(f"`{name}` must be {type_name}, got {type(variable).__name__}.")
    return True