"""Модуль включает вспомогательные функции, процедуры и обработчики."""
import os

from vextractor.console.config import _CONFIG as CFG


def check_results_dir(sub_folder: str = None) -> bool:
    """Проверяет директорию `ROOT/results/`.

    Если директория отсутствует, то создает ее.
    Если же указывается поддиректория, то создает и ее.

    Args:
        sub_folder (str): Поддиректория.

    Returns:
        bool: Существует `ROOT/results`? `True` - да (была или создали только что).
        `False` - нет (ошибка создания).
    """

    # Если `ROOT/results` не существует
    if not os.path.exists(results_dir_path := os.path.join(CFG["root_dir"], "results")):
        try:
            os.makedirs(results_dir_path)  # Пробуем создать
        except OSError:
            return False

    if sub_folder:
        try:
            os.makedirs(os.path.join(results_dir_path, sub_folder))  # Пробуем создать 2
        except OSError:
            return False

    return True


def define_result_file_path(file_name: str, need_results: bool = True) -> str:
    """Определяет путь к результирующему файлу csv.

    Если `ROOT/results` не существует, создает директорию.

    Args:
        file_name (str): Наименование результирующего файла.
        need_results (bool): Нужно ли создавать результирующую директорию?
            Если `False`, то кладем файл в ROOT директорию.

    Returns:
        str: Путь к результирующему файлу csv.
    """

    file_name = file_name or "result"
    file_name += ".csv" if not file_name.endswith(".csv") else ""

    if need_results and check_results_dir():
        return os.path.join(CFG["root_dir"], "results", file_name)
    else:
        return os.path.join(CFG["root_dir"], file_name)


def define_result_folder_path(folder_name: str, need_results: bool = True) -> str:
    """Определяем путь к результирующей директории.

    Если `ROOT/results` не существует, создает директорию.

    Args:
        folder_name (str): Наименование результирующей директории.
        need_results (bool): Нужно ли создавать результирующую директорию?
            Если `False`, то кладем файл в ROOT директорию.

    Returns:
        str: Путь к результирующей директории.
    """
    folder_name = folder_name or "result"

    if need_results and check_results_dir(folder_name):
        return os.path.join(CFG["root_dir"], "results", folder_name)
    else:
        return os.path.join(CFG["root_dir"], folder_name)
