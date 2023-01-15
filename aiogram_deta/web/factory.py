from aiogram import Dispatcher, Bot
from deta import Deta
from fastapi import FastAPI

from aiogram_deta.web.webhook import webhook_router
from aiogram_deta.web.stubs import BotStub, DispatcherStub, SecretStub


def create_app(deta: Deta, bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )

    app.include_router(webhook_router)

    return app
