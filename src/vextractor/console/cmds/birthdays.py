"""Модуль обрабатывает консольную команду `vextract birthdays`.

ToDo:
    * Протестировать работу через --login и --password. Мб придется отказаться от ручного
    ввода. Проще создать файл `.env`.
"""
from csv import DictWriter
from dataclasses import asdict, fields

import click

from vextractor.utils import define_result_file_path
from vextractor.vk.core import VK
from vextractor.vk.dataclasses import Friend


@click.command
@click.help_option("-h", "--help")
@click.option("--login", envvar="VK_LOGIN", help="Fill vk login from console.")
@click.password_option(envvar="VK_PASSWORD", help="Fill vk password from console.")
def birthdays(login, password):
    """Extract friends birthdays."""

    api = VK(login, password)
    result = api.get_friends_birthdays()

    if hasattr(result, "items"):

        file_name = define_result_file_path("birthdays")

        with click.open_file(file_name, "w", encoding="utf-8") as f:

            writer = DictWriter(f, fieldnames=[field.name for field in fields(Friend)])
            writer.writeheader()

            for row in result.items:
                writer.writerow(asdict(row))

        click.echo("Vextractor saved file: {}".format(file_name))
