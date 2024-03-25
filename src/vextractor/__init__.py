"""Инициализация пакета Vextractor.

В момент инициализации пакета заполняются метаданные пакета:
    - `__version__` из файла `pyproject.toml`.
Так же заполняются переменные окружения из `.env` файла.
По заполнению чистится память от импортируемых объектов, в силу ненадобности.
"""

from importlib import metadata

from dotenv import load_dotenv

__version__ = metadata.version(__package__)

load_dotenv()

del metadata
del load_dotenv
