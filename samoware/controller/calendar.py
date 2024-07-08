from datetime import datetime
from datetime import timedelta

import httpx

from samoware.client import Samoware
from samoware.interface.builder import XIMSSBuilder


class Calendar(Samoware):

    async def open(self):
        """Открывает календарь."""
        await self.make_session_key()
        builder = XIMSSBuilder('XIMSS')
        builder.add_element(tag='calendarOpen',
                            text='',
                            attributes={
                                'mailbox': f'{self.calendar_author}/{self.room_name}" encrypted="false',
                                'calendar': f'{self.calendar_author}/{self.room_name}-CM-{self.room_id}',
                                'id': self.room_id})
        resp = await self.send(str(builder))
        print(f'Открыть {resp.status_code}')

    async def close(self):
        """Закрывает календарь."""
        builder = XIMSSBuilder('XIMSS')
        builder.add_element(
            tag='calendarClose',
            text='',
            attributes={'mailbox': f'{self.calendar_author}/{self.room_name}" encrypted="false',
                        'calendar': f'{self.calendar_author}/{self.room_name}-CM-{self.room_id}',
                        'id': self.room_id})
        resp = await self.send(str(builder))
        print(f'Закрыть {resp.status_code}')

    async def all(self,
                  start: datetime = datetime.now(),
                  end: datetime = datetime.now() + timedelta(hours=1)):
        """Взять все события из календаря за период.

        :param
        start: начало периода (по умолчания текущая дата-время)
        end: конец периода (по умолчанию +1 час к start)

        """
        builder = XIMSSBuilder('XIMSS')
        builder.add_element(tag='findEvents', text='',
                            attributes={
                                'calendar': f'{self.calendar_author}/{self.room_name}-CM-0',
                                'timeFrom': start,
                                'timeTill': end,
                                'id': '2'
                            })
        resp = await self.send(str(builder))

    async def filter_by(self, filter: dict):
        ...

    async def create(self, body: dict):
        ...

    async def update(self, body: dict):
        ...

    async def delete(self, uid: int):
        ...

    async def send(self, body: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(url=self._host + self._session_key + '/sync', data=body)
            if not response.status_code == 200:
                raise ValueError(f'Ошибка: {response}')
            return response
