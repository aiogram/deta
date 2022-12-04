from os import getenv

from deta import Deta

from example_bot.bot.factory import create_bot, create_dispatcher
from example_bot.web.factory import create_app

deta = Deta()
bot = create_bot(token=getenv("TELEGRAM_TOKEN"))
dispatcher = create_dispatcher(deta=deta)
app = create_app(
    deta=deta,
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=getenv("TELEGRAM_SECRET"),
)
