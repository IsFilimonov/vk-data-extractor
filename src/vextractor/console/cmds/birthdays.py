"""Модуль обрабатывает консольную команду `vextract birthdays`.

ToDo:
    * Протестировать работу через --login и --password. Мб придется отказаться от ручного
    ввода. Проще создать файл `.env`.
"""
import os
from csv import DictWriter
from dataclasses import asdict, fields

import click

from vextractor.console.config import _CONFIG as cfg
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

        """Определяем директорию для сохранения результатов.

        Для начала проверяем root директорию пакета на наличие папки root/result.
        Если таковая не существует и у нас имеются права на запись - создаем root/results.
        Иначе, пишем файлы в root пакета.
        """
        if not os.path.exists(
            result_dir := os.path.join(cfg["download_dir"], "results")
        ):
            try:
                os.makedirs(result_dir)
            except OSError:
                result_dir_file = os.path.join(cfg["download_dir"], "birthdays.csv")
            else:
                result_dir_file = os.path.join(result_dir, "birthdays.csv")

        with click.open_file(result_dir_file, "w", encoding="utf-8") as f:

            writer = DictWriter(f, fieldnames=[field.name for field in fields(Friend)])
            writer.writeheader()

            for row in result.items:  # type: ignore
                writer.writerow(asdict(row))

        click.echo("File saved: {} !".format(result_dir_file))
