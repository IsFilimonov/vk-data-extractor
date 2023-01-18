"""Модуль объединяет датаклассы.

TODO:
    * upgrade User.__post_init__
        При наследовании User -> Friend, метод __post_init__ перезаписывается, хотя
        поля используются те же. Такое поведение приводит к дублированию кода
        валидации и конвертации.
    * refactor converting fields in __post_init__
        for field in fields(self):
            if issubclass(field.type, Factor):
                setattr(self, field.name, field.type(getattr(self, field.name)))
    * After upgrading to 3.11:
        from enum import verify, UNIQUE, CONTINUOUS, NAMED_FLAGS
        @verify(UNIQUE, CONTINUOUS, NAMED_FLAGS)
        class Test(Enum)

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, Optional

from vextractor.vk.enumerates import Platform


@dataclass(slots=True, kw_only=True)
class LastSeen:
    """Время последнего посещения [VKontakte](https://vk.com).

    Info:
        VK `API` → `User` → `last_seen`:
        [https://dev.vk.com/reference/objects/user#last_seen](
            https://dev.vk.com/reference/objects/user#last_seen)

    Args:
        platform (Platform): Тип платформы.
        time (int): Время последнего посещения в формате Unixtime.
    """

    platform: Platform
    time: int

    def __post_init__(self) -> None:
        """Постобработка: конвертация и валидация объектов."""
        # Validation
        if not (0 < self.platform and self.platform < 8):
            assert not self.platform, f"Unsupported platform id: {self.platform}"
        else:
            # Converting
            if isinstance(self.platform, int):
                self.platform = Platform(self.platform)


@dataclass(slots=True, kw_only=True)
class User:
    """Пользователь [VKontakte](https://vk.com).

    Info:
        VK `API` → `User`:
        [https://dev.vk.com/reference/objects/user](
            https://dev.vk.com/reference/objects/user)

    Args:
        id (int): Идентификатор пользователя.
        last_name (Optional[str]): Фамилия.
        deactivated (Optional[str]): Поле возвращается, если страница пользователя удалена
            или заблокирована, содержит значение `deleted` или `banned`.
            В этом случае опциональные поля не возвращаются.
        is_closed (Optional[bool]): Скрыт ли профиль пользователя настройками приватности.
        can_access_closed  (Optional[bool]): Может ли текущий пользователь видеть профиль
            при `is_closed = 1` (например, он есть в друзьях).

        bdate (Optional[str]): Дата рождения. Возвращается в формате D.M.YYYY или D.M
            (если год рождения скрыт). Если дата рождения скрыта целиком, поле
            отсутствует в ответе.
        last_seen (Optional[LastSeen]): Время последнего посещения.
        nickname: (Optional[str]): Никнейм (отчество) пользователя.
    """

    # Base fields
    id: int
    first_name: str
    last_name: Optional[str] = field(default=None)
    deactivated: Optional[str] = field(default=None)
    is_closed: Optional[bool] = field(default=None)
    can_access_closed: Optional[bool] = field(default=None)

    # Optional fields [A-I]
    bdate: Optional[str] = field(default=None)

    # Optional fields [L-R]
    last_seen: Optional[LastSeen] = field(default=None)
    nickname: Optional[str] = field(default=None)

    # Optional fields [S-W]
    ...


@dataclass(slots=True, kw_only=True)
class Friend(User):
    """Описание характеристик друга.

    Структура идентичная `User`, за исключением полей ниже.

    Args:
        track_code (Optional[str]): Нет официальной информации
    """

    track_code: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Постобработка: конвертация и валидация объектов."""
        # Validation
        if self.deactivated not in ("deleted", "banned"):
            assert not self.deactivated, "Unsupported deactivated status {}".format(
                self.deactivated
            )

        if not isinstance(self.id, int):
            assert not self.id, f"Unsupported id data type: {type(self.id)}"

        # Converting
        if isinstance(self.last_seen, dict):
            self.last_seen = LastSeen(**self.last_seen)


@dataclass(slots=True)
class Friends:
    """Объединение друзей в группу.

    Args:
        items (Iterable): Массив друзей.
    """

    items: Iterable[Any] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Постобработка: конвертация и валидация объектов."""
        # Converting
        if isinstance(self.items, list):
            self.items = [Friend(**row) for row in self.items]
