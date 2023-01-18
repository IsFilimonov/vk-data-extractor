"""Модуль включает вспомогательные функции, процедуры и обработчики."""
import os

from vextractor.console.config import _CONFIG as CFG


def check_results_dir() -> bool:
    """Проверяет директорию `ROOT/results/`.

    Если директория отсутствует, то создает ее.
    требуется, создает директорию для хранения результатов работы Vextractor.

    Returns:
        bool: Существует `ROOT/results`? `True` - да (была или создали только что).
        `False` - нет (ошибка создания).
    """

    # Если `ROOT/results` не существует
    if not os.path.exists(results_dir_path := os.path.join(CFG["root_dir"], "results")):
        # Пробуем создать
        try:
            os.makedirs(results_dir_path)
        except OSError:
            return False

    return True


def define_result_file_path(file_name: str, need_results: bool = True) -> str:
    """Определяет путь к результирующему файлу.

    Если `ROOT/results` не существует, создает директорию.

    Args:
        file_name (str): Наименование результирующего файла.
        need_results (bool): Нужно ли создавать результирующую директорию?
            Если `False`, то кладем файл в ROOT директорию.
    """

    file_name = "result" if not file_name else file_name
    file_name += ".csv" if not file_name.endswith(".csv") else file_name

    if need_results and check_results_dir():
        return os.path.join(CFG["root_dir"], "results", file_name)
    else:
        return os.path.join(CFG["root_dir"], file_name)
