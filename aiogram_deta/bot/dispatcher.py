from typing import Optional, Union

from deta import Deta
from aiogram import Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.base import BaseEventIsolation

from aiogram_deta.bot.fsm import DetaFSMContext


def create_dispatcher(
    *,
    deta: Deta,
    fsm_host: Union[str, None] = None,
    fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
    events_isolation: Optional[BaseEventIsolation] = None,
    name: Optional[str] = None,
    **kwargs,
) -> Dispatcher:
    kwargs['disable_fsm'] = False
    kwargs['storage'] = DetaFSMContext(
        deta_base=deta.AsyncBase(name="fsm", host=fsm_host),
    )
    return Dispatcher(
        fsm_strategy=fsm_strategy,
        events_isolation=events_isolation,
        name=name,
        **kwargs,
    )
