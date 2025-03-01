import functools
import inspect
import logging
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)


def time_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator to log the execution time of a function.

    This decorator can be applied to both synchronous and asynchronous functions.
    It measures the time taken for the function to execute and logs the execution
    time using the standard logging module.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function that logs its execution time.

    Raises:
        Any exceptions raised by the decorated function will be propagated.

    Example:
        @time_logger
        def my_function():
            # Function logic here
            pass

        @time_logger
        async def my_async_function():
            # Asynchronous function logic here
            pass
    """

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"Executed {func.__name__} in {execution_time:.4f} seconds")
            return result

        return async_wrapper
    else:

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"Executed {func.__name__} in {execution_time:.4f} seconds")
            return result

        return sync_wrapper
