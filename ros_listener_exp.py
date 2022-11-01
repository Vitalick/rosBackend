import asyncio
import datetime
from typing import List

from ws_manager import ConnectionManager


class RosSubscriber:

    def __init__(self):
        self.callback_list: List = []
        asyncio.create_task(self._periodic_broadcast())

    async def _periodic_broadcast(self, wait_sec: int = 1):
        while True:
            await asyncio.sleep(wait_sec)
            self.send_to_callbacks(str(datetime.datetime.now()))

    def send_to_callbacks(self, msg):
        for callback in self.callback_list:
            callback(msg)

    def subscribe(self, callback):
        self.callback_list.append(callback)


ros = RosSubscriber()


async def ros_listen(manager: ConnectionManager):
    def ros_callback(msg):
        asyncio.create_task(manager.broadcast(f"Message from ros: {msg}"))

    ros.subscribe(ros_callback)
    # Вместо строки выше нужно подписать ros на эту функцию
    # ros_callback как раз то что будет отсылать в manager вебсокета
    # а тут нужно сделать действия которые этот коллбэк подпишут
