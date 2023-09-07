import logging
import asyncio

from deta import Deta
from aiogram import Bot, Dispatcher
from aiogram_deta.bot import create_dispatcher
from aiogram_deta.fastapi import create_app
from aiogram_deta.space import DetaBase

from .handlers import setup_handlers
from .utils import config
from .utils.commands import set_bot_commands

logger = logging.getLogger(__name__)


def setup () -> (Bot, Dispatcher):
    # deta.AsyncBase should be created within running event loop
    # because otherwise this error appears if run *locally*:
    # https://stackoverflow.com/questions/52232177/runtimeerror-timeout-context-manager-should-be-used-inside-a-task
    # therefore such architecture with setup() function

    # Deta
    deta = Deta()
    trigger_base = DetaBase(  # custom table in DetaBase
        deta.AsyncBase('triggers')
    )

    # Aiogram bot
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dispatcher = create_dispatcher(
        deta=deta,
        trigger_base=trigger_base,  # to use triggers
    )
    setup_handlers(dispatcher)

    return bot, dispatcher


async def on_startup_common (bot: Bot):
    await bot.delete_webhook()
    await set_bot_commands(bot)
    logger.info("\n\nBot: online\n\n")


if config.USE_WEBHOOKS:
    bot, dispatcher = setup()

    async def on_startup ():
        await on_startup_common(bot)

        logger.info(f"The bot will be using webhook at {config.WEBHOOK_URL}")
        await bot.set_webhook(url=config.WEBHOOK_URL, secret_token=config.WEBHOOK_SECRET)

    app = create_app(
        bot=bot,
        dispatcher=dispatcher,
        webhook_secret=config.WEBHOOK_SECRET,
    )
    app.add_event_handler('startup', on_startup)

else:
    async def main ():
        bot, dispatcher = setup()

        await on_startup_common(bot)

        logger.info("The bot will be using long polling")
        await dispatcher.start_polling(bot)

    asyncio.run(main())
