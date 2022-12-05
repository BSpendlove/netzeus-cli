from pathlib import Path, PurePath
from dotenv import load_dotenv, find_dotenv
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
import click

from netzeus_cli.common.modules import envloader


@with_plugins(iter_entry_points("netzeus_cli.plugins"))
@with_plugins(iter_entry_points("click_command_tree"))
@click.group()
def cli():
    """CLI Application with plugin based architecture to perform network related functions"""
    env_path = PurePath.joinpath(Path.home(), ".netzeus_cli")
    if not find_dotenv(env_path):
        exit(
            f"Unable to find .netzeus_cli env, please create this in your home directory ({Path.home()})"
        )

    load_dotenv(dotenv_path=env_path, verbose=True)
    envloader.validate_module_env_requirements()
