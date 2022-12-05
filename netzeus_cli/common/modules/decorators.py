from functools import wraps
from typing import Any
import asyncio

from netzeus_cli.common.modules.envloader import (
    add_module_env_requirements,
    validate_module_env_requirements,
)


def require_envs(**kwargs) -> Any:
    """Enables you to specify required environment variables to perform basic check
    before the user continues to run a command/plugin

    Args:
        **kwargs:   Wrapper function takes kwargs as environment variable names
    """
    env_args = kwargs

    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            add_module_env_requirements(func.__name__, **env_args)
            validate_module_env_requirements()
            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def coro(f):
    """Decorates a click command so that you can run async eg. using aiohttp"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
