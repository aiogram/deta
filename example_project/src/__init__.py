from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


bot_commands = (
    ('dialog', "Start a dialog"),
    ('cancel', "Stop the dialog"),
    ('add_trigger', "Add trigger"),
    ('del_trigger', "Delete trigger"),
    ('show_triggers', "List of triggers"),
    ('lie_detector', "Lie detector"),
    ('never', "Regular Expression")
)


async def set_bot_commands(bot: Bot):
    wrapped_commands = list(
        BotCommand(command='/' + cmd, description=text)
        for cmd, text in bot_commands
    )
    await bot.set_my_commands(
        wrapped_commands,
        scope=BotCommandScopeAllPrivateChats(),
    )


