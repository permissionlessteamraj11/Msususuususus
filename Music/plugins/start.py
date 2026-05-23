from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import config
from Music.database.users_groups import add_user, add_group

@filters.on_message(filters.command("start") & filters.private)
async def start_private(_, message: Message):
    await add_user(message.from_user.id)
    await message.reply_photo(
        photo=config.START_URL,
        caption=config.START_CAPTION,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true"),
            ],
            [
                InlineKeyboardButton("🛠 Help & Commands", callback_data="help_callback"),
            ],
            [
                InlineKeyboardButton("📢 Channel", url=config.SUPPORT_CHANNEL),
                InlineKeyboardButton("💬 Support", url=config.SUPPORT_CHAT),
            ],
            [
                InlineKeyboardButton("👤 Owner", url=f"https://t.me/{config.OWNER_USERNAME}"),
            ]
        ])
    )

@filters.on_message(filters.command("start") & filters.group)
async def start_group(_, message: Message):
    await add_group(message.chat.id)
    await message.reply_text("✨ PritiMusic is now active in this group!")

@filters.on_message(filters.command("help"))
async def help_command(_, message: Message):
    await message.reply_photo(
        photo=config.HELP_URL,
        caption="✨ **PritiMusic Help Menu**\n\nClick the buttons below to see commands.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Music Controls", callback_data="music_help"),
                InlineKeyboardButton("Admin Panel", callback_data="admin_help"),
            ],
            [
                InlineKeyboardButton("Premium Features", callback_data="premium_help"),
            ]
        ])
    )
