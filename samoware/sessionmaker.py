from client import Samoware
from exceptions.common_exceptions import NotFoundConnection


class SamowareSession:
    """
    Создание сессии с календарем

    Пример использования:
    создаем объект нужного нам сервиса
    calendar = Calendar(host=samoware.get('host'),
                            username=samoware.get('user'),
                            password=samoware.get('password'),
                            cached=True,
                            calendar_author=None,
                            room_id=1,
                            room_name='ExampleRoom',
                            storage=redis)
    Дальше можно использовать сессию календаря:
        async with SamowareSession(calendar) as session:
            result = await session.all()

    :param
    service_samoware: объект нужного сервиса Календарь или Почта. В зависимости от нужного.

    :raise NotFoundConnection если не удалось подключиться к календарю
    """

    def __init__(self, service_samoware: Samoware):
        self._connection = service_samoware

    async def __aenter__(self):
        if self._connection:
            await self._connection.open()
            return self._connection
        raise NotFoundConnection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            await self._connection.close()
