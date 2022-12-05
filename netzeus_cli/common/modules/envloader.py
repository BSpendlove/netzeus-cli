from os import environ
from pathlib import Path
from typing import Any, Union, Tuple
from dotenv import load_dotenv, dotenv_values, set_key, unset_key
from loguru import logger

from netzeus_cli.common.models.env import EnvironmentVariableModule, EnvironmentVariable

REQUIRED_ENV = []


def load_netzeus_env(home_path: Path = Path.home(), as_dict: bool = False) -> dict:
    """Loads the default netzeus_cli env located in the home directory by default as ~/.netzeus_cli

    Args:
        home_path:  Typically the user path (windows, linx and mac friendly if using Path.home())
        as_dict:    Return the environment variables in a dictionary
    """
    env_path = home_path.joinpath(".netzeus_cli")
    if not env_path.exists():
        logger.error("Unable to find netzeus_cli env file")
        exit()

    if as_dict:
        return dict(dotenv_values(env_path))
    load_dotenv(dotenv_path=env_path, verbose=True)


def set_netzeus_env(
    key: str, value: str, home_path: Path = Path.home(), include_quote: bool = False
) -> Tuple[bool, str, str]:
    """Set a environment variable in the netzeus_cli env located in the home directory by default as ~/.netzeus_cli

    Args:
        key:            Key to set
        value:          Value to set
        home_path:      Typically the user path (windows, linx and mac friendly if using Path.home())
        include_quote:  Wraps the environment value in quotes
    """
    env_path = home_path.joinpath(".netzeus_cli")
    if not env_path.exists():
        logger.error("Unable to find netzeus_cli env file")
        exit()

    return set_key(
        dotenv_path=env_path,
        key_to_set=key,
        value_to_set=value,
        quote_mode="never" if not include_quote else "always",
    )


def delete_netzeus_env(key: str, home_path: Path = Path.home()) -> Tuple[bool, str]:
    """Deletes an environment variable in the netzeus_cli env located in the home directory by default as ~/.netzeus_cli

    Args:
        key:        Key to find environment variable and delete it
    """
    env_path = home_path.joinpath(".netzeus_cli")
    if not env_path.exists():
        logger.error("Unable to find netzeus_cli env file")
        exit()

    return unset_key(dotenv_path=env_path, key_to_unset=key)


def add_module_env_requirements(module_name: str, **kwargs) -> None:
    """Add a required ENV variable, this function can be called from any netzeus_cli
    plugin to ensure user has setup the ENV file properly.

    Args:
        module_name: Name of the Module
    """
    variables = []
    for k, v in kwargs.items():
        try:
            variables.append(EnvironmentVariable(name=k, var_type=v))
        except Exception as err:
            logger.error(
                f"Unable to add ENV requirement to module {module_name} "
                "for: {k} = {v}. \nError: {error}"
            )
            exit()

    REQUIRED_ENV.append(
        EnvironmentVariableModule(module=module_name, variables=variables)
    )


def validate_module_env_requirements() -> Union[bool, str]:
    """Validates ENV exist for the required modules in netzeus_cli."""
    for module_ in REQUIRED_ENV:
        for module_variable in module_.variables:
            if not environ.get(module_variable.name):
                logger.error(
                    f"Module {module_.module} can not load required environment variable: {module_variable.name}. Please ensure this exist in your ~/.netzeus_cli file"
                )
                exit()
            else:
                try:
                    module_variable.var_type(environ.get(module_variable.name))
                except Exception as err:
                    logger.error(
                        f"Module {module_.module} can not convert to correct type: {module_variable.var_type}"
                    )
                    exit()

    return False


def print_required_envs():
    """Prints the required ENVs based on plugin requirements."""
    for module_obj in REQUIRED_ENV:
        print("=" * 42)
        print(f"Module {module_obj.module} required variables")
        print("=" * 42)
        for module_variable in module_obj.variables:
            print(module_variable.name)
    print("=" * 42)
