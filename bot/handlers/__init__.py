from aiogram import Dispatcher

from bot.handlers import (
    language_form,
    triggers,
    echo,
)


def setup_handlers(dp: Dispatcher):
    dp.include_routers(
        language_form.router,
        triggers.router,
        echo.router,
    )
