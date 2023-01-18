"""Модуль хранит объекты конфигурации."""

import os

_CONFIG = {
    # Для cwd (current working directory) берется верхнее значение.
    # Исп. собственное решение, тк click по-умолчанию использует:
    #   __package__ из переименнованного [tool.poetry.scripts]
    "prog_name": os.path.basename(os.getcwd()).capitalize(),
    # Директория проекта
    "root_dir": os.path.dirname(os.path.abspath(__package__)),
}
