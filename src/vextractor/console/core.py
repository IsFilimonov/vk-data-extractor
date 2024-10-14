"""Модуль представляет точку входа при работе из консоли.

ToDo:
    * Общий параметр `-t`, `--time`, добавляющий к имени временную метку.
"""

import click

from vextractor.console.cmds.album import album
from vextractor.console.cmds.birthdays import birthdays
from vextractor.console.config import _CONFIG as CONFIG


@click.group()
@click.help_option("-h", "--help")
@click.version_option(prog_name=CONFIG["prog_name"])
def start():
    """Hi! This is Vextractor help page. You are welcome."""
    ...


start.add_command(birthdays)
start.add_command(album)
