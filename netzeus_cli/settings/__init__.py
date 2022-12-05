from netzeus_cli.cli import cli


@cli.group("settings")
def netzeus_cli_settings() -> None:
    """NetZeus CLI commands to view/maintain settings"""

from netzeus_cli.settings.env import add, delete, edit