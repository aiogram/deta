from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message
from aiogram_deta.space import DetaBase



class TriggerFilter(Filter):
    async def __call__(
        self,
        msg: Message,
        trigger_base: DetaBase,
    ) -> Union[bool, dict]:
        if not msg.text:
            return False
        if trigger := await trigger_base.get(msg.text.casefold()):
            return {
                'trigger_id': int(trigger.value),
            }
        return False
