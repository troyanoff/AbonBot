import time
import traceback


from functools import wraps


def safe_exec_api(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        try:
            result = await func(*args, **kwargs)
            end = time() - start
            result.ttc = end
            return result
        except Exception as e:
            print(traceback.format_exc())
            end = time() - start
            print(
                f'{func.__name__}: time to complete: {end:.2f}')
            return None
    return wrapper
