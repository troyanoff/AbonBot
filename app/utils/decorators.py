import traceback

from functools import wraps
from time import time

from schemas.utils import ExceptSchema, DoneSchema, FailSchema


def safe_exec_api(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        try:
            result: DoneSchema | FailSchema = await func(*args, **kwargs)
            end = time() - start
            result.response.ttc = end
            return result
        except Exception:
            end = time() - start
            return ExceptSchema(
                msg=f'{func.__name__}: time to complete: {end:.2f}',
                exc=traceback.format_exc()
            )
    return wrapper
