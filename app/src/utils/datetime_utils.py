from datetime import time

def time_to_string(time_obj):
    return time_obj.strftime('%H:%M:%S') if isinstance(time_obj, time) else time_obj
