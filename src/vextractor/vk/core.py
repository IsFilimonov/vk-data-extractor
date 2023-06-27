"""Модуль представляет основной класс работы с VKontakte и способствующие этому объекты.

ToDo:
    * `format_friends_birthdays` -> Friends, если в этом будет необходимость. Пока что
        затраченные ресурсы на работу превосходят гипотетическую потребность.

"""
import os
import re
from typing import Any, Final, Optional, TypedDict

import vk_api
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod

from vextractor.vk.dataclasses import Friends


class APIResponse(TypedDict):
    """Структурированный ответ API Vkontakte.

    Данный класс структурирует ответ, полученный с помощью библиотеки `vk_api`.

    Info:
        Более подробно смотреть секцию `return` объекта:
        ```python
        from vk_api.tools import vk_get_all_items
        ```

    Args:
        count (int): Количество записей в ответе.
        items (list[dict[str, Any]]): Записи ответа.
        offset (int): Смещение ответа на количество элементов.
        more (Any): Нет информации.
    """

    count: int
    items: list[dict[str, Any]]
    offset: int
    more: Any


def captcha_handler(captcha: Any) -> Any:
    """Обработчик каптчи в консоле.

    При возникновении капчи вызывается эта функция и ей передается объект каптчи.
    Через метод `get_url` можно получить ссылку на изображение.
    Через метод `try_again` можно попытаться отправить запрос с кодом капчи.

    Info:
        [http://vk.com/dev/captcha_error](
            http://vk.com/dev/captcha_error)

    Args:
        captcha (): Объект исключения `Captcha`.

    Returns:
        Пробуем снова отправить запрос с каптчей.
    """

    key = input("Enter captcha code {}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


class VK:
    """Основной класс для работы с API VKontakte.

    Args:
        login (Optional[str]): Логин доступа к VK.
            Приоритет заполнения вручную из консоли, иначе из переменной окружения
            `VK_LOGIN`.
        password (Optional[str]): Пароль доступа к VK.
            Приоритет заполнения вручную из консоли, иначе из переменной окружения
            `VK_PASSWORD`.

    Attributes:
        _f_b_api_fields (Final[tuple[str, ...]]): Перечень полей для заполнения
            параметра `fields` при обращении к методу `friends.get` API VKontakte.
    """

    # Friends birthdays api fields
    _f_b_api_fields: Final[tuple[str, ...]] = ("bdate", "last_seen", "nickname")

    def __init__(
        self, login: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        if not login and not password:
            login = os.environ.get("VK_LOGIN")
            password = os.environ.get("VK_PASSWORD")

        s = vk_api.VkApi(login, password, captcha_handler=captcha_handler)

        try:
            s.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        # Приватный API для работы с API VK.
        self.__api: VkApiMethod = s.get_api()

    def get_friends(self, fields: str) -> APIResponse:
        """Получает результат VK API метода `friends.get`.

        Info:
            [https://dev.vk.com/method/friends.get](
                https://dev.vk.com/method/friends.get)

        Args:
            fields (str): Список дополнительных полей, которые необходимо вернуть.

        Returns:
            Список друзей пользователя, но не более 5000.
        """
        return self.api.friends.get(fields=fields)

    def get_friends_birthdays(self, need_format: bool = False) -> Friends | None:
        """Запрашивает дни рождения друзей у API VK.

        Args:
            need_format (bool): Требуется ли дополнительное форматирование данных?
                По умолчанию возвращает данные как есть.

        Returns:
            Таблица друзей с информацией о днях рождения.
        """

        def format_friends_birthdays(data: Friends) -> Friends:
            return data

        fields = ", ".join(VK.get_friends_birthdays_api_fields())

        response = self.get_friends(fields=fields)

        friends = Friends(response["items"]) if "items" in response else None

        return format_friends_birthdays(friends) if need_format and friends else friends

    @property
    def api(self) -> VkApi:
        """Публичный API для работы с API VK.

        Интерфейс приватного объекта API для защиты от изменений.

        Returns:
            Возвращает приватный API для работы с API VK.
        """
        return self.__api

    @staticmethod
    def get_friends_birthdays_api_fields() -> tuple[str, ...]:
        """Поля для параметра `fields` метода API `friends.get`.

        Чтобы напрямую не обращаться к атрибуту класса.

        Returns:
            Строка с перечнем полей.
        """

        if isinstance(VK._f_b_api_fields, tuple):
            return VK._f_b_api_fields

    @staticmethod
    def extract_album_parametrs_from_url(url: str) -> tuple[str, str]:
        """Получаем параметры из ссылки на альбом.

        В url содержится как id владельца альбома (отрицательное значение означает,
        что владелец - группа), так и id альбома.

        Args:
            url (str): Ссылка на альбом.

        Returns:
            id владельца, id альбома.
        """
        pattern_url = r"^https:.*album\-\d+_\d+$"

        owner_match = re.search(r"album(-\d+)_", url)
        album_match = re.search(r"album-\d+_(\d+)$", url)

        if not re.match(pattern_url, url):
            raise ValueError("Invalid url: {}".format(url))
        if not owner_match:
            raise ValueError("Owner not found in URL")
        if not album_match:
            raise ValueError("Album not found in URL")

        owner, album = owner_match.group(1), album_match.group(1)

        return owner, album

    def get_list_of_album_images(self, owner: str, album: str) -> APIResponse:
        """Получаем список изображений в альбоме.

        Информация по изображениям хранится в различных размерах. Максимальное количество
        изображения за один запрос - 1000, иначе потребуется использовать `offset`.
        Более подробно читайте документацию: https://vk.com/dev/objects/photo_sizes .

        Args:
            owner (str): Идентификатор владельца. Может быть отрицательным для групп.
            album (str): Идентификатор альбома.

        Returns:
            Список изображений в формате JSON.
        """
        return self.api.photos.get(owner_id=owner, album_id=album, count=1000)
