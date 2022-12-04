from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message

echo_router = Router(name=__name__)


@echo_router.message(default_state)
async def echo_handler(message: Message):
    await message.copy_to(message.chat.id)
