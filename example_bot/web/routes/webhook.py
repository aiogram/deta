from aiogram import Dispatcher, Bot
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, SecretStr
from starlette import status

from example_bot.web.stubs import BotStub, DispatcherStub, SecretStub

webhook_router = APIRouter(prefix="/webhook")


class WebhookSecret(BaseModel):
    secret: SecretStr


@webhook_router.post("")
async def webhook_route(
    update: Update,
    secret: SecretStr = Header(alias="X-Telegram-Bot-Api-Secret-Token"),
    expected_secret: str = Depends(SecretStub),
    bot: Bot = Depends(BotStub),
    dispatcher: Dispatcher = Depends(DispatcherStub),
):
    if secret.get_secret_value() != expected_secret:
        raise HTTPException(detail="Invalid secret", status_code=status.HTTP_401_UNAUTHORIZED)

    await dispatcher.feed_update(bot, update=update)
    return {"ok": True}
