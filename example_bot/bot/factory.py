from aiogram import Dispatcher, Bot
from deta import Deta

from aiogram_deta.storage import DetaStorage
from example_bot.bot.handlers.echo import echo_router
from example_bot.bot.handlers.form import form_router


def create_dispatcher(deta: Deta) -> Dispatcher:
    storage = DetaStorage(deta_base=deta.AsyncBase("fsm"))
    dispatcher = Dispatcher(storage=storage)

    for router in [
        form_router,
        echo_router,
    ]:
        dispatcher.include_router(router)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode="HTML")
