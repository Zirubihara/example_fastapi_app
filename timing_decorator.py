import time
import logging
import functools
import inspect
import asyncio

logger = logging.getLogger(__name__)

def time_logger(func):
    """Decorator to log the execution time of a function."""

    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                f"Executed {func.__name__} in {execution_time:.4f} seconds"
            )
            return result
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                f"Executed {func.__name__} in {execution_time:.4f} seconds"
            )
            return result
        return sync_wrapper
