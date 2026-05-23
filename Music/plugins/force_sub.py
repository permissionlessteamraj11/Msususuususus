from pyrogram import filters, errors
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config

@filters.on_message(filters.group & ~filters.forwarded, group=-1)
async def force_subscribe(client, message: Message):
    if not config.MUST_JOIN:
        return

    try:
        await client.get_chat_member(config.MUST_JOIN, message.from_user.id)
    except errors.UserNotParticipant:
        await message.stop_propagation()
        await message.reply_text(
            f"❌ You must join our channel to use this bot!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Join Channel", url=f"https://t.me/{config.MUST_JOIN}")
            ]])
        )
    except Exception:
        pass
