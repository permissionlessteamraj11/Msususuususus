from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import config
from Music.database.others import get_settings, update_settings

@filters.on_message(filters.command("settings") & filters.group)
async def settings_panel(client, message: Message):
    settings = await get_settings(message.chat.id)
    text = f"⚙️ **Settings for {message.chat.title}**\n\n"
    text += f"🔹 **Play Type:** {settings['play_type']}\n"
    text += f"🔹 **Quality:** {settings['quality']}\n"
    text += f"🔹 **Volume:** {settings['volume']}%"

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Play Type", callback_data="set_play_type"),
                InlineKeyboardButton("Quality", callback_data="set_quality"),
            ],
            [
                InlineKeyboardButton("Close", callback_data="close_settings")
            ]
        ])
    )

@filters.on_callback_query(filters.regex("set_play_type"))
async def set_play_type_cb(client, query: CallbackQuery):
    settings = await get_settings(query.message.chat.id)
    new_type = "admin" if settings["play_type"] == "everyone" else "everyone"
    await update_settings(query.message.chat.id, "play_type", new_type)
    await query.answer(f"Play type set to {new_type}")
    # Refresh panel
    await settings_panel(client, query.message)
    await query.message.delete()
