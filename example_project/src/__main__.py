import logging
from os import getenv

from deta import Deta
from aiogram import Bot
from aiogram_deta.bot import create_dispatcher
from aiogram_deta.fastapi import create_app
from aiogram_deta.space import DetaBase

from .handlers import setup_handlers
from .utils.commands import set_bot_commands

logger = logging.getLogger(__name__)


# Deta
deta = Deta()
trigger_base = DetaBase(  # custom table in DetaBase
    deta.AsyncBase('triggers')
)


# Aiogram bot
bot = Bot(token=getenv('BOT_TOKEN'), parse_mode='HTML')
dispatcher = create_dispatcher(
    deta=deta,
    trigger_base=trigger_base,  # to use triggers
)
setup_handlers(dispatcher)


# FastAPI
async def on_startup():
    await set_bot_commands(bot)
    logger.error("\n\nBot: online\n\n")

app = create_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=getenv('WEBHOOK_SECRET'),
)
app.add_event_handler('startup', on_startup)
