from typing import Optional, Union

import httpx
from lxml import etree

from samoware.exceptions.common_exceptions import AuthenticationError


class Samoware:

    def __init__(self,
                 host: str,
                 username: str,
                 password: str,
                 calendar_author: str,
                 room_id: int,
                 room_name: str,
                 auth_url: str = 'ximsslogin/',
                 cached: bool = False,
                 storage=None
                 ):

        if not host:
            raise ValueError
        if not username:
            raise ValueError
        if not password:
            raise ValueError
        if cached and storage is None:
            raise ValueError('Add storage for caching request!')

        self.service = None
        self._host = host
        self._user = username
        self._password = password
        self._session_key: Optional[str] = None
        self._auth_url: str = auth_url
        self.cached = cached
        self.storage = storage
        self.calendar_author: int = calendar_author
        self.room_id: int = room_id
        self.room_name: str = room_name

    async def make_session_key(self) -> None:
        """
        Сохраняет ключ аутентифицированного пользователя в стейт объекта.
        """
        if await self.storage.get(self._user):
            self._session_key = (await self.storage.get(self._user)).decode()
            print('et')
        else:
            token_body = await self.auth()
            root = etree.fromstring(token_body)
            self._session_key = f'Session/{root.xpath("//session/@urlID")[0]}'
            print('no')
            await self.storage.setex(self._user, 1000, self._session_key)

    async def auth(self) -> Union[Exception, str]:
        """
        Аутентифицирует пользователя в почте.

        :return: str - Вернет ответ серверва в формате строки.
        :raise AuthenticationError - не удалось аутентифицировать пользователя.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self._host + self._auth_url,
                                        params={'username': self._user, 'password': self._password})
            if not response.status_code == 200:
                raise AuthenticationError(response.text)
            return response.text
