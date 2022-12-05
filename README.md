# netzeus-cli
A plugin based CLI application that is targeted towards Network Engineers and System Administrators. The idea of this application is that you have a centralized CLI application with autocompletion and can develop your own CLI plugins with a very easy and structured approach using the click python module which uses the concept of command groups, commands and options along with auto-documenting the CLI using the --help functionality.

# Plugins

Netzeus CLI plugins are separate python packages which utilizes the Entry Points feature within setup tools (setup.py). Plugins can be developed simply be creating a brand new python package and can be maintained directly by the plugin developer while utilizing the CLI wrapper of NetZeus CLI. This is easily achievable by using the [click-plugins](https://github.com/click-contrib/click-plugins) module and registering an entry point in the main CLI, any developed plugins which have errors will be caught and not affect other NetZeus CLI plugins.

While there isn't any enforcing of code style or specific practices to writing a NetZeus plugin, you should always follow the Google styleguide, [PEP-484](https://peps.python.org/pep-0484/) for type annotation and docstrings as per [PEP-257](https://peps.python.org/pep-0257/). Environment variable functions are available via `netzeus_cli.common.modules.envloader`. If there is a generic class/function which would benefit to be available to all NetZeus CLI plugins, open a PR to add this functionality into the main NetZeus CLI python package via GitHub.

## Project Structure and Command Tree

![NetZeus CLI Plugins](./docs/img/netzeus_cli_plugins.png)

The project structure of a NetZeus CLI plugin should follow of each command group being a separate folder with a relevant `__init__.py` that initiates the command group, and the sub-commands within that folder using the command group and essentially importing at the top level (`core.py`) for all your relevant command groups and sub-commands, take a look at the below command tree as an example.

### CLI Tree Structure example

Below is an example of 2 root command groups (access and authenticate) with nested sub-command groups, each command is located in their respective sub-command group python file. You could go one step further and separate each create/read(get)/update/delete command when working with REST APIs to follow the CRUD concept in the file layout of your commands, however this seems to be the best balance of lines of code to file ratio that I've personally found.

```
cli - CLI Application with plugin based architecture to perform network related functions
├── proxmox-ve - Interact with Proxmox VE API                                                   core.py                 -       CLI Plugin Entrypoint
│   ├── access - /access API endpoints for Promox VE                                            /access                 -       Command Group "proxmox-ve access"
│   │   ├── domains - Create/Get/Update/Delete domains/realms                                   /access/domains.py      -       Sub-Command Group "proxmox-ve access domains"
│   │   │   ├── create - Create an authentication server/domain                                 /access/domains.py      -       Create command "proxmox-ve access domains create"
│   │   │   ├── delete - Delete a specific auth server/domain                                   /access/domains.py      -       Delete command "proxmox-ve access domains delete"
│   │   │   ├── get - Get details for a specific domain                                         /access/domains.py      -       Get command "proxmox-ve access domains get"
│   │   │   ├── get-all - Get all domains                                                       /access/domains.py      -       Get All command "proxmox-ve access domains get-all"
│   │   │   └── update - Update a specific auth server/domain                                   /access/domains.py      -       Update command "proxmox-ve access domains update"
│   │   ├── ticket - Create or verify authentication tickets/cookies                            /access/ticket.py       -       Sub-Command Group "proxmox-ve access ticket"       
│   │   │   ├── create - Create an authentication ticket                                        /access/ticket.py       -       Create command "proxmox-ve access ticket create"
│   │   │   └── verify - Verify an authentication ticket                                        /access/ticket.py       -       Verify command  "proxmox-ve access ticket verify"
│   │   └── users - Create/Get/Update/Delete Users                                              /access/users.py        -       Sub-Command Group "proxmox-ve access users"
            ├── create - Create a User                                                          /access/users.py        -       Create command "proxmox-ve access users create"
            ├── delete - Delete a specific user                                                 /access/users.py        -       Delete command "proxmox-ve access users delete"
            ├── get - Get details for a specific user                                           /access/users.py        -       Get command "proxmox-ve access users get"
            ├── get-all - Get details about all users                                           /access/users.py        -       Get All command "proxmox-ve access users get-all"
            └── update - Update a specific user                                                 /access/users.py        -       Update command "proxmox-ve access users update"
│   └── authenticate - Authenticate against a Proxmox VE server                                 /authenticate           -       Command Group "proxmox-ve authenticate"
        ├── cookie - Cookie Authentication related commands                                     /authenticate/cookie.py -       Sub-Command Group "proxmox-ve authenticate cookie"
│   │   │   └── get - Get a Proxmox VE Ticket Cookie for authentication purposes                /authenticate/cookie.py -       Get command "proxmox-ve authenticate cookie get"
        └── token - Token Authentication related commands                                       /authenticate/token.py  -       Sub-Command Group "proxmox-ve authenticate token"
            └── test - Test your Proxmox VE API token to ensure it is valid                     /authenticate/token.py  -       Test Token command "proxmox-ve authenticate token test"
```

### Developing a NetZeus CLI Plugin

Firstly, you need to create the initial entrypoint of your root command group which includes a `setup.py` with something similar to this:

```
from setuptools import setup, find_packages

setup(
    name='netzeus_cli_plugin_cool_plugin',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [netzeus_cli.plugins]
        cool-plugin=netzeus_cli_plugin_cool_plugin.core:cool_plugin
    ''',
)
```

The entrypoint within the `setup.py` should follow the format of:

`<cli-command>=<python-package-name>.core:<command_group_function_name>`

so if your `core.py` looks like this:

```
import click

from netzeus_cli.common.modules.decorators import require_envs


@click.group("ding-dong")
@require_envs(SOME_PLUGIN_SPECIFIC_VARIABLE=str)
def ding_dong_root() -> None:
    """Interact with the DingDong API"""
```

then your root command group is called "ding_dong_root" and the `setup.py` entrypoint should look like:

```
    entry_points='''
        [netzeus_cli.plugins]
        ding-dong=netzeus_cli_plugin_ding_dong.core:ding_dong_root
    '''
```

### Documenting NetZeus CLI Plugins

Because NetZeus CLI encourages other people to develop their own plugins, they are also responsible for the documentation and also a good point to make is that because each plugin is a separate repository, this allows each plugin to have its own CI/CD workflow whether it be just linting code and packaging it or running fully fledge tests to ensure each command works before pushing to production. I can not enforce developers to follow a specific documentation standard however examples are provided of plugins developed by the creator of NetZeus CLI and you should try your best to follow the same style practices (or at least provide feedback if you think certain documentation should be amended).

[Click](https://click.palletsprojects.com/en/8.1.x/) should inspire the developer to document on the fly while writing code as efficiently as possible, since the command line interface auto generates the command documentation based on docstrings for command groups, commands and command options (also using the `help` keyword for click options) and therefore you should document your code as much as possible to utilize the self documenting feature that click provides when a user provides the `--help` flag to your command groups/commands. When possible, try to follow the [click documentation practices](https://click.palletsprojects.com/en/8.1.x/documentation/)