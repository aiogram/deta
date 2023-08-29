import re
import random

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_deta.space import DetaBase
from aiogram.utils.markdown import hide_link

from ..filters import TriggerFilter

router = Router()


@router.message(Command('add_trigger'), F.reply_to_message)
async def add_trigger(
    msg: Message,
    command: CommandObject,
    trigger_base: DetaBase,
):
    if not command.args:
        await msg.reply("Where is the name of the trigger?")
        return
    if len(command.args) > 10:
        await msg.reply("The name is too long")
        return

    await trigger_base.put(
        str(msg.reply_to_message.message_id),
        command.args.casefold(),
    )
    await msg.reply(
        "Trigger added"
    )


@router.message(Command('del_trigger'))
async def delete_trigger(
    msg: Message,
    command: CommandObject,
    trigger_base: DetaBase,
):
    if not command.args:
        await msg.reply("Where is the name of the trigger?")
        return

    trigger_name = command.args.casefold()
    if await trigger_base.get(trigger_name):
        await trigger_base.delete(trigger_name)
        await msg.reply("I don't remember that anymore")
    else:
        await msg.reply("I don't know of any such trigger")


@router.message(TriggerFilter())
async def send_trigger(msg: Message, bot: Bot, trigger_id: int):
    await bot.copy_message(
        msg.chat.id,
        msg.chat.id,
        trigger_id,
    )


@router.message(Command('show_triggers'))
async def show_triggers(msg: Message, trigger_base: DetaBase):
    triggers = tuple(
        entry['key']
        for entry in (await trigger_base.fetch()).items
    )
    if triggers:
        triggers_list = ' • '.join(triggers)
        await msg.reply(
            "List of all triggers"
            f"\n\n• {triggers_list}"
        )
    else:
        await msg.reply(
            "There are no triggers"
        )


@router.message(Command('never'))
@router.message(F.text.regexp(r"(^|(.+) )never(.+)?", flags=re.IGNORECASE))
async def never_handler(msg: Message):
    await msg.reply(
        f"{hide_link('https://www.youtube.com/watch?v=dQw4w9WgXcQ')}never...",
    )


@router.message(Command('lie_detector'))
async def lie_detector(msg: Message):
    if not msg.reply_to_message:
        await msg.answer("This command should be a response to a message")
        return
    side = random.choice(("true!", "not true"))
    await msg.reply_to_message.reply(
        f"It's <b>{side}</b>"
    )
