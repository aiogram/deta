from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message

router = Router()


@router.message(default_state)
async def echo_handler(message: Message):
    await message.copy_to(message.chat.id)
