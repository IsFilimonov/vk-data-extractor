"""Модуль объединяет исчисляемые объекты.
"""

from enum import IntEnum


class Platform(IntEnum):
    """Перечень платформ для `LastSeen` датакласса.

    На какой платформе был замечен пользователь в последнее посещение.
    Хранятся в объекте вместе с временем последнего посещения пользователя `time`
    в Unix формате.

    Info:
        VK `API` → `User` → `last_seen` → `platform`:
        [https://dev.vk.com/reference/objects/user#last_seen](
            https://dev.vk.com/reference/objects/user#last_seen)

    """

    MOBILE = 1
    """Мобильная версия."""
    IPHONE = 2
    """Приложение для iPhone."""
    IPAD = 3
    """Приложение для iPad."""
    ANDROID = 4
    """Приложение для Android."""
    WINDOWS_PHONE = 5
    """Приложение для Windows Phone."""
    WINDOWS_10 = 6
    """Приложение для Windows 10."""
    FULL = 7
    """Полная версия сайта."""
